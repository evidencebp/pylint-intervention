create or replace function RandomForest_4 (same_day_duration_avg_diff int64, low_McCabe_max_before int64, Single comments_before int64, one_file_fix_rate_diff int64, length_diff int64, Comments_after int64, Single comments_diff int64, too-many-statements int64, cur_count int64, Comments_diff int64, bugs_diff int64, McCabe_max_after int64, h2_diff int64, low_ccp_group int64, changed_lines int64, high_McCabe_sum_before int64, volume_diff int64, Multi_diff int64, LLOC_before int64, high_McCabe_max_diff int64, hunks_num int64, LOC_before int64, calculated_length_diff int64, low_McCabe_sum_before int64, McCabe_sum_before int64, high_ccp_group int64, McCabe_max_before int64, mostly_delete int64, LLOC_diff int64, effort_diff int64, too-many-nested-blocks int64, cur_count_y int64, h1_diff int64, low_McCabe_max_diff int64, Single comments_after int64, massive_change int64, SLOC_diff int64, added_lines int64, prev_count_x int64, N2_diff int64, high_McCabe_sum_diff int64, Blank_diff int64, LOC_diff int64, new_function int64, prev_count int64, prev_count_y int64, SLOC_before int64, McCabe_sum_after int64, high_McCabe_max_before int64, avg_coupling_code_size_cut_diff int64, Blank_before int64, McCabe_max_diff int64, refactor_mle_diff int64, is_refactor int64, low_McCabe_sum_diff int64, added_functions int64, modified_McCabe_max_diff int64, too-many-branches int64, time_diff int64, only_removal int64, N1_diff int64, Comments_before int64, McCabe_sum_diff int64, vocabulary_diff int64, removed_lines int64, too-many-return-statements int64, difficulty_diff int64, cur_count_x int64) as (
  case when Single comments_after <= 115.0 then
    case when high_ccp_group <= 0.5 then
      case when removed_lines <= 62.5 then
        case when SLOC_diff <= -20.5 then
           return 0.16666666666666666 # (0.16666666666666666 out of 1.0)
        else  # if SLOC_diff > -20.5
          case when SLOC_diff <= 1.5 then
            case when SLOC_before <= 260.0 then
               return 0.21428571428571427 # (0.21428571428571427 out of 1.0)
            else  # if SLOC_before > 260.0
               return 0.6551724137931034 # (0.6551724137931034 out of 1.0)
            end           else  # if SLOC_diff > 1.5
             return 0.06666666666666667 # (0.06666666666666667 out of 1.0)
          end         end       else  # if removed_lines > 62.5
        case when Single comments_after <= 38.5 then
           return 0.8095238095238095 # (0.8095238095238095 out of 1.0)
        else  # if Single comments_after > 38.5
           return 0.3684210526315789 # (0.3684210526315789 out of 1.0)
        end       end     else  # if high_ccp_group > 0.5
      case when LOC_before <= 904.0 then
        case when refactor_mle_diff <= -0.09760291501879692 then
           return 0.8333333333333334 # (0.8333333333333334 out of 1.0)
        else  # if refactor_mle_diff > -0.09760291501879692
           return 1.0 # (1.0 out of 1.0)
        end       else  # if LOC_before > 904.0
         return 0.4 # (0.4 out of 1.0)
      end     end   else  # if Single comments_after > 115.0
    case when McCabe_max_before <= 26.5 then
       return 0.3 # (0.3 out of 1.0)
    else  # if McCabe_max_before > 26.5
       return 0.0 # (0.0 out of 1.0)
    end   end )