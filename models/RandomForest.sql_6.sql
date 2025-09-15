create or replace function RandomForest_6 (Blank_diff int64, bugs_diff int64, hunks_num int64, low_McCabe_sum_before int64, low_McCabe_max_diff int64, effort_diff int64, McCabe_max_diff int64, McCabe_sum_diff int64, Comments_before int64, massive_change int64, too-many-branches int64, low_McCabe_sum_diff int64, Blank_before int64, McCabe_sum_after int64, high_ccp_group int64, high_McCabe_sum_before int64, too-many-return-statements int64, cur_count_y int64, Comments_diff int64, Multi_diff int64, refactor_mle_diff int64, cur_count int64, new_function int64, added_lines int64, Comments_after int64, Single comments_diff int64, McCabe_max_before int64, LOC_before int64, SLOC_before int64, modified_McCabe_max_diff int64, h2_diff int64, too-many-statements int64, Single comments_after int64, high_McCabe_max_diff int64, vocabulary_diff int64, prev_count_y int64, LOC_diff int64, too-many-nested-blocks int64, N1_diff int64, changed_lines int64, calculated_length_diff int64, difficulty_diff int64, mostly_delete int64, low_ccp_group int64, McCabe_max_after int64, cur_count_x int64, length_diff int64, only_removal int64, avg_coupling_code_size_cut_diff int64, prev_count_x int64, one_file_fix_rate_diff int64, high_McCabe_max_before int64, Single comments_before int64, SLOC_diff int64, time_diff int64, low_McCabe_max_before int64, added_functions int64, N2_diff int64, high_McCabe_sum_diff int64, is_refactor int64, volume_diff int64, LLOC_diff int64, same_day_duration_avg_diff int64, LLOC_before int64, prev_count int64, McCabe_sum_before int64, removed_lines int64, h1_diff int64) as (
  case when h2_diff <= -0.5 then
    case when h2_diff <= -20.5 then
      case when hunks_num <= 3.5 then
         return 0.07692307692307693 # (0.07692307692307693 out of 1.0)
      else  # if hunks_num > 3.5
         return 0.6842105263157895 # (0.6842105263157895 out of 1.0)
      end     else  # if h2_diff > -20.5
      case when Comments_before <= 76.0 then
        case when changed_lines <= 37.5 then
           return 0.3076923076923077 # (0.3076923076923077 out of 1.0)
        else  # if changed_lines > 37.5
          case when McCabe_max_before <= 17.5 then
             return 0.8 # (0.8 out of 1.0)
          else  # if McCabe_max_before > 17.5
             return 0.9642857142857143 # (0.9642857142857143 out of 1.0)
          end         end       else  # if Comments_before > 76.0
         return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
      end     end   else  # if h2_diff > -0.5
    case when Comments_before <= 38.0 then
      case when LOC_diff <= -6.5 then
         return 0.125 # (0.125 out of 1.0)
      else  # if LOC_diff > -6.5
        case when refactor_mle_diff <= 0.005958525463938713 then
          case when Single comments_after <= 18.0 then
             return 0.6842105263157895 # (0.6842105263157895 out of 1.0)
          else  # if Single comments_after > 18.0
             return 1.0 # (1.0 out of 1.0)
          end         else  # if refactor_mle_diff > 0.005958525463938713
           return 0.2 # (0.2 out of 1.0)
        end       end     else  # if Comments_before > 38.0
      case when LOC_diff <= 22.0 then
        case when Comments_after <= 87.0 then
           return 0.15384615384615385 # (0.15384615384615385 out of 1.0)
        else  # if Comments_after > 87.0
           return 0.047619047619047616 # (0.047619047619047616 out of 1.0)
        end       else  # if LOC_diff > 22.0
         return 0.6923076923076923 # (0.6923076923076923 out of 1.0)
      end     end   end )