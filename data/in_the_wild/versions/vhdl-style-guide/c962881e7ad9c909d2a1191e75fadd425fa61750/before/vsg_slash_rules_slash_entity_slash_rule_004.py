
from vsg.rules import case_rule
from vsg import utils

class rule_004(case_rule):
    '''
    Entity rule 004 checks the entity keyword has proper case.
    '''

    def __init__(self):
        case_rule.__init__(self, 'entity', '004', 'isEntityDeclaration', utils.extract_first_keyword)
        self.solution = 'Change entity keyword to ' + self.case + 'case'
