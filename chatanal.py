#!/usr/bin/env python3
"""
friendslist.json:
    author_id: author_name
viplist.json:
    author_id: nickname
"""
import json
import errors
import copy
from win32com.client import Dispatch
from chat_downloader import ChatDownloader
from chat_downloader import errors as c_errors
from datetime import datetime
from sys import argv
from os import path, mkdir
from chatsettings import AnalSettings

DOT_FOLDER = ".settings"

class VipSubService:
    def __init__(self):
        self._set_vip_list()
        
    def _set_vip_list(self):
        for a_id, nickname in self.vip_list.items():
            if a_id in self.friends_list:
                self.friends_list[a_id] = nickname

    def vip_check_if_friend(self, author, author_id) -> str:
        """VIP Sub Service function"""
        vip_author = self.vip_list.get(author_id, None)
        return vip_author if vip_author else author

class TtsService(VipSubService):
    speak = Dispatch("SAPI.SpVoice").Speak

    def __init__(self):
        VipSubService.__init__(self)

    def tts_message(self, servs:dict, message):
        """TTS Service function"""
        author_id = message.get("author").get("id")
        author = message.get("author").get("name")
        if "flag_onlyfriends" in servs:
            author = servs.get("flag_onlyfriends")(author, author_id)
        mes = message.get("message")
        self.speak(f"{author} says {mes}")

class ChatAnalyzer(TtsService):
    """ChatAnal with added services.
    Each service function needs to take in services + message.
    """
    chat = None
    now = datetime.now().timestamp()
    _json_files = {
        "viplist.json": "vip_list",
        "friendslist.json": "friends_list",
        "flags.json": "flags"
    }
    # FLAGS
    flags = None
    # SERVICES
    services = {}
    vip_list = None
    friends_list = None

    def __init__(self, url):
        self._set_json_files()
        self.chat = self._get_chat(url)
        TtsService.__init__(self)
        self._init_services()

    def _init_services(self):
        self.services = {
            "flag_tts": {
                "main": self.tts_message,
                "flag_onlyfriends": self.vip_check_if_friend
            },
        }

    def _set_json_files(self):
        if not path.exists(DOT_FOLDER):
            mkdir(DOT_FOLDER)
        for jfile, jattr in self._json_files.items():
            jpath = path.join(DOT_FOLDER, jfile)
            if path.exists(jpath):
                with open(jpath, "r") as f:
                    setattr(self, jattr, json.load(f))
            else:
                with open(jpath, "w") as f:
                    f.write("{}")
                    setattr(self, jattr, {})
                if jattr == "flags":
                    AnalSettings.add_flags_template(jpath)

    def _get_chat(self, url):
        try:
            chat = ChatDownloader().get_chat(url)
            return chat
        except c_errors.SiteNotSupported:
            raise errors.ChatAnalyzerUrlError()

    def _print_message(self, mes):
        """Custom output that shows author_id to give to services"""
        ts = mes["timestamp"]/1000000 
        t = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%m")
        print(f"{t} | {mes['author']['name']} ({mes['author']['id']}): {mes['message']}")

    def _get_services(self) -> dict:
        servs = {}
        for s_attr, func_set in self.services.items():
            if self.flags.get(s_attr, None) == True:
                servs[s_attr] = {"main": func_set["main"]}
                for ss_attr, func in func_set.items():
                    if self.flags.get(ss_attr) == True:
                        servs[s_attr][ss_attr] = func
        return servs

    def _run_service(self, serv, message):
        if len(serv) > 1:
            serv["main"](serv, message)
        else:
            serv["main"]({}, message)

    def run(self):
        servs = self._get_services()
        for message in self.chat:
            if message.get("timestamp")/1000000 > self.now:
                self._print_message(message)
                for name, funcs in servs.items():
                    self._run_service(funcs, message)

if __name__ == "__main__":
    url = argv[1]
    chat = ChatAnalyzer(url)
    chat.run()
