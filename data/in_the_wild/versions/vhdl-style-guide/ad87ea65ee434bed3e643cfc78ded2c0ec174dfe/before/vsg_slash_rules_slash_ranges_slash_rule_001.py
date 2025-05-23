
from vsg.rules import token_case

from vsg import token

lTokens = []
lTokens.append(token.direction.downto)


class rule_001(token_case):
    '''
    This rule checks the case of the **downto** keyword.

    Refer to `Configuring Uppercase and Lowercase Rules <configuring_uppercase_and_lowercase_rules.html>`_ for information on changing the default case.

    **Violation**

    .. code-block:: vhdl

       signal sig1 : std_logic_vector(3 DOWNTO 0);
       signal sig2 : std_logic_vector(16 downTO 1);

    **Fix**

    .. code-block:: vhdl

       signal sig1 : std_logic_vector(3 downto 0);
       signal sig2 : std_logic_vector(16 downTO 1);
    '''

    def __init__(self):
        token_case.__init__(self, 'range', '001', lTokens)
        self.groups.append('case::keyword')
