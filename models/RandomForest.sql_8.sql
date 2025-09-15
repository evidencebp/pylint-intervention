create or replace function RandomForest_8 (same_day_duration_avg_diff int64, low_McCabe_max_before int64, Single comments_before int64, one_file_fix_rate_diff int64, length_diff int64, Comments_after int64, Single comments_diff int64, too-many-statements int64, cur_count int64, Comments_diff int64, bugs_diff int64, McCabe_max_after int64, h2_diff int64, low_ccp_group int64, changed_lines int64, high_McCabe_sum_before int64, volume_diff int64, Multi_diff int64, LLOC_before int64, high_McCabe_max_diff int64, hunks_num int64, LOC_before int64, calculated_length_diff int64, low_McCabe_sum_before int64, McCabe_sum_before int64, high_ccp_group int64, McCabe_max_before int64, mostly_delete int64, LLOC_diff int64, effort_diff int64, too-many-nested-blocks int64, cur_count_y int64, h1_diff int64, low_McCabe_max_diff int64, Single comments_after int64, massive_change int64, SLOC_diff int64, added_lines int64, prev_count_x int64, N2_diff int64, high_McCabe_sum_diff int64, Blank_diff int64, LOC_diff int64, new_function int64, prev_count int64, prev_count_y int64, SLOC_before int64, McCabe_sum_after int64, high_McCabe_max_before int64, avg_coupling_code_size_cut_diff int64, Blank_before int64, McCabe_max_diff int64, refactor_mle_diff int64, is_refactor int64, low_McCabe_sum_diff int64, added_functions int64, modified_McCabe_max_diff int64, too-many-branches int64, time_diff int64, only_removal int64, N1_diff int64, Comments_before int64, McCabe_sum_diff int64, vocabulary_diff int64, removed_lines int64, too-many-return-statements int64, difficulty_diff int64, cur_count_x int64) as (
  case when Multi_diff <= 0.5 then
    case when Single comments_after <= 115.0 then
      case when Single comments_diff <= -2.5 then
        case when Single comments_before <= 36.5 then
           return 0.8823529411764706 # (0.8823529411764706 out of 1.0)
        else  # if Single comments_before > 36.5
           return 0.4666666666666667 # (0.4666666666666667 out of 1.0)
        end       else  # if Single comments_diff > -2.5
        case when low_ccp_group <= 0.5 then
          case when modified_McCabe_max_diff <= -4.5 then
             return 0.7857142857142857 # (0.7857142857142857 out of 1.0)
          else  # if modified_McCabe_max_diff > -4.5
            case when refactor_mle_diff <= -0.02997202519327402 then
               return 0.2727272727272727 # (0.2727272727272727 out of 1.0)
            else  # if refactor_mle_diff > -0.02997202519327402
              case when McCabe_max_before <= 16.5 then
                 return 0.6470588235294118 # (0.6470588235294118 out of 1.0)
              else  # if McCabe_max_before > 16.5
                 return 0.15384615384615385 # (0.15384615384615385 out of 1.0)
              end             end           end         else  # if low_ccp_group > 0.5
          case when changed_lines <= 73.0 then
             return 0.26666666666666666 # (0.26666666666666666 out of 1.0)
          else  # if changed_lines > 73.0
             return 0.0 # (0.0 out of 1.0)
          end         end       end     else  # if Single comments_after > 115.0
       return 0.024390243902439025 # (0.024390243902439025 out of 1.0)
    end   else  # if Multi_diff > 0.5
     return 0.76 # (0.76 out of 1.0)
  end )