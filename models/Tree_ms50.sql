create or replace function Tree_ms50 (Blank_diff int64, bugs_diff int64, hunks_num int64, low_McCabe_sum_before int64, low_McCabe_max_diff int64, effort_diff int64, McCabe_max_diff int64, McCabe_sum_diff int64, Comments_before int64, massive_change int64, too-many-branches int64, low_McCabe_sum_diff int64, Blank_before int64, McCabe_sum_after int64, high_ccp_group int64, high_McCabe_sum_before int64, too-many-return-statements int64, cur_count_y int64, Comments_diff int64, Multi_diff int64, refactor_mle_diff int64, cur_count int64, new_function int64, added_lines int64, Comments_after int64, Single comments_diff int64, McCabe_max_before int64, LOC_before int64, SLOC_before int64, modified_McCabe_max_diff int64, h2_diff int64, too-many-statements int64, Single comments_after int64, high_McCabe_max_diff int64, vocabulary_diff int64, prev_count_y int64, LOC_diff int64, too-many-nested-blocks int64, N1_diff int64, changed_lines int64, calculated_length_diff int64, difficulty_diff int64, mostly_delete int64, low_ccp_group int64, McCabe_max_after int64, cur_count_x int64, length_diff int64, only_removal int64, avg_coupling_code_size_cut_diff int64, prev_count_x int64, one_file_fix_rate_diff int64, high_McCabe_max_before int64, Single comments_before int64, SLOC_diff int64, time_diff int64, low_McCabe_max_before int64, added_functions int64, N2_diff int64, high_McCabe_sum_diff int64, is_refactor int64, volume_diff int64, LLOC_diff int64, same_day_duration_avg_diff int64, LLOC_before int64, prev_count int64, McCabe_sum_before int64, removed_lines int64, h1_diff int64) as (
  case when Blank_before <= 42.5 then
    case when low_ccp_group <= 0.5 then
       return 1.0 # (1.0 out of 1.0)
    else  # if low_ccp_group > 0.5
       return 0.75 # (0.75 out of 1.0)
    end   else  # if Blank_before > 42.5
    case when McCabe_sum_before <= 40.5 then
       return 0.0 # (0.0 out of 1.0)
    else  # if McCabe_sum_before > 40.5
      case when Blank_diff <= -1.5 then
        case when avg_coupling_code_size_cut_diff <= 0.5208333432674408 then
          case when refactor_mle_diff <= -0.2706191688776016 then
             return 0.6 # (0.6 out of 1.0)
          else  # if refactor_mle_diff > -0.2706191688776016
            case when McCabe_sum_after <= 121.5 then
              case when h2_diff <= -5.5 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if h2_diff > -5.5
                 return 0.9642857142857143 # (0.9642857142857143 out of 1.0)
              end             else  # if McCabe_sum_after > 121.5
              case when Blank_before <= 207.5 then
                 return 0.5625 # (0.5625 out of 1.0)
              else  # if Blank_before > 207.5
                 return 0.9545454545454546 # (0.9545454545454546 out of 1.0)
              end             end           end         else  # if avg_coupling_code_size_cut_diff > 0.5208333432674408
          case when length_diff <= -56.0 then
             return 0.0 # (0.0 out of 1.0)
          else  # if length_diff > -56.0
             return 0.75 # (0.75 out of 1.0)
          end         end       else  # if Blank_diff > -1.5
        case when refactor_mle_diff <= -0.1971895471215248 then
           return 0.8108108108108109 # (0.8108108108108109 out of 1.0)
        else  # if refactor_mle_diff > -0.1971895471215248
          case when LOC_before <= 432.0 then
             return 0.8181818181818182 # (0.8181818181818182 out of 1.0)
          else  # if LOC_before > 432.0
            case when high_ccp_group <= 0.5 then
              case when Single comments_diff <= 0.5 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if Single comments_diff > 0.5
                 return 0.4 # (0.4 out of 1.0)
              end             else  # if high_ccp_group > 0.5
              case when McCabe_max_after <= 25.5 then
                 return 0.8181818181818182 # (0.8181818181818182 out of 1.0)
              else  # if McCabe_max_after > 25.5
                 return 0.25 # (0.25 out of 1.0)
              end             end           end         end       end     end   end )