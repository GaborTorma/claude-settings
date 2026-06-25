#!/usr/bin/env python3
"""App Store screenshot helper — capture from a simulator and convert to the
exact size App Store Connect requires.

Two things reliably bite you: (1) ASC wants a *pixel-exact* size with **no alpha**,
and (2) you can't tap to navigate the sim. This handles both.

Needs `xcrun simctl` (full Xcode — if only Command Line Tools are active, set
`export DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer`). `convert`
needs Pillow, `generate` needs PyYAML.

Pass screen state as **launch arguments** (`-key value` → NSArgumentDomain →
UserDefaults.standard), NOT `defaults write`: launch args are never cfprefsd-cached,
so each launch is deterministic. Gate such debug-only keys to DEBUG so they no-op
in App Store builds.

  generate --config screenshots.yaml --out .   # all shots × languages (see example yaml)
  capture  --device "iPhone 14 Plus" --bundle com.example.app --arg startTab=0 --out s.png
  convert  --in s.png --size 1284x2778          # strip alpha + resize to exact size
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path


def simctl(*args: str, quiet: bool = True) -> int:
    return subprocess.run(
        ["xcrun", "simctl", *args],
        stdout=subprocess.DEVNULL if quiet else None,
        stderr=subprocess.DEVNULL if quiet else None,
    ).returncode


def _status_bar(device: str, sb: dict) -> None:
    simctl("status_bar", device, "override",
           "--time", str(sb.get("time", "9:41")),
           "--batteryState", "charged", "--batteryLevel", str(sb.get("battery", 100)),
           "--cellularBars", str(sb.get("cellular", 4)), "--wifiBars", str(sb.get("wifi", 3)))


def _shot(device: str, bundle: str, args: list[str], out: str, settle: float) -> int:
    """Launch with the given -key value args and screenshot to `out`."""
    simctl("terminate", device, bundle)
    simctl("launch", device, bundle, *args)
    time.sleep(settle)
    return simctl("io", device, "screenshot", out, quiet=False)


def _resize(src: str, tw: int, th: int, dst: str) -> None:
    """Drop alpha + uniform-scale (cover) + center-crop to exactly tw×th."""
    from PIL import Image
    im = Image.open(src).convert("RGB")
    w, h = im.size
    scale = max(tw / w, th / h)
    rw, rh = round(w * scale), round(h * scale)
    im = im.resize((rw, rh), Image.LANCZOS)
    left, top = (rw - tw) // 2, (rh - th) // 2
    im.crop((left, top, left + tw, top + th)).save(dst, "PNG")


def _parse_size(s: str) -> tuple[int, int]:
    w, h = (int(x) for x in s.lower().split("x"))
    return w, h


def capture(a: argparse.Namespace) -> int:
    simctl("boot", a.device)
    simctl("bootstatus", a.device, "-b")
    _status_bar(a.device, {})
    if a.app and simctl("install", a.device, a.app, quiet=False) != 0:
        return 1
    if a.grant_location:
        simctl("privacy", a.device, "grant", "location", a.bundle)
    args: list[str] = []
    for pair in a.arg or []:
        if "=" not in pair:
            print(f"--arg expects key=value, got: {pair}", file=sys.stderr)
            return 2
        k, v = pair.split("=", 1)
        args += [f"-{k}", v]
    if _shot(a.device, a.bundle, args, a.out, a.wait) != 0:
        return 1
    print(f"captured -> {a.out}")
    return 0


def convert(a: argparse.Namespace) -> int:
    try:
        import PIL  # noqa: F401
    except ImportError:
        print("Pillow required:  pip install pillow", file=sys.stderr)
        return 3
    tw, th = _parse_size(a.size)
    _resize(a.input, tw, th, a.out or a.input)
    print(f"{a.out or a.input}  {tw}x{th}  RGB (no alpha)")
    return 0


def generate(a: argparse.Namespace) -> int:
    try:
        import yaml
    except ImportError:
        print("PyYAML required:  pip install pyyaml", file=sys.stderr)
        return 3
    cfg = yaml.safe_load(Path(a.config).read_text())
    langs = cfg.get("languages", ["en"])
    locale_arg = cfg.get("locale_arg", "locale")
    settle = cfg.get("settle", 5)
    sb = cfg.get("status_bar") or {}
    devices = cfg["devices"]
    out_root = Path(a.out)
    booted: set[str] = set()

    for shot in cfg["shots"]:
        dev = devices[shot["device"]]
        name, bundle = dev["name"], dev["bundle"]
        if name not in booted:
            simctl("boot", name)
            simctl("bootstatus", name, "-b")
            if dev.get("app"):
                simctl("install", name, dev["app"])
            if cfg.get("grant_location"):
                simctl("privacy", name, "grant", "location", bundle)
            booted.add(name)
        for lang in langs:
            if sb:
                _status_bar(name, sb)
            args = [f"-{locale_arg}", lang]
            for k, v in (shot.get("args") or {}).items():
                args += [f"-{k}", str(v)]
            dest_dir = out_root / lang
            dest_dir.mkdir(parents=True, exist_ok=True)
            png = dest_dir / f"{shot['device']}-{shot['name']}.png"
            if _shot(name, bundle, args, str(png), settle) != 0:
                print(f"  ✗ {png}", file=sys.stderr)
                continue
            if dev.get("size"):
                tw, th = _parse_size(str(dev["size"]))
                _resize(str(png), tw, th, str(png))
            print(f"  ✓ {png}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="App Store screenshot helper")
    sub = p.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate", help="render all shots × languages from a YAML config")
    g.add_argument("--config", required=True, help="screenshots.yaml (see assets/ example)")
    g.add_argument("--out", default=".", help="output root; <lang>/ subfolders created")
    g.set_defaults(func=generate)

    c = sub.add_parser("capture", help="one screenshot with a clean status bar")
    c.add_argument("--device", required=True, help="simulator name or UDID")
    c.add_argument("--bundle", required=True, help="app bundle id")
    c.add_argument("--app", help="path to a .app to install first")
    c.add_argument("--arg", action="append", metavar="KEY=VALUE",
                   help="launch argument -> -KEY VALUE (repeatable)")
    c.add_argument("--grant-location", action="store_true")
    c.add_argument("--wait", type=float, default=4.0, help="seconds before capture")
    c.add_argument("--out", required=True, help="output PNG")
    c.set_defaults(func=capture)

    v = sub.add_parser("convert", help="strip alpha + resize to an exact size")
    v.add_argument("--in", dest="input", required=True, help="input PNG")
    v.add_argument("--size", required=True, help="exact target WxH, e.g. 1284x2778")
    v.add_argument("--out", help="output PNG (default: overwrite --in)")
    v.set_defaults(func=convert)

    a = p.parse_args()
    return a.func(a)


if __name__ == "__main__":
    raise SystemExit(main())
