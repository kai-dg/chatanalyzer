#!/usr/bin/env python3
class Error(Exception):
    pass

class ChatAnalyzerUrlError(Error):
    """Raised when the livestream url is not available."""
    message = "Livestream url not available."
    def __str__(self):
        return self.message

class MissingSettingFileError(Error):
    """Raised when cannot find a settings file."""
    message = "Setting file {} could not be found."
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
    def __str__(self, filename):
        return self.message.format(self.filename)
