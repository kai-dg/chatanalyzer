#!/usr/bin/env python3
"""
friendslist.json:
    author_id: author_name
viplist.json:
    author_id: nickname
"""
import json
import errors
from win32com.client import Dispatch
from chat_downloader import ChatDownloader
from chat_downloader import errors as c_errors
from datetime import datetime
from sys import argv, exit
from os import path

class TtsService:
    speak = Dispatch("SAPI.SpVoice").Speak

    def tts_message(self, servs:dict, message):
        """TTS Service function"""
        author_id = message.get("author").get("id")
        author = message.get("author").get("name")
        if "flag_onlyfriends" in servs:
            author = serv.get("flag_onlyfriends")
        mes = message.get("message")
        self.speak(f"{author} says {mes}")

class VipSubService(TtsService):
    vip_list = None
    friends_list = None
    _json_files = {
        "viplist.json": "vip_list",
        "friendslist.json": "friends_list"
    }

    def __init__(self):
        TtsService.__init__(self)
        self._set_json_files()
        self._set_vip_list()

    def _set_json_files(self):
        for jfile, jattr in self._json_files.items():
            if path.exists(jfile):
                with open(jfile, "r") as f:
                    setattr(self, jattr, json.load(f))
            else:
                with open(jfile, "w") as f:
                    f.write("{}")
                    setattr(self, jattr, {})

    def _set_vip_list(self):
        for a_id, nickname in self.vip_list.items():
            if a_id in self.friends_list:
                self.friends_list[a_id] = nickname

    def vip_check_if_friend(self, author) -> str:
        """VIP Sub Service function"""
        vip_author = self.vip_list.get(author, None)
        return vip_author if vip_author else author

class ChatAnalyzer(VipSubService):
    """ChatAnal with added services.
    Each service function needs to take in services + message.
    """
    chat = None
    now = datetime.now().timestamp()
    services = {}
    flag_onlyfriends = False
    flag_tts = True

    def __init__(self, url):
        VipSubService.__init__(self)
        self._init_services()
        self.chat = self._get_chat(url)

    def _init_services(self):
        self.services = {
            "flag_tts": {
                "main": self.tts_message,
                "flag_onlyfriends": self.vip_check_if_friend
            },
        }

    def _get_chat(self, url):
        try:
            chat = ChatDownloader().get_chat(url)
        except c_errors.SiteNotSupported:
            raise errors.ChatAnalyzerUrlError()

    def _print_message(self, mes):
        """Custom output that shows author_id to give to services"""
        ts = mes["timestamp"]/1000000 
        t = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%m")
        print(f"{t} | {mes['author']['name']} ({mes['author']['id']}): {mes['message']}")

    def _get_services(self) -> dict:
        servs = self.services.copy()
        for s_attr, func_set in self.services.items():
            if getattr(self, s_attr) == True:
                for ss_attr in func_set.item():
                    if getattr(self, ss_attr) == False:
                        del servs[s_attr][ss_attr]
            else:
                del servs[s_attr]
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
                for s in servs:
                    self._run_service(s, message)

if __name__ == "__main__":
    url = argv[1]
    chat = ChatAnalyzer(url)
