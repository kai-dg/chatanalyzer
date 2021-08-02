#!/ussr/bin/env python3
import json
from os import path, remove

# GLOBALS
g = {
    # filename: variable name
    "JSON_FILES": {
        "viplist.json": "vip_list",
        "flags.json": "flags",
        "friendslist.json": "friends_list",
        "blacklist.json": "blacklist",
    },
    "CHATLOG": ".chatlog.json",
    "DOT_FOLDER": ".settings"
}

class Settings:
    @staticmethod
    def add_flags_template(filepath):
        template = {
            "flag_tts": True,
            "flag_blacklist": True,
            "flag_onlyfriends": False
        }
        with open(filepath, "w+") as f:
            json.dump(template, f)

    @staticmethod
    def add_blacklist_template(filepath):
        template = {"ids": []}
        with open(filepath, "w+") as f:
            json.dump(template, f)

    @staticmethod
    def edit_flags(filepath):
        pass

    @staticmethod
    def edit_friends_list():
        pass

    @staticmethod
    def edit_vip_list():
        pass

    @staticmethod
    def reset_chatlog():
        if path.exists(g["CHATLOG"]):
            remove(g["CHATLOG"])
