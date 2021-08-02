#!/usr/bin/env python3
from cmd import Cmd
import subprocess
import psutil
import atexit
from chatsettings import Settings

ADD_SERVICES = {
    "vip": ""
}
EDIT_SERVICES = {
    "vip": ""
}


def kill_proc_tree(pid:int):
    pobj = psutil.Process(pid)
    for c in pobj.children(recursive=True):
        c.kill()
    pobj.kill()

class ChatAnalyzerCmd(Cmd):
    prompt = "ChatAnalyzer > "
    intro = "Commands:\n start [url]\n end"
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
        print(inp)
        self.do_restart("")

    do_EOF = do_exit

if __name__ == "__main__":
    atexit.register(Settings.reset_chatlog)
    ChatAnalyzerCmd().cmdloop()
