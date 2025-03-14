
from vsg.rules import remove_blank_lines_above_item_rule

from vsg.token import context_declaration as token


class rule_027(remove_blank_lines_above_item_rule):
    '''
    Checks for a single space between the context keyword and the context identifier

    '''

    def __init__(self):
        remove_blank_lines_above_item_rule.__init__(self, 'context', '027', token.end_keyword)
        self.regionBegin = token.context_keyword
        self.regionEnd = token.semicolon
