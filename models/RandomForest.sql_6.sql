create or replace function RandomForest_6 (hunks_num int64, McCabe_sum_after int64, added_lines int64, cur_count_y int64, changed_lines int64, N1_diff int64, added_functions int64, Single comments_before int64, McCabe_max_after int64, calculated_length_diff int64, h1_diff int64, difficulty_diff int64, too-many-nested-blocks int64, modified_McCabe_max_diff int64, removed_lines int64, prev_count int64, Blank_diff int64, prev_count_x int64, h2_diff int64, LLOC_before int64, Multi_diff int64, volume_diff int64, same_day_duration_avg_diff int64, N2_diff int64, one_file_fix_rate_diff int64, Comments_after int64, massive_change int64, Single comments_diff int64, Comments_before int64, SLOC_before int64, prev_count_y int64, vocabulary_diff int64, LOC_before int64, McCabe_sum_diff int64, high_ccp_group int64, McCabe_sum_before int64, is_refactor int64, cur_count_x int64, refactor_mle_diff int64, time_diff int64, bugs_diff int64, avg_coupling_code_size_cut_diff int64, LLOC_diff int64, Single comments_after int64, too-many-branches int64, McCabe_max_diff int64, too-many-statements int64, mostly_delete int64, effort_diff int64, length_diff int64, Blank_before int64, SLOC_diff int64, McCabe_max_before int64, LOC_diff int64, cur_count int64, too-many-return-statements int64, only_removal int64, Comments_diff int64) as (
  case when LLOC_before <= 345.5 then
    case when LOC_diff <= 9.5 then
      case when modified_McCabe_max_diff <= -0.5 then
        case when Comments_after <= 24.0 then
           return 0.2222222222222222 # (4.0 out of 18.0)
        else  # if Comments_after > 24.0
           return 0.9090909090909091 # (20.0 out of 22.0)
        end       else  # if modified_McCabe_max_diff > -0.5
         return 0.2903225806451613 # (9.0 out of 31.0)
      end     else  # if LOC_diff > 9.5
       return 0.875 # (28.0 out of 32.0)
    end   else  # if LLOC_before > 345.5
    case when N2_diff <= -3.5 then
      case when McCabe_sum_after <= 290.0 then
        case when length_diff <= -55.0 then
           return 0.35294117647058826 # (6.0 out of 17.0)
        else  # if length_diff > -55.0
           return 0.875 # (14.0 out of 16.0)
        end       else  # if McCabe_sum_after > 290.0
         return 0.3125 # (5.0 out of 16.0)
      end     else  # if N2_diff > -3.5
      case when hunks_num <= 3.5 then
         return 0.375 # (9.0 out of 24.0)
      else  # if hunks_num > 3.5
        case when LLOC_diff <= 1.5 then
           return 0.08823529411764706 # (3.0 out of 34.0)
        else  # if LLOC_diff > 1.5
           return 0.15789473684210525 # (3.0 out of 19.0)
        end       end     end   end )