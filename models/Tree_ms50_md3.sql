create or replace function Tree_ms50_md3 (is_refactor int64, McCabe_max_before int64, N1_diff int64, high_McCabe_sum_before int64, same_day_duration_avg_diff int64, Comments_before int64, hunks_num int64, added_lines int64, prev_count int64, low_McCabe_max_before int64, high_McCabe_max_diff int64, vocabulary_diff int64, modified_McCabe_max_diff int64, avg_coupling_code_size_cut_diff int64, too-many-nested-blocks int64, low_McCabe_max_diff int64, changed_lines int64, effort_diff int64, removed_lines int64, Blank_before int64, SLOC_diff int64, length_diff int64, low_ccp_group int64, calculated_length_diff int64, McCabe_max_diff int64, McCabe_max_after int64, LOC_diff int64, too-many-return-statements int64, Single comments_after int64, McCabe_sum_diff int64, LLOC_diff int64, too-many-statements int64, Comments_after int64, low_McCabe_sum_diff int64, McCabe_sum_before int64, difficulty_diff int64, Single comments_before int64, massive_change int64, prev_count_x int64, refactor_mle_diff int64, cur_count_y int64, N2_diff int64, prev_count_y int64, Single comments_diff int64, cur_count int64, high_McCabe_max_before int64, one_file_fix_rate_diff int64, h1_diff int64, low_McCabe_sum_before int64, time_diff int64, LOC_before int64, SLOC_before int64, too-many-branches int64, volume_diff int64, McCabe_sum_after int64, mostly_delete int64, Multi_diff int64, high_McCabe_sum_diff int64, Blank_diff int64, bugs_diff int64, h2_diff int64, cur_count_x int64, added_functions int64, LLOC_before int64, high_ccp_group int64, Comments_diff int64, only_removal int64) as (
  case when hunks_num <= 11.5 then
    case when changed_lines <= 137.0 then
      case when McCabe_max_diff <= -5.5 then
         return 0.1935483870967742 # (0.1935483870967742 out of 1.0)
      else  # if McCabe_max_diff > -5.5
         return 0.7183098591549296 # (0.7183098591549296 out of 1.0)
      end     else  # if changed_lines > 137.0
      case when McCabe_sum_diff <= -5.0 then
         return 0.9574468085106383 # (0.9574468085106383 out of 1.0)
      else  # if McCabe_sum_diff > -5.0
         return 0.6585365853658537 # (0.6585365853658537 out of 1.0)
      end     end   else  # if hunks_num > 11.5
    case when removed_lines <= 68.5 then
       return 0.0 # (0.0 out of 1.0)
    else  # if removed_lines > 68.5
       return 0.625 # (0.625 out of 1.0)
    end   end )