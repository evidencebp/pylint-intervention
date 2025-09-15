create or replace function RandomForest_9 (same_day_duration_avg_diff int64, low_McCabe_max_before int64, Single comments_before int64, one_file_fix_rate_diff int64, length_diff int64, Comments_after int64, Single comments_diff int64, too-many-statements int64, cur_count int64, Comments_diff int64, bugs_diff int64, McCabe_max_after int64, h2_diff int64, low_ccp_group int64, changed_lines int64, high_McCabe_sum_before int64, volume_diff int64, Multi_diff int64, LLOC_before int64, high_McCabe_max_diff int64, hunks_num int64, LOC_before int64, calculated_length_diff int64, low_McCabe_sum_before int64, McCabe_sum_before int64, high_ccp_group int64, McCabe_max_before int64, mostly_delete int64, LLOC_diff int64, effort_diff int64, too-many-nested-blocks int64, cur_count_y int64, h1_diff int64, low_McCabe_max_diff int64, Single comments_after int64, massive_change int64, SLOC_diff int64, added_lines int64, prev_count_x int64, N2_diff int64, high_McCabe_sum_diff int64, Blank_diff int64, LOC_diff int64, new_function int64, prev_count int64, prev_count_y int64, SLOC_before int64, McCabe_sum_after int64, high_McCabe_max_before int64, avg_coupling_code_size_cut_diff int64, Blank_before int64, McCabe_max_diff int64, refactor_mle_diff int64, is_refactor int64, low_McCabe_sum_diff int64, added_functions int64, modified_McCabe_max_diff int64, too-many-branches int64, time_diff int64, only_removal int64, N1_diff int64, Comments_before int64, McCabe_sum_diff int64, vocabulary_diff int64, removed_lines int64, too-many-return-statements int64, difficulty_diff int64, cur_count_x int64) as (
  case when h2_diff <= 2.5 then
    case when added_functions <= 1.5 then
      case when added_lines <= 151.5 then
        case when hunks_num <= 2.5 then
          case when removed_lines <= 6.5 then
            case when SLOC_before <= 500.0 then
               return 0.6190476190476191 # (0.6190476190476191 out of 1.0)
            else  # if SLOC_before > 500.0
               return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
            end           else  # if removed_lines > 6.5
             return 0.7222222222222222 # (0.7222222222222222 out of 1.0)
          end         else  # if hunks_num > 2.5
          case when LLOC_before <= 323.5 then
            case when low_ccp_group <= 0.5 then
               return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
            else  # if low_ccp_group > 0.5
               return 0.07692307692307693 # (0.07692307692307693 out of 1.0)
            end           else  # if LLOC_before > 323.5
            case when hunks_num <= 6.5 then
               return 0.17647058823529413 # (0.17647058823529413 out of 1.0)
            else  # if hunks_num > 6.5
               return 0.0 # (0.0 out of 1.0)
            end           end         end       else  # if added_lines > 151.5
         return 0.75 # (0.75 out of 1.0)
      end     else  # if added_functions > 1.5
      case when Single comments_diff <= -2.5 then
         return 1.0 # (1.0 out of 1.0)
      else  # if Single comments_diff > -2.5
         return 0.44 # (0.44 out of 1.0)
      end     end   else  # if h2_diff > 2.5
     return 0.13333333333333333 # (0.13333333333333333 out of 1.0)
  end )