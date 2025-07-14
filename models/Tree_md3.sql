create or replace function Tree_md3 (SLOC_before int64, simplifiable-condition int64, bugs_diff int64, Blank_before int64, LLOC_diff int64, try-except-raise int64, LLOC_before int64, changed_lines int64, h2_diff int64, prev_count_x int64, too-many-lines int64, cur_count_y int64, Comments_before int64, McCabe_sum_after int64, cur_count_x int64, vocabulary_diff int64, Single comments_before int64, N2_diff int64, high_ccp_group int64, massive_change int64, added_lines int64, prev_count int64, refactor_mle_diff int64, superfluous-parens int64, avg_coupling_code_size_cut_diff int64, McCabe_sum_diff int64, LOC_before int64, too-many-return-statements int64, too-many-branches int64, too-many-nested-blocks int64, difficulty_diff int64, time_diff int64, Single comments_after int64, calculated_length_diff int64, Simplify-boolean-expression int64, unnecessary-semicolon int64, mostly_delete int64, effort_diff int64, Multi_diff int64, McCabe_max_diff int64, is_refactor int64, only_removal int64, LOC_diff int64, one_file_fix_rate_diff int64, Comments_after int64, comparison-of-constants int64, McCabe_max_after int64, length_diff int64, simplifiable-if-statement int64, removed_lines int64, unnecessary-pass int64, Comments_diff int64, cur_count int64, same_day_duration_avg_diff int64, hunks_num int64, N1_diff int64, line-too-long int64, volume_diff int64, using-constant-test int64, too-many-boolean-expressions int64, modified_McCabe_max_diff int64, h1_diff int64, added_functions int64, SLOC_diff int64, too-many-statements int64, pointless-statement int64, wildcard-import int64, McCabe_max_before int64, prev_count_y int64, broad-exception-caught int64, Blank_diff int64, McCabe_sum_before int64, simplifiable-if-expression int64, Single comments_diff int64) as (
  case when Comments_after <= 5.5 then
    case when Comments_after <= 1.5 then
       return 1.0 # (23.0 out of 23.0)
    else  # if Comments_after > 1.5
      case when SLOC_before <= 176.5 then
         return 0.3793103448275862 # (11.0 out of 29.0)
      else  # if SLOC_before > 176.5
         return 1.0 # (9.0 out of 9.0)
      end     end   else  # if Comments_after > 5.5
    case when high_ccp_group <= 0.5 then
      case when Comments_diff <= -21.0 then
         return 0.5 # (27.0 out of 54.0)
      else  # if Comments_diff > -21.0
         return 0.14757709251101322 # (134.0 out of 908.0)
      end     else  # if high_ccp_group > 0.5
      case when LOC_before <= 729.0 then
         return 0.7692307692307693 # (40.0 out of 52.0)
      else  # if LOC_before > 729.0
         return 0.27450980392156865 # (42.0 out of 153.0)
      end     end   end )