# Chat Analyzer

Livestream chat analyzer. Windows support only.

---

## Setup :wrench:

1. Install Python (python.org) and have Python in your cmd PATH

2. Run cmd.bat

## Usage

`ChatAnalyzer > start [url]`

`ChatAnalyzer > end`

`ChatAnalyzer > edit flags [flags_*] [on/off]`

`ChatAnalyzer > edit [name] [key/id] [value]*`

---

## Features

1. TTS OnlyFriends

    - Have TTS when specific user ids show up in chat

2. TTS Blacklist

    - Have TTS blacklist specific user ids

2. (TTS) VIP List

    - Rename selected users to change their name when TTS says their chat

---

## Examples

```
ChatAnalyzer > start https://youtube.com/mylivestream
ChatAnalyzer > end
ChatAnalyzer > edit flags flag_tts on
ChatAnalyzer > edit vip 123abcXYZ rick astley
ChatAnalyzer > edit friendslist 123abcXYZ rick astley
ChatAnalyzer > edit blacklist 123abcXYZ
```
