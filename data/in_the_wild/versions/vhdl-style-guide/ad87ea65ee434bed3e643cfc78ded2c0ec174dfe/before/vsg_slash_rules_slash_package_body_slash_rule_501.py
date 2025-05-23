
from vsg.rules import token_case

from vsg import token

lTokens = []
lTokens.append(token.package_body.body_keyword)


class rule_501(token_case):
    '''
    This rule checks the **body** keyword has proper case.

    Refer to `Configuring Uppercase and Lowercase Rules <configuring_uppercase_and_lowercase_rules.html>`_ for information on changing the default case.

    **Violation**

    .. code-block:: vhdl

       package BODY FIFO_PKG is

    **Fix**

    .. code-block:: vhdl

       package body FIFO_PKG is
    '''

    def __init__(self):
        token_case.__init__(self, 'package_body', '501', lTokens)
        self.groups.append('case::keyword')
