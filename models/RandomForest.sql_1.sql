create or replace function RandomForest_1 (simplifiable-if-expression int64, too-many-branches int64, too-many-statements int64, superfluous-parens int64, too-many-return-statements int64, too-many-nested-blocks int64, too-many-boolean-expressions int64, simplifiable-condition int64, Simplify-boolean-expression int64, comparison-of-constants int64, unnecessary-semicolon int64, using-constant-test int64, simplifiable-if-statement int64, try-except-raise int64, broad-exception-caught int64, wildcard-import int64, unnecessary-pass int64, pointless-statement int64, too-many-lines int64, line-too-long int64, is_refactor int64, McCabe_sum_reduced int64, McCabe_max_reduced int64, only_removal int64, mostly_delete int64, massive_change int64, high_ccp_group int64) as (
  case when pointless-statement <= 0.5 then
    case when high_ccp_group <= 0.5 then
      case when massive_change <= 0.5 then
        case when too-many-return-statements <= 0.5 then
          case when mostly_delete <= 0.5 then
            case when only_removal <= 0.5 then
              case when line-too-long <= 0.5 then
                case when McCabe_max_reduced <= 0.5 then
                   return 0.3727810650887574 # (63.0 out of 169.0)
                else  # if McCabe_max_reduced > 0.5
                   return 0.3176470588235294 # (27.0 out of 85.0)
                end               else  # if line-too-long > 0.5
                 return 0.5897435897435898 # (23.0 out of 39.0)
              end             else  # if only_removal > 0.5
               return 0.4444444444444444 # (8.0 out of 18.0)
            end           else  # if mostly_delete > 0.5
             return 0.6341463414634146 # (26.0 out of 41.0)
          end         else  # if too-many-return-statements > 0.5
           return 0.1111111111111111 # (2.0 out of 18.0)
        end       else  # if massive_change > 0.5
        case when too-many-statements <= 0.5 then
          case when superfluous-parens <= 0.5 then
             return 0.5714285714285714 # (20.0 out of 35.0)
          else  # if superfluous-parens > 0.5
             return 0.5714285714285714 # (12.0 out of 21.0)
          end         else  # if too-many-statements > 0.5
           return 0.5555555555555556 # (15.0 out of 27.0)
        end       end     else  # if high_ccp_group > 0.5
      case when McCabe_sum_reduced <= 0.5 then
         return 0.5396825396825397 # (34.0 out of 63.0)
      else  # if McCabe_sum_reduced > 0.5
        case when McCabe_max_reduced <= 0.5 then
           return 0.7 # (21.0 out of 30.0)
        else  # if McCabe_max_reduced > 0.5
           return 0.7297297297297297 # (27.0 out of 37.0)
        end       end     end   else  # if pointless-statement > 0.5
     return 0.6470588235294118 # (11.0 out of 17.0)
  end )