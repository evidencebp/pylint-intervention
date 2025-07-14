create or replace function RandomForest_5 (simplifiable-if-expression int64, too-many-branches int64, too-many-statements int64, superfluous-parens int64, too-many-return-statements int64, too-many-nested-blocks int64, too-many-boolean-expressions int64, simplifiable-condition int64, Simplify-boolean-expression int64, comparison-of-constants int64, unnecessary-semicolon int64, using-constant-test int64, simplifiable-if-statement int64, try-except-raise int64, broad-exception-caught int64, wildcard-import int64, unnecessary-pass int64, pointless-statement int64, too-many-lines int64, line-too-long int64, is_refactor int64, McCabe_sum_reduced int64, McCabe_max_reduced int64, only_removal int64, mostly_delete int64, massive_change int64, high_ccp_group int64) as (
  case when high_ccp_group <= 0.5 then
    case when superfluous-parens <= 0.5 then
      case when is_refactor <= 0.5 then
        case when too-many-lines <= 0.5 then
          case when too-many-branches <= 0.5 then
            case when broad-exception-caught <= 0.5 then
              case when massive_change <= 0.5 then
                 return 0.29310344827586204 # (51.0 out of 174.0)
              else  # if massive_change > 0.5
                 return 0.5862068965517241 # (17.0 out of 29.0)
              end             else  # if broad-exception-caught > 0.5
               return 0.06666666666666667 # (1.0 out of 15.0)
            end           else  # if too-many-branches > 0.5
             return 0.16279069767441862 # (7.0 out of 43.0)
          end         else  # if too-many-lines > 0.5
           return 0.4339622641509434 # (23.0 out of 53.0)
        end       else  # if is_refactor > 0.5
        case when McCabe_max_reduced <= 0.5 then
           return 0.5517241379310345 # (16.0 out of 29.0)
        else  # if McCabe_max_reduced > 0.5
           return 0.34285714285714286 # (12.0 out of 35.0)
        end       end     else  # if superfluous-parens > 0.5
       return 0.5340909090909091 # (47.0 out of 88.0)
    end   else  # if high_ccp_group > 0.5
    case when only_removal <= 0.5 then
       return 0.6583333333333333 # (79.0 out of 120.0)
    else  # if only_removal > 0.5
       return 0.7142857142857143 # (10.0 out of 14.0)
    end   end )