create or replace function RandomForest_7 (N1_diff int64, Single comments_diff int64, h2_diff int64, new_function int64, added_lines int64, difficulty_diff int64, too-many-return-statements int64, effort_diff int64, length_diff int64, McCabe_sum_after int64, removed_lines int64, McCabe_sum_before int64, low_McCabe_sum_before int64, high_McCabe_max_diff int64, prev_count_x int64, prev_count int64, LOC_before int64, SLOC_diff int64, low_McCabe_sum_diff int64, cur_count int64, calculated_length_diff int64, Blank_before int64, Comments_after int64, bugs_diff int64, too-many-statements int64, volume_diff int64, only_removal int64, too-many-branches int64, low_McCabe_max_diff int64, low_McCabe_max_before int64, McCabe_max_diff int64, is_refactor int64, cur_count_x int64, Single comments_before int64, McCabe_max_after int64, Blank_diff int64, McCabe_max_before int64, added_functions int64, Multi_diff int64, SLOC_before int64, prev_count_y int64, massive_change int64, LOC_diff int64, time_diff int64, h1_diff int64, vocabulary_diff int64, LLOC_diff int64, high_ccp_group int64, hunks_num int64, Single comments_after int64, high_McCabe_sum_before int64, modified_McCabe_max_diff int64, N2_diff int64, same_day_duration_avg_diff int64, low_ccp_group int64, Comments_before int64, cur_count_y int64, high_McCabe_sum_diff int64, changed_lines int64, high_McCabe_max_before int64, Comments_diff int64, LLOC_before int64, one_file_fix_rate_diff int64, too-many-nested-blocks int64, McCabe_sum_diff int64, refactor_mle_diff int64, avg_coupling_code_size_cut_diff int64, mostly_delete int64) as (
  case when McCabe_max_before <= 15.5 then
    case when changed_lines <= 32.0 then
       return 0.25 # (0.25 out of 1.0)
    else  # if changed_lines > 32.0
      case when LLOC_before <= 213.0 then
         return 0.5714285714285714 # (0.5714285714285714 out of 1.0)
      else  # if LLOC_before > 213.0
         return 0.9259259259259259 # (0.9259259259259259 out of 1.0)
      end     end   else  # if McCabe_max_before > 15.5
    case when LOC_diff <= -133.0 then
      case when too-many-statements <= 0.5 then
         return 0.4117647058823529 # (0.4117647058823529 out of 1.0)
      else  # if too-many-statements > 0.5
         return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
      end     else  # if LOC_diff > -133.0
      case when LOC_diff <= 27.5 then
        case when changed_lines <= 6.5 then
           return 0.47368421052631576 # (0.47368421052631576 out of 1.0)
        else  # if changed_lines > 6.5
          case when LOC_before <= 467.5 then
             return 0.4166666666666667 # (0.4166666666666667 out of 1.0)
          else  # if LOC_before > 467.5
            case when McCabe_max_before <= 18.5 then
               return 0.3076923076923077 # (0.3076923076923077 out of 1.0)
            else  # if McCabe_max_before > 18.5
              case when removed_lines <= 17.5 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if removed_lines > 17.5
                 return 0.11538461538461539 # (0.11538461538461539 out of 1.0)
              end             end           end         end       else  # if LOC_diff > 27.5
         return 0.5333333333333333 # (0.5333333333333333 out of 1.0)
      end     end   end )