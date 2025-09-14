create or replace function Tree_ms50_md3 (h1_diff int64, simplifiable-if-statement int64, McCabe_max_after int64, McCabe_sum_before int64, Single comments_before int64, low_McCabe_max_diff int64, high_ccp_group int64, pointless-statement int64, too-many-branches int64, high_McCabe_max_before int64, superfluous-parens int64, Multi_diff int64, wildcard-import int64, high_McCabe_sum_before int64, LLOC_before int64, cur_count int64, unnecessary-semicolon int64, Comments_after int64, mostly_delete int64, simplifiable-condition int64, avg_coupling_code_size_cut_diff int64, added_functions int64, McCabe_max_diff int64, McCabe_sum_diff int64, LLOC_diff int64, LOC_before int64, Comments_diff int64, prev_count_x int64, effort_diff int64, try-except-raise int64, difficulty_diff int64, line-too-long int64, Simplify-boolean-expression int64, SLOC_diff int64, McCabe_sum_after int64, refactor_mle_diff int64, one_file_fix_rate_diff int64, is_refactor int64, too-many-lines int64, too-many-boolean-expressions int64, Single comments_diff int64, low_McCabe_sum_diff int64, cur_count_y int64, comparison-of-constants int64, Comments_before int64, too-many-return-statements int64, vocabulary_diff int64, massive_change int64, hunks_num int64, modified_McCabe_max_diff int64, high_McCabe_sum_diff int64, N2_diff int64, broad-exception-caught int64, length_diff int64, unnecessary-pass int64, time_diff int64, changed_lines int64, Single comments_after int64, h2_diff int64, low_McCabe_sum_before int64, cur_count_x int64, McCabe_max_before int64, using-constant-test int64, added_lines int64, same_day_duration_avg_diff int64, prev_count_y int64, Blank_diff int64, LOC_diff int64, only_removal int64, low_McCabe_max_before int64, bugs_diff int64, too-many-statements int64, simplifiable-if-expression int64, calculated_length_diff int64, volume_diff int64, Blank_before int64, high_McCabe_max_diff int64, SLOC_before int64, too-many-nested-blocks int64, removed_lines int64, low_ccp_group int64, N1_diff int64, prev_count int64) as (
  case when high_ccp_group <= 0.5 then
    case when Single comments_diff <= -18.5 then
      case when Single comments_after <= 45.0 then
         return 1.0 # (1.0 out of 1.0)
      else  # if Single comments_after > 45.0
         return 0.5333333333333333 # (0.5333333333333333 out of 1.0)
      end     else  # if Single comments_diff > -18.5
      case when low_ccp_group <= 0.5 then
         return 0.44485294117647056 # (0.44485294117647056 out of 1.0)
      else  # if low_ccp_group > 0.5
         return 0.17105263157894737 # (0.17105263157894737 out of 1.0)
      end     end   else  # if high_ccp_group > 0.5
    case when Comments_diff <= 10.5 then
      case when changed_lines <= 418.5 then
         return 0.7796610169491526 # (0.7796610169491526 out of 1.0)
      else  # if changed_lines > 418.5
         return 0.16666666666666666 # (0.16666666666666666 out of 1.0)
      end     else  # if Comments_diff > 10.5
       return 0.09090909090909091 # (0.09090909090909091 out of 1.0)
    end   end )