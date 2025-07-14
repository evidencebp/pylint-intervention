create or replace function RandomForest_2 (hunks_num int64, McCabe_sum_after int64, added_lines int64, cur_count_y int64, changed_lines int64, N1_diff int64, added_functions int64, Single comments_before int64, McCabe_max_after int64, calculated_length_diff int64, h1_diff int64, difficulty_diff int64, too-many-nested-blocks int64, modified_McCabe_max_diff int64, removed_lines int64, prev_count int64, Blank_diff int64, prev_count_x int64, h2_diff int64, LLOC_before int64, Multi_diff int64, volume_diff int64, same_day_duration_avg_diff int64, N2_diff int64, one_file_fix_rate_diff int64, Comments_after int64, massive_change int64, Single comments_diff int64, Comments_before int64, SLOC_before int64, prev_count_y int64, vocabulary_diff int64, LOC_before int64, McCabe_sum_diff int64, high_ccp_group int64, McCabe_sum_before int64, is_refactor int64, cur_count_x int64, refactor_mle_diff int64, time_diff int64, bugs_diff int64, avg_coupling_code_size_cut_diff int64, LLOC_diff int64, Single comments_after int64, too-many-branches int64, McCabe_max_diff int64, too-many-statements int64, mostly_delete int64, effort_diff int64, length_diff int64, Blank_before int64, SLOC_diff int64, McCabe_max_before int64, LOC_diff int64, cur_count int64, too-many-return-statements int64, only_removal int64, Comments_diff int64) as (
  case when N2_diff <= -25.0 then
    case when avg_coupling_code_size_cut_diff <= -0.444230780005455 then
       return 0.92 # (23.0 out of 25.0)
    else  # if avg_coupling_code_size_cut_diff > -0.444230780005455
       return 0.48 # (12.0 out of 25.0)
    end   else  # if N2_diff > -25.0
    case when McCabe_max_before <= 16.5 then
      case when avg_coupling_code_size_cut_diff <= 0.5625 then
        case when Single comments_before <= 26.0 then
           return 0.42105263157894735 # (8.0 out of 19.0)
        else  # if Single comments_before > 26.0
          case when added_functions <= 0.5 then
             return 0.6470588235294118 # (11.0 out of 17.0)
          else  # if added_functions > 0.5
             return 0.8235294117647058 # (14.0 out of 17.0)
          end         end       else  # if avg_coupling_code_size_cut_diff > 0.5625
         return 0.1875 # (3.0 out of 16.0)
      end     else  # if McCabe_max_before > 16.5
      case when high_ccp_group <= 0.5 then
        case when Blank_diff <= 1.5 then
          case when LOC_diff <= -14.5 then
            case when changed_lines <= 109.5 then
               return 0.15384615384615385 # (2.0 out of 13.0)
            else  # if changed_lines > 109.5
               return 0.1111111111111111 # (2.0 out of 18.0)
            end           else  # if LOC_diff > -14.5
             return 0.32 # (8.0 out of 25.0)
          end         else  # if Blank_diff > 1.5
           return 0.06666666666666667 # (2.0 out of 30.0)
        end       else  # if high_ccp_group > 0.5
         return 0.5 # (12.0 out of 24.0)
      end     end   end )