create or replace function Tree_ms50 (too-many-branches int64, too-many-statements int64, too-many-return-statements int64, too-many-nested-blocks int64, is_refactor int64, McCabe_sum_reduced int64, McCabe_max_reduced int64, only_removal int64, mostly_delete int64, massive_change int64, high_ccp_group int64) as (
  case when high_ccp_group <= 0.5 then
    case when mostly_delete <= 0.5 then
      case when massive_change <= 0.5 then
        case when is_refactor <= 0.5 then
          case when McCabe_max_reduced <= 0.5 then
            case when McCabe_sum_reduced <= 0.5 then
              case when too-many-statements <= 0.5 then
                 return 0.03571428571428571 # (1.0 out of 28.0)
              else  # if too-many-statements > 0.5
                 return 0.1 # (4.0 out of 40.0)
              end             else  # if McCabe_sum_reduced > 0.5
               return 0.13333333333333333 # (6.0 out of 45.0)
            end           else  # if McCabe_max_reduced > 0.5
            case when too-many-branches <= 0.5 then
               return 0.0425531914893617 # (2.0 out of 47.0)
            else  # if too-many-branches > 0.5
               return 0.08695652173913043 # (4.0 out of 46.0)
            end           end         else  # if is_refactor > 0.5
          case when McCabe_sum_reduced <= 0.5 then
            case when McCabe_max_reduced <= 0.5 then
               return 0.1111111111111111 # (3.0 out of 27.0)
            else  # if McCabe_max_reduced > 0.5
               return 0.07142857142857142 # (3.0 out of 42.0)
            end           else  # if McCabe_sum_reduced > 0.5
            case when too-many-statements <= 0.5 then
               return 0.4 # (8.0 out of 20.0)
            else  # if too-many-statements > 0.5
               return 0.25 # (5.0 out of 20.0)
            end           end         end       else  # if massive_change > 0.5
        case when is_refactor <= 0.5 then
           return 0.5 # (12.0 out of 24.0)
        else  # if is_refactor > 0.5
           return 0.14285714285714285 # (4.0 out of 28.0)
        end       end     else  # if mostly_delete > 0.5
       return 0.5 # (9.0 out of 18.0)
    end   else  # if high_ccp_group > 0.5
    case when too-many-return-statements <= 0.5 then
      case when McCabe_sum_reduced <= 0.5 then
        case when is_refactor <= 0.5 then
           return 0.19230769230769232 # (5.0 out of 26.0)
        else  # if is_refactor > 0.5
           return 0.5263157894736842 # (10.0 out of 19.0)
        end       else  # if McCabe_sum_reduced > 0.5
         return 0.5714285714285714 # (20.0 out of 35.0)
      end     else  # if too-many-return-statements > 0.5
       return 0.07692307692307693 # (2.0 out of 26.0)
    end   end )