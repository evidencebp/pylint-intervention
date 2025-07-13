create or replace function Tree_ms50_md3 (LOC_diff int64, Comments_after int64, volume_diff int64, LOC_before int64, McCabe_max_diff int64, Blank_diff int64, unnecessary-pass int64, McCabe_max_before int64, prev_count_x int64, prev_count_y int64, N2_diff int64, LLOC_before int64, prev_count int64, too-many-branches int64, added_functions int64, length_diff int64, h2_diff int64, removed_lines int64, too-many-nested-blocks int64, comparison-of-constants int64, bugs_diff int64, N1_diff int64, Comments_diff int64, line-too-long int64, McCabe_sum_diff int64, superfluous-parens int64, Multi_diff int64, changed_lines int64, McCabe_sum_before int64, calculated_length_diff int64, Single comments_after int64, time_diff int64, Single comments_diff int64, Comments_before int64, added_lines int64, effort_diff int64, refactor_mle_diff int64, Blank_before int64, too-many-return-statements int64, pointless-statement int64, too-many-statements int64, cur_count_y int64, unnecessary-semicolon int64, cur_count_x int64, using-constant-test int64, McCabe_sum_after int64, McCabe_max_after int64, too-many-lines int64, LLOC_diff int64, difficulty_diff int64, simplifiable-if-statement int64, vocabulary_diff int64, SLOC_before int64, modified_McCabe_max_diff int64, wildcard-import int64, one_file_fix_rate_diff int64, simplifiable-condition int64, SLOC_diff int64, h1_diff int64, same_day_duration_avg_diff int64, Single comments_before int64, cur_count int64, try-except-raise int64, Simplify-boolean-expression int64, simplifiable-if-expression int64, broad-exception-caught int64, hunks_num int64, too-many-boolean-expressions int64, avg_coupling_code_size_cut_diff int64) as (
  case when SLOC_diff <= 38.0 then
    case when hunks_num <= 11.5 then
      case when Single comments_diff <= -2.5 then
         return 0.6886792452830188 # (73.0 out of 106.0)
      else  # if Single comments_diff > -2.5
         return 0.44028405422853456 # (682.0 out of 1549.0)
      end     else  # if hunks_num > 11.5
      case when Comments_after <= 213.0 then
         return 0.13043478260869565 # (12.0 out of 92.0)
      else  # if Comments_after > 213.0
         return 0.7 # (7.0 out of 10.0)
      end     end   else  # if SLOC_diff > 38.0
    case when removed_lines <= 376.5 then
      case when length_diff <= 14.5 then
         return 0.9696969696969697 # (32.0 out of 33.0)
      else  # if length_diff > 14.5
         return 0.625 # (10.0 out of 16.0)
      end     else  # if removed_lines > 376.5
       return 0.35714285714285715 # (5.0 out of 14.0)
    end   end )