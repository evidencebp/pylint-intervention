create or replace function RandomForest_2 (is_refactor int64, McCabe_max_before int64, N1_diff int64, high_McCabe_sum_before int64, same_day_duration_avg_diff int64, Comments_before int64, hunks_num int64, added_lines int64, prev_count int64, low_McCabe_max_before int64, high_McCabe_max_diff int64, vocabulary_diff int64, modified_McCabe_max_diff int64, avg_coupling_code_size_cut_diff int64, too-many-nested-blocks int64, low_McCabe_max_diff int64, changed_lines int64, effort_diff int64, removed_lines int64, Blank_before int64, SLOC_diff int64, length_diff int64, low_ccp_group int64, calculated_length_diff int64, McCabe_max_diff int64, McCabe_max_after int64, LOC_diff int64, too-many-return-statements int64, Single comments_after int64, McCabe_sum_diff int64, LLOC_diff int64, too-many-statements int64, Comments_after int64, low_McCabe_sum_diff int64, McCabe_sum_before int64, difficulty_diff int64, Single comments_before int64, massive_change int64, prev_count_x int64, refactor_mle_diff int64, cur_count_y int64, N2_diff int64, prev_count_y int64, Single comments_diff int64, cur_count int64, high_McCabe_max_before int64, one_file_fix_rate_diff int64, h1_diff int64, low_McCabe_sum_before int64, time_diff int64, LOC_before int64, SLOC_before int64, too-many-branches int64, volume_diff int64, McCabe_sum_after int64, mostly_delete int64, Multi_diff int64, high_McCabe_sum_diff int64, Blank_diff int64, bugs_diff int64, h2_diff int64, cur_count_x int64, added_functions int64, LLOC_before int64, high_ccp_group int64, Comments_diff int64, only_removal int64) as (
  case when high_ccp_group <= 0.5 then
    case when N1_diff <= -1.5 then
      case when Comments_after <= 39.5 then
        case when h2_diff <= -22.5 then
           return 0.7142857142857143 # (0.7142857142857143 out of 1.0)
        else  # if h2_diff > -22.5
           return 0.4444444444444444 # (0.4444444444444444 out of 1.0)
        end       else  # if Comments_after > 39.5
        case when avg_coupling_code_size_cut_diff <= 0.43809525668621063 then
           return 0.64 # (0.64 out of 1.0)
        else  # if avg_coupling_code_size_cut_diff > 0.43809525668621063
           return 0.1 # (0.1 out of 1.0)
        end       end     else  # if N1_diff > -1.5
      case when hunks_num <= 2.5 then
         return 0.3235294117647059 # (0.3235294117647059 out of 1.0)
      else  # if hunks_num > 2.5
        case when same_day_duration_avg_diff <= -19.76388931274414 then
           return 0.27586206896551724 # (0.27586206896551724 out of 1.0)
        else  # if same_day_duration_avg_diff > -19.76388931274414
          case when Single comments_after <= 14.0 then
             return 0.21428571428571427 # (0.21428571428571427 out of 1.0)
          else  # if Single comments_after > 14.0
             return 0.041666666666666664 # (0.041666666666666664 out of 1.0)
          end         end       end     end   else  # if high_ccp_group > 0.5
    case when LOC_before <= 904.0 then
      case when refactor_mle_diff <= -0.09760291501879692 then
         return 0.875 # (0.875 out of 1.0)
      else  # if refactor_mle_diff > -0.09760291501879692
         return 0.9411764705882353 # (0.9411764705882353 out of 1.0)
      end     else  # if LOC_before > 904.0
       return 0.2777777777777778 # (0.2777777777777778 out of 1.0)
    end   end )