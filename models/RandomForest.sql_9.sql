create or replace function RandomForest_9 (length_diff int64, N1_diff int64, N2_diff int64, McCabe_sum_diff int64, bugs_diff int64, McCabe_sum_after int64, too-many-branches int64, is_refactor int64, high_ccp_group int64, mostly_delete int64, cur_count_y int64, low_ccp_group int64, prev_count_x int64, difficulty_diff int64, removed_lines int64, Blank_before int64, LOC_before int64, low_McCabe_sum_before int64, cur_count_x int64, Comments_diff int64, Comments_before int64, h2_diff int64, Comments_after int64, McCabe_sum_before int64, McCabe_max_after int64, high_McCabe_max_diff int64, added_functions int64, SLOC_diff int64, avg_coupling_code_size_cut_diff int64, too-many-nested-blocks int64, changed_lines int64, high_McCabe_sum_before int64, prev_count int64, high_McCabe_sum_diff int64, vocabulary_diff int64, SLOC_before int64, LOC_diff int64, low_McCabe_max_diff int64, Single comments_before int64, one_file_fix_rate_diff int64, too-many-statements int64, added_lines int64, new_function int64, massive_change int64, LLOC_before int64, calculated_length_diff int64, Single comments_diff int64, modified_McCabe_max_diff int64, McCabe_max_before int64, LLOC_diff int64, refactor_mle_diff int64, low_McCabe_sum_diff int64, hunks_num int64, low_McCabe_max_before int64, too-many-return-statements int64, only_removal int64, same_day_duration_avg_diff int64, h1_diff int64, time_diff int64, prev_count_y int64, effort_diff int64, Multi_diff int64, Blank_diff int64, cur_count int64, volume_diff int64, high_McCabe_max_before int64, Single comments_after int64, McCabe_max_diff int64) as (
  case when new_function <= 0.5 then
    case when added_lines <= 142.0 then
      case when McCabe_sum_after <= 68.5 then
        case when Single comments_after <= 18.0 then
           return 0.2857142857142857 # (0.2857142857142857 out of 1.0)
        else  # if Single comments_after > 18.0
           return 0.6153846153846154 # (0.6153846153846154 out of 1.0)
        end       else  # if McCabe_sum_after > 68.5
        case when refactor_mle_diff <= 0.1733204647898674 then
          case when Comments_before <= 43.0 then
             return 0.2413793103448276 # (0.2413793103448276 out of 1.0)
          else  # if Comments_before > 43.0
            case when Comments_diff <= 1.0 then
               return 0.0 # (0.0 out of 1.0)
            else  # if Comments_diff > 1.0
               return 0.07692307692307693 # (0.07692307692307693 out of 1.0)
            end           end         else  # if refactor_mle_diff > 0.1733204647898674
           return 0.35714285714285715 # (0.35714285714285715 out of 1.0)
        end       end     else  # if added_lines > 142.0
       return 0.5 # (0.5 out of 1.0)
    end   else  # if new_function > 0.5
    case when Single comments_diff <= -2.5 then
       return 0.9090909090909091 # (0.9090909090909091 out of 1.0)
    else  # if Single comments_diff > -2.5
      case when modified_McCabe_max_diff <= -0.5 then
        case when SLOC_diff <= 6.0 then
           return 0.06666666666666667 # (0.06666666666666667 out of 1.0)
        else  # if SLOC_diff > 6.0
           return 0.35714285714285715 # (0.35714285714285715 out of 1.0)
        end       else  # if modified_McCabe_max_diff > -0.5
         return 0.7916666666666666 # (0.7916666666666666 out of 1.0)
      end     end   end )