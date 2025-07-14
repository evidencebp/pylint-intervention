create or replace function RandomForest_7 (too-many-branches int64, too-many-statements int64, too-many-return-statements int64, too-many-nested-blocks int64, is_refactor int64, McCabe_sum_reduced int64, McCabe_max_reduced int64, only_removal int64, mostly_delete int64, massive_change int64, high_ccp_group int64) as (
  case when too-many-statements <= 0.5 then
    case when too-many-return-statements <= 0.5 then
      case when McCabe_sum_reduced <= 0.5 then
         return 0.20689655172413793 # (6.0 out of 29.0)
      else  # if McCabe_sum_reduced > 0.5
        case when is_refactor <= 0.5 then
           return 0.40540540540540543 # (15.0 out of 37.0)
        else  # if is_refactor > 0.5
           return 0.5714285714285714 # (8.0 out of 14.0)
        end       end     else  # if too-many-return-statements > 0.5
       return 0.23076923076923078 # (6.0 out of 26.0)
    end   else  # if too-many-statements > 0.5
    case when high_ccp_group <= 0.5 then
       return 0.4367816091954023 # (38.0 out of 87.0)
    else  # if high_ccp_group > 0.5
      case when McCabe_max_reduced <= 0.5 then
         return 0.47619047619047616 # (10.0 out of 21.0)
      else  # if McCabe_max_reduced > 0.5
         return 0.8666666666666667 # (13.0 out of 15.0)
      end     end   end )