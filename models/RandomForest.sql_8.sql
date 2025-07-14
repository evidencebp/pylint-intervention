create or replace function RandomForest_8 (too-many-branches int64, too-many-statements int64, too-many-return-statements int64, too-many-nested-blocks int64, is_refactor int64, McCabe_sum_reduced int64, McCabe_max_reduced int64, only_removal int64, mostly_delete int64, massive_change int64, high_ccp_group int64) as (
  case when high_ccp_group <= 0.5 then
    case when massive_change <= 0.5 then
      case when too-many-nested-blocks <= 0.5 then
        case when too-many-return-statements <= 0.5 then
          case when is_refactor <= 0.5 then
            case when McCabe_max_reduced <= 0.5 then
               return 0.21875 # (7.0 out of 32.0)
            else  # if McCabe_max_reduced > 0.5
               return 0.2 # (6.0 out of 30.0)
            end           else  # if is_refactor > 0.5
            case when too-many-statements <= 0.5 then
               return 0.3888888888888889 # (7.0 out of 18.0)
            else  # if too-many-statements > 0.5
               return 0.5 # (18.0 out of 36.0)
            end           end         else  # if too-many-return-statements > 0.5
           return 0.3333333333333333 # (4.0 out of 12.0)
        end       else  # if too-many-nested-blocks > 0.5
         return 0.11764705882352941 # (2.0 out of 17.0)
      end     else  # if massive_change > 0.5
       return 0.45161290322580644 # (14.0 out of 31.0)
    end   else  # if high_ccp_group > 0.5
    case when too-many-branches <= 0.5 then
      case when McCabe_sum_reduced <= 0.5 then
         return 0.47058823529411764 # (8.0 out of 17.0)
      else  # if McCabe_sum_reduced > 0.5
         return 0.6111111111111112 # (11.0 out of 18.0)
      end     else  # if too-many-branches > 0.5
       return 0.7222222222222222 # (13.0 out of 18.0)
    end   end )