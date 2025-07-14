create or replace function RandomForest_5 (too-many-branches int64, too-many-statements int64, too-many-return-statements int64, too-many-nested-blocks int64, is_refactor int64, McCabe_sum_reduced int64, McCabe_max_reduced int64, only_removal int64, mostly_delete int64, massive_change int64, high_ccp_group int64) as (
  case when McCabe_sum_reduced <= 0.5 then
    case when mostly_delete <= 0.5 then
      case when is_refactor <= 0.5 then
         return 0.22448979591836735 # (11.0 out of 49.0)
      else  # if is_refactor > 0.5
         return 0.375 # (15.0 out of 40.0)
      end     else  # if mostly_delete > 0.5
       return 0.8 # (8.0 out of 10.0)
    end   else  # if McCabe_sum_reduced > 0.5
    case when too-many-branches <= 0.5 then
       return 0.5806451612903226 # (54.0 out of 93.0)
    else  # if too-many-branches > 0.5
       return 0.4594594594594595 # (17.0 out of 37.0)
    end   end )