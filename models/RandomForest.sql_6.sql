create or replace function RandomForest_6 (same_day_duration_avg_diff int64, low_McCabe_max_before int64, Single comments_before int64, one_file_fix_rate_diff int64, length_diff int64, Comments_after int64, Single comments_diff int64, too-many-statements int64, cur_count int64, Comments_diff int64, bugs_diff int64, McCabe_max_after int64, h2_diff int64, low_ccp_group int64, changed_lines int64, high_McCabe_sum_before int64, volume_diff int64, Multi_diff int64, LLOC_before int64, high_McCabe_max_diff int64, hunks_num int64, LOC_before int64, calculated_length_diff int64, low_McCabe_sum_before int64, McCabe_sum_before int64, high_ccp_group int64, McCabe_max_before int64, mostly_delete int64, LLOC_diff int64, effort_diff int64, too-many-nested-blocks int64, cur_count_y int64, h1_diff int64, low_McCabe_max_diff int64, Single comments_after int64, massive_change int64, SLOC_diff int64, added_lines int64, prev_count_x int64, N2_diff int64, high_McCabe_sum_diff int64, Blank_diff int64, LOC_diff int64, new_function int64, prev_count int64, prev_count_y int64, SLOC_before int64, McCabe_sum_after int64, high_McCabe_max_before int64, avg_coupling_code_size_cut_diff int64, Blank_before int64, McCabe_max_diff int64, refactor_mle_diff int64, is_refactor int64, low_McCabe_sum_diff int64, added_functions int64, modified_McCabe_max_diff int64, too-many-branches int64, time_diff int64, only_removal int64, N1_diff int64, Comments_before int64, McCabe_sum_diff int64, vocabulary_diff int64, removed_lines int64, too-many-return-statements int64, difficulty_diff int64, cur_count_x int64) as (
  case when Blank_before <= 46.5 then
    case when length_diff <= -2.5 then
       return 0.5263157894736842 # (0.5263157894736842 out of 1.0)
    else  # if length_diff > -2.5
       return 0.8787878787878788 # (0.8787878787878788 out of 1.0)
    end   else  # if Blank_before > 46.5
    case when LLOC_diff <= -3.5 then
      case when removed_lines <= 6.5 then
         return 0.4 # (0.4 out of 1.0)
      else  # if removed_lines > 6.5
        case when Comments_before <= 70.0 then
          case when Comments_before <= 46.5 then
             return 0.8125 # (0.8125 out of 1.0)
          else  # if Comments_before > 46.5
             return 0.9375 # (0.9375 out of 1.0)
          end         else  # if Comments_before > 70.0
           return 0.4375 # (0.4375 out of 1.0)
        end       end     else  # if LLOC_diff > -3.5
      case when N2_diff <= -0.5 then
         return 0.47058823529411764 # (0.47058823529411764 out of 1.0)
      else  # if N2_diff > -0.5
        case when avg_coupling_code_size_cut_diff <= 1.4373015761375427 then
          case when length_diff <= 1.0 then
             return 0.1 # (0.1 out of 1.0)
          else  # if length_diff > 1.0
             return 0.0 # (0.0 out of 1.0)
          end         else  # if avg_coupling_code_size_cut_diff > 1.4373015761375427
           return 0.5625 # (0.5625 out of 1.0)
        end       end     end   end )