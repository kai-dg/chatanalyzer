#!/ussr/bin/env python3
import json
from os import path, remove

_VIP = "viplist.json"
_FLAGS = "flags.json"
_BLACKLIST = "blacklist.json"
_FRIENDSLIST= "friendslist.json"
# GLOBALS
g = {
    # filename: variable name
    "JSON_FILES": {
        _VIP: "vip_list",
        _FLAGS: "flags",
        _FRIENDSLIST: "friends_list",
        _BLACKLIST: "blacklist",
    },
    "READ_NAMES": {
        "vip": _VIP,
        "flags": _FLAGS,
        "friendslist": _FRIENDSLIST,
        "blacklist": _BLACKLIST
    },
    "CHATLOG": ".chatlog.json",
    "DOT_FOLDER": ".settings"
}

def read_json(name):
    """Cmd function"""
    filename = g["READ_NAMES"].get(name, None)
    if filename:
        with open(filename, "r") as f:
            return json.load(f)

def update_json(name, data):
    """Cmd function"""
    filename = g["READ_NAMES"].get(name, None)
    if filename:
        with open(filename, "w+") as f:
            return json.dump(data, f)
    return data

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
    def edit_flags():
        g["EDIT_FILES"]["flags"]

    @staticmethod
    def edit_friends_list():
        pass

    @staticmethod
    def edit_vip_list():
        pass

    @staticmethod
    def edit_blacklist():
        pass

    @staticmethod
    def reset_chatlog():
        if path.exists(g["CHATLOG"]):
            remove(g["CHATLOG"])
