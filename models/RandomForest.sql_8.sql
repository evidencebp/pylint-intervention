create or replace function RandomForest_8 (N1_diff int64, Single comments_diff int64, h2_diff int64, new_function int64, added_lines int64, difficulty_diff int64, too-many-return-statements int64, effort_diff int64, length_diff int64, McCabe_sum_after int64, removed_lines int64, McCabe_sum_before int64, low_McCabe_sum_before int64, high_McCabe_max_diff int64, prev_count_x int64, prev_count int64, LOC_before int64, SLOC_diff int64, low_McCabe_sum_diff int64, cur_count int64, calculated_length_diff int64, Blank_before int64, Comments_after int64, bugs_diff int64, too-many-statements int64, volume_diff int64, only_removal int64, too-many-branches int64, low_McCabe_max_diff int64, low_McCabe_max_before int64, McCabe_max_diff int64, is_refactor int64, cur_count_x int64, Single comments_before int64, McCabe_max_after int64, Blank_diff int64, McCabe_max_before int64, added_functions int64, Multi_diff int64, SLOC_before int64, prev_count_y int64, massive_change int64, LOC_diff int64, time_diff int64, h1_diff int64, vocabulary_diff int64, LLOC_diff int64, high_ccp_group int64, hunks_num int64, Single comments_after int64, high_McCabe_sum_before int64, modified_McCabe_max_diff int64, N2_diff int64, same_day_duration_avg_diff int64, low_ccp_group int64, Comments_before int64, cur_count_y int64, high_McCabe_sum_diff int64, changed_lines int64, high_McCabe_max_before int64, Comments_diff int64, LLOC_before int64, one_file_fix_rate_diff int64, too-many-nested-blocks int64, McCabe_sum_diff int64, refactor_mle_diff int64, avg_coupling_code_size_cut_diff int64, mostly_delete int64) as (
  case when Blank_before <= 42.0 then
     return 0.84 # (0.84 out of 1.0)
  else  # if Blank_before > 42.0
    case when SLOC_before <= 177.5 then
       return 0.0 # (0.0 out of 1.0)
    else  # if SLOC_before > 177.5
      case when Comments_after <= 23.5 then
        case when Blank_diff <= -7.0 then
           return 0.38461538461538464 # (0.38461538461538464 out of 1.0)
        else  # if Blank_diff > -7.0
           return 0.7692307692307693 # (0.7692307692307693 out of 1.0)
        end       else  # if Comments_after > 23.5
        case when Comments_diff <= -8.0 then
           return 0.8095238095238095 # (0.8095238095238095 out of 1.0)
        else  # if Comments_diff > -8.0
          case when LLOC_diff <= -14.5 then
             return 0.07142857142857142 # (0.07142857142857142 out of 1.0)
          else  # if LLOC_diff > -14.5
            case when hunks_num <= 9.5 then
              case when LLOC_diff <= -1.5 then
                 return 0.6521739130434783 # (0.6521739130434783 out of 1.0)
              else  # if LLOC_diff > -1.5
                case when one_file_fix_rate_diff <= -0.019284188863821328 then
                   return 0.5384615384615384 # (0.5384615384615384 out of 1.0)
                else  # if one_file_fix_rate_diff > -0.019284188863821328
                  case when modified_McCabe_max_diff <= -1.5 then
                     return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
                  else  # if modified_McCabe_max_diff > -1.5
                     return 0.0 # (0.0 out of 1.0)
                  end                 end               end             else  # if hunks_num > 9.5
               return 0.06666666666666667 # (0.06666666666666667 out of 1.0)
            end           end         end       end     end   end )