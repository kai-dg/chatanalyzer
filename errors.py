#!/usr/bin/env python3
class Error(Exception):
    pass

class ChatAnalyzerUrlError(Error):
    """Raised when the livestream url is not available."""
    message = "Livestream url not available."
    def __str__(self):
        return self.message
