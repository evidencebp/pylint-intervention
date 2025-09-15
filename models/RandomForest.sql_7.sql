create or replace function RandomForest_7 (same_day_duration_avg_diff int64, low_McCabe_max_before int64, Single comments_before int64, one_file_fix_rate_diff int64, length_diff int64, Comments_after int64, Single comments_diff int64, too-many-statements int64, cur_count int64, Comments_diff int64, bugs_diff int64, McCabe_max_after int64, h2_diff int64, low_ccp_group int64, changed_lines int64, high_McCabe_sum_before int64, volume_diff int64, Multi_diff int64, LLOC_before int64, high_McCabe_max_diff int64, hunks_num int64, LOC_before int64, calculated_length_diff int64, low_McCabe_sum_before int64, McCabe_sum_before int64, high_ccp_group int64, McCabe_max_before int64, mostly_delete int64, LLOC_diff int64, effort_diff int64, too-many-nested-blocks int64, cur_count_y int64, h1_diff int64, low_McCabe_max_diff int64, Single comments_after int64, massive_change int64, SLOC_diff int64, added_lines int64, prev_count_x int64, N2_diff int64, high_McCabe_sum_diff int64, Blank_diff int64, LOC_diff int64, new_function int64, prev_count int64, prev_count_y int64, SLOC_before int64, McCabe_sum_after int64, high_McCabe_max_before int64, avg_coupling_code_size_cut_diff int64, Blank_before int64, McCabe_max_diff int64, refactor_mle_diff int64, is_refactor int64, low_McCabe_sum_diff int64, added_functions int64, modified_McCabe_max_diff int64, too-many-branches int64, time_diff int64, only_removal int64, N1_diff int64, Comments_before int64, McCabe_sum_diff int64, vocabulary_diff int64, removed_lines int64, too-many-return-statements int64, difficulty_diff int64, cur_count_x int64) as (
  case when Single comments_after <= 35.5 then
    case when McCabe_sum_after <= 85.5 then
      case when Single comments_after <= 21.5 then
        case when avg_coupling_code_size_cut_diff <= -0.4375 then
           return 0.8125 # (0.8125 out of 1.0)
        else  # if avg_coupling_code_size_cut_diff > -0.4375
           return 0.4 # (0.4 out of 1.0)
        end       else  # if Single comments_after > 21.5
        case when McCabe_sum_before <= 47.0 then
           return 0.75 # (0.75 out of 1.0)
        else  # if McCabe_sum_before > 47.0
           return 0.8947368421052632 # (0.8947368421052632 out of 1.0)
        end       end     else  # if McCabe_sum_after > 85.5
      case when Comments_after <= 18.5 then
         return 0.125 # (0.125 out of 1.0)
      else  # if Comments_after > 18.5
         return 0.4166666666666667 # (0.4166666666666667 out of 1.0)
      end     end   else  # if Single comments_after > 35.5
    case when McCabe_sum_diff <= 0.5 then
      case when SLOC_before <= 724.5 then
        case when LOC_before <= 777.5 then
           return 0.23809523809523808 # (0.23809523809523808 out of 1.0)
        else  # if LOC_before > 777.5
          case when avg_coupling_code_size_cut_diff <= -0.5163888931274414 then
             return 0.2 # (0.2 out of 1.0)
          else  # if avg_coupling_code_size_cut_diff > -0.5163888931274414
             return 0.0 # (0.0 out of 1.0)
          end         end       else  # if SLOC_before > 724.5
        case when McCabe_sum_after <= 235.0 then
           return 0.6153846153846154 # (0.6153846153846154 out of 1.0)
        else  # if McCabe_sum_after > 235.0
           return 0.2 # (0.2 out of 1.0)
        end       end     else  # if McCabe_sum_diff > 0.5
       return 0.5384615384615384 # (0.5384615384615384 out of 1.0)
    end   end )