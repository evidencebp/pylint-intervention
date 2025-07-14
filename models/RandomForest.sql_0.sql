create or replace function RandomForest_0 (simplifiable-if-expression int64, too-many-branches int64, too-many-statements int64, superfluous-parens int64, too-many-return-statements int64, too-many-nested-blocks int64, too-many-boolean-expressions int64, simplifiable-condition int64, Simplify-boolean-expression int64, comparison-of-constants int64, unnecessary-semicolon int64, using-constant-test int64, simplifiable-if-statement int64, try-except-raise int64, broad-exception-caught int64, wildcard-import int64, unnecessary-pass int64, pointless-statement int64, too-many-lines int64, line-too-long int64, is_refactor int64, McCabe_sum_reduced int64, McCabe_max_reduced int64, only_removal int64, mostly_delete int64, massive_change int64, high_ccp_group int64) as (
  case when too-many-statements <= 0.5 then
    case when too-many-return-statements <= 0.5 then
      case when line-too-long <= 0.5 then
        case when McCabe_max_reduced <= 0.5 then
          case when mostly_delete <= 0.5 then
            case when broad-exception-caught <= 0.5 then
              case when superfluous-parens <= 0.5 then
                case when McCabe_sum_reduced <= 0.5 then
                  case when only_removal <= 0.5 then
                     return 0.4 # (24.0 out of 60.0)
                  else  # if only_removal > 0.5
                     return 0.2631578947368421 # (5.0 out of 19.0)
                  end                 else  # if McCabe_sum_reduced > 0.5
                   return 0.3968253968253968 # (25.0 out of 63.0)
                end               else  # if superfluous-parens > 0.5
                case when McCabe_sum_reduced <= 0.5 then
                   return 0.5 # (29.0 out of 58.0)
                else  # if McCabe_sum_reduced > 0.5
                   return 0.5833333333333334 # (14.0 out of 24.0)
                end               end             else  # if broad-exception-caught > 0.5
               return 0.4 # (8.0 out of 20.0)
            end           else  # if mostly_delete > 0.5
            case when superfluous-parens <= 0.5 then
               return 0.6666666666666666 # (10.0 out of 15.0)
            else  # if superfluous-parens > 0.5
               return 0.8333333333333334 # (15.0 out of 18.0)
            end           end         else  # if McCabe_max_reduced > 0.5
          case when massive_change <= 0.5 then
            case when high_ccp_group <= 0.5 then
               return 0.32857142857142857 # (23.0 out of 70.0)
            else  # if high_ccp_group > 0.5
               return 0.8947368421052632 # (17.0 out of 19.0)
            end           else  # if massive_change > 0.5
             return 0.7037037037037037 # (19.0 out of 27.0)
          end         end       else  # if line-too-long > 0.5
         return 0.6153846153846154 # (40.0 out of 65.0)
      end     else  # if too-many-return-statements > 0.5
       return 0.25806451612903225 # (8.0 out of 31.0)
    end   else  # if too-many-statements > 0.5
    case when McCabe_sum_reduced <= 0.5 then
      case when is_refactor <= 0.5 then
         return 0.3870967741935484 # (12.0 out of 31.0)
      else  # if is_refactor > 0.5
         return 0.34285714285714286 # (12.0 out of 35.0)
      end     else  # if McCabe_sum_reduced > 0.5
      case when high_ccp_group <= 0.5 then
        case when is_refactor <= 0.5 then
           return 0.3888888888888889 # (7.0 out of 18.0)
        else  # if is_refactor > 0.5
           return 0.5 # (7.0 out of 14.0)
        end       else  # if high_ccp_group > 0.5
         return 0.7692307692307693 # (10.0 out of 13.0)
      end     end   end )