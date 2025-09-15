create or replace function RandomForest_2 (N1_diff int64, Single comments_diff int64, h2_diff int64, new_function int64, added_lines int64, difficulty_diff int64, too-many-return-statements int64, effort_diff int64, length_diff int64, McCabe_sum_after int64, removed_lines int64, McCabe_sum_before int64, low_McCabe_sum_before int64, high_McCabe_max_diff int64, prev_count_x int64, prev_count int64, LOC_before int64, SLOC_diff int64, low_McCabe_sum_diff int64, cur_count int64, calculated_length_diff int64, Blank_before int64, Comments_after int64, bugs_diff int64, too-many-statements int64, volume_diff int64, only_removal int64, too-many-branches int64, low_McCabe_max_diff int64, low_McCabe_max_before int64, McCabe_max_diff int64, is_refactor int64, cur_count_x int64, Single comments_before int64, McCabe_max_after int64, Blank_diff int64, McCabe_max_before int64, added_functions int64, Multi_diff int64, SLOC_before int64, prev_count_y int64, massive_change int64, LOC_diff int64, time_diff int64, h1_diff int64, vocabulary_diff int64, LLOC_diff int64, high_ccp_group int64, hunks_num int64, Single comments_after int64, high_McCabe_sum_before int64, modified_McCabe_max_diff int64, N2_diff int64, same_day_duration_avg_diff int64, low_ccp_group int64, Comments_before int64, cur_count_y int64, high_McCabe_sum_diff int64, changed_lines int64, high_McCabe_max_before int64, Comments_diff int64, LLOC_before int64, one_file_fix_rate_diff int64, too-many-nested-blocks int64, McCabe_sum_diff int64, refactor_mle_diff int64, avg_coupling_code_size_cut_diff int64, mostly_delete int64) as (
  case when hunks_num <= 12.0 then
    case when Comments_after <= 6.5 then
       return 0.8 # (0.8 out of 1.0)
    else  # if Comments_after > 6.5
      case when Comments_diff <= -0.5 then
        case when McCabe_max_before <= 20.0 then
          case when low_ccp_group <= 0.5 then
             return 0.9259259259259259 # (0.9259259259259259 out of 1.0)
          else  # if low_ccp_group > 0.5
             return 0.5384615384615384 # (0.5384615384615384 out of 1.0)
          end         else  # if McCabe_max_before > 20.0
          case when changed_lines <= 239.5 then
             return 0.09523809523809523 # (0.09523809523809523 out of 1.0)
          else  # if changed_lines > 239.5
             return 0.5384615384615384 # (0.5384615384615384 out of 1.0)
          end         end       else  # if Comments_diff > -0.5
        case when N1_diff <= 0.5 then
          case when McCabe_sum_after <= 176.5 then
            case when Blank_diff <= -0.5 then
               return 0.3157894736842105 # (0.3157894736842105 out of 1.0)
            else  # if Blank_diff > -0.5
              case when Blank_before <= 53.5 then
                 return 0.3076923076923077 # (0.3076923076923077 out of 1.0)
              else  # if Blank_before > 53.5
                 return 0.06060606060606061 # (0.06060606060606061 out of 1.0)
              end             end           else  # if McCabe_sum_after > 176.5
             return 0.47058823529411764 # (0.47058823529411764 out of 1.0)
          end         else  # if N1_diff > 0.5
           return 0.6428571428571429 # (0.6428571428571429 out of 1.0)
        end       end     end   else  # if hunks_num > 12.0
    case when N1_diff <= -16.0 then
       return 0.29411764705882354 # (0.29411764705882354 out of 1.0)
    else  # if N1_diff > -16.0
       return 0.045454545454545456 # (0.045454545454545456 out of 1.0)
    end   end )