create or replace function RandomForest_7 (Blank_diff int64, bugs_diff int64, hunks_num int64, low_McCabe_sum_before int64, low_McCabe_max_diff int64, effort_diff int64, McCabe_max_diff int64, McCabe_sum_diff int64, Comments_before int64, massive_change int64, too-many-branches int64, low_McCabe_sum_diff int64, Blank_before int64, McCabe_sum_after int64, high_ccp_group int64, high_McCabe_sum_before int64, too-many-return-statements int64, cur_count_y int64, Comments_diff int64, Multi_diff int64, refactor_mle_diff int64, cur_count int64, new_function int64, added_lines int64, Comments_after int64, Single comments_diff int64, McCabe_max_before int64, LOC_before int64, SLOC_before int64, modified_McCabe_max_diff int64, h2_diff int64, too-many-statements int64, Single comments_after int64, high_McCabe_max_diff int64, vocabulary_diff int64, prev_count_y int64, LOC_diff int64, too-many-nested-blocks int64, N1_diff int64, changed_lines int64, calculated_length_diff int64, difficulty_diff int64, mostly_delete int64, low_ccp_group int64, McCabe_max_after int64, cur_count_x int64, length_diff int64, only_removal int64, avg_coupling_code_size_cut_diff int64, prev_count_x int64, one_file_fix_rate_diff int64, high_McCabe_max_before int64, Single comments_before int64, SLOC_diff int64, time_diff int64, low_McCabe_max_before int64, added_functions int64, N2_diff int64, high_McCabe_sum_diff int64, is_refactor int64, volume_diff int64, LLOC_diff int64, same_day_duration_avg_diff int64, LLOC_before int64, prev_count int64, McCabe_sum_before int64, removed_lines int64, h1_diff int64) as (
  case when McCabe_sum_after <= 261.5 then
    case when avg_coupling_code_size_cut_diff <= -0.23963414877653122 then
      case when low_ccp_group <= 0.5 then
        case when length_diff <= -1.5 then
          case when Blank_diff <= -10.0 then
             return 0.9375 # (0.9375 out of 1.0)
          else  # if Blank_diff > -10.0
             return 1.0 # (1.0 out of 1.0)
          end         else  # if length_diff > -1.5
           return 0.64 # (0.64 out of 1.0)
        end       else  # if low_ccp_group > 0.5
         return 0.16 # (0.16 out of 1.0)
      end     else  # if avg_coupling_code_size_cut_diff > -0.23963414877653122
      case when same_day_duration_avg_diff <= -43.126028060913086 then
         return 0.10344827586206896 # (0.10344827586206896 out of 1.0)
      else  # if same_day_duration_avg_diff > -43.126028060913086
        case when Single comments_after <= 80.0 then
          case when LOC_before <= 371.0 then
             return 0.7 # (0.7 out of 1.0)
          else  # if LOC_before > 371.0
            case when same_day_duration_avg_diff <= -0.6108465194702148 then
               return 0.47619047619047616 # (0.47619047619047616 out of 1.0)
            else  # if same_day_duration_avg_diff > -0.6108465194702148
               return 0.10344827586206896 # (0.10344827586206896 out of 1.0)
            end           end         else  # if Single comments_after > 80.0
           return 0.8333333333333334 # (0.8333333333333334 out of 1.0)
        end       end     end   else  # if McCabe_sum_after > 261.5
     return 0.07142857142857142 # (0.07142857142857142 out of 1.0)
  end )