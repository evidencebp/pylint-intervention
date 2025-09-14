create or replace function RandomForest_6 (is_refactor int64, McCabe_max_before int64, N1_diff int64, high_McCabe_sum_before int64, same_day_duration_avg_diff int64, Comments_before int64, hunks_num int64, added_lines int64, prev_count int64, low_McCabe_max_before int64, high_McCabe_max_diff int64, vocabulary_diff int64, modified_McCabe_max_diff int64, avg_coupling_code_size_cut_diff int64, too-many-nested-blocks int64, low_McCabe_max_diff int64, changed_lines int64, effort_diff int64, removed_lines int64, Blank_before int64, SLOC_diff int64, length_diff int64, low_ccp_group int64, calculated_length_diff int64, McCabe_max_diff int64, McCabe_max_after int64, LOC_diff int64, too-many-return-statements int64, Single comments_after int64, McCabe_sum_diff int64, LLOC_diff int64, too-many-statements int64, Comments_after int64, low_McCabe_sum_diff int64, McCabe_sum_before int64, difficulty_diff int64, Single comments_before int64, massive_change int64, prev_count_x int64, refactor_mle_diff int64, cur_count_y int64, N2_diff int64, prev_count_y int64, Single comments_diff int64, cur_count int64, high_McCabe_max_before int64, one_file_fix_rate_diff int64, h1_diff int64, low_McCabe_sum_before int64, time_diff int64, LOC_before int64, SLOC_before int64, too-many-branches int64, volume_diff int64, McCabe_sum_after int64, mostly_delete int64, Multi_diff int64, high_McCabe_sum_diff int64, Blank_diff int64, bugs_diff int64, h2_diff int64, cur_count_x int64, added_functions int64, LLOC_before int64, high_ccp_group int64, Comments_diff int64, only_removal int64) as (
  case when changed_lines <= 122.5 then
    case when McCabe_max_before <= 17.5 then
      case when LLOC_before <= 467.5 then
        case when same_day_duration_avg_diff <= -33.50555610656738 then
           return 0.42857142857142855 # (0.42857142857142855 out of 1.0)
        else  # if same_day_duration_avg_diff > -33.50555610656738
           return 0.7241379310344828 # (0.7241379310344828 out of 1.0)
        end       else  # if LLOC_before > 467.5
         return 0.13333333333333333 # (0.13333333333333333 out of 1.0)
      end     else  # if McCabe_max_before > 17.5
      case when McCabe_sum_before <= 149.5 then
        case when Blank_before <= 75.5 then
           return 0.16666666666666666 # (0.16666666666666666 out of 1.0)
        else  # if Blank_before > 75.5
           return 0.03225806451612903 # (0.03225806451612903 out of 1.0)
        end       else  # if McCabe_sum_before > 149.5
        case when modified_McCabe_max_diff <= -1.5 then
           return 0.4666666666666667 # (0.4666666666666667 out of 1.0)
        else  # if modified_McCabe_max_diff > -1.5
           return 0.19230769230769232 # (0.19230769230769232 out of 1.0)
        end       end     end   else  # if changed_lines > 122.5
    case when low_ccp_group <= 0.5 then
      case when avg_coupling_code_size_cut_diff <= -0.47756411135196686 then
         return 0.9629629629629629 # (0.9629629629629629 out of 1.0)
      else  # if avg_coupling_code_size_cut_diff > -0.47756411135196686
        case when one_file_fix_rate_diff <= -0.048076923936605453 then
           return 0.26666666666666666 # (0.26666666666666666 out of 1.0)
        else  # if one_file_fix_rate_diff > -0.048076923936605453
           return 0.7 # (0.7 out of 1.0)
        end       end     else  # if low_ccp_group > 0.5
       return 0.2777777777777778 # (0.2777777777777778 out of 1.0)
    end   end )