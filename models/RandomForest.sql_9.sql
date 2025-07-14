create or replace function RandomForest_9 (hunks_num int64, McCabe_sum_after int64, added_lines int64, cur_count_y int64, changed_lines int64, N1_diff int64, added_functions int64, Single comments_before int64, McCabe_max_after int64, calculated_length_diff int64, h1_diff int64, difficulty_diff int64, too-many-nested-blocks int64, modified_McCabe_max_diff int64, removed_lines int64, prev_count int64, Blank_diff int64, prev_count_x int64, h2_diff int64, LLOC_before int64, Multi_diff int64, volume_diff int64, same_day_duration_avg_diff int64, N2_diff int64, one_file_fix_rate_diff int64, Comments_after int64, massive_change int64, Single comments_diff int64, Comments_before int64, SLOC_before int64, prev_count_y int64, vocabulary_diff int64, LOC_before int64, McCabe_sum_diff int64, high_ccp_group int64, McCabe_sum_before int64, is_refactor int64, cur_count_x int64, refactor_mle_diff int64, time_diff int64, bugs_diff int64, avg_coupling_code_size_cut_diff int64, LLOC_diff int64, Single comments_after int64, too-many-branches int64, McCabe_max_diff int64, too-many-statements int64, mostly_delete int64, effort_diff int64, length_diff int64, Blank_before int64, SLOC_diff int64, McCabe_max_before int64, LOC_diff int64, cur_count int64, too-many-return-statements int64, only_removal int64, Comments_diff int64) as (
  case when McCabe_sum_diff <= -24.5 then
     return 0.7222222222222222 # (26.0 out of 36.0)
  else  # if McCabe_sum_diff > -24.5
    case when added_lines <= 94.5 then
      case when hunks_num <= 11.5 then
        case when added_lines <= 67.5 then
          case when h2_diff <= 1.5 then
            case when refactor_mle_diff <= -0.10830256342887878 then
               return 0.15384615384615385 # (4.0 out of 26.0)
            else  # if refactor_mle_diff > -0.10830256342887878
              case when refactor_mle_diff <= 0.006461769342422485 then
                 return 0.8235294117647058 # (28.0 out of 34.0)
              else  # if refactor_mle_diff > 0.006461769342422485
                case when McCabe_max_after <= 16.5 then
                   return 0.13333333333333333 # (2.0 out of 15.0)
                else  # if McCabe_max_after > 16.5
                   return 0.6 # (15.0 out of 25.0)
                end               end             end           else  # if h2_diff > 1.5
             return 0.13636363636363635 # (3.0 out of 22.0)
          end         else  # if added_lines > 67.5
           return 0.8333333333333334 # (15.0 out of 18.0)
        end       else  # if hunks_num > 11.5
         return 0.05555555555555555 # (1.0 out of 18.0)
      end     else  # if added_lines > 94.5
      case when length_diff <= -27.5 then
         return 0.3076923076923077 # (4.0 out of 13.0)
      else  # if length_diff > -27.5
         return 0.045454545454545456 # (1.0 out of 22.0)
      end     end   end )