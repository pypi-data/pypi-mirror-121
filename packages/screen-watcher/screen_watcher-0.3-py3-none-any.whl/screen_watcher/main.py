from datetime import datetime
import os
import time
import socket
import argparse
import textwrap
import collections

from tabulate import tabulate
import psutil

from .slack import send_slack_msg
from .models import get_pinfo_list, update_pinfo


class Worker:
    tree = collections.defaultdict(list)

    screen_pids = set()
    running_pids = set()

    # traverse processes tree
    def traverse(cls, parent, indent=""):
        try:
            p = psutil.Process(parent).as_dict(
                attrs=[
                    "cwd",
                    "exe",
                    "pid",
                    "name",
                    "ppid",
                    "cmdline",
                    "environ",
                    "terminal",
                    "username",
                    "create_time",
                ]
            )

        except psutil.Error:
            p = {}

        pid = p.get("pid", None)
        name = p.get("name", None)
        cmdline = p.get("cmdline", [])
        environ = p.get("environ", None)

        if not (name == "screen" or cmdline == ["/bin/bash"]):
            is_created = update_pinfo(p)
            cls.running_pids.add(pid)

        if parent not in cls.tree:
            return
        children = cls.tree[parent][:-1]
        for child in children:
            cls.traverse(child, indent + "| ")
        child = cls.tree[parent][-1]
        cls.traverse(child, indent + "  ")

    def run(cls):
        # construct a dict where 'values' are all the processes
        # having 'key' as their parent
        for p in psutil.process_iter():
            try:
                cls.tree[p.ppid()].append(p.pid)
            except (psutil.NoSuchProcess, psutil.ZombieProcess):
                pass
            # on systems supporting PID 0, PID 0's parent is usually 0
            if p.name() == "screen":
                cls.screen_pids.add(p.pid)

        # traverse screen child processes
        for p in cls.screen_pids:
            cls.traverse(p)

        # find terminated process
        for pinfo in get_pinfo_list(only_running=True):
            if pinfo.pid not in cls.running_pids:
                update_pinfo(pinfo.as_dict(), False)

                if os.environ.get("SLACK_BOT_TOKEN"):

                    msg = (
                        "*"
                        + "[ALERT] screen process terminated"
                        + "*\n```"
                        + f"hostname : {socket.gethostname()}\n"
                        + f"sty      : {pinfo.environ.get('STY', None)}\n"
                        + f"cmdline  : {pinfo.cmdline}\n"
                        + f"cwd      : {pinfo.cwd}\n"
                        + "```\n"
                        + datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                    )

                    send_slack_msg(
                        os.environ.get("SLACK_BOT_CHANNEL", "screen-watcher"), msg
                    )


def main():
    parser = argparse.ArgumentParser(description="screen watcher")
    parser.add_argument(
        "--daemon",
        dest="is_daemon",
        action="store_const",
        const=True,
        default=False,
        help="worker daemon (default: print running processes)",
    )
    parser.add_argument(
        "--all",
        dest="only_running",
        action="store_const",
        const=False,
        default=True,
        help="all processes (default: only running process)",
    )
    parser.add_argument(
        "--json",
        dest="is_json",
        action="store_const",
        const=True,
        default=False,
        help="print json format (default: tabulate)",
    )
    parser.add_argument(
        "--cmd",
        dest="is_cmd",
        action="store_const",
        const=True,
        default=False,
        help="print cmd format (default: tabulate)",
    )

    args = parser.parse_args()

    if args.is_daemon:
        while True:
            Worker().run()
            time.sleep(10)

    else:
        Worker().run()

        headers = ["pid", "ppid", "username", "sty", "name", "cwd", "cmdline", "status"]
        rows = []
        for pinfo in get_pinfo_list(only_running=args.only_running):
            if args.is_json:
                print(pinfo.as_dict())
                continue

            if args.is_cmd:
                print("cd %s;%s" % (pinfo.cwd, pinfo.cmdline))
                continue

            row = [
                pinfo.pid,
                pinfo.ppid,
                pinfo.username,
                pinfo.environ.get("STY", None) if pinfo.environ else None,
                pinfo.name,
                pinfo.cwd,
                textwrap.fill(pinfo.cmdline, width=48),
                str(pinfo.status),
            ]
            rows.append(row)

        if not args.is_json:
            print(tabulate(rows, headers=headers))


if __name__ == "__main__":
    main()
