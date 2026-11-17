#!/usr/bin/env python3
"""herdr-machine-icons: tag every pane on this herdr server with this machine's icon, as the pane token machine_icon,
for herdr's sidebar rows ("$machine_icon"). Run by herdr at server start and when a pane or agent appears.

The icons live in one file, the same on every machine (e.g. from your dotfiles):
    $HERDR_PLUGIN_CONFIG_DIR/icons      one "<hostname> <icon>" per line; # starts a comment
A machine with no line gets no token, so the sidebar shows nothing for it. Standard library only.
"""
import json, os, socket, subprocess, sys

HERDR = os.environ.get("HERDR_BIN_PATH", "herdr")
CONFIG = os.environ.get("HERDR_PLUGIN_CONFIG_DIR") or os.path.expanduser("~/.config/herdr/plugins/config/benjmhart.machine-icons")
SOURCE, TOKEN = "plugin:machine-icons", "machine_icon"


def icon(host, text):
    for line in text.splitlines():
        f = line.split("#", 1)[0].split()
        if len(f) >= 2 and f[0] == host:
            return f[1]
    return None


def main():
    host = socket.gethostname().split(".")[0]
    try:
        with open(os.path.join(CONFIG, "icons"), encoding="utf-8") as f:
            mine = icon(host, f.read())
    except OSError:
        mine = None
    out = subprocess.run([HERDR, "pane", "list"], capture_output=True, encoding="utf-8", timeout=10)
    if out.returncode:
        sys.exit(f"machine-icons: pane list: {out.stderr.strip()}")
    for p in json.loads(out.stdout)["result"]["panes"]:
        tok = ["--token", f"{TOKEN}={mine}"] if mine else ["--clear-token", TOKEN]
        subprocess.run([HERDR, "pane", "report-metadata", p["pane_id"], "--source", SOURCE, *tok],
                       capture_output=True, timeout=10)


if __name__ == "__main__":
    if sys.argv[1:] == ["test"]:
        t = "# fleet\nbeast-arch 🐺\nmicro 🐭  # the laptop\n\ncarbon\n"
        assert icon("micro", t) == "🐭" and icon("beast-arch", t) == "🐺"
        assert icon("carbon", t) is None and icon("surfboard", t) is None
        print("ok")
    else:
        main()
