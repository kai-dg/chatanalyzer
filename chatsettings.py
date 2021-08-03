#!/ussr/bin/env python3
import json
import errors
from os import path, remove

_DOT_FOLDER = ".settings"
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
        "vip": path.join(_DOT_FOLDER, _VIP),
        "flags": path.join(_DOT_FOLDER, _FLAGS),
        "friendslist": path.join(_DOT_FOLDER, _FRIENDSLIST),
        "blacklist": path.join(_DOT_FOLDER, _BLACKLIST)
    },
    "DOT_FOLDER": _DOT_FOLDER
}

def read_json(name):
    """Cmd function"""
    try:
        with open(g["READ_NAMES"][name], "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise errors.MissingSettingFileError(g["READ_NAMES"][name])

def update_json(name, data):
    """Cmd function"""
    try:
        with open(g["READ_NAMES"][name], "w+") as f:
            return json.dump(data, f)
    except FileNotFoundError:
        raise errors.MissingSettingFileError(g["READ_NAMES"][name])

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
        a = g["EDIT_FILES"]["flags"]

    @staticmethod
    def edit_friends_list():
        pass

    @staticmethod
    def edit_vip_list():
        pass

    @staticmethod
    def edit_blacklist():
        pass
