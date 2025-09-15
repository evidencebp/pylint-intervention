create or replace function RandomForest_2 (same_day_duration_avg_diff int64, low_McCabe_max_before int64, Single comments_before int64, one_file_fix_rate_diff int64, length_diff int64, Comments_after int64, Single comments_diff int64, too-many-statements int64, cur_count int64, Comments_diff int64, bugs_diff int64, McCabe_max_after int64, h2_diff int64, low_ccp_group int64, changed_lines int64, high_McCabe_sum_before int64, volume_diff int64, Multi_diff int64, LLOC_before int64, high_McCabe_max_diff int64, hunks_num int64, LOC_before int64, calculated_length_diff int64, low_McCabe_sum_before int64, McCabe_sum_before int64, high_ccp_group int64, McCabe_max_before int64, mostly_delete int64, LLOC_diff int64, effort_diff int64, too-many-nested-blocks int64, cur_count_y int64, h1_diff int64, low_McCabe_max_diff int64, Single comments_after int64, massive_change int64, SLOC_diff int64, added_lines int64, prev_count_x int64, N2_diff int64, high_McCabe_sum_diff int64, Blank_diff int64, LOC_diff int64, new_function int64, prev_count int64, prev_count_y int64, SLOC_before int64, McCabe_sum_after int64, high_McCabe_max_before int64, avg_coupling_code_size_cut_diff int64, Blank_before int64, McCabe_max_diff int64, refactor_mle_diff int64, is_refactor int64, low_McCabe_sum_diff int64, added_functions int64, modified_McCabe_max_diff int64, too-many-branches int64, time_diff int64, only_removal int64, N1_diff int64, Comments_before int64, McCabe_sum_diff int64, vocabulary_diff int64, removed_lines int64, too-many-return-statements int64, difficulty_diff int64, cur_count_x int64) as (
  case when Comments_diff <= 1.5 then
    case when Single comments_after <= 70.5 then
      case when McCabe_max_before <= 32.0 then
        case when McCabe_sum_before <= 37.5 then
           return 1.0 # (1.0 out of 1.0)
        else  # if McCabe_sum_before > 37.5
          case when Comments_before <= 53.5 then
            case when Single comments_before <= 20.5 then
               return 0.2222222222222222 # (0.2222222222222222 out of 1.0)
            else  # if Single comments_before > 20.5
              case when Comments_after <= 36.5 then
                case when same_day_duration_avg_diff <= -19.366666793823242 then
                   return 0.8571428571428571 # (0.8571428571428571 out of 1.0)
                else  # if same_day_duration_avg_diff > -19.366666793823242
                   return 0.5 # (0.5 out of 1.0)
                end               else  # if Comments_after > 36.5
                 return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
              end             end           else  # if Comments_before > 53.5
             return 0.9230769230769231 # (0.9230769230769231 out of 1.0)
          end         end       else  # if McCabe_max_before > 32.0
         return 0.2727272727272727 # (0.2727272727272727 out of 1.0)
      end     else  # if Single comments_after > 70.5
      case when hunks_num <= 3.5 then
         return 0.0 # (0.0 out of 1.0)
      else  # if hunks_num > 3.5
         return 0.5 # (0.5 out of 1.0)
      end     end   else  # if Comments_diff > 1.5
    case when hunks_num <= 7.5 then
       return 0.23076923076923078 # (0.23076923076923078 out of 1.0)
    else  # if hunks_num > 7.5
       return 0.037037037037037035 # (0.037037037037037035 out of 1.0)
    end   end )