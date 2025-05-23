
from vsg.rules import token_case

from vsg import token

lTokens = []
lTokens.append(token.process_statement.end_keyword)


class rule_008(token_case):
    '''
    This rule checks the **end** keyword has proper case.

    Refer to `Configuring Uppercase and Lowercase Rules <configuring_uppercase_and_lowercase_rules.html>`_ for information on changing the default case.

    **Violation**

    .. code-block:: vhdl

       END process proc_a;

    **Fix**

    .. code-block:: vhdl

       end process proc_a;
    '''

    def __init__(self):
        token_case.__init__(self, 'process', '008', lTokens)
        self.groups.append('case::keyword')
