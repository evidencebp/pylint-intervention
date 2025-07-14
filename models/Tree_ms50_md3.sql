create or replace function Tree_ms50_md3 (too-many-branches int64, too-many-statements int64, too-many-return-statements int64, too-many-nested-blocks int64, is_refactor int64, McCabe_sum_reduced int64, McCabe_max_reduced int64, only_removal int64, mostly_delete int64, massive_change int64, high_ccp_group int64) as (
  case when high_ccp_group <= 0.5 then
    case when mostly_delete <= 0.5 then
      case when massive_change <= 0.5 then
         return 0.11428571428571428 # (36.0 out of 315.0)
      else  # if massive_change > 0.5
         return 0.3076923076923077 # (16.0 out of 52.0)
      end     else  # if mostly_delete > 0.5
       return 0.5 # (9.0 out of 18.0)
    end   else  # if high_ccp_group > 0.5
    case when too-many-return-statements <= 0.5 then
      case when McCabe_sum_reduced <= 0.5 then
         return 0.3333333333333333 # (15.0 out of 45.0)
      else  # if McCabe_sum_reduced > 0.5
         return 0.5714285714285714 # (20.0 out of 35.0)
      end     else  # if too-many-return-statements > 0.5
       return 0.07692307692307693 # (2.0 out of 26.0)
    end   end )