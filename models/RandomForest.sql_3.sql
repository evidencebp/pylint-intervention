create or replace function RandomForest_3 (too-many-branches int64, too-many-statements int64, too-many-return-statements int64, too-many-nested-blocks int64, is_refactor int64, McCabe_sum_reduced int64, McCabe_max_reduced int64, only_removal int64, mostly_delete int64, massive_change int64, high_ccp_group int64) as (
  case when is_refactor <= 0.5 then
    case when McCabe_sum_reduced <= 0.5 then
      case when high_ccp_group <= 0.5 then
         return 0.15789473684210525 # (6.0 out of 38.0)
      else  # if high_ccp_group > 0.5
         return 0.16666666666666666 # (3.0 out of 18.0)
      end     else  # if McCabe_sum_reduced > 0.5
      case when too-many-branches <= 0.5 then
        case when too-many-statements <= 0.5 then
           return 0.5 # (13.0 out of 26.0)
        else  # if too-many-statements > 0.5
           return 0.41379310344827586 # (12.0 out of 29.0)
        end       else  # if too-many-branches > 0.5
         return 0.30434782608695654 # (7.0 out of 23.0)
      end     end   else  # if is_refactor > 0.5
    case when too-many-branches <= 0.5 then
      case when massive_change <= 0.5 then
         return 0.5227272727272727 # (23.0 out of 44.0)
      else  # if massive_change > 0.5
         return 0.4090909090909091 # (9.0 out of 22.0)
      end     else  # if too-many-branches > 0.5
       return 0.6206896551724138 # (18.0 out of 29.0)
    end   end )