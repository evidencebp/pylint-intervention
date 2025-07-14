create or replace function RandomForest_4 (simplifiable-if-expression int64, too-many-branches int64, too-many-statements int64, superfluous-parens int64, too-many-return-statements int64, too-many-nested-blocks int64, too-many-boolean-expressions int64, simplifiable-condition int64, Simplify-boolean-expression int64, comparison-of-constants int64, unnecessary-semicolon int64, using-constant-test int64, simplifiable-if-statement int64, try-except-raise int64, broad-exception-caught int64, wildcard-import int64, unnecessary-pass int64, pointless-statement int64, too-many-lines int64, line-too-long int64, is_refactor int64, McCabe_sum_reduced int64, McCabe_max_reduced int64, only_removal int64, mostly_delete int64, massive_change int64, high_ccp_group int64) as (
  case when high_ccp_group <= 0.5 then
    case when line-too-long <= 0.5 then
      case when broad-exception-caught <= 0.5 then
        case when unnecessary-pass <= 0.5 then
          case when too-many-return-statements <= 0.5 then
            case when mostly_delete <= 0.5 then
              case when massive_change <= 0.5 then
                 return 0.38461538461538464 # (90.0 out of 234.0)
              else  # if massive_change > 0.5
                 return 0.5342465753424658 # (39.0 out of 73.0)
              end             else  # if mostly_delete > 0.5
              case when too-many-statements <= 0.5 then
                 return 0.4838709677419355 # (15.0 out of 31.0)
              else  # if too-many-statements > 0.5
                 return 0.8 # (12.0 out of 15.0)
              end             end           else  # if too-many-return-statements > 0.5
             return 0.047619047619047616 # (1.0 out of 21.0)
          end         else  # if unnecessary-pass > 0.5
           return 0.23076923076923078 # (3.0 out of 13.0)
        end       else  # if broad-exception-caught > 0.5
         return 0.09523809523809523 # (2.0 out of 21.0)
      end     else  # if line-too-long > 0.5
       return 0.5172413793103449 # (30.0 out of 58.0)
    end   else  # if high_ccp_group > 0.5
     return 0.664179104477612 # (89.0 out of 134.0)
  end )