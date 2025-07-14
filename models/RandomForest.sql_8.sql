create or replace function RandomForest_8 (simplifiable-if-expression int64, too-many-branches int64, too-many-statements int64, superfluous-parens int64, too-many-return-statements int64, too-many-nested-blocks int64, too-many-boolean-expressions int64, simplifiable-condition int64, Simplify-boolean-expression int64, comparison-of-constants int64, unnecessary-semicolon int64, using-constant-test int64, simplifiable-if-statement int64, try-except-raise int64, broad-exception-caught int64, wildcard-import int64, unnecessary-pass int64, pointless-statement int64, too-many-lines int64, line-too-long int64, is_refactor int64, McCabe_sum_reduced int64, McCabe_max_reduced int64, only_removal int64, mostly_delete int64, massive_change int64, high_ccp_group int64) as (
  case when high_ccp_group <= 0.5 then
    case when line-too-long <= 0.5 then
      case when massive_change <= 0.5 then
        case when too-many-statements <= 0.5 then
          case when superfluous-parens <= 0.5 then
             return 0.30288461538461536 # (63.0 out of 208.0)
          else  # if superfluous-parens > 0.5
            case when McCabe_sum_reduced <= 0.5 then
               return 0.4146341463414634 # (17.0 out of 41.0)
            else  # if McCabe_sum_reduced > 0.5
               return 0.4375 # (7.0 out of 16.0)
            end           end         else  # if too-many-statements > 0.5
          case when McCabe_sum_reduced <= 0.5 then
             return 0.5625 # (18.0 out of 32.0)
          else  # if McCabe_sum_reduced > 0.5
             return 0.28125 # (9.0 out of 32.0)
          end         end       else  # if massive_change > 0.5
        case when too-many-statements <= 0.5 then
          case when McCabe_max_reduced <= 0.5 then
             return 0.5357142857142857 # (15.0 out of 28.0)
          else  # if McCabe_max_reduced > 0.5
             return 0.47619047619047616 # (10.0 out of 21.0)
          end         else  # if too-many-statements > 0.5
           return 0.5555555555555556 # (10.0 out of 18.0)
        end       end     else  # if line-too-long > 0.5
       return 0.5357142857142857 # (30.0 out of 56.0)
    end   else  # if high_ccp_group > 0.5
    case when McCabe_max_reduced <= 0.5 then
      case when superfluous-parens <= 0.5 then
         return 0.581081081081081 # (43.0 out of 74.0)
      else  # if superfluous-parens > 0.5
         return 0.6 # (15.0 out of 25.0)
      end     else  # if McCabe_max_reduced > 0.5
       return 0.7959183673469388 # (39.0 out of 49.0)
    end   end )