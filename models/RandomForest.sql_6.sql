create or replace function RandomForest_6 (length_diff int64, N1_diff int64, N2_diff int64, McCabe_sum_diff int64, bugs_diff int64, McCabe_sum_after int64, too-many-branches int64, is_refactor int64, high_ccp_group int64, mostly_delete int64, cur_count_y int64, low_ccp_group int64, prev_count_x int64, difficulty_diff int64, removed_lines int64, Blank_before int64, LOC_before int64, low_McCabe_sum_before int64, cur_count_x int64, Comments_diff int64, Comments_before int64, h2_diff int64, Comments_after int64, McCabe_sum_before int64, McCabe_max_after int64, high_McCabe_max_diff int64, added_functions int64, SLOC_diff int64, avg_coupling_code_size_cut_diff int64, too-many-nested-blocks int64, changed_lines int64, high_McCabe_sum_before int64, prev_count int64, high_McCabe_sum_diff int64, vocabulary_diff int64, SLOC_before int64, LOC_diff int64, low_McCabe_max_diff int64, Single comments_before int64, one_file_fix_rate_diff int64, too-many-statements int64, added_lines int64, new_function int64, massive_change int64, LLOC_before int64, calculated_length_diff int64, Single comments_diff int64, modified_McCabe_max_diff int64, McCabe_max_before int64, LLOC_diff int64, refactor_mle_diff int64, low_McCabe_sum_diff int64, hunks_num int64, low_McCabe_max_before int64, too-many-return-statements int64, only_removal int64, same_day_duration_avg_diff int64, h1_diff int64, time_diff int64, prev_count_y int64, effort_diff int64, Multi_diff int64, Blank_diff int64, cur_count int64, volume_diff int64, high_McCabe_max_before int64, Single comments_after int64, McCabe_max_diff int64) as (
  case when SLOC_diff <= 22.0 then
    case when McCabe_sum_before <= 37.5 then
       return 0.782608695652174 # (0.782608695652174 out of 1.0)
    else  # if McCabe_sum_before > 37.5
      case when removed_lines <= 96.0 then
        case when added_functions <= 0.5 then
          case when Blank_before <= 129.5 then
            case when McCabe_sum_before <= 58.0 then
               return 0.125 # (0.125 out of 1.0)
            else  # if McCabe_sum_before > 58.0
              case when one_file_fix_rate_diff <= -0.12061302736401558 then
                 return 0.17391304347826086 # (0.17391304347826086 out of 1.0)
              else  # if one_file_fix_rate_diff > -0.12061302736401558
                case when refactor_mle_diff <= -0.01705536851659417 then
                   return 0.4 # (0.4 out of 1.0)
                else  # if refactor_mle_diff > -0.01705536851659417
                   return 0.7142857142857143 # (0.7142857142857143 out of 1.0)
                end               end             end           else  # if Blank_before > 129.5
            case when N1_diff <= -8.0 then
               return 0.17647058823529413 # (0.17647058823529413 out of 1.0)
            else  # if N1_diff > -8.0
               return 0.0 # (0.0 out of 1.0)
            end           end         else  # if added_functions > 0.5
          case when removed_lines <= 41.0 then
             return 0.5555555555555556 # (0.5555555555555556 out of 1.0)
          else  # if removed_lines > 41.0
             return 0.26666666666666666 # (0.26666666666666666 out of 1.0)
          end         end       else  # if removed_lines > 96.0
         return 0.7058823529411765 # (0.7058823529411765 out of 1.0)
      end     end   else  # if SLOC_diff > 22.0
     return 0.8125 # (0.8125 out of 1.0)
  end )