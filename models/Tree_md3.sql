create or replace function Tree_md3 (effort_diff int64, too-many-nested-blocks int64, Single comments_diff int64, N1_diff int64, avg_coupling_code_size_cut_diff int64, Simplify-boolean-expression int64, try-except-raise int64, h1_diff int64, added_functions int64, too-many-boolean-expressions int64, LLOC_diff int64, cur_count_x int64, wildcard-import int64, mostly_delete int64, LOC_diff int64, difficulty_diff int64, Comments_before int64, prev_count_y int64, time_diff int64, pointless-statement int64, vocabulary_diff int64, modified_McCabe_max_diff int64, prev_count int64, McCabe_sum_before int64, McCabe_max_after int64, Blank_diff int64, using-constant-test int64, McCabe_max_before int64, is_refactor int64, Comments_after int64, SLOC_before int64, superfluous-parens int64, too-many-branches int64, massive_change int64, comparison-of-constants int64, broad-exception-caught int64, Blank_before int64, N2_diff int64, McCabe_sum_after int64, too-many-statements int64, refactor_mle_diff int64, LOC_before int64, simplifiable-if-statement int64, only_removal int64, h2_diff int64, unnecessary-semicolon int64, too-many-lines int64, LLOC_before int64, volume_diff int64, too-many-return-statements int64, high_ccp_group int64, Single comments_before int64, simplifiable-if-expression int64, changed_lines int64, Multi_diff int64, one_file_fix_rate_diff int64, prev_count_x int64, simplifiable-condition int64, cur_count_y int64, calculated_length_diff int64, SLOC_diff int64, line-too-long int64, McCabe_max_diff int64, Comments_diff int64, cur_count int64, Single comments_after int64, removed_lines int64, added_lines int64, length_diff int64, unnecessary-pass int64, hunks_num int64, bugs_diff int64, same_day_duration_avg_diff int64, McCabe_sum_diff int64) as (
  case when high_ccp_group <= 0.5 then
    case when changed_lines <= 138.5 then
      case when LOC_diff <= 38.5 then
         return 0.27598566308243727 # (77.0 out of 279.0)
      else  # if LOC_diff > 38.5
         return 0.8421052631578947 # (16.0 out of 19.0)
      end     else  # if changed_lines > 138.5
      case when McCabe_max_after <= 7.5 then
         return 0.8297872340425532 # (39.0 out of 47.0)
      else  # if McCabe_max_after > 7.5
         return 0.46551724137931033 # (54.0 out of 116.0)
      end     end   else  # if high_ccp_group > 0.5
    case when LOC_before <= 718.0 then
      case when same_day_duration_avg_diff <= 40.03510284423828 then
         return 0.9722222222222222 # (35.0 out of 36.0)
      else  # if same_day_duration_avg_diff > 40.03510284423828
         return 0.7 # (14.0 out of 20.0)
      end     else  # if LOC_before > 718.0
      case when McCabe_sum_after <= 195.5 then
         return 0.3333333333333333 # (17.0 out of 51.0)
      else  # if McCabe_sum_after > 195.5
         return 0.84375 # (27.0 out of 32.0)
      end     end   end )