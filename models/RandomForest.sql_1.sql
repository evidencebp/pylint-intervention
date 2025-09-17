create or replace function RandomForest_1 (length_diff int64, N1_diff int64, N2_diff int64, McCabe_sum_diff int64, bugs_diff int64, McCabe_sum_after int64, too-many-branches int64, is_refactor int64, high_ccp_group int64, mostly_delete int64, cur_count_y int64, low_ccp_group int64, prev_count_x int64, difficulty_diff int64, removed_lines int64, Blank_before int64, LOC_before int64, low_McCabe_sum_before int64, cur_count_x int64, Comments_diff int64, Comments_before int64, h2_diff int64, Comments_after int64, McCabe_sum_before int64, McCabe_max_after int64, high_McCabe_max_diff int64, added_functions int64, SLOC_diff int64, avg_coupling_code_size_cut_diff int64, too-many-nested-blocks int64, changed_lines int64, high_McCabe_sum_before int64, prev_count int64, high_McCabe_sum_diff int64, vocabulary_diff int64, SLOC_before int64, LOC_diff int64, low_McCabe_max_diff int64, Single comments_before int64, one_file_fix_rate_diff int64, too-many-statements int64, added_lines int64, new_function int64, massive_change int64, LLOC_before int64, calculated_length_diff int64, Single comments_diff int64, modified_McCabe_max_diff int64, McCabe_max_before int64, LLOC_diff int64, refactor_mle_diff int64, low_McCabe_sum_diff int64, hunks_num int64, low_McCabe_max_before int64, too-many-return-statements int64, only_removal int64, same_day_duration_avg_diff int64, h1_diff int64, time_diff int64, prev_count_y int64, effort_diff int64, Multi_diff int64, Blank_diff int64, cur_count int64, volume_diff int64, high_McCabe_max_before int64, Single comments_after int64, McCabe_max_diff int64) as (
  case when Comments_after <= 7.5 then
     return 0.8571428571428571 # (0.8571428571428571 out of 1.0)
  else  # if Comments_after > 7.5
    case when Multi_diff <= -3.5 then
      case when low_McCabe_sum_diff <= 0.5 then
         return 0.75 # (0.75 out of 1.0)
      else  # if low_McCabe_sum_diff > 0.5
         return 0.4482758620689655 # (0.4482758620689655 out of 1.0)
      end     else  # if Multi_diff > -3.5
      case when h2_diff <= -15.5 then
         return 0.037037037037037035 # (0.037037037037037035 out of 1.0)
      else  # if h2_diff > -15.5
        case when low_McCabe_max_before <= 0.5 then
          case when refactor_mle_diff <= -0.1839260309934616 then
             return 0.7 # (0.7 out of 1.0)
          else  # if refactor_mle_diff > -0.1839260309934616
            case when prev_count <= 1.5 then
              case when Single comments_after <= 30.5 then
                 return 0.5625 # (0.5625 out of 1.0)
              else  # if Single comments_after > 30.5
                case when h2_diff <= -0.5 then
                   return 0.36363636363636365 # (0.36363636363636365 out of 1.0)
                else  # if h2_diff > -0.5
                   return 0.038461538461538464 # (0.038461538461538464 out of 1.0)
                end               end             else  # if prev_count > 1.5
               return 0.05263157894736842 # (0.05263157894736842 out of 1.0)
            end           end         else  # if low_McCabe_max_before > 0.5
          case when LLOC_before <= 356.0 then
             return 0.6 # (0.6 out of 1.0)
          else  # if LLOC_before > 356.0
             return 0.8125 # (0.8125 out of 1.0)
          end         end       end     end   end )