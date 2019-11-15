import re
import logging


class ContainsExpression(logging.Filter):
    def __init__(self, regex):
        self.regex = regex

    def filter(self, record):
        if re.match(self.regex, record.msg):
            return True
        else:
            return False
