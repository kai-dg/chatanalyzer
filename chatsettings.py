#!/ussr/bin/env python3
import json
class AnalSettings:
    @staticmethod
    def add_flags_template(filepath):
        template = {
            "flag_tts": True,
            "flag_onlyfriends": False
        }
        with open(filepath, "w+") as f:
            json.dump(template, f)
