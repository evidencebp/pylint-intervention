create or replace function Tree_ms50 (same_day_duration_avg_diff int64, low_McCabe_max_before int64, Single comments_before int64, one_file_fix_rate_diff int64, length_diff int64, Comments_after int64, Single comments_diff int64, too-many-statements int64, cur_count int64, Comments_diff int64, bugs_diff int64, McCabe_max_after int64, h2_diff int64, low_ccp_group int64, changed_lines int64, high_McCabe_sum_before int64, volume_diff int64, Multi_diff int64, LLOC_before int64, high_McCabe_max_diff int64, hunks_num int64, LOC_before int64, calculated_length_diff int64, low_McCabe_sum_before int64, McCabe_sum_before int64, high_ccp_group int64, McCabe_max_before int64, mostly_delete int64, LLOC_diff int64, effort_diff int64, too-many-nested-blocks int64, cur_count_y int64, h1_diff int64, low_McCabe_max_diff int64, Single comments_after int64, massive_change int64, SLOC_diff int64, added_lines int64, prev_count_x int64, N2_diff int64, high_McCabe_sum_diff int64, Blank_diff int64, LOC_diff int64, new_function int64, prev_count int64, prev_count_y int64, SLOC_before int64, McCabe_sum_after int64, high_McCabe_max_before int64, avg_coupling_code_size_cut_diff int64, Blank_before int64, McCabe_max_diff int64, refactor_mle_diff int64, is_refactor int64, low_McCabe_sum_diff int64, added_functions int64, modified_McCabe_max_diff int64, too-many-branches int64, time_diff int64, only_removal int64, N1_diff int64, Comments_before int64, McCabe_sum_diff int64, vocabulary_diff int64, removed_lines int64, too-many-return-statements int64, difficulty_diff int64, cur_count_x int64) as (
  case when low_ccp_group <= 0.5 then
    case when Blank_before <= 53.5 then
      case when low_McCabe_max_before <= 0.5 then
        case when Comments_after <= 28.5 then
           return 1.0 # (1.0 out of 1.0)
        else  # if Comments_after > 28.5
           return 0.9 # (0.9 out of 1.0)
        end       else  # if low_McCabe_max_before > 0.5
         return 0.5454545454545454 # (0.5454545454545454 out of 1.0)
      end     else  # if Blank_before > 53.5
      case when same_day_duration_avg_diff <= -103.56983184814453 then
         return 0.9166666666666666 # (0.9166666666666666 out of 1.0)
      else  # if same_day_duration_avg_diff > -103.56983184814453
        case when Single comments_before <= 114.5 then
          case when Blank_before <= 87.5 then
            case when McCabe_max_after <= 21.0 then
               return 0.0 # (0.0 out of 1.0)
            else  # if McCabe_max_after > 21.0
               return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
            end           else  # if Blank_before > 87.5
            case when McCabe_max_after <= 17.5 then
              case when McCabe_sum_after <= 78.5 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if McCabe_sum_after > 78.5
                 return 0.625 # (0.625 out of 1.0)
              end             else  # if McCabe_max_after > 17.5
              case when high_ccp_group <= 0.5 then
                 return 0.125 # (0.125 out of 1.0)
              else  # if high_ccp_group > 0.5
                 return 0.6 # (0.6 out of 1.0)
              end             end           end         else  # if Single comments_before > 114.5
          case when Blank_before <= 305.0 then
             return 0.2 # (0.2 out of 1.0)
          else  # if Blank_before > 305.0
             return 0.0 # (0.0 out of 1.0)
          end         end       end     end   else  # if low_ccp_group > 0.5
    case when N1_diff <= -13.5 then
       return 0.7 # (0.7 out of 1.0)
    else  # if N1_diff > -13.5
      case when SLOC_before <= 674.5 then
        case when avg_coupling_code_size_cut_diff <= 0.16153846681118034 then
           return 0.0 # (0.0 out of 1.0)
        else  # if avg_coupling_code_size_cut_diff > 0.16153846681118034
           return 0.1 # (0.1 out of 1.0)
        end       else  # if SLOC_before > 674.5
         return 0.42857142857142855 # (0.42857142857142855 out of 1.0)
      end     end   end )