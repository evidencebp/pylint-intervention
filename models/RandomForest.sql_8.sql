create or replace function RandomForest_8 (length_diff int64, N1_diff int64, N2_diff int64, McCabe_sum_diff int64, bugs_diff int64, McCabe_sum_after int64, too-many-branches int64, is_refactor int64, high_ccp_group int64, mostly_delete int64, cur_count_y int64, low_ccp_group int64, prev_count_x int64, difficulty_diff int64, removed_lines int64, Blank_before int64, LOC_before int64, low_McCabe_sum_before int64, cur_count_x int64, Comments_diff int64, Comments_before int64, h2_diff int64, Comments_after int64, McCabe_sum_before int64, McCabe_max_after int64, high_McCabe_max_diff int64, added_functions int64, SLOC_diff int64, avg_coupling_code_size_cut_diff int64, too-many-nested-blocks int64, changed_lines int64, high_McCabe_sum_before int64, prev_count int64, high_McCabe_sum_diff int64, vocabulary_diff int64, SLOC_before int64, LOC_diff int64, low_McCabe_max_diff int64, Single comments_before int64, one_file_fix_rate_diff int64, too-many-statements int64, added_lines int64, new_function int64, massive_change int64, LLOC_before int64, calculated_length_diff int64, Single comments_diff int64, modified_McCabe_max_diff int64, McCabe_max_before int64, LLOC_diff int64, refactor_mle_diff int64, low_McCabe_sum_diff int64, hunks_num int64, low_McCabe_max_before int64, too-many-return-statements int64, only_removal int64, same_day_duration_avg_diff int64, h1_diff int64, time_diff int64, prev_count_y int64, effort_diff int64, Multi_diff int64, Blank_diff int64, cur_count int64, volume_diff int64, high_McCabe_max_before int64, Single comments_after int64, McCabe_max_diff int64) as (
  case when McCabe_sum_after <= 279.0 then
    case when LLOC_before <= 527.5 then
      case when McCabe_max_after <= 6.5 then
         return 0.84 # (0.84 out of 1.0)
      else  # if McCabe_max_after > 6.5
        case when low_ccp_group <= 0.5 then
          case when added_lines <= 5.5 then
             return 0.17391304347826086 # (0.17391304347826086 out of 1.0)
          else  # if added_lines > 5.5
            case when SLOC_diff <= -63.5 then
               return 0.19047619047619047 # (0.19047619047619047 out of 1.0)
            else  # if SLOC_diff > -63.5
              case when McCabe_max_diff <= -1.0 then
                case when LOC_diff <= 5.0 then
                   return 0.90625 # (0.90625 out of 1.0)
                else  # if LOC_diff > 5.0
                   return 0.6363636363636364 # (0.6363636363636364 out of 1.0)
                end               else  # if McCabe_max_diff > -1.0
                 return 0.47619047619047616 # (0.47619047619047616 out of 1.0)
              end             end           end         else  # if low_ccp_group > 0.5
          case when Comments_after <= 54.5 then
             return 0.0 # (0.0 out of 1.0)
          else  # if Comments_after > 54.5
             return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
          end         end       end     else  # if LLOC_before > 527.5
      case when new_function <= 0.5 then
         return 0.6190476190476191 # (0.6190476190476191 out of 1.0)
      else  # if new_function > 0.5
         return 0.84 # (0.84 out of 1.0)
      end     end   else  # if McCabe_sum_after > 279.0
     return 0.07142857142857142 # (0.07142857142857142 out of 1.0)
  end )