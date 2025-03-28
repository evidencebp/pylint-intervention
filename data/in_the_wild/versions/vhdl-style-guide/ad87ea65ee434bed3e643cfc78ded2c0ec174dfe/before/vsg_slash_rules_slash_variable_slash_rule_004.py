
from vsg.rules import token_case_with_prefix_suffix

from vsg import token

lTokens = []
lTokens.append(token.variable_declaration.identifier)


class rule_004(token_case_with_prefix_suffix):
    '''
    This rule checks the variable name has proper case.

    Refer to `Configuring Uppercase and Lowercase Rules <configuring_uppercase_and_lowercase_rules.html>`_ for information on changing the default case.

    **Violation**

    .. code-block:: vhdl

       variable COUNT : integer;

    **Fix**

    .. code-block:: vhdl

       variable count : integer;
    '''

    def __init__(self):
        token_case_with_prefix_suffix.__init__(self, 'variable', '004', lTokens)
        self.groups.append('case::name')
