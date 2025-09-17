create or replace function RandomForest_4 (length_diff int64, N1_diff int64, N2_diff int64, McCabe_sum_diff int64, bugs_diff int64, McCabe_sum_after int64, too-many-branches int64, is_refactor int64, high_ccp_group int64, mostly_delete int64, cur_count_y int64, low_ccp_group int64, prev_count_x int64, difficulty_diff int64, removed_lines int64, Blank_before int64, LOC_before int64, low_McCabe_sum_before int64, cur_count_x int64, Comments_diff int64, Comments_before int64, h2_diff int64, Comments_after int64, McCabe_sum_before int64, McCabe_max_after int64, high_McCabe_max_diff int64, added_functions int64, SLOC_diff int64, avg_coupling_code_size_cut_diff int64, too-many-nested-blocks int64, changed_lines int64, high_McCabe_sum_before int64, prev_count int64, high_McCabe_sum_diff int64, vocabulary_diff int64, SLOC_before int64, LOC_diff int64, low_McCabe_max_diff int64, Single comments_before int64, one_file_fix_rate_diff int64, too-many-statements int64, added_lines int64, new_function int64, massive_change int64, LLOC_before int64, calculated_length_diff int64, Single comments_diff int64, modified_McCabe_max_diff int64, McCabe_max_before int64, LLOC_diff int64, refactor_mle_diff int64, low_McCabe_sum_diff int64, hunks_num int64, low_McCabe_max_before int64, too-many-return-statements int64, only_removal int64, same_day_duration_avg_diff int64, h1_diff int64, time_diff int64, prev_count_y int64, effort_diff int64, Multi_diff int64, Blank_diff int64, cur_count int64, volume_diff int64, high_McCabe_max_before int64, Single comments_after int64, McCabe_max_diff int64) as (
  case when removed_lines <= 70.5 then
    case when LLOC_before <= 397.0 then
      case when SLOC_diff <= 0.5 then
        case when Comments_before <= 30.5 then
          case when N1_diff <= -0.5 then
             return 0.16666666666666666 # (0.16666666666666666 out of 1.0)
          else  # if N1_diff > -0.5
             return 0.7142857142857143 # (0.7142857142857143 out of 1.0)
          end         else  # if Comments_before > 30.5
           return 0.7931034482758621 # (0.7931034482758621 out of 1.0)
        end       else  # if SLOC_diff > 0.5
         return 0.16666666666666666 # (0.16666666666666666 out of 1.0)
      end     else  # if LLOC_before > 397.0
      case when LOC_diff <= -3.0 then
        case when added_lines <= 74.5 then
           return 0.5263157894736842 # (0.5263157894736842 out of 1.0)
        else  # if added_lines > 74.5
           return 0.20833333333333334 # (0.20833333333333334 out of 1.0)
        end       else  # if LOC_diff > -3.0
        case when SLOC_before <= 737.5 then
           return 0.0 # (0.0 out of 1.0)
        else  # if SLOC_before > 737.5
           return 0.125 # (0.125 out of 1.0)
        end       end     end   else  # if removed_lines > 70.5
    case when avg_coupling_code_size_cut_diff <= 0.058908045291900635 then
      case when LOC_before <= 528.0 then
         return 0.6190476190476191 # (0.6190476190476191 out of 1.0)
      else  # if LOC_before > 528.0
         return 0.9047619047619048 # (0.9047619047619048 out of 1.0)
      end     else  # if avg_coupling_code_size_cut_diff > 0.058908045291900635
       return 0.42105263157894735 # (0.42105263157894735 out of 1.0)
    end   end )