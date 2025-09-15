create or replace function RandomForest_0 (same_day_duration_avg_diff int64, low_McCabe_max_before int64, Single comments_before int64, one_file_fix_rate_diff int64, length_diff int64, Comments_after int64, Single comments_diff int64, too-many-statements int64, cur_count int64, Comments_diff int64, bugs_diff int64, McCabe_max_after int64, h2_diff int64, low_ccp_group int64, changed_lines int64, high_McCabe_sum_before int64, volume_diff int64, Multi_diff int64, LLOC_before int64, high_McCabe_max_diff int64, hunks_num int64, LOC_before int64, calculated_length_diff int64, low_McCabe_sum_before int64, McCabe_sum_before int64, high_ccp_group int64, McCabe_max_before int64, mostly_delete int64, LLOC_diff int64, effort_diff int64, too-many-nested-blocks int64, cur_count_y int64, h1_diff int64, low_McCabe_max_diff int64, Single comments_after int64, massive_change int64, SLOC_diff int64, added_lines int64, prev_count_x int64, N2_diff int64, high_McCabe_sum_diff int64, Blank_diff int64, LOC_diff int64, new_function int64, prev_count int64, prev_count_y int64, SLOC_before int64, McCabe_sum_after int64, high_McCabe_max_before int64, avg_coupling_code_size_cut_diff int64, Blank_before int64, McCabe_max_diff int64, refactor_mle_diff int64, is_refactor int64, low_McCabe_sum_diff int64, added_functions int64, modified_McCabe_max_diff int64, too-many-branches int64, time_diff int64, only_removal int64, N1_diff int64, Comments_before int64, McCabe_sum_diff int64, vocabulary_diff int64, removed_lines int64, too-many-return-statements int64, difficulty_diff int64, cur_count_x int64) as (
  case when changed_lines <= 137.0 then
    case when low_ccp_group <= 0.5 then
      case when Comments_before <= 38.0 then
        case when one_file_fix_rate_diff <= 0.1339285746216774 then
           return 0.56 # (0.56 out of 1.0)
        else  # if one_file_fix_rate_diff > 0.1339285746216774
           return 0.8695652173913043 # (0.8695652173913043 out of 1.0)
        end       else  # if Comments_before > 38.0
        case when SLOC_before <= 603.5 then
           return 0.3225806451612903 # (0.3225806451612903 out of 1.0)
        else  # if SLOC_before > 603.5
          case when one_file_fix_rate_diff <= -0.0476190485060215 then
             return 0.0 # (0.0 out of 1.0)
          else  # if one_file_fix_rate_diff > -0.0476190485060215
             return 0.2 # (0.2 out of 1.0)
          end         end       end     else  # if low_ccp_group > 0.5
      case when LOC_before <= 873.0 then
         return 0.0 # (0.0 out of 1.0)
      else  # if LOC_before > 873.0
         return 0.42857142857142855 # (0.42857142857142855 out of 1.0)
      end     end   else  # if changed_lines > 137.0
    case when added_functions <= 2.5 then
      case when McCabe_max_diff <= -9.0 then
         return 1.0 # (1.0 out of 1.0)
      else  # if McCabe_max_diff > -9.0
         return 0.46153846153846156 # (0.46153846153846156 out of 1.0)
      end     else  # if added_functions > 2.5
      case when Single comments_diff <= 0.5 then
         return 0.6470588235294118 # (0.6470588235294118 out of 1.0)
      else  # if Single comments_diff > 0.5
         return 0.2222222222222222 # (0.2222222222222222 out of 1.0)
      end     end   end )