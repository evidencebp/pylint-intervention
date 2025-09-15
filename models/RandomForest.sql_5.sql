create or replace function RandomForest_5 (N1_diff int64, Single comments_diff int64, h2_diff int64, new_function int64, added_lines int64, difficulty_diff int64, too-many-return-statements int64, effort_diff int64, length_diff int64, McCabe_sum_after int64, removed_lines int64, McCabe_sum_before int64, low_McCabe_sum_before int64, high_McCabe_max_diff int64, prev_count_x int64, prev_count int64, LOC_before int64, SLOC_diff int64, low_McCabe_sum_diff int64, cur_count int64, calculated_length_diff int64, Blank_before int64, Comments_after int64, bugs_diff int64, too-many-statements int64, volume_diff int64, only_removal int64, too-many-branches int64, low_McCabe_max_diff int64, low_McCabe_max_before int64, McCabe_max_diff int64, is_refactor int64, cur_count_x int64, Single comments_before int64, McCabe_max_after int64, Blank_diff int64, McCabe_max_before int64, added_functions int64, Multi_diff int64, SLOC_before int64, prev_count_y int64, massive_change int64, LOC_diff int64, time_diff int64, h1_diff int64, vocabulary_diff int64, LLOC_diff int64, high_ccp_group int64, hunks_num int64, Single comments_after int64, high_McCabe_sum_before int64, modified_McCabe_max_diff int64, N2_diff int64, same_day_duration_avg_diff int64, low_ccp_group int64, Comments_before int64, cur_count_y int64, high_McCabe_sum_diff int64, changed_lines int64, high_McCabe_max_before int64, Comments_diff int64, LLOC_before int64, one_file_fix_rate_diff int64, too-many-nested-blocks int64, McCabe_sum_diff int64, refactor_mle_diff int64, avg_coupling_code_size_cut_diff int64, mostly_delete int64) as (
  case when Comments_diff <= -2.5 then
    case when h1_diff <= -2.5 then
       return 0.9130434782608695 # (0.9130434782608695 out of 1.0)
    else  # if h1_diff > -2.5
      case when avg_coupling_code_size_cut_diff <= -1.1180555820465088 then
         return 0.9411764705882353 # (0.9411764705882353 out of 1.0)
      else  # if avg_coupling_code_size_cut_diff > -1.1180555820465088
         return 0.30303030303030304 # (0.30303030303030304 out of 1.0)
      end     end   else  # if Comments_diff > -2.5
    case when prev_count_y <= 1.5 then
      case when high_ccp_group <= 0.5 then
        case when LOC_before <= 1039.5 then
          case when McCabe_sum_diff <= -5.5 then
             return 0.0 # (0.0 out of 1.0)
          else  # if McCabe_sum_diff > -5.5
            case when same_day_duration_avg_diff <= -21.859999656677246 then
               return 0.44 # (0.44 out of 1.0)
            else  # if same_day_duration_avg_diff > -21.859999656677246
              case when refactor_mle_diff <= 0.03131047170609236 then
                 return 0.13636363636363635 # (0.13636363636363635 out of 1.0)
              else  # if refactor_mle_diff > 0.03131047170609236
                 return 0.0 # (0.0 out of 1.0)
              end             end           end         else  # if LOC_before > 1039.5
           return 0.68 # (0.68 out of 1.0)
        end       else  # if high_ccp_group > 0.5
         return 0.8461538461538461 # (0.8461538461538461 out of 1.0)
      end     else  # if prev_count_y > 1.5
       return 0.0 # (0.0 out of 1.0)
    end   end )