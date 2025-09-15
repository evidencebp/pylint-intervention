create or replace function RandomForest_1 (same_day_duration_avg_diff int64, low_McCabe_max_before int64, Single comments_before int64, one_file_fix_rate_diff int64, length_diff int64, Comments_after int64, Single comments_diff int64, too-many-statements int64, cur_count int64, Comments_diff int64, bugs_diff int64, McCabe_max_after int64, h2_diff int64, low_ccp_group int64, changed_lines int64, high_McCabe_sum_before int64, volume_diff int64, Multi_diff int64, LLOC_before int64, high_McCabe_max_diff int64, hunks_num int64, LOC_before int64, calculated_length_diff int64, low_McCabe_sum_before int64, McCabe_sum_before int64, high_ccp_group int64, McCabe_max_before int64, mostly_delete int64, LLOC_diff int64, effort_diff int64, too-many-nested-blocks int64, cur_count_y int64, h1_diff int64, low_McCabe_max_diff int64, Single comments_after int64, massive_change int64, SLOC_diff int64, added_lines int64, prev_count_x int64, N2_diff int64, high_McCabe_sum_diff int64, Blank_diff int64, LOC_diff int64, new_function int64, prev_count int64, prev_count_y int64, SLOC_before int64, McCabe_sum_after int64, high_McCabe_max_before int64, avg_coupling_code_size_cut_diff int64, Blank_before int64, McCabe_max_diff int64, refactor_mle_diff int64, is_refactor int64, low_McCabe_sum_diff int64, added_functions int64, modified_McCabe_max_diff int64, too-many-branches int64, time_diff int64, only_removal int64, N1_diff int64, Comments_before int64, McCabe_sum_diff int64, vocabulary_diff int64, removed_lines int64, too-many-return-statements int64, difficulty_diff int64, cur_count_x int64) as (
  case when Comments_diff <= -21.0 then
     return 0.8181818181818182 # (0.8181818181818182 out of 1.0)
  else  # if Comments_diff > -21.0
    case when Blank_diff <= 5.5 then
      case when avg_coupling_code_size_cut_diff <= -1.1835317611694336 then
        case when hunks_num <= 3.5 then
           return 0.2727272727272727 # (0.2727272727272727 out of 1.0)
        else  # if hunks_num > 3.5
           return 0.038461538461538464 # (0.038461538461538464 out of 1.0)
        end       else  # if avg_coupling_code_size_cut_diff > -1.1835317611694336
        case when Comments_after <= 38.0 then
          case when h2_diff <= -26.0 then
             return 0.2777777777777778 # (0.2777777777777778 out of 1.0)
          else  # if h2_diff > -26.0
            case when McCabe_max_diff <= -0.5 then
               return 0.38095238095238093 # (0.38095238095238093 out of 1.0)
            else  # if McCabe_max_diff > -0.5
              case when avg_coupling_code_size_cut_diff <= 0.5458333343267441 then
                 return 0.8888888888888888 # (0.8888888888888888 out of 1.0)
              else  # if avg_coupling_code_size_cut_diff > 0.5458333343267441
                 return 0.46153846153846156 # (0.46153846153846156 out of 1.0)
              end             end           end         else  # if Comments_after > 38.0
          case when modified_McCabe_max_diff <= -4.5 then
             return 0.0 # (0.0 out of 1.0)
          else  # if modified_McCabe_max_diff > -4.5
            case when McCabe_sum_after <= 171.0 then
              case when McCabe_sum_before <= 98.5 then
                 return 0.375 # (0.375 out of 1.0)
              else  # if McCabe_sum_before > 98.5
                 return 0.15 # (0.15 out of 1.0)
              end             else  # if McCabe_sum_after > 171.0
               return 0.55 # (0.55 out of 1.0)
            end           end         end       end     else  # if Blank_diff > 5.5
       return 0.75 # (0.75 out of 1.0)
    end   end )