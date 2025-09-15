create or replace function RandomForest_1 (Blank_diff int64, bugs_diff int64, hunks_num int64, low_McCabe_sum_before int64, low_McCabe_max_diff int64, effort_diff int64, McCabe_max_diff int64, McCabe_sum_diff int64, Comments_before int64, massive_change int64, too-many-branches int64, low_McCabe_sum_diff int64, Blank_before int64, McCabe_sum_after int64, high_ccp_group int64, high_McCabe_sum_before int64, too-many-return-statements int64, cur_count_y int64, Comments_diff int64, Multi_diff int64, refactor_mle_diff int64, cur_count int64, new_function int64, added_lines int64, Comments_after int64, Single comments_diff int64, McCabe_max_before int64, LOC_before int64, SLOC_before int64, modified_McCabe_max_diff int64, h2_diff int64, too-many-statements int64, Single comments_after int64, high_McCabe_max_diff int64, vocabulary_diff int64, prev_count_y int64, LOC_diff int64, too-many-nested-blocks int64, N1_diff int64, changed_lines int64, calculated_length_diff int64, difficulty_diff int64, mostly_delete int64, low_ccp_group int64, McCabe_max_after int64, cur_count_x int64, length_diff int64, only_removal int64, avg_coupling_code_size_cut_diff int64, prev_count_x int64, one_file_fix_rate_diff int64, high_McCabe_max_before int64, Single comments_before int64, SLOC_diff int64, time_diff int64, low_McCabe_max_before int64, added_functions int64, N2_diff int64, high_McCabe_sum_diff int64, is_refactor int64, volume_diff int64, LLOC_diff int64, same_day_duration_avg_diff int64, LLOC_before int64, prev_count int64, McCabe_sum_before int64, removed_lines int64, h1_diff int64) as (
  case when modified_McCabe_max_diff <= 0.5 then
    case when avg_coupling_code_size_cut_diff <= 0.5946428775787354 then
      case when Single comments_after <= 58.5 then
        case when McCabe_max_after <= 8.0 then
           return 0.92 # (0.92 out of 1.0)
        else  # if McCabe_max_after > 8.0
          case when same_day_duration_avg_diff <= -3.2529643774032593 then
            case when Comments_before <= 49.0 then
               return 0.6538461538461539 # (0.6538461538461539 out of 1.0)
            else  # if Comments_before > 49.0
               return 0.8823529411764706 # (0.8823529411764706 out of 1.0)
            end           else  # if same_day_duration_avg_diff > -3.2529643774032593
            case when Blank_diff <= -1.5 then
               return 0.5 # (0.5 out of 1.0)
            else  # if Blank_diff > -1.5
               return 0.21052631578947367 # (0.21052631578947367 out of 1.0)
            end           end         end       else  # if Single comments_after > 58.5
        case when removed_lines <= 35.5 then
          case when Blank_before <= 215.0 then
             return 0.07142857142857142 # (0.07142857142857142 out of 1.0)
          else  # if Blank_before > 215.0
             return 0.21052631578947367 # (0.21052631578947367 out of 1.0)
          end         else  # if removed_lines > 35.5
           return 0.5833333333333334 # (0.5833333333333334 out of 1.0)
        end       end     else  # if avg_coupling_code_size_cut_diff > 0.5946428775787354
      case when McCabe_sum_after <= 148.0 then
         return 0.0 # (0.0 out of 1.0)
      else  # if McCabe_sum_after > 148.0
         return 0.47619047619047616 # (0.47619047619047616 out of 1.0)
      end     end   else  # if modified_McCabe_max_diff > 0.5
     return 0.0 # (0.0 out of 1.0)
  end )