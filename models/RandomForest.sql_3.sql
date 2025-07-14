create or replace function RandomForest_3 (simplifiable-if-expression int64, too-many-branches int64, too-many-statements int64, superfluous-parens int64, too-many-return-statements int64, too-many-nested-blocks int64, too-many-boolean-expressions int64, simplifiable-condition int64, Simplify-boolean-expression int64, comparison-of-constants int64, unnecessary-semicolon int64, using-constant-test int64, simplifiable-if-statement int64, try-except-raise int64, broad-exception-caught int64, wildcard-import int64, unnecessary-pass int64, pointless-statement int64, too-many-lines int64, line-too-long int64, is_refactor int64, McCabe_sum_reduced int64, McCabe_max_reduced int64, only_removal int64, mostly_delete int64, massive_change int64, high_ccp_group int64) as (
  case when line-too-long <= 0.5 then
    case when McCabe_sum_reduced <= 0.5 then
      case when superfluous-parens <= 0.5 then
        case when too-many-branches <= 0.5 then
          case when only_removal <= 0.5 then
            case when massive_change <= 0.5 then
              case when is_refactor <= 0.5 then
                 return 0.29347826086956524 # (27.0 out of 92.0)
              else  # if is_refactor > 0.5
                 return 0.5142857142857142 # (18.0 out of 35.0)
              end             else  # if massive_change > 0.5
               return 0.25 # (5.0 out of 20.0)
            end           else  # if only_removal > 0.5
             return 0.6842105263157895 # (13.0 out of 19.0)
          end         else  # if too-many-branches > 0.5
           return 0.45 # (9.0 out of 20.0)
        end       else  # if superfluous-parens > 0.5
         return 0.5254237288135594 # (31.0 out of 59.0)
      end     else  # if McCabe_sum_reduced > 0.5
      case when too-many-return-statements <= 0.5 then
        case when McCabe_max_reduced <= 0.5 then
          case when superfluous-parens <= 0.5 then
             return 0.45 # (45.0 out of 100.0)
          else  # if superfluous-parens > 0.5
             return 0.5555555555555556 # (10.0 out of 18.0)
          end         else  # if McCabe_max_reduced > 0.5
          case when too-many-branches <= 0.5 then
            case when too-many-statements <= 0.5 then
               return 0.5692307692307692 # (37.0 out of 65.0)
            else  # if too-many-statements > 0.5
              case when massive_change <= 0.5 then
                 return 0.3333333333333333 # (11.0 out of 33.0)
              else  # if massive_change > 0.5
                 return 0.7142857142857143 # (15.0 out of 21.0)
              end             end           else  # if too-many-branches > 0.5
             return 0.47368421052631576 # (18.0 out of 38.0)
          end         end       else  # if too-many-return-statements > 0.5
         return 0.13636363636363635 # (3.0 out of 22.0)
      end     end   else  # if line-too-long > 0.5
     return 0.6379310344827587 # (37.0 out of 58.0)
  end )