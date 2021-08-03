#!/usr/bin/env python3
from cmd import Cmd
import subprocess
import psutil
import atexit
from chatsettings import Settings, g, read_json, update_json
from chatanal import ChatAnalyzer
INTEGRITY_CHECKS = {
}


def kill_proc_tree(pid:int):
    pobj = psutil.Process(pid)
    for c in pobj.children(recursive=True):
        c.kill()
    pobj.kill()

def check_edit_args(inp) -> list:
    """Return:
    idx 0: file name
    idx 1: key or list item
    idx 2: value
    """
    args = inp.split()
    # TODO To future me: find better way to handle this
    if len(args) > 1:
        # Key to list
        if args[0] in ["blacklist"] and len(args) == 2:
            return args
        elif len(args) > 2:
            value = " ".join(args[2:])
            args = args[:2]
            args.append(value)
            return args
    return ["invalid"]

class ChatAnalyzerCmd(Cmd):
    prompt = "ChatAnalyzer > "
    intro = """Commands:\n start [url]\n end\nEdit files:\
            \n vip friendslist blacklist flags\
            \nTurn on flags:\n flag_tts flag_vip flag_blacklist flag_onlyfriends
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

    def do_edit(self, inp):
        args = check_edit_args(inp)
        data = read_json(args[0])
        # Key to list files
        if args[0] in ["blacklist"]:
            key = list(data.keys())[0]
            data[key].append(args[1])
        # Key to value files
        else:
            # TODO Need to make integrity check later
            if args[2] in ["true", "on"]:
                args[2] = True
            if args[2] in ["false", "off"]:
                args[2] = False
            data[args[1]] = args[2]
        update_json(args[0], data)
        if self.PROC:
            self.do_restart("")

    def do_del(self, inp):
        """del [filename] [id]"""
        args = check_edit_args(inp)
        data = read_json(args[0])
        if args[0] in ["blacklist"]:
            key = list(data.keys())[0]
            data[key].remove(args[1])
        else:
            del data[args[1]]
        update_json(args[0], data)
        if self.PROC:
            self.do_restart("")

    def do_list(self, inp):
        pass

    do_EOF = do_exit

if __name__ == "__main__":
    c = ChatAnalyzerCmd()
    atexit.register(c.do_exit, "")
    ChatAnalyzerCmd().cmdloop()
