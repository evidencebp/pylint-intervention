create or replace function Tree_md3 (using-constant-test int64, simplifiable-if-statement int64, Comments_after int64, same_day_duration_avg_diff int64, Single comments_before int64, one_file_fix_rate_diff int64, too-many-boolean-expressions int64, Single comments_diff int64, high_McCabe_sum_before int64, pointless-statement int64, bugs_diff int64, McCabe_max_before int64, length_diff int64, LOC_diff int64, N2_diff int64, superfluous-parens int64, too-many-nested-blocks int64, effort_diff int64, cur_count_x int64, high_McCabe_max_before int64, comparison-of-constants int64, SLOC_diff int64, hunks_num int64, high_McCabe_max_diff int64, prev_count int64, McCabe_sum_after int64, cur_count_y int64, refactor_mle_diff int64, too-many-return-statements int64, too-many-statements int64, too-many-lines int64, only_removal int64, removed_lines int64, cur_count int64, volume_diff int64, is_refactor int64, prev_count_y int64, calculated_length_diff int64, Simplify-boolean-expression int64, h1_diff int64, McCabe_max_diff int64, wildcard-import int64, McCabe_sum_before int64, line-too-long int64, N1_diff int64, too-many-branches int64, h2_diff int64, McCabe_max_after int64, unnecessary-pass int64, avg_coupling_code_size_cut_diff int64, high_ccp_group int64, vocabulary_diff int64, try-except-raise int64, broad-exception-caught int64, simplifiable-condition int64, LLOC_before int64, added_functions int64, LLOC_diff int64, difficulty_diff int64, McCabe_sum_diff int64, Multi_diff int64, massive_change int64, mostly_delete int64, Comments_before int64, changed_lines int64, Comments_diff int64, time_diff int64, Blank_before int64, high_McCabe_sum_diff int64, added_lines int64, prev_count_x int64, unnecessary-semicolon int64, Blank_diff int64, modified_McCabe_max_diff int64, Single comments_after int64, LOC_before int64, simplifiable-if-expression int64, SLOC_before int64) as (
  case when high_ccp_group <= 0.5 then
    case when Comments_diff <= -21.0 then
      case when same_day_duration_avg_diff <= -33.64265823364258 then
         return 0.42857142857142855 # (3.0 out of 7.0)
      else  # if same_day_duration_avg_diff > -33.64265823364258
         return 0.9629629629629629 # (26.0 out of 27.0)
      end     else  # if Comments_diff > -21.0
      case when SLOC_diff <= 38.0 then
         return 0.3191489361702128 # (120.0 out of 376.0)
      else  # if SLOC_diff > 38.0
         return 0.6415094339622641 # (34.0 out of 53.0)
      end     end   else  # if high_ccp_group > 0.5
    case when changed_lines <= 312.5 then
      case when refactor_mle_diff <= -0.0790850818157196 then
         return 0.627906976744186 # (27.0 out of 43.0)
      else  # if refactor_mle_diff > -0.0790850818157196
         return 0.863013698630137 # (63.0 out of 73.0)
      end     else  # if changed_lines > 312.5
      case when refactor_mle_diff <= 0.09177327528595924 then
         return 0.125 # (2.0 out of 16.0)
      else  # if refactor_mle_diff > 0.09177327528595924
         return 1.0 # (5.0 out of 5.0)
      end     end   end )