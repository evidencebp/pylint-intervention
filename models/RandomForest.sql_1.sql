create or replace function RandomForest_1 (hunks_num int64, McCabe_sum_after int64, added_lines int64, cur_count_y int64, changed_lines int64, N1_diff int64, added_functions int64, Single comments_before int64, McCabe_max_after int64, calculated_length_diff int64, h1_diff int64, difficulty_diff int64, too-many-nested-blocks int64, modified_McCabe_max_diff int64, removed_lines int64, prev_count int64, Blank_diff int64, prev_count_x int64, h2_diff int64, LLOC_before int64, Multi_diff int64, volume_diff int64, same_day_duration_avg_diff int64, N2_diff int64, one_file_fix_rate_diff int64, Comments_after int64, massive_change int64, Single comments_diff int64, Comments_before int64, SLOC_before int64, prev_count_y int64, vocabulary_diff int64, LOC_before int64, McCabe_sum_diff int64, high_ccp_group int64, McCabe_sum_before int64, is_refactor int64, cur_count_x int64, refactor_mle_diff int64, time_diff int64, bugs_diff int64, avg_coupling_code_size_cut_diff int64, LLOC_diff int64, Single comments_after int64, too-many-branches int64, McCabe_max_diff int64, too-many-statements int64, mostly_delete int64, effort_diff int64, length_diff int64, Blank_before int64, SLOC_diff int64, McCabe_max_before int64, LOC_diff int64, cur_count int64, too-many-return-statements int64, only_removal int64, Comments_diff int64) as (
  case when refactor_mle_diff <= 0.4425845444202423 then
    case when Comments_after <= 6.5 then
       return 0.8928571428571429 # (25.0 out of 28.0)
    else  # if Comments_after > 6.5
      case when vocabulary_diff <= -53.5 then
         return 0.72 # (18.0 out of 25.0)
      else  # if vocabulary_diff > -53.5
        case when LOC_diff <= 18.5 then
          case when LOC_before <= 423.5 then
            case when McCabe_sum_after <= 30.5 then
               return 0.2 # (3.0 out of 15.0)
            else  # if McCabe_sum_after > 30.5
               return 0.7058823529411765 # (12.0 out of 17.0)
            end           else  # if LOC_before > 423.5
            case when one_file_fix_rate_diff <= -0.24444445222616196 then
               return 0.0 # (0.0 out of 23.0)
            else  # if one_file_fix_rate_diff > -0.24444445222616196
              case when N2_diff <= -6.5 then
                 return 0.5217391304347826 # (12.0 out of 23.0)
              else  # if N2_diff > -6.5
                case when changed_lines <= 39.0 then
                  case when McCabe_sum_after <= 158.5 then
                     return 0.0 # (0.0 out of 15.0)
                  else  # if McCabe_sum_after > 158.5
                     return 0.3333333333333333 # (5.0 out of 15.0)
                  end                 else  # if changed_lines > 39.0
                   return 0.0 # (0.0 out of 26.0)
                end               end             end           end         else  # if LOC_diff > 18.5
           return 0.7142857142857143 # (15.0 out of 21.0)
        end       end     end   else  # if refactor_mle_diff > 0.4425845444202423
     return 0.7619047619047619 # (16.0 out of 21.0)
  end )