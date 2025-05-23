
from vsg.rules import token_case

from vsg import token

lTokens = []
lTokens.append(token.if_statement.end_if_keyword)


class rule_034(token_case):
    '''
    This rule checks the **if** keyword in the **end if** has proper case.

    Refer to `Configuring Uppercase and Lowercase Rules <configuring_uppercase_and_lowercase_rules.html>`_ for information on changing the default case.

    **Violation**

    .. code-block:: vhdl

       end If;

       end IF;

    **Fix**

    .. code-block:: vhdl

       end if;

       end if;
    '''

    def __init__(self):
        token_case.__init__(self, 'if', '034', lTokens)
        self.groups.append('case::keyword')
