create or replace function Tree_md3 (simplifiable-if-expression int64, too-many-branches int64, too-many-statements int64, superfluous-parens int64, too-many-return-statements int64, too-many-nested-blocks int64, too-many-boolean-expressions int64, simplifiable-condition int64, Simplify-boolean-expression int64, comparison-of-constants int64, unnecessary-semicolon int64, using-constant-test int64, simplifiable-if-statement int64, try-except-raise int64, broad-exception-caught int64, wildcard-import int64, unnecessary-pass int64, pointless-statement int64, too-many-lines int64, line-too-long int64, is_refactor int64, McCabe_sum_reduced int64, McCabe_max_reduced int64, only_removal int64, mostly_delete int64, massive_change int64, high_ccp_group int64) as (
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
      case when broad-exception-caught <= 0.5 then
         return 0.44785276073619634 # (73.0 out of 163.0)
      else  # if broad-exception-caught > 0.5
         return 1.0 # (8.0 out of 8.0)
      end     else  # if massive_change > 0.5
      case when too-many-branches <= 0.5 then
         return 0.1346153846153846 # (7.0 out of 52.0)
      else  # if too-many-branches > 0.5
         return 1.0 # (2.0 out of 2.0)
      end     end   end )