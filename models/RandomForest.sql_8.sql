create or replace function RandomForest_8 (Blank_diff int64, bugs_diff int64, hunks_num int64, low_McCabe_sum_before int64, low_McCabe_max_diff int64, effort_diff int64, McCabe_max_diff int64, McCabe_sum_diff int64, Comments_before int64, massive_change int64, too-many-branches int64, low_McCabe_sum_diff int64, Blank_before int64, McCabe_sum_after int64, high_ccp_group int64, high_McCabe_sum_before int64, too-many-return-statements int64, cur_count_y int64, Comments_diff int64, Multi_diff int64, refactor_mle_diff int64, cur_count int64, new_function int64, added_lines int64, Comments_after int64, Single comments_diff int64, McCabe_max_before int64, LOC_before int64, SLOC_before int64, modified_McCabe_max_diff int64, h2_diff int64, too-many-statements int64, Single comments_after int64, high_McCabe_max_diff int64, vocabulary_diff int64, prev_count_y int64, LOC_diff int64, too-many-nested-blocks int64, N1_diff int64, changed_lines int64, calculated_length_diff int64, difficulty_diff int64, mostly_delete int64, low_ccp_group int64, McCabe_max_after int64, cur_count_x int64, length_diff int64, only_removal int64, avg_coupling_code_size_cut_diff int64, prev_count_x int64, one_file_fix_rate_diff int64, high_McCabe_max_before int64, Single comments_before int64, SLOC_diff int64, time_diff int64, low_McCabe_max_before int64, added_functions int64, N2_diff int64, high_McCabe_sum_diff int64, is_refactor int64, volume_diff int64, LLOC_diff int64, same_day_duration_avg_diff int64, LLOC_before int64, prev_count int64, McCabe_sum_before int64, removed_lines int64, h1_diff int64) as (
  case when changed_lines <= 122.5 then
    case when Single comments_after <= 102.0 then
      case when same_day_duration_avg_diff <= 156.3499984741211 then
        case when McCabe_sum_before <= 122.0 then
          case when hunks_num <= 3.5 then
            case when McCabe_sum_after <= 51.5 then
               return 0.45 # (0.45 out of 1.0)
            else  # if McCabe_sum_after > 51.5
               return 0.625 # (0.625 out of 1.0)
            end           else  # if hunks_num > 3.5
             return 0.2777777777777778 # (0.2777777777777778 out of 1.0)
          end         else  # if McCabe_sum_before > 122.0
          case when same_day_duration_avg_diff <= -41.710784912109375 then
             return 0.20833333333333334 # (0.20833333333333334 out of 1.0)
          else  # if same_day_duration_avg_diff > -41.710784912109375
            case when too-many-statements <= 0.5 then
               return 0.06666666666666667 # (0.06666666666666667 out of 1.0)
            else  # if too-many-statements > 0.5
               return 0.0 # (0.0 out of 1.0)
            end           end         end       else  # if same_day_duration_avg_diff > 156.3499984741211
         return 0.8333333333333334 # (0.8333333333333334 out of 1.0)
      end     else  # if Single comments_after > 102.0
       return 0.03333333333333333 # (0.03333333333333333 out of 1.0)
    end   else  # if changed_lines > 122.5
    case when LOC_diff <= -213.0 then
       return 0.2608695652173913 # (0.2608695652173913 out of 1.0)
    else  # if LOC_diff > -213.0
      case when McCabe_max_diff <= -6.5 then
         return 0.8076923076923077 # (0.8076923076923077 out of 1.0)
      else  # if McCabe_max_diff > -6.5
         return 0.5 # (0.5 out of 1.0)
      end     end   end )