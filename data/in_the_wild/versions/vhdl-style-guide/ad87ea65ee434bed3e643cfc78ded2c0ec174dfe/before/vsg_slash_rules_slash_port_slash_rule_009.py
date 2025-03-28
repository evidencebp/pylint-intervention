
from vsg import token

from vsg.rules import spaces_before_and_after_tokens_when_bounded_by_tokens as Rule

lTokens = []
lTokens.append(token.mode.inout_keyword)

lBetween = [token.port_clause.open_parenthesis, token.port_clause.close_parenthesis]


class rule_009(Rule):
    '''
    This rule checks for spaces before and after the **inout** mode keyword.

    Refer to `Configuring Port Mode Alignment <configuring_port_mode_alignment.html>`_ for information on changing spaces.

    **Violation**

    .. code-block:: vhdl

       port (
         WR_EN    : in    std_logic;
         RD_EN    : in    std_logic;
         DATA     : inout    std_logic
       );

    **Fix**

    .. code-block:: vhdl

       port (
         WR_EN    : in    std_logic;
         RD_EN    : in    std_logic;
         DATA     : inout std_logic
       );
    '''
    def __init__(self):
        Rule.__init__(self, 'port', '009', lTokens, lBetween)
        self.spaces_before = 1
        self.spaces_after = 1
