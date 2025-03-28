
from vsg.rules import token_case

from vsg import token

lTokens = []
lTokens.append(token.signal_declaration.signal_keyword)


class rule_002(token_case):
    '''
    This rule checks the **signal** keyword has proper case.

    Refer to `Configuring Uppercase and Lowercase Rules <configuring_uppercase_and_lowercase_rules.html>`_ for information on changing the default case.

    **Violation**

    .. code-block:: vhdl

       SIGNAL wr_en : std_logic;

    **Fix**

    .. code-block:: vhdl

       signal wr_en : std_logic;
    '''

    def __init__(self):
        token_case.__init__(self, 'signal', '002', lTokens)
        self.groups.append('case::keyword')
