create or replace function RandomForest_4 (hunks_num int64, McCabe_sum_after int64, added_lines int64, cur_count_y int64, changed_lines int64, N1_diff int64, added_functions int64, Single comments_before int64, McCabe_max_after int64, calculated_length_diff int64, h1_diff int64, difficulty_diff int64, too-many-nested-blocks int64, modified_McCabe_max_diff int64, removed_lines int64, prev_count int64, Blank_diff int64, prev_count_x int64, h2_diff int64, LLOC_before int64, Multi_diff int64, volume_diff int64, same_day_duration_avg_diff int64, N2_diff int64, one_file_fix_rate_diff int64, Comments_after int64, massive_change int64, Single comments_diff int64, Comments_before int64, SLOC_before int64, prev_count_y int64, vocabulary_diff int64, LOC_before int64, McCabe_sum_diff int64, high_ccp_group int64, McCabe_sum_before int64, is_refactor int64, cur_count_x int64, refactor_mle_diff int64, time_diff int64, bugs_diff int64, avg_coupling_code_size_cut_diff int64, LLOC_diff int64, Single comments_after int64, too-many-branches int64, McCabe_max_diff int64, too-many-statements int64, mostly_delete int64, effort_diff int64, length_diff int64, Blank_before int64, SLOC_diff int64, McCabe_max_before int64, LOC_diff int64, cur_count int64, too-many-return-statements int64, only_removal int64, Comments_diff int64) as (
  case when LLOC_before <= 348.0 then
    case when LOC_before <= 594.0 then
      case when Comments_diff <= -2.5 then
         return 0.75 # (15.0 out of 20.0)
      else  # if Comments_diff > -2.5
        case when hunks_num <= 2.5 then
           return 0.6428571428571429 # (18.0 out of 28.0)
        else  # if hunks_num > 2.5
          case when McCabe_max_after <= 10.5 then
             return 0.0 # (0.0 out of 17.0)
          else  # if McCabe_max_after > 10.5
             return 0.35 # (7.0 out of 20.0)
          end         end       end     else  # if LOC_before > 594.0
       return 1.0 # (20.0 out of 20.0)
    end   else  # if LLOC_before > 348.0
    case when changed_lines <= 136.5 then
      case when LOC_before <= 838.0 then
         return 0.6666666666666666 # (10.0 out of 15.0)
      else  # if LOC_before > 838.0
        case when Comments_after <= 38.5 then
           return 0.42857142857142855 # (6.0 out of 14.0)
        else  # if Comments_after > 38.5
          case when Single comments_diff <= 0.5 then
            case when McCabe_max_after <= 24.5 then
               return 0.0 # (0.0 out of 25.0)
            else  # if McCabe_max_after > 24.5
               return 0.07692307692307693 # (1.0 out of 13.0)
            end           else  # if Single comments_diff > 0.5
             return 0.06666666666666667 # (1.0 out of 15.0)
          end         end       end     else  # if changed_lines > 136.5
      case when N1_diff <= -31.5 then
         return 0.2857142857142857 # (6.0 out of 21.0)
      else  # if N1_diff > -31.5
         return 0.7142857142857143 # (15.0 out of 21.0)
      end     end   end )