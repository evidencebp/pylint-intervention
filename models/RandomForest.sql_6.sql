create or replace function RandomForest_6 (too-many-branches int64, too-many-statements int64, too-many-return-statements int64, too-many-nested-blocks int64, is_refactor int64, McCabe_sum_reduced int64, McCabe_max_reduced int64, only_removal int64, mostly_delete int64, massive_change int64, high_ccp_group int64) as (
  case when too-many-statements <= 0.5 then
    case when is_refactor <= 0.5 then
      case when too-many-return-statements <= 0.5 then
         return 0.4262295081967213 # (26.0 out of 61.0)
      else  # if too-many-return-statements > 0.5
         return 0.1111111111111111 # (2.0 out of 18.0)
      end     else  # if is_refactor > 0.5
       return 0.5 # (15.0 out of 30.0)
    end   else  # if too-many-statements > 0.5
    case when is_refactor <= 0.5 then
      case when McCabe_max_reduced <= 0.5 then
         return 0.375 # (12.0 out of 32.0)
      else  # if McCabe_max_reduced > 0.5
         return 0.6666666666666666 # (26.0 out of 39.0)
      end     else  # if is_refactor > 0.5
      case when McCabe_sum_reduced <= 0.5 then
         return 0.59375 # (19.0 out of 32.0)
      else  # if McCabe_sum_reduced > 0.5
         return 0.4117647058823529 # (7.0 out of 17.0)
      end     end   end )