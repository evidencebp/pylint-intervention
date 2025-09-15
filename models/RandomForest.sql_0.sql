create or replace function RandomForest_0 (N1_diff int64, Single comments_diff int64, h2_diff int64, new_function int64, added_lines int64, difficulty_diff int64, too-many-return-statements int64, effort_diff int64, length_diff int64, McCabe_sum_after int64, removed_lines int64, McCabe_sum_before int64, low_McCabe_sum_before int64, high_McCabe_max_diff int64, prev_count_x int64, prev_count int64, LOC_before int64, SLOC_diff int64, low_McCabe_sum_diff int64, cur_count int64, calculated_length_diff int64, Blank_before int64, Comments_after int64, bugs_diff int64, too-many-statements int64, volume_diff int64, only_removal int64, too-many-branches int64, low_McCabe_max_diff int64, low_McCabe_max_before int64, McCabe_max_diff int64, is_refactor int64, cur_count_x int64, Single comments_before int64, McCabe_max_after int64, Blank_diff int64, McCabe_max_before int64, added_functions int64, Multi_diff int64, SLOC_before int64, prev_count_y int64, massive_change int64, LOC_diff int64, time_diff int64, h1_diff int64, vocabulary_diff int64, LLOC_diff int64, high_ccp_group int64, hunks_num int64, Single comments_after int64, high_McCabe_sum_before int64, modified_McCabe_max_diff int64, N2_diff int64, same_day_duration_avg_diff int64, low_ccp_group int64, Comments_before int64, cur_count_y int64, high_McCabe_sum_diff int64, changed_lines int64, high_McCabe_max_before int64, Comments_diff int64, LLOC_before int64, one_file_fix_rate_diff int64, too-many-nested-blocks int64, McCabe_sum_diff int64, refactor_mle_diff int64, avg_coupling_code_size_cut_diff int64, mostly_delete int64) as (
  case when Single comments_diff <= -2.5 then
    case when McCabe_sum_before <= 84.5 then
       return 0.8235294117647058 # (0.8235294117647058 out of 1.0)
    else  # if McCabe_sum_before > 84.5
       return 0.4642857142857143 # (0.4642857142857143 out of 1.0)
    end   else  # if Single comments_diff > -2.5
    case when changed_lines <= 148.0 then
      case when SLOC_before <= 177.5 then
         return 0.10714285714285714 # (0.10714285714285714 out of 1.0)
      else  # if SLOC_before > 177.5
        case when hunks_num <= 11.5 then
          case when Blank_before <= 98.0 then
            case when one_file_fix_rate_diff <= 0.02777777798473835 then
               return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
            else  # if one_file_fix_rate_diff > 0.02777777798473835
               return 0.7777777777777778 # (0.7777777777777778 out of 1.0)
            end           else  # if Blank_before > 98.0
            case when high_McCabe_max_before <= 0.5 then
              case when avg_coupling_code_size_cut_diff <= 0.3680555671453476 then
                 return 0.43478260869565216 # (0.43478260869565216 out of 1.0)
              else  # if avg_coupling_code_size_cut_diff > 0.3680555671453476
                 return 0.07692307692307693 # (0.07692307692307693 out of 1.0)
              end             else  # if high_McCabe_max_before > 0.5
               return 0.05 # (0.05 out of 1.0)
            end           end         else  # if hunks_num > 11.5
           return 0.0 # (0.0 out of 1.0)
        end       end     else  # if changed_lines > 148.0
      case when Blank_diff <= 7.5 then
         return 0.47619047619047616 # (0.47619047619047616 out of 1.0)
      else  # if Blank_diff > 7.5
         return 0.65 # (0.65 out of 1.0)
      end     end   end )