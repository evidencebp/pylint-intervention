
from vsg.rules import token_case

from vsg import token

lTokens = []
lTokens.append(token.case_statement_alternative.when_keyword)


class rule_016(token_case):
    '''
    This rule checks the **when** has proper case.

    Refer to `Configuring Uppercase and Lowercase Rules <configuring_uppercase_and_lowercase_rules.html>`_ for information on changing the default case.

    **Violation**

    .. code-block:: vhdl

         WHEN a =>
         When b =>
         when c =>

    **Fix**

    .. code-block:: vhdl

         when a =>
         when b =>
         when c =>
    '''

    def __init__(self):
        token_case.__init__(self, 'case', '016', lTokens)
        self.groups.append('case::keyword')
