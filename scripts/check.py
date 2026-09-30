#!/usr/bin/env python3
"""A /check futtatója: fájlt író lépések sorban, utána az ellenőrzések párhuzamosan.

    check.py [--pre NÉV=PARANCS ...] [NÉV=PARANCS ...]

A --pre lépések (pl. `format --write`, `lint --fix`) sorban futnak, mert fájlt
írnak. Utána az ellenőrzések egyszerre indulnak; az első bukás a többit leállítja.

Kimenet a /check Válasz-formájában: `Check: lint ✓ · test ✗`, bukásnál alatta a
bukott lépés kimenetének vége. Exit: 0 siker, 1 bukás, 2 hibás argumentum.
"""

import argparse
import os
import signal
import subprocess
import sys
import tempfile
import time

TAIL_LINES = 60


def parse_step(raw: str) -> tuple[str, str]:
    name, sep, cmd = raw.partition("=")
    if not sep or not name.strip() or not cmd.strip():
        raise argparse.ArgumentTypeError(f"NÉV=PARANCS kell, ez nem az: {raw!r}")
    return name.strip(), cmd.strip()


def start(cmd: str, log) -> subprocess.Popen:
    # Saját process group, hogy a bukáskor a parancs gyerekei is leálljanak.
    return subprocess.Popen(
        cmd, shell=True, stdout=log, stderr=subprocess.STDOUT, start_new_session=True
    )


def kill(proc: subprocess.Popen) -> None:
    try:
        os.killpg(proc.pid, signal.SIGTERM)
    except (ProcessLookupError, PermissionError):
        pass  # a csoport már kilépett (macOS-en zombi vezetőnél EPERM)
    proc.wait()


def tail(log) -> str:
    log.seek(0)
    lines = log.read().decode(errors="replace").splitlines()
    return "\n".join(lines[-TAIL_LINES:])


def report(done: list[tuple[str, bool]], failed_log=None) -> None:
    print("Check: " + " · ".join(f"{n} {'✓' if ok else '✗'}" for n, ok in done))
    if failed_log is not None:
        print()
        print(tail(failed_log))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--pre", action="append", default=[], type=parse_step, metavar="NÉV=PARANCS")
    ap.add_argument("checks", nargs="*", type=parse_step, metavar="NÉV=PARANCS")
    args = ap.parse_args()

    if not args.pre and not args.checks:
        print("Check: nincs ellenőrzés.")
        return 0

    done: list[tuple[str, bool]] = []

    for name, cmd in args.pre:
        with tempfile.TemporaryFile() as log:
            ok = start(cmd, log).wait() == 0
            done.append((name, ok))
            if not ok:
                report(done, log)
                return 1

    logs = {name: tempfile.TemporaryFile() for name, _ in args.checks}
    running = {name: start(cmd, logs[name]) for name, cmd in args.checks}
    order = [name for name, _ in args.checks]
    results: dict[str, bool] = {}

    try:
        while running:
            for name, proc in list(running.items()):
                if proc.poll() is None:
                    continue
                del running[name]
                results[name] = proc.returncode == 0
                if not results[name]:
                    for other in running.values():
                        kill(other)
                    running.clear()
                    # Csak a ténylegesen lefutottak kerülnek a Check-sorba.
                    done += [(n, results[n]) for n in order if n in results]
                    report(done, logs[name])
                    return 1
            time.sleep(0.05)
    finally:
        for proc in running.values():
            kill(proc)
        for log in logs.values():
            log.close()

    report(done + [(n, results[n]) for n in order])
    return 0


if __name__ == "__main__":
    sys.exit(main())
