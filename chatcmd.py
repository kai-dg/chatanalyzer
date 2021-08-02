#!/usr/bin/env python3
from cmd import Cmd
import subprocess
import psutil
import atexit
from chatsettings import Settings, read_json, update_json

EDIT_SERVICES = {
    "vip": Settings.edit_vip_list,
    "friends": Settings.edit_friends_list,
    "flags": Settings.edit_flags,
    "blacklist": Settings.edit_blacklist
}
INTEGRITY_CHECKS = {
}


def kill_proc_tree(pid:int):
    pobj = psutil.Process(pid)
    for c in pobj.children(recursive=True):
        c.kill()
    pobj.kill()

def check_edit_args(inp) -> list:
    args = inp.split()
    # TODO To future me: find better way to handle this
    if args > 1:
        # Key to list
        if args[0] in ["blacklist"] and len(args) == 2:
            return args
        elif len(args) == 3:
            return args
    return ["invalid"]

class ChatAnalyzerCmd(Cmd):
    prompt = "ChatAnalyzer > "
    intro = """Commands:\n start [url]\n end\nEdit files:\
            \n vip friendslist blacklist flags
            """
    PROC = None
    URL = None

    def do_exit(self, inp):
        print("Exiting")
        return True

    def do_start(self, inp):
        command = ["cmd", "/c", "venv\\scripts\\activate.bat",
                   "&&", "python", "chatanal.py", inp]
        self.URL = inp
        self.PROC = subprocess.Popen(
            command,
            creationflags=subprocess.CREATE_NEW_CONSOLE,
        )

    def do_restart(self, inp):
        print("> Restarting Chat Analyzer")
        self.do_end("")
        self.do_start(self.URL)

    def do_end(self, inp):
        kill_proc_tree(self.PROC.pid)
        self.PROC = None

    def do_add(self, inp):
        print(inp)
        self.do_restart("")

    def do_edit(self, inp):
        args = check_edit_args(inp)
        func = EDIT_SERVICES.get(args[0], None)
        data = read_json(args[0]) if func else None
        # Key to list files
        if func and inp in ["blacklist"]:
            key = data.keys()[0]
            data[key].append(args[1])
        # Key to value files
        else:
            # TODO Need to make integrity check later
            data[args[1]] = args[2]
        self.do_restart("")

    def do_del(self, inp):
        pass

    do_EOF = do_exit

if __name__ == "__main__":
    atexit.register(Settings.reset_chatlog)
    ChatAnalyzerCmd().cmdloop()
