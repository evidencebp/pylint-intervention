create or replace function RandomForest_9 (is_refactor int64, McCabe_max_before int64, N1_diff int64, high_McCabe_sum_before int64, same_day_duration_avg_diff int64, Comments_before int64, hunks_num int64, added_lines int64, prev_count int64, low_McCabe_max_before int64, high_McCabe_max_diff int64, vocabulary_diff int64, modified_McCabe_max_diff int64, avg_coupling_code_size_cut_diff int64, too-many-nested-blocks int64, low_McCabe_max_diff int64, changed_lines int64, effort_diff int64, removed_lines int64, Blank_before int64, SLOC_diff int64, length_diff int64, low_ccp_group int64, calculated_length_diff int64, McCabe_max_diff int64, McCabe_max_after int64, LOC_diff int64, too-many-return-statements int64, Single comments_after int64, McCabe_sum_diff int64, LLOC_diff int64, too-many-statements int64, Comments_after int64, low_McCabe_sum_diff int64, McCabe_sum_before int64, difficulty_diff int64, Single comments_before int64, massive_change int64, prev_count_x int64, refactor_mle_diff int64, cur_count_y int64, N2_diff int64, prev_count_y int64, Single comments_diff int64, cur_count int64, high_McCabe_max_before int64, one_file_fix_rate_diff int64, h1_diff int64, low_McCabe_sum_before int64, time_diff int64, LOC_before int64, SLOC_before int64, too-many-branches int64, volume_diff int64, McCabe_sum_after int64, mostly_delete int64, Multi_diff int64, high_McCabe_sum_diff int64, Blank_diff int64, bugs_diff int64, h2_diff int64, cur_count_x int64, added_functions int64, LLOC_before int64, high_ccp_group int64, Comments_diff int64, only_removal int64) as (
  case when avg_coupling_code_size_cut_diff <= 0.5946428775787354 then
    case when Comments_diff <= -2.5 then
      case when avg_coupling_code_size_cut_diff <= -1.0400000214576721 then
         return 0.6956521739130435 # (0.6956521739130435 out of 1.0)
      else  # if avg_coupling_code_size_cut_diff > -1.0400000214576721
         return 0.9523809523809523 # (0.9523809523809523 out of 1.0)
      end     else  # if Comments_diff > -2.5
      case when vocabulary_diff <= -4.5 then
        case when length_diff <= -30.0 then
           return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
        else  # if length_diff > -30.0
           return 0.10526315789473684 # (0.10526315789473684 out of 1.0)
        end       else  # if vocabulary_diff > -4.5
        case when Comments_before <= 37.5 then
          case when modified_McCabe_max_diff <= -1.5 then
             return 0.2 # (0.2 out of 1.0)
          else  # if modified_McCabe_max_diff > -1.5
             return 0.896551724137931 # (0.896551724137931 out of 1.0)
          end         else  # if Comments_before > 37.5
          case when removed_lines <= 30.5 then
             return 0.11538461538461539 # (0.11538461538461539 out of 1.0)
          else  # if removed_lines > 30.5
             return 0.4838709677419355 # (0.4838709677419355 out of 1.0)
          end         end       end     end   else  # if avg_coupling_code_size_cut_diff > 0.5946428775787354
    case when LOC_before <= 1231.0 then
       return 0.34375 # (0.34375 out of 1.0)
    else  # if LOC_before > 1231.0
       return 0.0 # (0.0 out of 1.0)
    end   end )