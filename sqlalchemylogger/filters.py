import re
import logging


class ContainsExpression(logging.Filter):
    """
    Returns True if the regex is matched in the log message
    """
    def __init__(self, regex):
        self.regex = regex

    def filter(self, record):
        return bool(re.search(self.regex, record.msg))


class DoesNotContainExpression(logging.Filter):
    """
    Returns True if the regex is NOT matched in the log message
    """
    def __init__(self, regex):
        self.regex = regex

    def filter(self, record):
        return not bool(re.search(self.regex, record.msg))

