#!/usr/bin/env python3
from cmd import Cmd
import subprocess


def kill_proc_tree(pid:int):
    pobj = psutil.Process(pid)
    for c in pobj.children(recursive=True):
        c.kill()
    pobj.kill()

class ChatAnalyzerCmd(Cmd):
    prompt = "ChatAnalyzer > "
    intro = "Commands:\n start [url]\n end"
    PROC = None

    def do_exit(self, inp):
        print("Exiting")
        return True
    def do_start(self, inp):
        command = ["cmd", "/c", "venv\\scripts\\activate.bat", "&&", "python", "chatanal.py", "random"]
        self.PROC = subprocess.Popen(
            command,
            creationflags=subprocess.CREATE_NEW_CONSOLE,
        )
    def do_end(self, inp):
        kill_proc_tree(self.PROC.pid)

    do_EOF = do_exit

if __name__ == "__main__":
    ChatAnalyzerCmd().cmdloop()
