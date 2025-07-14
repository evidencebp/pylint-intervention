create or replace function RandomForest_0 (hunks_num int64, McCabe_sum_after int64, added_lines int64, cur_count_y int64, changed_lines int64, N1_diff int64, added_functions int64, Single comments_before int64, McCabe_max_after int64, calculated_length_diff int64, h1_diff int64, difficulty_diff int64, too-many-nested-blocks int64, modified_McCabe_max_diff int64, removed_lines int64, prev_count int64, Blank_diff int64, prev_count_x int64, h2_diff int64, LLOC_before int64, Multi_diff int64, volume_diff int64, same_day_duration_avg_diff int64, N2_diff int64, one_file_fix_rate_diff int64, Comments_after int64, massive_change int64, Single comments_diff int64, Comments_before int64, SLOC_before int64, prev_count_y int64, vocabulary_diff int64, LOC_before int64, McCabe_sum_diff int64, high_ccp_group int64, McCabe_sum_before int64, is_refactor int64, cur_count_x int64, refactor_mle_diff int64, time_diff int64, bugs_diff int64, avg_coupling_code_size_cut_diff int64, LLOC_diff int64, Single comments_after int64, too-many-branches int64, McCabe_max_diff int64, too-many-statements int64, mostly_delete int64, effort_diff int64, length_diff int64, Blank_before int64, SLOC_diff int64, McCabe_max_before int64, LOC_diff int64, cur_count int64, too-many-return-statements int64, only_removal int64, Comments_diff int64) as (
  case when McCabe_max_after <= 12.5 then
    case when refactor_mle_diff <= -0.10672381147742271 then
      case when Single comments_before <= 41.5 then
         return 0.08695652173913043 # (2.0 out of 23.0)
      else  # if Single comments_before > 41.5
         return 0.7692307692307693 # (10.0 out of 13.0)
      end     else  # if refactor_mle_diff > -0.10672381147742271
      case when Blank_before <= 47.5 then
         return 1.0 # (27.0 out of 27.0)
      else  # if Blank_before > 47.5
        case when SLOC_diff <= -27.0 then
           return 0.8571428571428571 # (18.0 out of 21.0)
        else  # if SLOC_diff > -27.0
           return 0.4 # (8.0 out of 20.0)
        end       end     end   else  # if McCabe_max_after > 12.5
    case when LOC_before <= 493.5 then
       return 0.6923076923076923 # (9.0 out of 13.0)
    else  # if LOC_before > 493.5
      case when hunks_num <= 11.0 then
        case when changed_lines <= 20.5 then
           return 0.14705882352941177 # (5.0 out of 34.0)
        else  # if changed_lines > 20.5
          case when Single comments_before <= 48.5 then
             return 0.13333333333333333 # (2.0 out of 15.0)
          else  # if Single comments_before > 48.5
            case when McCabe_sum_after <= 225.5 then
               return 0.6470588235294118 # (11.0 out of 17.0)
            else  # if McCabe_sum_after > 225.5
               return 0.4 # (6.0 out of 15.0)
            end           end         end       else  # if hunks_num > 11.0
         return 0.06451612903225806 # (2.0 out of 31.0)
      end     end   end )