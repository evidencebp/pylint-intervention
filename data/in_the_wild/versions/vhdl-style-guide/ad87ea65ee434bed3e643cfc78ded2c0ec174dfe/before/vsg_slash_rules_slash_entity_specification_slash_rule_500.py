
from vsg.rules import token_case

from vsg import token

lTokens = []
lTokens.append(token.entity_name_list.others_keyword)


class rule_500(token_case):
    '''
    This rule checks the **others** keyword has proper case.

    Refer to `Configuring Uppercase and Lowercase Rules <configuring_uppercase_and_lowercase_rules.html>`_ for information on changing the default case.

    **Violation**

    .. code-block:: vhdl

       attribute coordinate of OTHERS : component is (0.0, 17.5);

    **Fix**

    .. code-block:: vhdl

       attribute coordinate of others : component is (0.0, 17.5);
    '''

    def __init__(self):
        token_case.__init__(self, 'entity_specification', '500', lTokens)
        self.groups.append('case::keyword')
