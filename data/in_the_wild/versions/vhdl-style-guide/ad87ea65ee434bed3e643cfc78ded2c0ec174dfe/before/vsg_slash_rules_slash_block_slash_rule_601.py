
from vsg import token

from vsg.rules import token_prefix

lTokens = []
lTokens.append(token.block_statement.block_label)
lTokens.append(token.block_statement.end_block_label)


class rule_601(token_prefix):
    '''
    This rule checks for valid prefixes on block labels.
    The default prefix is *blk_*.

    Refer to `Configuring Prefix and Suffix Rules <configuring_prefix_and_suffix_rules.html>`_ for information on changing the allowed prefixes.

    **Violation**

    .. code-block:: vhdl

       block_label : block is

    **Fix**

    .. code-block:: vhdl

       blk_block_label : block is
    '''

    def __init__(self):
        token_prefix.__init__(self, 'block', '601', lTokens)
        self.prefixes = ['blk_']
        self.solution = 'block label'
