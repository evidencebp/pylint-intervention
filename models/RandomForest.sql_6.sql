create or replace function RandomForest_6 (N1_diff int64, Single comments_diff int64, h2_diff int64, new_function int64, added_lines int64, difficulty_diff int64, too-many-return-statements int64, effort_diff int64, length_diff int64, McCabe_sum_after int64, removed_lines int64, McCabe_sum_before int64, low_McCabe_sum_before int64, high_McCabe_max_diff int64, prev_count_x int64, prev_count int64, LOC_before int64, SLOC_diff int64, low_McCabe_sum_diff int64, cur_count int64, calculated_length_diff int64, Blank_before int64, Comments_after int64, bugs_diff int64, too-many-statements int64, volume_diff int64, only_removal int64, too-many-branches int64, low_McCabe_max_diff int64, low_McCabe_max_before int64, McCabe_max_diff int64, is_refactor int64, cur_count_x int64, Single comments_before int64, McCabe_max_after int64, Blank_diff int64, McCabe_max_before int64, added_functions int64, Multi_diff int64, SLOC_before int64, prev_count_y int64, massive_change int64, LOC_diff int64, time_diff int64, h1_diff int64, vocabulary_diff int64, LLOC_diff int64, high_ccp_group int64, hunks_num int64, Single comments_after int64, high_McCabe_sum_before int64, modified_McCabe_max_diff int64, N2_diff int64, same_day_duration_avg_diff int64, low_ccp_group int64, Comments_before int64, cur_count_y int64, high_McCabe_sum_diff int64, changed_lines int64, high_McCabe_max_before int64, Comments_diff int64, LLOC_before int64, one_file_fix_rate_diff int64, too-many-nested-blocks int64, McCabe_sum_diff int64, refactor_mle_diff int64, avg_coupling_code_size_cut_diff int64, mostly_delete int64) as (
  case when SLOC_before <= 704.5 then
    case when N2_diff <= -25.0 then
       return 0.8378378378378378 # (0.8378378378378378 out of 1.0)
    else  # if N2_diff > -25.0
      case when Comments_before <= 50.5 then
        case when avg_coupling_code_size_cut_diff <= 0.1966772973537445 then
          case when McCabe_sum_before <= 50.5 then
             return 0.47368421052631576 # (0.47368421052631576 out of 1.0)
          else  # if McCabe_sum_before > 50.5
            case when is_refactor <= 0.5 then
               return 0.42857142857142855 # (0.42857142857142855 out of 1.0)
            else  # if is_refactor > 0.5
               return 0.09523809523809523 # (0.09523809523809523 out of 1.0)
            end           end         else  # if avg_coupling_code_size_cut_diff > 0.1966772973537445
          case when SLOC_diff <= -1.5 then
             return 0.9473684210526315 # (0.9473684210526315 out of 1.0)
          else  # if SLOC_diff > -1.5
             return 0.6 # (0.6 out of 1.0)
          end         end       else  # if Comments_before > 50.5
        case when removed_lines <= 41.0 then
           return 0.08333333333333333 # (0.08333333333333333 out of 1.0)
        else  # if removed_lines > 41.0
           return 0.375 # (0.375 out of 1.0)
        end       end     end   else  # if SLOC_before > 704.5
    case when LOC_diff <= 5.5 then
      case when LLOC_before <= 982.5 then
         return 0.2727272727272727 # (0.2727272727272727 out of 1.0)
      else  # if LLOC_before > 982.5
         return 0.0 # (0.0 out of 1.0)
      end     else  # if LOC_diff > 5.5
       return 0.375 # (0.375 out of 1.0)
    end   end )