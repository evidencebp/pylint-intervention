create or replace function RandomForest_2 (too-many-branches int64, too-many-statements int64, too-many-return-statements int64, too-many-nested-blocks int64, is_refactor int64, McCabe_sum_reduced int64, McCabe_max_reduced int64, only_removal int64, mostly_delete int64, massive_change int64, high_ccp_group int64) as (
  case when McCabe_sum_reduced <= 0.5 then
    case when too-many-statements <= 0.5 then
       return 0.16666666666666666 # (6.0 out of 36.0)
    else  # if too-many-statements > 0.5
      case when is_refactor <= 0.5 then
         return 0.41379310344827586 # (12.0 out of 29.0)
      else  # if is_refactor > 0.5
         return 0.45 # (18.0 out of 40.0)
      end     end   else  # if McCabe_sum_reduced > 0.5
    case when high_ccp_group <= 0.5 then
      case when too-many-statements <= 0.5 then
         return 0.46808510638297873 # (22.0 out of 47.0)
      else  # if too-many-statements > 0.5
         return 0.5 # (21.0 out of 42.0)
      end     else  # if high_ccp_group > 0.5
       return 0.6857142857142857 # (24.0 out of 35.0)
    end   end )