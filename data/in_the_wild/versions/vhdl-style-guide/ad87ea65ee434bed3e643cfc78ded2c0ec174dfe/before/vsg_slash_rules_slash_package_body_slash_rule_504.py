
from vsg.rules import token_case

from vsg import token

lTokens = []
lTokens.append(token.package_body.end_keyword)


class rule_504(token_case):
    '''
    This rule checks the **end** keyword has proper case.

    Refer to `Configuring Uppercase and Lowercase Rules <configuring_uppercase_and_lowercase_rules.html>`_ for information on changing the default case.

    **Violation**

    .. code-block:: vhdl

       END package fifo_pkg;

    **Fix**

    .. code-block:: vhdl

       end package fifo_pkg;
    '''

    def __init__(self):
        token_case.__init__(self, 'package_body', '504', lTokens)
        self.groups.append('case::keyword')
