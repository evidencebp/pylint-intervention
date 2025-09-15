create or replace function RandomForest_9 (Blank_diff int64, bugs_diff int64, hunks_num int64, low_McCabe_sum_before int64, low_McCabe_max_diff int64, effort_diff int64, McCabe_max_diff int64, McCabe_sum_diff int64, Comments_before int64, massive_change int64, too-many-branches int64, low_McCabe_sum_diff int64, Blank_before int64, McCabe_sum_after int64, high_ccp_group int64, high_McCabe_sum_before int64, too-many-return-statements int64, cur_count_y int64, Comments_diff int64, Multi_diff int64, refactor_mle_diff int64, cur_count int64, new_function int64, added_lines int64, Comments_after int64, Single comments_diff int64, McCabe_max_before int64, LOC_before int64, SLOC_before int64, modified_McCabe_max_diff int64, h2_diff int64, too-many-statements int64, Single comments_after int64, high_McCabe_max_diff int64, vocabulary_diff int64, prev_count_y int64, LOC_diff int64, too-many-nested-blocks int64, N1_diff int64, changed_lines int64, calculated_length_diff int64, difficulty_diff int64, mostly_delete int64, low_ccp_group int64, McCabe_max_after int64, cur_count_x int64, length_diff int64, only_removal int64, avg_coupling_code_size_cut_diff int64, prev_count_x int64, one_file_fix_rate_diff int64, high_McCabe_max_before int64, Single comments_before int64, SLOC_diff int64, time_diff int64, low_McCabe_max_before int64, added_functions int64, N2_diff int64, high_McCabe_sum_diff int64, is_refactor int64, volume_diff int64, LLOC_diff int64, same_day_duration_avg_diff int64, LLOC_before int64, prev_count int64, McCabe_sum_before int64, removed_lines int64, h1_diff int64) as (
  case when Blank_before <= 43.0 then
    case when LOC_before <= 280.0 then
       return 0.8421052631578947 # (0.8421052631578947 out of 1.0)
    else  # if LOC_before > 280.0
       return 0.8125 # (0.8125 out of 1.0)
    end   else  # if Blank_before > 43.0
    case when McCabe_sum_diff <= -25.0 then
      case when avg_coupling_code_size_cut_diff <= -0.4149184226989746 then
         return 1.0 # (1.0 out of 1.0)
      else  # if avg_coupling_code_size_cut_diff > -0.4149184226989746
         return 0.4375 # (0.4375 out of 1.0)
      end     else  # if McCabe_sum_diff > -25.0
      case when McCabe_sum_after <= 207.5 then
        case when McCabe_sum_diff <= -14.5 then
           return 0.0 # (0.0 out of 1.0)
        else  # if McCabe_sum_diff > -14.5
          case when h2_diff <= -0.5 then
            case when vocabulary_diff <= -4.5 then
               return 0.4444444444444444 # (0.4444444444444444 out of 1.0)
            else  # if vocabulary_diff > -4.5
               return 0.8235294117647058 # (0.8235294117647058 out of 1.0)
            end           else  # if h2_diff > -0.5
            case when McCabe_sum_before <= 153.5 then
              case when LLOC_diff <= 1.0 then
                 return 0.375 # (0.375 out of 1.0)
              else  # if LLOC_diff > 1.0
                 return 0.0 # (0.0 out of 1.0)
              end             else  # if McCabe_sum_before > 153.5
               return 0.5 # (0.5 out of 1.0)
            end           end         end       else  # if McCabe_sum_after > 207.5
        case when hunks_num <= 4.5 then
           return 0.0 # (0.0 out of 1.0)
        else  # if hunks_num > 4.5
           return 0.16666666666666666 # (0.16666666666666666 out of 1.0)
        end       end     end   end )