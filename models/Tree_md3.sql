create or replace function Tree_md3 (McCabe_sum_before int64, changed_lines int64, prev_count_y int64, mostly_delete int64, h1_diff int64, too-many-lines int64, low_McCabe_sum_before int64, length_diff int64, LOC_before int64, simplifiable-if-expression int64, added_functions int64, broad-exception-caught int64, simplifiable-condition int64, prev_count_x int64, McCabe_max_diff int64, SLOC_before int64, LLOC_before int64, low_McCabe_max_diff int64, bugs_diff int64, same_day_duration_avg_diff int64, cur_count_x int64, only_removal int64, McCabe_max_after int64, Single comments_after int64, low_ccp_group int64, one_file_fix_rate_diff int64, effort_diff int64, difficulty_diff int64, removed_lines int64, Comments_diff int64, too-many-boolean-expressions int64, refactor_mle_diff int64, high_McCabe_max_before int64, hunks_num int64, LOC_diff int64, SLOC_diff int64, cur_count_y int64, vocabulary_diff int64, using-constant-test int64, Simplify-boolean-expression int64, low_McCabe_max_before int64, high_McCabe_sum_diff int64, high_McCabe_sum_before int64, McCabe_max_before int64, Comments_after int64, McCabe_sum_diff int64, unnecessary-pass int64, avg_coupling_code_size_cut_diff int64, simplifiable-if-statement int64, is_refactor int64, volume_diff int64, added_lines int64, high_McCabe_max_diff int64, superfluous-parens int64, cur_count int64, low_McCabe_sum_diff int64, calculated_length_diff int64, Multi_diff int64, N2_diff int64, h2_diff int64, Single comments_before int64, McCabe_sum_after int64, N1_diff int64, too-many-statements int64, comparison-of-constants int64, pointless-statement int64, time_diff int64, prev_count int64, Single comments_diff int64, massive_change int64, Blank_diff int64, too-many-nested-blocks int64, Comments_before int64, modified_McCabe_max_diff int64, LLOC_diff int64, Blank_before int64, try-except-raise int64, too-many-branches int64, too-many-return-statements int64, unnecessary-semicolon int64, wildcard-import int64, high_ccp_group int64, line-too-long int64) as (
  case when high_ccp_group <= 0.5 then
    case when Single comments_diff <= -18.5 then
      case when hunks_num <= 12.5 then
         return 0.9032258064516129 # (0.9032258064516129 out of 1.0)
      else  # if hunks_num > 12.5
         return 0.0 # (0.0 out of 1.0)
      end     else  # if Single comments_diff > -18.5
      case when low_ccp_group <= 0.5 then
         return 0.425531914893617 # (0.425531914893617 out of 1.0)
      else  # if low_ccp_group > 0.5
         return 0.18181818181818182 # (0.18181818181818182 out of 1.0)
      end     end   else  # if high_ccp_group > 0.5
    case when changed_lines <= 350.5 then
      case when Single comments_diff <= 4.5 then
         return 0.7706422018348624 # (0.7706422018348624 out of 1.0)
      else  # if Single comments_diff > 4.5
         return 0.1 # (0.1 out of 1.0)
      end     else  # if changed_lines > 350.5
      case when refactor_mle_diff <= 0.09177327528595924 then
         return 0.0 # (0.0 out of 1.0)
      else  # if refactor_mle_diff > 0.09177327528595924
         return 0.75 # (0.75 out of 1.0)
      end     end   end )