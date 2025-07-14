create or replace function RandomForest_2 (simplifiable-if-expression int64, too-many-branches int64, too-many-statements int64, superfluous-parens int64, too-many-return-statements int64, too-many-nested-blocks int64, too-many-boolean-expressions int64, simplifiable-condition int64, Simplify-boolean-expression int64, comparison-of-constants int64, unnecessary-semicolon int64, using-constant-test int64, simplifiable-if-statement int64, try-except-raise int64, broad-exception-caught int64, wildcard-import int64, unnecessary-pass int64, pointless-statement int64, too-many-lines int64, line-too-long int64, is_refactor int64, McCabe_sum_reduced int64, McCabe_max_reduced int64, only_removal int64, mostly_delete int64, massive_change int64, high_ccp_group int64) as (
  case when line-too-long <= 0.5 then
    case when too-many-return-statements <= 0.5 then
      case when mostly_delete <= 0.5 then
         return 0.4698275862068966 # (218.0 out of 464.0)
      else  # if mostly_delete > 0.5
         return 0.6875 # (33.0 out of 48.0)
      end     else  # if too-many-return-statements > 0.5
       return 0.08 # (2.0 out of 25.0)
    end   else  # if line-too-long > 0.5
     return 0.6031746031746031 # (38.0 out of 63.0)
  end )