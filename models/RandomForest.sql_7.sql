create or replace function RandomForest_7 (simplifiable-if-expression int64, too-many-branches int64, too-many-statements int64, superfluous-parens int64, too-many-return-statements int64, too-many-nested-blocks int64, too-many-boolean-expressions int64, simplifiable-condition int64, Simplify-boolean-expression int64, comparison-of-constants int64, unnecessary-semicolon int64, using-constant-test int64, simplifiable-if-statement int64, try-except-raise int64, broad-exception-caught int64, wildcard-import int64, unnecessary-pass int64, pointless-statement int64, too-many-lines int64, line-too-long int64, is_refactor int64, McCabe_sum_reduced int64, McCabe_max_reduced int64, only_removal int64, mostly_delete int64, massive_change int64, high_ccp_group int64) as (
  case when too-many-branches <= 0.5 then
    case when high_ccp_group <= 0.5 then
      case when McCabe_sum_reduced <= 0.5 then
        case when too-many-statements <= 0.5 then
          case when superfluous-parens <= 0.5 then
             return 0.3979591836734694 # (39.0 out of 98.0)
          else  # if superfluous-parens > 0.5
             return 0.4626865671641791 # (31.0 out of 67.0)
          end         else  # if too-many-statements > 0.5
          case when is_refactor <= 0.5 then
             return 0.3076923076923077 # (8.0 out of 26.0)
          else  # if is_refactor > 0.5
             return 0.34615384615384615 # (9.0 out of 26.0)
          end         end       else  # if McCabe_sum_reduced > 0.5
        case when too-many-lines <= 0.5 then
          case when too-many-return-statements <= 0.5 then
             return 0.4496124031007752 # (58.0 out of 129.0)
          else  # if too-many-return-statements > 0.5
             return 0.16666666666666666 # (3.0 out of 18.0)
          end         else  # if too-many-lines > 0.5
           return 0.43103448275862066 # (25.0 out of 58.0)
        end       end     else  # if high_ccp_group > 0.5
       return 0.6782608695652174 # (78.0 out of 115.0)
    end   else  # if too-many-branches > 0.5
    case when McCabe_max_reduced <= 0.5 then
       return 0.5555555555555556 # (10.0 out of 18.0)
    else  # if McCabe_max_reduced > 0.5
      case when is_refactor <= 0.5 then
         return 0.3076923076923077 # (8.0 out of 26.0)
      else  # if is_refactor > 0.5
         return 0.42105263157894735 # (8.0 out of 19.0)
      end     end   end )