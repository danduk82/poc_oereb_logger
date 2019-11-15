import re
import logging


class ContainsExpression(logging.Filter):
    def __init__(self, regex):
        self.regex = regex

    def filter(self, record):
        return not bool(re.search(self.regex, record.msg))

