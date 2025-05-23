
from vsg.rules import blank_line_below_line_ending_with_token

from vsg import token

lTokens = []
lTokens.append(token.package_declaration.is_keyword)


class rule_011(blank_line_below_line_ending_with_token):
    '''
    This rule checks for a blank line below the **package** keyword.

    Refer to `Configuring Blank Lines <configuring_blank_lines.html>`_ for options regarding comments.

    **Violation**

    .. code-block:: vhdl

       package FIFO_PKG is
         constant width : integer := 32;

    **Fix**

    .. code-block:: vhdl

       package FIFO_PKG is

         constant width : integer := 32;
    '''

    def __init__(self):
        blank_line_below_line_ending_with_token.__init__(self, 'package', '011', lTokens)
