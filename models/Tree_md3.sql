create or replace function Tree_md3 (N1_diff int64, Single comments_diff int64, h2_diff int64, new_function int64, added_lines int64, difficulty_diff int64, too-many-return-statements int64, effort_diff int64, length_diff int64, McCabe_sum_after int64, removed_lines int64, McCabe_sum_before int64, low_McCabe_sum_before int64, high_McCabe_max_diff int64, prev_count_x int64, prev_count int64, LOC_before int64, SLOC_diff int64, low_McCabe_sum_diff int64, cur_count int64, calculated_length_diff int64, Blank_before int64, Comments_after int64, bugs_diff int64, too-many-statements int64, volume_diff int64, only_removal int64, too-many-branches int64, low_McCabe_max_diff int64, low_McCabe_max_before int64, McCabe_max_diff int64, is_refactor int64, cur_count_x int64, Single comments_before int64, McCabe_max_after int64, Blank_diff int64, McCabe_max_before int64, added_functions int64, Multi_diff int64, SLOC_before int64, prev_count_y int64, massive_change int64, LOC_diff int64, time_diff int64, h1_diff int64, vocabulary_diff int64, LLOC_diff int64, high_ccp_group int64, hunks_num int64, Single comments_after int64, high_McCabe_sum_before int64, modified_McCabe_max_diff int64, N2_diff int64, same_day_duration_avg_diff int64, low_ccp_group int64, Comments_before int64, cur_count_y int64, high_McCabe_sum_diff int64, changed_lines int64, high_McCabe_max_before int64, Comments_diff int64, LLOC_before int64, one_file_fix_rate_diff int64, too-many-nested-blocks int64, McCabe_sum_diff int64, refactor_mle_diff int64, avg_coupling_code_size_cut_diff int64, mostly_delete int64) as (
  case when low_ccp_group <= 0.5 then
    case when LOC_before <= 377.5 then
      case when Single comments_after <= 55.5 then
         return 0.9354838709677419 # (0.9354838709677419 out of 1.0)
      else  # if Single comments_after > 55.5
         return 0.0 # (0.0 out of 1.0)
      end     else  # if LOC_before > 377.5
      case when one_file_fix_rate_diff <= -0.10583669319748878 then
         return 0.1875 # (0.1875 out of 1.0)
      else  # if one_file_fix_rate_diff > -0.10583669319748878
         return 0.5365853658536586 # (0.5365853658536586 out of 1.0)
      end     end   else  # if low_ccp_group > 0.5
    case when Single comments_diff <= -18.5 then
       return 1.0 # (1.0 out of 1.0)
    else  # if Single comments_diff > -18.5
      case when Single comments_diff <= 21.0 then
         return 0.07142857142857142 # (0.07142857142857142 out of 1.0)
      else  # if Single comments_diff > 21.0
         return 1.0 # (1.0 out of 1.0)
      end     end   end )