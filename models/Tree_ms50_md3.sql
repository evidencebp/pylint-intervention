create or replace function Tree_ms50_md3 (prev_count int64, prev_count_x int64, prev_count_y int64, using-constant-test int64, Comments_diff int64, massive_change int64, McCabe_max_after int64, Comments_before int64, too-many-statements int64, cur_count_x int64, h1_diff int64, McCabe_sum_diff int64, LLOC_before int64, McCabe_sum_before int64, high_McCabe_max_before int64, avg_coupling_code_size_cut_diff int64, is_refactor int64, N2_diff int64, too-many-branches int64, SLOC_before int64, too-many-nested-blocks int64, too-many-lines int64, bugs_diff int64, time_diff int64, Single comments_after int64, simplifiable-condition int64, Multi_diff int64, high_McCabe_sum_before int64, low_ccp_group int64, refactor_mle_diff int64, low_McCabe_max_diff int64, SLOC_diff int64, changed_lines int64, hunks_num int64, McCabe_sum_after int64, cur_count_y int64, one_file_fix_rate_diff int64, low_McCabe_sum_before int64, modified_McCabe_max_diff int64, superfluous-parens int64, mostly_delete int64, added_functions int64, Comments_after int64, N1_diff int64, McCabe_max_diff int64, simplifiable-if-statement int64, LOC_before int64, low_McCabe_max_before int64, McCabe_max_before int64, try-except-raise int64, line-too-long int64, unnecessary-semicolon int64, wildcard-import int64, difficulty_diff int64, Simplify-boolean-expression int64, cur_count int64, low_McCabe_sum_diff int64, pointless-statement int64, length_diff int64, broad-exception-caught int64, h2_diff int64, high_McCabe_sum_diff int64, only_removal int64, comparison-of-constants int64, Single comments_diff int64, too-many-boolean-expressions int64, Blank_before int64, calculated_length_diff int64, Single comments_before int64, removed_lines int64, simplifiable-if-expression int64, LOC_diff int64, volume_diff int64, high_McCabe_max_diff int64, high_ccp_group int64, same_day_duration_avg_diff int64, Blank_diff int64, effort_diff int64, too-many-return-statements int64, added_lines int64, unnecessary-pass int64, vocabulary_diff int64, LLOC_diff int64) as (
  case when high_ccp_group <= 0.5 then
    case when h1_diff <= -4.5 then
      case when Blank_before <= 86.0 then
         return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
      else  # if Blank_before > 86.0
         return 0.8636363636363636 # (0.8636363636363636 out of 1.0)
      end     else  # if h1_diff > -4.5
      case when low_ccp_group <= 0.5 then
         return 0.22370617696160267 # (0.22370617696160267 out of 1.0)
      else  # if low_ccp_group > 0.5
         return 0.07008086253369272 # (0.07008086253369272 out of 1.0)
      end     end   else  # if high_ccp_group > 0.5
    case when McCabe_sum_before <= 135.5 then
      case when refactor_mle_diff <= -0.02819955162703991 then
         return 0.4827586206896552 # (0.4827586206896552 out of 1.0)
      else  # if refactor_mle_diff > -0.02819955162703991
         return 0.9333333333333333 # (0.9333333333333333 out of 1.0)
      end     else  # if McCabe_sum_before > 135.5
      case when McCabe_sum_after <= 195.5 then
         return 0.14285714285714285 # (0.14285714285714285 out of 1.0)
      else  # if McCabe_sum_after > 195.5
         return 0.6037735849056604 # (0.6037735849056604 out of 1.0)
      end     end   end )