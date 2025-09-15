create or replace function RandomForest_3 (N1_diff int64, Single comments_diff int64, h2_diff int64, new_function int64, added_lines int64, difficulty_diff int64, too-many-return-statements int64, effort_diff int64, length_diff int64, McCabe_sum_after int64, removed_lines int64, McCabe_sum_before int64, low_McCabe_sum_before int64, high_McCabe_max_diff int64, prev_count_x int64, prev_count int64, LOC_before int64, SLOC_diff int64, low_McCabe_sum_diff int64, cur_count int64, calculated_length_diff int64, Blank_before int64, Comments_after int64, bugs_diff int64, too-many-statements int64, volume_diff int64, only_removal int64, too-many-branches int64, low_McCabe_max_diff int64, low_McCabe_max_before int64, McCabe_max_diff int64, is_refactor int64, cur_count_x int64, Single comments_before int64, McCabe_max_after int64, Blank_diff int64, McCabe_max_before int64, added_functions int64, Multi_diff int64, SLOC_before int64, prev_count_y int64, massive_change int64, LOC_diff int64, time_diff int64, h1_diff int64, vocabulary_diff int64, LLOC_diff int64, high_ccp_group int64, hunks_num int64, Single comments_after int64, high_McCabe_sum_before int64, modified_McCabe_max_diff int64, N2_diff int64, same_day_duration_avg_diff int64, low_ccp_group int64, Comments_before int64, cur_count_y int64, high_McCabe_sum_diff int64, changed_lines int64, high_McCabe_max_before int64, Comments_diff int64, LLOC_before int64, one_file_fix_rate_diff int64, too-many-nested-blocks int64, McCabe_sum_diff int64, refactor_mle_diff int64, avg_coupling_code_size_cut_diff int64, mostly_delete int64) as (
  case when LLOC_before <= 132.0 then
     return 0.7 # (0.7 out of 1.0)
  else  # if LLOC_before > 132.0
    case when changed_lines <= 137.0 then
      case when McCabe_sum_before <= 131.0 then
        case when LLOC_diff <= -34.0 then
           return 0.05263157894736842 # (0.05263157894736842 out of 1.0)
        else  # if LLOC_diff > -34.0
          case when low_McCabe_max_before <= 0.5 then
             return 0.3548387096774194 # (0.3548387096774194 out of 1.0)
          else  # if low_McCabe_max_before > 0.5
             return 0.7894736842105263 # (0.7894736842105263 out of 1.0)
          end         end       else  # if McCabe_sum_before > 131.0
        case when McCabe_max_after <= 28.5 then
          case when LOC_before <= 1372.0 then
             return 0.0 # (0.0 out of 1.0)
          else  # if LOC_before > 1372.0
             return 0.2 # (0.2 out of 1.0)
          end         else  # if McCabe_max_after > 28.5
           return 0.35294117647058826 # (0.35294117647058826 out of 1.0)
        end       end     else  # if changed_lines > 137.0
      case when Comments_diff <= 0.5 then
        case when SLOC_before <= 685.0 then
           return 0.6428571428571429 # (0.6428571428571429 out of 1.0)
        else  # if SLOC_before > 685.0
           return 0.8571428571428571 # (0.8571428571428571 out of 1.0)
        end       else  # if Comments_diff > 0.5
         return 0.22727272727272727 # (0.22727272727272727 out of 1.0)
      end     end   end )