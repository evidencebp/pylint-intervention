create or replace function RandomForest_4 (N1_diff int64, Single comments_diff int64, h2_diff int64, new_function int64, added_lines int64, difficulty_diff int64, too-many-return-statements int64, effort_diff int64, length_diff int64, McCabe_sum_after int64, removed_lines int64, McCabe_sum_before int64, low_McCabe_sum_before int64, high_McCabe_max_diff int64, prev_count_x int64, prev_count int64, LOC_before int64, SLOC_diff int64, low_McCabe_sum_diff int64, cur_count int64, calculated_length_diff int64, Blank_before int64, Comments_after int64, bugs_diff int64, too-many-statements int64, volume_diff int64, only_removal int64, too-many-branches int64, low_McCabe_max_diff int64, low_McCabe_max_before int64, McCabe_max_diff int64, is_refactor int64, cur_count_x int64, Single comments_before int64, McCabe_max_after int64, Blank_diff int64, McCabe_max_before int64, added_functions int64, Multi_diff int64, SLOC_before int64, prev_count_y int64, massive_change int64, LOC_diff int64, time_diff int64, h1_diff int64, vocabulary_diff int64, LLOC_diff int64, high_ccp_group int64, hunks_num int64, Single comments_after int64, high_McCabe_sum_before int64, modified_McCabe_max_diff int64, N2_diff int64, same_day_duration_avg_diff int64, low_ccp_group int64, Comments_before int64, cur_count_y int64, high_McCabe_sum_diff int64, changed_lines int64, high_McCabe_max_before int64, Comments_diff int64, LLOC_before int64, one_file_fix_rate_diff int64, too-many-nested-blocks int64, McCabe_sum_diff int64, refactor_mle_diff int64, avg_coupling_code_size_cut_diff int64, mostly_delete int64) as (
  case when SLOC_diff <= 36.0 then
    case when LOC_before <= 377.5 then
      case when Comments_before <= 13.5 then
         return 0.36363636363636365 # (0.36363636363636365 out of 1.0)
      else  # if Comments_before > 13.5
         return 0.8484848484848485 # (0.8484848484848485 out of 1.0)
      end     else  # if LOC_before > 377.5
      case when length_diff <= -13.5 then
        case when LOC_before <= 960.0 then
           return 0.7272727272727273 # (0.7272727272727273 out of 1.0)
        else  # if LOC_before > 960.0
          case when McCabe_sum_diff <= -24.0 then
             return 0.5789473684210527 # (0.5789473684210527 out of 1.0)
          else  # if McCabe_sum_diff > -24.0
             return 0.14285714285714285 # (0.14285714285714285 out of 1.0)
          end         end       else  # if length_diff > -13.5
        case when Comments_after <= 39.0 then
          case when removed_lines <= 2.0 then
             return 0.4 # (0.4 out of 1.0)
          else  # if removed_lines > 2.0
             return 0.125 # (0.125 out of 1.0)
          end         else  # if Comments_after > 39.0
          case when McCabe_sum_after <= 155.5 then
             return 0.0 # (0.0 out of 1.0)
          else  # if McCabe_sum_after > 155.5
             return 0.21428571428571427 # (0.21428571428571427 out of 1.0)
          end         end       end     end   else  # if SLOC_diff > 36.0
     return 0.9473684210526315 # (0.9473684210526315 out of 1.0)
  end )