create or replace function RandomForest_9 (too-many-branches int64, too-many-statements int64, too-many-return-statements int64, too-many-nested-blocks int64, is_refactor int64, McCabe_sum_reduced int64, McCabe_max_reduced int64, only_removal int64, mostly_delete int64, massive_change int64, high_ccp_group int64) as (
  case when too-many-return-statements <= 0.5 then
    case when too-many-statements <= 0.5 then
      case when McCabe_sum_reduced <= 0.5 then
         return 0.42424242424242425 # (14.0 out of 33.0)
      else  # if McCabe_sum_reduced > 0.5
         return 0.47058823529411764 # (24.0 out of 51.0)
      end     else  # if too-many-statements > 0.5
      case when is_refactor <= 0.5 then
         return 0.375 # (24.0 out of 64.0)
      else  # if is_refactor > 0.5
         return 0.38181818181818183 # (21.0 out of 55.0)
      end     end   else  # if too-many-return-statements > 0.5
     return 0.15384615384615385 # (4.0 out of 26.0)
  end )