create or replace function RandomForest_4 (too-many-branches int64, too-many-statements int64, too-many-return-statements int64, too-many-nested-blocks int64, is_refactor int64, McCabe_sum_reduced int64, McCabe_max_reduced int64, only_removal int64, mostly_delete int64, massive_change int64, high_ccp_group int64) as (
  case when McCabe_sum_reduced <= 0.5 then
    case when is_refactor <= 0.5 then
      case when too-many-statements <= 0.5 then
         return 0.0625 # (1.0 out of 16.0)
      else  # if too-many-statements > 0.5
         return 0.22727272727272727 # (5.0 out of 22.0)
      end     else  # if is_refactor > 0.5
      case when too-many-statements <= 0.5 then
         return 0.4444444444444444 # (8.0 out of 18.0)
      else  # if too-many-statements > 0.5
         return 0.5135135135135135 # (19.0 out of 37.0)
      end     end   else  # if McCabe_sum_reduced > 0.5
    case when too-many-return-statements <= 0.5 then
      case when is_refactor <= 0.5 then
        case when high_ccp_group <= 0.5 then
          case when too-many-branches <= 0.5 then
             return 0.38461538461538464 # (15.0 out of 39.0)
          else  # if too-many-branches > 0.5
             return 0.3333333333333333 # (7.0 out of 21.0)
          end         else  # if high_ccp_group > 0.5
           return 0.8076923076923077 # (21.0 out of 26.0)
        end       else  # if is_refactor > 0.5
        case when too-many-statements <= 0.5 then
           return 0.7777777777777778 # (14.0 out of 18.0)
        else  # if too-many-statements > 0.5
           return 0.5294117647058824 # (9.0 out of 17.0)
        end       end     else  # if too-many-return-statements > 0.5
       return 0.3333333333333333 # (5.0 out of 15.0)
    end   end )