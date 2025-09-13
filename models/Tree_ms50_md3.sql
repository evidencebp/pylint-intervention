create or replace function Tree_ms50_md3 (h1_diff int64, SLOC_before int64, avg_coupling_code_size_cut_diff int64, Multi_diff int64, using-constant-test int64, high_McCabe_sum_diff int64, difficulty_diff int64, LLOC_diff int64, length_diff int64, Comments_after int64, McCabe_max_before int64, low_McCabe_sum_before int64, cur_count int64, LOC_before int64, low_McCabe_max_before int64, massive_change int64, too-many-return-statements int64, Comments_diff int64, added_lines int64, broad-exception-caught int64, comparison-of-constants int64, Single comments_diff int64, refactor_mle_diff int64, prev_count_x int64, McCabe_sum_before int64, modified_McCabe_max_diff int64, Simplify-boolean-expression int64, Blank_diff int64, added_functions int64, LLOC_before int64, cur_count_x int64, high_McCabe_sum_before int64, volume_diff int64, low_McCabe_max_diff int64, LOC_diff int64, calculated_length_diff int64, changed_lines int64, N2_diff int64, h2_diff int64, too-many-lines int64, unnecessary-pass int64, simplifiable-if-statement int64, prev_count int64, too-many-nested-blocks int64, Comments_before int64, SLOC_diff int64, McCabe_sum_after int64, bugs_diff int64, cur_count_y int64, Single comments_after int64, McCabe_max_diff int64, N1_diff int64, wildcard-import int64, McCabe_sum_diff int64, prev_count_y int64, superfluous-parens int64, hunks_num int64, try-except-raise int64, simplifiable-if-expression int64, McCabe_max_after int64, high_McCabe_max_diff int64, too-many-statements int64, simplifiable-condition int64, only_removal int64, unnecessary-semicolon int64, effort_diff int64, is_refactor int64, same_day_duration_avg_diff int64, one_file_fix_rate_diff int64, high_McCabe_max_before int64, vocabulary_diff int64, too-many-branches int64, mostly_delete int64, high_ccp_group int64, low_ccp_group int64, removed_lines int64, Single comments_before int64, low_McCabe_sum_diff int64, time_diff int64, Blank_before int64, line-too-long int64, too-many-boolean-expressions int64, pointless-statement int64) as (
  case when high_ccp_group <= 0.5 then
    case when Comments_diff <= -21.0 then
      case when h1_diff <= -2.5 then
         return 1.0 # (1.0 out of 1.0)
      else  # if h1_diff > -2.5
         return 0.55 # (0.55 out of 1.0)
      end     else  # if Comments_diff > -21.0
      case when SLOC_diff <= 38.0 then
         return 0.30601092896174864 # (0.30601092896174864 out of 1.0)
      else  # if SLOC_diff > 38.0
         return 0.717391304347826 # (0.717391304347826 out of 1.0)
      end     end   else  # if high_ccp_group > 0.5
    case when massive_change <= 0.5 then
      case when LOC_before <= 794.0 then
         return 0.9285714285714286 # (0.9285714285714286 out of 1.0)
      else  # if LOC_before > 794.0
         return 0.631578947368421 # (0.631578947368421 out of 1.0)
      end     else  # if massive_change > 0.5
      case when one_file_fix_rate_diff <= -0.3621392250061035 then
         return 0.0 # (0.0 out of 1.0)
      else  # if one_file_fix_rate_diff > -0.3621392250061035
         return 0.5217391304347826 # (0.5217391304347826 out of 1.0)
      end     end   end )