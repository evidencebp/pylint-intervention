create or replace function RandomForest_1 (too-many-branches int64, too-many-statements int64, too-many-return-statements int64, too-many-nested-blocks int64, is_refactor int64, McCabe_sum_reduced int64, McCabe_max_reduced int64, only_removal int64, mostly_delete int64, massive_change int64, high_ccp_group int64) as (
  case when mostly_delete <= 0.5 then
    case when high_ccp_group <= 0.5 then
      case when massive_change <= 0.5 then
        case when too-many-statements <= 0.5 then
          case when is_refactor <= 0.5 then
            case when too-many-branches <= 0.5 then
               return 0.11764705882352941 # (2.0 out of 17.0)
            else  # if too-many-branches > 0.5
               return 0.24 # (6.0 out of 25.0)
            end           else  # if is_refactor > 0.5
             return 0.2777777777777778 # (5.0 out of 18.0)
          end         else  # if too-many-statements > 0.5
          case when is_refactor <= 0.5 then
             return 0.3 # (12.0 out of 40.0)
          else  # if is_refactor > 0.5
             return 0.25 # (5.0 out of 20.0)
          end         end       else  # if massive_change > 0.5
         return 0.52 # (13.0 out of 25.0)
      end     else  # if high_ccp_group > 0.5
      case when too-many-statements <= 0.5 then
         return 0.3333333333333333 # (9.0 out of 27.0)
      else  # if too-many-statements > 0.5
        case when McCabe_max_reduced <= 0.5 then
           return 0.3888888888888889 # (7.0 out of 18.0)
        else  # if McCabe_max_reduced > 0.5
           return 0.8181818181818182 # (18.0 out of 22.0)
        end       end     end   else  # if mostly_delete > 0.5
     return 0.8823529411764706 # (15.0 out of 17.0)
  end )