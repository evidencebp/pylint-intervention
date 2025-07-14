create or replace function RandomForest_5 (hunks_num int64, McCabe_sum_after int64, added_lines int64, cur_count_y int64, changed_lines int64, N1_diff int64, added_functions int64, Single comments_before int64, McCabe_max_after int64, calculated_length_diff int64, h1_diff int64, difficulty_diff int64, too-many-nested-blocks int64, modified_McCabe_max_diff int64, removed_lines int64, prev_count int64, Blank_diff int64, prev_count_x int64, h2_diff int64, LLOC_before int64, Multi_diff int64, volume_diff int64, same_day_duration_avg_diff int64, N2_diff int64, one_file_fix_rate_diff int64, Comments_after int64, massive_change int64, Single comments_diff int64, Comments_before int64, SLOC_before int64, prev_count_y int64, vocabulary_diff int64, LOC_before int64, McCabe_sum_diff int64, high_ccp_group int64, McCabe_sum_before int64, is_refactor int64, cur_count_x int64, refactor_mle_diff int64, time_diff int64, bugs_diff int64, avg_coupling_code_size_cut_diff int64, LLOC_diff int64, Single comments_after int64, too-many-branches int64, McCabe_max_diff int64, too-many-statements int64, mostly_delete int64, effort_diff int64, length_diff int64, Blank_before int64, SLOC_diff int64, McCabe_max_before int64, LOC_diff int64, cur_count int64, too-many-return-statements int64, only_removal int64, Comments_diff int64) as (
  case when McCabe_sum_after <= 89.0 then
    case when refactor_mle_diff <= -0.18896696716547012 then
      case when h2_diff <= -0.5 then
         return 0.6 # (12.0 out of 20.0)
      else  # if h2_diff > -0.5
         return 0.05 # (1.0 out of 20.0)
      end     else  # if refactor_mle_diff > -0.18896696716547012
      case when McCabe_sum_diff <= -13.5 then
         return 1.0 # (18.0 out of 18.0)
      else  # if McCabe_sum_diff > -13.5
        case when Blank_before <= 77.5 then
          case when added_lines <= 29.5 then
             return 1.0 # (17.0 out of 17.0)
          else  # if added_lines > 29.5
             return 0.8 # (16.0 out of 20.0)
          end         else  # if Blank_before > 77.5
           return 0.13333333333333333 # (2.0 out of 15.0)
        end       end     end   else  # if McCabe_sum_after > 89.0
    case when hunks_num <= 11.5 then
      case when McCabe_sum_before <= 242.5 then
        case when McCabe_max_diff <= -5.5 then
           return 0.058823529411764705 # (1.0 out of 17.0)
        else  # if McCabe_max_diff > -5.5
          case when SLOC_before <= 511.0 then
             return 0.2916666666666667 # (7.0 out of 24.0)
          else  # if SLOC_before > 511.0
             return 0.8461538461538461 # (22.0 out of 26.0)
          end         end       else  # if McCabe_sum_before > 242.5
         return 0.2222222222222222 # (6.0 out of 27.0)
      end     else  # if hunks_num > 11.5
       return 0.04 # (1.0 out of 25.0)
    end   end )