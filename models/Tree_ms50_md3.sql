create or replace function Tree_ms50_md3 (simplifiable-if-expression int64, too-many-branches int64, too-many-statements int64, superfluous-parens int64, too-many-return-statements int64, too-many-nested-blocks int64, too-many-boolean-expressions int64, simplifiable-condition int64, Simplify-boolean-expression int64, comparison-of-constants int64, unnecessary-semicolon int64, using-constant-test int64, simplifiable-if-statement int64, try-except-raise int64, broad-exception-caught int64, wildcard-import int64, unnecessary-pass int64, pointless-statement int64, too-many-lines int64, line-too-long int64, is_refactor int64, McCabe_sum_reduced int64, McCabe_max_reduced int64, only_removal int64, mostly_delete int64, massive_change int64, high_ccp_group int64) as (
  case when high_ccp_group <= 0.5 then
    case when superfluous-parens <= 0.5 then
      case when line-too-long <= 0.5 then
         return 0.14732724902216426 # (113.0 out of 767.0)
      else  # if line-too-long > 0.5
         return 0.24299065420560748 # (26.0 out of 107.0)
      end     else  # if superfluous-parens > 0.5
      case when McCabe_sum_reduced <= 0.5 then
         return 0.22321428571428573 # (25.0 out of 112.0)
      else  # if McCabe_sum_reduced > 0.5
         return 0.4418604651162791 # (19.0 out of 43.0)
      end     end   else  # if high_ccp_group > 0.5
    case when massive_change <= 0.5 then
      case when is_refactor <= 0.5 then
         return 0.445859872611465 # (70.0 out of 157.0)
      else  # if is_refactor > 0.5
         return 0.7857142857142857 # (11.0 out of 14.0)
      end     else  # if massive_change > 0.5
      case when McCabe_max_reduced <= 0.5 then
         return 0.08333333333333333 # (3.0 out of 36.0)
      else  # if McCabe_max_reduced > 0.5
         return 0.3333333333333333 # (6.0 out of 18.0)
      end     end   end )