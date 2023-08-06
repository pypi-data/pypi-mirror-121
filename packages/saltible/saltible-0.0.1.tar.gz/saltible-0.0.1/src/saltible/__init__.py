#!/usr/bin/env python3

import sys
import subprocess
import os

MASTER_TEMPLATE = """
root_dir: {root_dir}
file_roots:
  base:
    - {root_dir}/states
pillar_roots:
  base:
    - {root_dir}/pillars
"""

ROSTER_TEMPLATE = """
{name}:
  host: {ip}
  user: {user}
  port: {port}
"""


def init():
    cwd = os.path.abspath(os.getcwd())
    master_path = os.path.join(cwd, "master")
    if not os.path.exists(master_path):
        with open(master_path, "wt") as f:
            f.write(MASTER_TEMPLATE.format(root_dir=cwd))
        return
    else:
        master = input("master config file exists, override? [Yn]")
        if master.lower() in ("y", ""):
            with open(master_path, "wt") as f:
                f.write(MASTER_TEMPLATE.format(root_dir=cwd))
                print("Overrode master")
        else:
            print("Do nothing")

    roster_path = os.path.join(cwd, "roster")

    def fill_roster():
        name = input("Give the target host a short name: ")
        ip = input("IP: ")
        port = input("Port to ssh in, default 22: ") or "22"
        user = input("User to ssh in, default root: ") or "root"
        with open(roster_path, "wt") as f:
            f.write(
                ROSTER_TEMPLATE.format(name=name, ip=ip, user=user, port=port)
            )

    if os.path.exists(roster_path):
        roster = input("roster config file exists, override? [Yn]")
        if roster.lower() in ("y", ""):
            fill_roster()
    else:
        fill_roster()

def ping():
    cmd = ["salt-ssh", "--config", ".", '*', "test.ping"]

    print("Running cmd: {}".format(cmd))
    subprocess.run(cmd)

def bye():
    print("bye")


def main():
    subcmd = sys.argv[1]
    cmdmap = {
        "init": init,
        "bye": bye,
        "ping": ping,
    }
    try:
        func = cmdmap[subcmd]
    except KeyError:
        raise Exception("Unknown cmd")
    else:
        func()
