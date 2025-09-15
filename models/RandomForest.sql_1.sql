create or replace function RandomForest_1 (N1_diff int64, Single comments_diff int64, h2_diff int64, new_function int64, added_lines int64, difficulty_diff int64, too-many-return-statements int64, effort_diff int64, length_diff int64, McCabe_sum_after int64, removed_lines int64, McCabe_sum_before int64, low_McCabe_sum_before int64, high_McCabe_max_diff int64, prev_count_x int64, prev_count int64, LOC_before int64, SLOC_diff int64, low_McCabe_sum_diff int64, cur_count int64, calculated_length_diff int64, Blank_before int64, Comments_after int64, bugs_diff int64, too-many-statements int64, volume_diff int64, only_removal int64, too-many-branches int64, low_McCabe_max_diff int64, low_McCabe_max_before int64, McCabe_max_diff int64, is_refactor int64, cur_count_x int64, Single comments_before int64, McCabe_max_after int64, Blank_diff int64, McCabe_max_before int64, added_functions int64, Multi_diff int64, SLOC_before int64, prev_count_y int64, massive_change int64, LOC_diff int64, time_diff int64, h1_diff int64, vocabulary_diff int64, LLOC_diff int64, high_ccp_group int64, hunks_num int64, Single comments_after int64, high_McCabe_sum_before int64, modified_McCabe_max_diff int64, N2_diff int64, same_day_duration_avg_diff int64, low_ccp_group int64, Comments_before int64, cur_count_y int64, high_McCabe_sum_diff int64, changed_lines int64, high_McCabe_max_before int64, Comments_diff int64, LLOC_before int64, one_file_fix_rate_diff int64, too-many-nested-blocks int64, McCabe_sum_diff int64, refactor_mle_diff int64, avg_coupling_code_size_cut_diff int64, mostly_delete int64) as (
  case when SLOC_before <= 745.5 then
    case when McCabe_sum_after <= 86.0 then
      case when high_ccp_group <= 0.5 then
        case when is_refactor <= 0.5 then
          case when Single comments_before <= 21.5 then
             return 0.16666666666666666 # (0.16666666666666666 out of 1.0)
          else  # if Single comments_before > 21.5
             return 0.5909090909090909 # (0.5909090909090909 out of 1.0)
          end         else  # if is_refactor > 0.5
           return 0.875 # (0.875 out of 1.0)
        end       else  # if high_ccp_group > 0.5
         return 0.92 # (0.92 out of 1.0)
      end     else  # if McCabe_sum_after > 86.0
      case when Blank_before <= 140.5 then
        case when same_day_duration_avg_diff <= -28.75 then
           return 0.0 # (0.0 out of 1.0)
        else  # if same_day_duration_avg_diff > -28.75
           return 0.38095238095238093 # (0.38095238095238093 out of 1.0)
        end       else  # if Blank_before > 140.5
         return 0.5294117647058824 # (0.5294117647058824 out of 1.0)
      end     end   else  # if SLOC_before > 745.5
    case when LLOC_diff <= -70.0 then
       return 0.5238095238095238 # (0.5238095238095238 out of 1.0)
    else  # if LLOC_diff > -70.0
      case when SLOC_before <= 1032.0 then
         return 0.037037037037037035 # (0.037037037037037035 out of 1.0)
      else  # if SLOC_before > 1032.0
         return 0.375 # (0.375 out of 1.0)
      end     end   end )