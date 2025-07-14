create or replace function RandomForest_6 (simplifiable-if-expression int64, too-many-branches int64, too-many-statements int64, superfluous-parens int64, too-many-return-statements int64, too-many-nested-blocks int64, too-many-boolean-expressions int64, simplifiable-condition int64, Simplify-boolean-expression int64, comparison-of-constants int64, unnecessary-semicolon int64, using-constant-test int64, simplifiable-if-statement int64, try-except-raise int64, broad-exception-caught int64, wildcard-import int64, unnecessary-pass int64, pointless-statement int64, too-many-lines int64, line-too-long int64, is_refactor int64, McCabe_sum_reduced int64, McCabe_max_reduced int64, only_removal int64, mostly_delete int64, massive_change int64, high_ccp_group int64) as (
  case when too-many-nested-blocks <= 0.5 then
    case when superfluous-parens <= 0.5 then
      case when too-many-lines <= 0.5 then
        case when high_ccp_group <= 0.5 then
          case when line-too-long <= 0.5 then
            case when McCabe_sum_reduced <= 0.5 then
               return 0.23931623931623933 # (28.0 out of 117.0)
            else  # if McCabe_sum_reduced > 0.5
              case when too-many-branches <= 0.5 then
                 return 0.28440366972477066 # (31.0 out of 109.0)
              else  # if too-many-branches > 0.5
                 return 0.5862068965517241 # (17.0 out of 29.0)
              end             end           else  # if line-too-long > 0.5
             return 0.6046511627906976 # (26.0 out of 43.0)
          end         else  # if high_ccp_group > 0.5
          case when McCabe_max_reduced <= 0.5 then
             return 0.5862068965517241 # (34.0 out of 58.0)
          else  # if McCabe_max_reduced > 0.5
             return 0.625 # (25.0 out of 40.0)
          end         end       else  # if too-many-lines > 0.5
        case when massive_change <= 0.5 then
          case when McCabe_sum_reduced <= 0.5 then
             return 0.7142857142857143 # (15.0 out of 21.0)
          else  # if McCabe_sum_reduced > 0.5
             return 0.3076923076923077 # (12.0 out of 39.0)
          end         else  # if massive_change > 0.5
           return 0.42105263157894735 # (8.0 out of 19.0)
        end       end     else  # if superfluous-parens > 0.5
       return 0.6074766355140186 # (65.0 out of 107.0)
    end   else  # if too-many-nested-blocks > 0.5
     return 0.5 # (9.0 out of 18.0)
  end )