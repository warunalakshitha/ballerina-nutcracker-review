#!/usr/bin/env python3
"""Lock for cloud review rounds: `reports/round.lock` on `main` of this repo.

A push to main is rejected unless it builds on the latest main, so only one session can take the lock.
All lock commits are made in a separate worktree ($LOCK_WT), never in the $TOOLS checkout the round reads.

  round_lock.py status                      free | running | stale; exit 3 if running
  round_lock.py unchanged <scan file>       exit 0 if the scan matches reports/last-scan.txt (nothing to do)
  round_lock.py take <STARTED> <session>    take the lock; exit 3 if another round holds it
  round_lock.py beat <STARTED>              update the lock now; exit 3 if it's no longer ours (stop posting)
  round_lock.py heartbeat <STARTED>         start a detached loop that runs `beat` every hour
  round_lock.py release <STARTED>           drop our lock (round stopped early)
  round_lock.py queue <STARTED> <file> <name>
                                            queue a GitHub write as outbox/<name> for the post-outbox Action;
                                            exit 3 if the lock is no longer ours (stop posting)
  round_lock.py wait-outbox [minutes]       wait (default 15 min) until the Action has emptied outbox/;
                                            exit 1 if items are still there (not posted, or failed)
  round_lock.py finish <STARTED> <report> <scan file>
                                            commit the report and the scan, drop the lock, push
"""
import os
import signal
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone

TOOLS = os.environ.get("TOOLS") or os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
WT = os.environ.get("LOCK_WT", "/tmp/review-lock")
PID = WT + ".heartbeat.pid"
LOCK = "reports/round.lock"
SCAN = "reports/last-scan.txt"
OUTBOX = "outbox"
STALE = timedelta(hours=2)  # no heartbeat for this long: the round is dead
BEAT = int(os.environ.get("LOCK_BEAT_SECONDS", "3600"))


def git(*args, check=True):
    return subprocess.run(["git", "-C", WT, *args], capture_output=True, text=True, check=check)


def sync():
    if not os.path.isdir(os.path.join(WT, ".git")) and not os.path.isfile(os.path.join(WT, ".git")):
        subprocess.run(["git", "-C", TOOLS, "worktree", "prune"], check=True)
        subprocess.run(["git", "-C", TOOLS, "worktree", "add", "-q", "--detach", WT], check=True)
    git("fetch", "-q", "origin", "main")
    git("reset", "-q", "--hard", "origin/main")


def read():
    path = os.path.join(WT, LOCK)
    if not os.path.exists(path):
        return None
    return dict(line.strip().split("=", 1) for line in open(path) if "=" in line)


def now():
    return datetime.now(timezone.utc).replace(microsecond=0)


def is_stale(lock):
    t = lock.get("heartbeat_utc") or lock.get("started_utc", "")
    try:
        return now() - datetime.fromisoformat(t) > STALE
    except ValueError:
        return True


def write(lock):
    with open(os.path.join(WT, LOCK), "w") as f:
        f.writelines(f"{k}={v}\n" for k, v in lock.items())


def commit_push(message, *paths):
    present = [p for p in paths if os.path.exists(os.path.join(WT, p))]  # deletions are staged by `git rm`
    if present:
        git("add", "-A", "--", *present)
    if git("diff", "--cached", "--quiet", check=False).returncode == 0:
        return True  # nothing changed (e.g. a heartbeat within the same second)
    git("commit", "-q", "-m", message)
    return git("push", "-q", "origin", "HEAD:main", check=False).returncode == 0


def describe(lock):
    return f"round {lock.get('started')} (session {lock.get('session', '?')}, last heartbeat {lock.get('heartbeat_utc')})"


def ours(lock, started):
    return lock is not None and lock.get("started") == started


def stop_heartbeat():
    try:
        os.kill(int(open(PID).read()), signal.SIGTERM)
    except (OSError, ValueError):
        pass
    try:
        os.remove(PID)
    except OSError:
        pass


def status():
    sync()
    lock = read()
    if lock is None:
        print("free")
        return 0
    if is_stale(lock):
        print(f"stale: {describe(lock)}")
        return 0
    print(f"running: {describe(lock)}")
    return 3


def unchanged(scan_file):
    sync()
    new = sorted(l.strip() for l in open(scan_file) if l.strip())
    old_path = os.path.join(WT, SCAN)
    old = sorted(l.strip() for l in open(old_path) if l.strip()) if os.path.exists(old_path) else None
    if old is None or any(" ERR" in l for l in new) or new != old:
        print("changed")
        return 1
    print("unchanged since the last round")
    return 0


def take(started, session):
    for _ in range(5):
        sync()
        lock = read()
        if lock is not None and not is_stale(lock):
            print(f"running: {describe(lock)}")
            return 3
        t = now().isoformat()
        write({"started": started, "started_utc": t, "heartbeat_utc": t, "session": session})
        if commit_push(f"chore(review): start {started} round", LOCK):
            print(f"taken{' (took over stale ' + describe(lock) + ')' if lock else ''}")
            return 0
    print("could not push the lock")
    return 1


def beat(started):
    for _ in range(5):
        sync()
        lock = read()
        if not ours(lock, started):
            return 3
        lock["heartbeat_utc"] = now().isoformat()
        write(lock)
        if commit_push(f"chore(review): {started} round still running", LOCK):
            return 0
    return 1


def heartbeat(started):
    stop_heartbeat()
    if os.fork():
        return 0
    os.setsid()
    with open(PID, "w") as f:
        f.write(str(os.getpid()))
    while True:
        time.sleep(BEAT)
        try:
            if beat(started) == 3:
                break
        except subprocess.CalledProcessError:
            pass  # a network hiccup: try again next hour
    os._exit(0)


def release(started):
    stop_heartbeat()
    for _ in range(5):
        sync()
        lock = read()
        if lock is None:
            return 0
        if not ours(lock, started):
            print(f"not ours: {describe(lock)}")
            return 3
        git("rm", "-q", LOCK)
        if commit_push(f"chore(review): release {started} round lock", LOCK):
            return 0
    return 1


def queue(started, path, name):
    if "/" in name or not name.endswith(".json") or not name.startswith(("review-", "issue-")):
        print("name must be review-<N>.json, issue-<slug>.json or issue-comment-<slug>.json")
        return 2
    content = open(path).read()
    for _ in range(5):
        sync()
        lock = read()
        if not ours(lock, started):
            print(f"lock is no longer ours: {describe(lock) if lock else 'free'}")
            return 3
        os.makedirs(os.path.join(WT, OUTBOX), exist_ok=True)
        with open(os.path.join(WT, OUTBOX, name), "w") as f:
            f.write(content)
        lock["heartbeat_utc"] = now().isoformat()
        write(lock)
        if commit_push(f"chore(review): queue {name}", os.path.join(OUTBOX, name), LOCK):
            print(f"queued {OUTBOX}/{name}")
            return 0
    return 1


def wait_outbox(minutes="15"):
    deadline = time.time() + 60 * float(minutes)
    while True:
        sync()
        left = sorted(n for n in os.listdir(os.path.join(WT, OUTBOX)) if n.endswith(".json")) \
            if os.path.isdir(os.path.join(WT, OUTBOX)) else []
        if not left:
            print("outbox empty: everything was posted (see outbox/posted.log)")
            return 0
        if time.time() > deadline:
            print("still queued: " + ", ".join(left) + " (see outbox/posted.log and the post-outbox Action runs)")
            return 1
        time.sleep(30)


def finish(started, report, scan_file):
    stop_heartbeat()
    text = open(report).read()
    text = text[text.index("# "):] if "# " in text else text
    for _ in range(5):
        sync()
        lock = read()
        if lock is not None and not ours(lock, started):
            print(f"lock is held by another round, not pushing: {describe(lock)}")
            return 3
        with open(os.path.join(WT, "reports/latest.md"), "w") as f:
            f.write(text)
        with open(os.path.join(WT, SCAN), "w") as f:
            f.write(open(scan_file).read())
        if lock is not None:
            git("rm", "-q", LOCK)
        if commit_push(f"chore(review): add {started} round report", "reports/latest.md", SCAN, LOCK):
            return 0
    return 1


def main():
    cmd, args = (sys.argv[1], sys.argv[2:]) if len(sys.argv) > 1 else ("", [])
    commands = {"status": (status, 0), "unchanged": (unchanged, 1), "take": (take, 2), "beat": (beat, 1), "heartbeat": (heartbeat, 1),
                "release": (release, 1), "finish": (finish, 3), "queue": (queue, 3), "wait-outbox": (wait_outbox, 1)}
    if cmd == "wait-outbox" and not args:
        return wait_outbox()
    if cmd not in commands or len(args) != commands[cmd][1]:
        print(__doc__)
        return 2
    return commands[cmd][0](*args)


if __name__ == "__main__":
    sys.exit(main())
