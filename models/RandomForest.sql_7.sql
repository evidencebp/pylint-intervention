create or replace function RandomForest_7 (hunks_num int64, McCabe_sum_after int64, added_lines int64, cur_count_y int64, changed_lines int64, N1_diff int64, added_functions int64, Single comments_before int64, McCabe_max_after int64, calculated_length_diff int64, h1_diff int64, difficulty_diff int64, too-many-nested-blocks int64, modified_McCabe_max_diff int64, removed_lines int64, prev_count int64, Blank_diff int64, prev_count_x int64, h2_diff int64, LLOC_before int64, Multi_diff int64, volume_diff int64, same_day_duration_avg_diff int64, N2_diff int64, one_file_fix_rate_diff int64, Comments_after int64, massive_change int64, Single comments_diff int64, Comments_before int64, SLOC_before int64, prev_count_y int64, vocabulary_diff int64, LOC_before int64, McCabe_sum_diff int64, high_ccp_group int64, McCabe_sum_before int64, is_refactor int64, cur_count_x int64, refactor_mle_diff int64, time_diff int64, bugs_diff int64, avg_coupling_code_size_cut_diff int64, LLOC_diff int64, Single comments_after int64, too-many-branches int64, McCabe_max_diff int64, too-many-statements int64, mostly_delete int64, effort_diff int64, length_diff int64, Blank_before int64, SLOC_diff int64, McCabe_max_before int64, LOC_diff int64, cur_count int64, too-many-return-statements int64, only_removal int64, Comments_diff int64) as (
  case when hunks_num <= 11.5 then
    case when McCabe_max_before <= 20.5 then
      case when added_functions <= 1.5 then
        case when Single comments_after <= 15.5 then
           return 0.07407407407407407 # (2.0 out of 27.0)
        else  # if Single comments_after > 15.5
          case when LLOC_before <= 496.5 then
            case when Comments_before <= 58.0 then
              case when LLOC_diff <= -6.5 then
                 return 0.7857142857142857 # (11.0 out of 14.0)
              else  # if LLOC_diff > -6.5
                 return 0.5555555555555556 # (10.0 out of 18.0)
              end             else  # if Comments_before > 58.0
               return 1.0 # (17.0 out of 17.0)
            end           else  # if LLOC_before > 496.5
             return 0.2777777777777778 # (5.0 out of 18.0)
          end         end       else  # if added_functions > 1.5
         return 0.9473684210526315 # (18.0 out of 19.0)
      end     else  # if McCabe_max_before > 20.5
      case when length_diff <= -8.5 then
        case when removed_lines <= 8.0 then
           return 0.3333333333333333 # (5.0 out of 15.0)
        else  # if removed_lines > 8.0
           return 0.7647058823529411 # (13.0 out of 17.0)
        end       else  # if length_diff > -8.5
         return 0.11627906976744186 # (5.0 out of 43.0)
      end     end   else  # if hunks_num > 11.5
     return 0.0 # (0.0 out of 41.0)
  end )