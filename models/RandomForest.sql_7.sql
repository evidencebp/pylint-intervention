create or replace function RandomForest_7 (length_diff int64, N1_diff int64, N2_diff int64, McCabe_sum_diff int64, bugs_diff int64, McCabe_sum_after int64, too-many-branches int64, is_refactor int64, high_ccp_group int64, mostly_delete int64, cur_count_y int64, low_ccp_group int64, prev_count_x int64, difficulty_diff int64, removed_lines int64, Blank_before int64, LOC_before int64, low_McCabe_sum_before int64, cur_count_x int64, Comments_diff int64, Comments_before int64, h2_diff int64, Comments_after int64, McCabe_sum_before int64, McCabe_max_after int64, high_McCabe_max_diff int64, added_functions int64, SLOC_diff int64, avg_coupling_code_size_cut_diff int64, too-many-nested-blocks int64, changed_lines int64, high_McCabe_sum_before int64, prev_count int64, high_McCabe_sum_diff int64, vocabulary_diff int64, SLOC_before int64, LOC_diff int64, low_McCabe_max_diff int64, Single comments_before int64, one_file_fix_rate_diff int64, too-many-statements int64, added_lines int64, new_function int64, massive_change int64, LLOC_before int64, calculated_length_diff int64, Single comments_diff int64, modified_McCabe_max_diff int64, McCabe_max_before int64, LLOC_diff int64, refactor_mle_diff int64, low_McCabe_sum_diff int64, hunks_num int64, low_McCabe_max_before int64, too-many-return-statements int64, only_removal int64, same_day_duration_avg_diff int64, h1_diff int64, time_diff int64, prev_count_y int64, effort_diff int64, Multi_diff int64, Blank_diff int64, cur_count int64, volume_diff int64, high_McCabe_max_before int64, Single comments_after int64, McCabe_max_diff int64) as (
  case when McCabe_max_diff <= -9.5 then
    case when avg_coupling_code_size_cut_diff <= -0.5021853297948837 then
       return 0.8947368421052632 # (0.8947368421052632 out of 1.0)
    else  # if avg_coupling_code_size_cut_diff > -0.5021853297948837
       return 0.6111111111111112 # (0.6111111111111112 out of 1.0)
    end   else  # if McCabe_max_diff > -9.5
    case when Single comments_diff <= -2.5 then
      case when Blank_before <= 135.5 then
         return 0.75 # (0.75 out of 1.0)
      else  # if Blank_before > 135.5
         return 0.29411764705882354 # (0.29411764705882354 out of 1.0)
      end     else  # if Single comments_diff > -2.5
      case when SLOC_diff <= -7.0 then
        case when LLOC_diff <= -10.5 then
           return 0.03571428571428571 # (0.03571428571428571 out of 1.0)
        else  # if LLOC_diff > -10.5
           return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
        end       else  # if SLOC_diff > -7.0
        case when length_diff <= -2.5 then
           return 0.7142857142857143 # (0.7142857142857143 out of 1.0)
        else  # if length_diff > -2.5
          case when added_lines <= 11.0 then
             return 0.45454545454545453 # (0.45454545454545453 out of 1.0)
          else  # if added_lines > 11.0
            case when McCabe_max_before <= 20.0 then
               return 0.2857142857142857 # (0.2857142857142857 out of 1.0)
            else  # if McCabe_max_before > 20.0
               return 0.0 # (0.0 out of 1.0)
            end           end         end       end     end   end )