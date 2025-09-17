create or replace function RandomForest_2 (length_diff int64, N1_diff int64, N2_diff int64, McCabe_sum_diff int64, bugs_diff int64, McCabe_sum_after int64, too-many-branches int64, is_refactor int64, high_ccp_group int64, mostly_delete int64, cur_count_y int64, low_ccp_group int64, prev_count_x int64, difficulty_diff int64, removed_lines int64, Blank_before int64, LOC_before int64, low_McCabe_sum_before int64, cur_count_x int64, Comments_diff int64, Comments_before int64, h2_diff int64, Comments_after int64, McCabe_sum_before int64, McCabe_max_after int64, high_McCabe_max_diff int64, added_functions int64, SLOC_diff int64, avg_coupling_code_size_cut_diff int64, too-many-nested-blocks int64, changed_lines int64, high_McCabe_sum_before int64, prev_count int64, high_McCabe_sum_diff int64, vocabulary_diff int64, SLOC_before int64, LOC_diff int64, low_McCabe_max_diff int64, Single comments_before int64, one_file_fix_rate_diff int64, too-many-statements int64, added_lines int64, new_function int64, massive_change int64, LLOC_before int64, calculated_length_diff int64, Single comments_diff int64, modified_McCabe_max_diff int64, McCabe_max_before int64, LLOC_diff int64, refactor_mle_diff int64, low_McCabe_sum_diff int64, hunks_num int64, low_McCabe_max_before int64, too-many-return-statements int64, only_removal int64, same_day_duration_avg_diff int64, h1_diff int64, time_diff int64, prev_count_y int64, effort_diff int64, Multi_diff int64, Blank_diff int64, cur_count int64, volume_diff int64, high_McCabe_max_before int64, Single comments_after int64, McCabe_max_diff int64) as (
  case when Single comments_diff <= -2.5 then
    case when Comments_before <= 116.5 then
      case when vocabulary_diff <= -12.5 then
         return 0.9714285714285714 # (0.9714285714285714 out of 1.0)
      else  # if vocabulary_diff > -12.5
         return 0.6086956521739131 # (0.6086956521739131 out of 1.0)
      end     else  # if Comments_before > 116.5
       return 0.3125 # (0.3125 out of 1.0)
    end   else  # if Single comments_diff > -2.5
    case when low_McCabe_max_before <= 0.5 then
      case when Comments_after <= 119.0 then
        case when avg_coupling_code_size_cut_diff <= 0.13033661991357803 then
          case when McCabe_sum_before <= 136.5 then
            case when modified_McCabe_max_diff <= -6.5 then
               return 0.058823529411764705 # (0.058823529411764705 out of 1.0)
            else  # if modified_McCabe_max_diff > -6.5
               return 0.3684210526315789 # (0.3684210526315789 out of 1.0)
            end           else  # if McCabe_sum_before > 136.5
            case when Single comments_before <= 53.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if Single comments_before > 53.5
               return 0.3076923076923077 # (0.3076923076923077 out of 1.0)
            end           end         else  # if avg_coupling_code_size_cut_diff > 0.13033661991357803
           return 0.43478260869565216 # (0.43478260869565216 out of 1.0)
        end       else  # if Comments_after > 119.0
         return 0.5416666666666666 # (0.5416666666666666 out of 1.0)
      end     else  # if low_McCabe_max_before > 0.5
      case when McCabe_sum_before <= 76.5 then
         return 0.4444444444444444 # (0.4444444444444444 out of 1.0)
      else  # if McCabe_sum_before > 76.5
         return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
      end     end   end )