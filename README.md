# herdr-machine-icons

A [herdr](https://herdr.dev) plugin: every pane on a machine carries that machine's icon as the pane token
`machine_icon`, so herdr's sidebar can show which machine an agent runs on in one character instead of its name.

```toml
# ~/.config/herdr/config.toml
[ui.sidebar.agents]
rows = [["state_icon", "workspace", "$machine_icon", "tab"]]
```

## Install

    herdr plugin install Benjmhart/herdr-machine-icons

on every machine herdr reaches, and give each the same icon list, one `<hostname> <icon>` per line
(`#` starts a comment):

    # $(herdr plugin config-dir benjmhart.machine-icons)/icons
    beast-arch 🐺
    carbon     💎
    micro      🐭

The hostname is `uname -n` up to the first dot. A machine with no line gets no token, so its agents show none.

## How

Each machine tags its own panes, so no machine needs to reach another: at server start and whenever a pane or an agent
appears, `machine_icons.py` sets `machine_icon` on every pane of that server (`herdr pane report-metadata`). herdr does
not keep pane tokens across a restart; the startup hook puts them back. Change the list, then restart the server or open
a pane for it to apply.

Standard library Python 3 only. Linux and macOS.

## Test

    python3 machine_icons.py test
