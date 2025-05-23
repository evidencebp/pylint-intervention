
from vsg.rules import token_case

from vsg import token

lTokens = []
lTokens.append(token.if_statement.else_keyword)


class rule_027(token_case):
    '''
    This rule checks the **else** keyword has proper case.

    Refer to `Configuring Uppercase and Lowercase Rules <configuring_uppercase_and_lowercase_rules.html>`_ for information on changing the default case.

    **Violation**

    .. code-block:: vhdl

       ELSE

    **Fix**

    .. code-block:: vhdl

       else
    '''

    def __init__(self):
        token_case.__init__(self, 'if', '027', lTokens)
        self.groups.append('case::keyword')
