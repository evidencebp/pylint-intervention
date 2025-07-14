create or replace function Tree_md3 (hunks_num int64, McCabe_sum_after int64, added_lines int64, cur_count_y int64, changed_lines int64, N1_diff int64, added_functions int64, Single comments_before int64, McCabe_max_after int64, calculated_length_diff int64, h1_diff int64, difficulty_diff int64, too-many-nested-blocks int64, modified_McCabe_max_diff int64, removed_lines int64, prev_count int64, Blank_diff int64, prev_count_x int64, h2_diff int64, LLOC_before int64, Multi_diff int64, volume_diff int64, same_day_duration_avg_diff int64, N2_diff int64, one_file_fix_rate_diff int64, Comments_after int64, massive_change int64, Single comments_diff int64, Comments_before int64, SLOC_before int64, prev_count_y int64, vocabulary_diff int64, LOC_before int64, McCabe_sum_diff int64, high_ccp_group int64, McCabe_sum_before int64, is_refactor int64, cur_count_x int64, refactor_mle_diff int64, time_diff int64, bugs_diff int64, avg_coupling_code_size_cut_diff int64, LLOC_diff int64, Single comments_after int64, too-many-branches int64, McCabe_max_diff int64, too-many-statements int64, mostly_delete int64, effort_diff int64, length_diff int64, Blank_before int64, SLOC_diff int64, McCabe_max_before int64, LOC_diff int64, cur_count int64, too-many-return-statements int64, only_removal int64, Comments_diff int64) as (
  case when Single comments_diff <= -2.5 then
    case when removed_lines <= 12.5 then
      case when McCabe_sum_diff <= -24.0 then
         return 1.0 # (5.0 out of 5.0)
      else  # if McCabe_sum_diff > -24.0
         return 0.0 # (0.0 out of 13.0)
      end     else  # if removed_lines > 12.5
      case when McCabe_sum_diff <= 0.0 then
         return 0.9230769230769231 # (36.0 out of 39.0)
      else  # if McCabe_sum_diff > 0.0
         return 0.0 # (0.0 out of 2.0)
      end     end   else  # if Single comments_diff > -2.5
    case when Blank_before <= 42.5 then
      case when N2_diff <= -0.5 then
         return 0.25 # (3.0 out of 12.0)
      else  # if N2_diff > -0.5
         return 1.0 # (15.0 out of 15.0)
      end     else  # if Blank_before > 42.5
      case when hunks_num <= 3.5 then
         return 0.4 # (26.0 out of 65.0)
      else  # if hunks_num > 3.5
         return 0.1794871794871795 # (14.0 out of 78.0)
      end     end   end )