
from vsg.rules import token_case

from vsg import token

lTokens = []
lTokens.append(token.port_clause.port_keyword)


class rule_017(token_case):
    '''
    This rule checks the **port** keyword has proper case.

    Refer to `Configuring Uppercase and Lowercase Rules <configuring_uppercase_and_lowercase_rules.html>`_ for information on changing the default case.

    **Violation**

    .. code-block:: vhdl

       PORT (

    **Fix**

    .. code-block:: vhdl

       port (
    '''

    def __init__(self):
        token_case.__init__(self, 'port', '017', lTokens)
        self.groups.append('case::keyword')
