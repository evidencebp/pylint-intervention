create or replace function RandomForest_9 (simplifiable-if-expression int64, too-many-branches int64, too-many-statements int64, superfluous-parens int64, too-many-return-statements int64, too-many-nested-blocks int64, too-many-boolean-expressions int64, simplifiable-condition int64, Simplify-boolean-expression int64, comparison-of-constants int64, unnecessary-semicolon int64, using-constant-test int64, simplifiable-if-statement int64, try-except-raise int64, broad-exception-caught int64, wildcard-import int64, unnecessary-pass int64, pointless-statement int64, too-many-lines int64, line-too-long int64, is_refactor int64, McCabe_sum_reduced int64, McCabe_max_reduced int64, only_removal int64, mostly_delete int64, massive_change int64, high_ccp_group int64) as (
  case when mostly_delete <= 0.5 then
    case when only_removal <= 0.5 then
      case when superfluous-parens <= 0.5 then
        case when too-many-statements <= 0.5 then
          case when high_ccp_group <= 0.5 then
            case when broad-exception-caught <= 0.5 then
              case when line-too-long <= 0.5 then
                case when is_refactor <= 0.5 then
                  case when massive_change <= 0.5 then
                     return 0.32116788321167883 # (44.0 out of 137.0)
                  else  # if massive_change > 0.5
                     return 0.2857142857142857 # (10.0 out of 35.0)
                  end                 else  # if is_refactor > 0.5
                   return 0.5 # (18.0 out of 36.0)
                end               else  # if line-too-long > 0.5
                 return 0.4166666666666667 # (20.0 out of 48.0)
              end             else  # if broad-exception-caught > 0.5
               return 0.15789473684210525 # (3.0 out of 19.0)
            end           else  # if high_ccp_group > 0.5
             return 0.7761194029850746 # (52.0 out of 67.0)
          end         else  # if too-many-statements > 0.5
          case when McCabe_max_reduced <= 0.5 then
             return 0.30303030303030304 # (10.0 out of 33.0)
          else  # if McCabe_max_reduced > 0.5
            case when McCabe_sum_reduced <= 0.5 then
               return 0.15384615384615385 # (2.0 out of 13.0)
            else  # if McCabe_sum_reduced > 0.5
              case when massive_change <= 0.5 then
                 return 0.3225806451612903 # (10.0 out of 31.0)
              else  # if massive_change > 0.5
                 return 0.5416666666666666 # (13.0 out of 24.0)
              end             end           end         end       else  # if superfluous-parens > 0.5
        case when McCabe_sum_reduced <= 0.5 then
           return 0.41818181818181815 # (23.0 out of 55.0)
        else  # if McCabe_sum_reduced > 0.5
           return 0.5909090909090909 # (13.0 out of 22.0)
        end       end     else  # if only_removal > 0.5
      case when high_ccp_group <= 0.5 then
         return 0.5 # (10.0 out of 20.0)
      else  # if high_ccp_group > 0.5
         return 0.6875 # (11.0 out of 16.0)
      end     end   else  # if mostly_delete > 0.5
     return 0.6818181818181818 # (30.0 out of 44.0)
  end )