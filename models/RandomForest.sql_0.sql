create or replace function RandomForest_0 (too-many-branches int64, too-many-statements int64, too-many-return-statements int64, too-many-nested-blocks int64, is_refactor int64, McCabe_sum_reduced int64, McCabe_max_reduced int64, only_removal int64, mostly_delete int64, massive_change int64, high_ccp_group int64) as (
  case when mostly_delete <= 0.5 then
    case when is_refactor <= 0.5 then
      case when high_ccp_group <= 0.5 then
        case when McCabe_max_reduced <= 0.5 then
          case when too-many-statements <= 0.5 then
             return 0.2727272727272727 # (6.0 out of 22.0)
          else  # if too-many-statements > 0.5
             return 0.09523809523809523 # (2.0 out of 21.0)
          end         else  # if McCabe_max_reduced > 0.5
           return 0.4 # (14.0 out of 35.0)
        end       else  # if high_ccp_group > 0.5
        case when McCabe_max_reduced <= 0.5 then
           return 0.42105263157894735 # (8.0 out of 19.0)
        else  # if McCabe_max_reduced > 0.5
           return 0.8571428571428571 # (24.0 out of 28.0)
        end       end     else  # if is_refactor > 0.5
      case when too-many-statements <= 0.5 then
        case when McCabe_sum_reduced <= 0.5 then
           return 0.5263157894736842 # (10.0 out of 19.0)
        else  # if McCabe_sum_reduced > 0.5
           return 0.65 # (13.0 out of 20.0)
        end       else  # if too-many-statements > 0.5
         return 0.46808510638297873 # (22.0 out of 47.0)
      end     end   else  # if mostly_delete > 0.5
     return 0.7777777777777778 # (14.0 out of 18.0)
  end )