create or replace function RandomForest_3 (is_refactor int64, McCabe_max_before int64, N1_diff int64, high_McCabe_sum_before int64, same_day_duration_avg_diff int64, Comments_before int64, hunks_num int64, added_lines int64, prev_count int64, low_McCabe_max_before int64, high_McCabe_max_diff int64, vocabulary_diff int64, modified_McCabe_max_diff int64, avg_coupling_code_size_cut_diff int64, too-many-nested-blocks int64, low_McCabe_max_diff int64, changed_lines int64, effort_diff int64, removed_lines int64, Blank_before int64, SLOC_diff int64, length_diff int64, low_ccp_group int64, calculated_length_diff int64, McCabe_max_diff int64, McCabe_max_after int64, LOC_diff int64, too-many-return-statements int64, Single comments_after int64, McCabe_sum_diff int64, LLOC_diff int64, too-many-statements int64, Comments_after int64, low_McCabe_sum_diff int64, McCabe_sum_before int64, difficulty_diff int64, Single comments_before int64, massive_change int64, prev_count_x int64, refactor_mle_diff int64, cur_count_y int64, N2_diff int64, prev_count_y int64, Single comments_diff int64, cur_count int64, high_McCabe_max_before int64, one_file_fix_rate_diff int64, h1_diff int64, low_McCabe_sum_before int64, time_diff int64, LOC_before int64, SLOC_before int64, too-many-branches int64, volume_diff int64, McCabe_sum_after int64, mostly_delete int64, Multi_diff int64, high_McCabe_sum_diff int64, Blank_diff int64, bugs_diff int64, h2_diff int64, cur_count_x int64, added_functions int64, LLOC_before int64, high_ccp_group int64, Comments_diff int64, only_removal int64) as (
  case when LOC_diff <= 60.0 then
    case when Single comments_before <= 102.5 then
      case when Comments_before <= 64.5 then
        case when Comments_diff <= 0.5 then
          case when McCabe_max_after <= 5.5 then
             return 0.85 # (0.85 out of 1.0)
          else  # if McCabe_max_after > 5.5
            case when McCabe_max_diff <= -2.5 then
              case when low_McCabe_max_diff <= 0.5 then
                 return 0.05263157894736842 # (0.05263157894736842 out of 1.0)
              else  # if low_McCabe_max_diff > 0.5
                 return 0.46153846153846156 # (0.46153846153846156 out of 1.0)
              end             else  # if McCabe_max_diff > -2.5
              case when Comments_before <= 38.0 then
                case when added_lines <= 14.5 then
                   return 0.7058823529411765 # (0.7058823529411765 out of 1.0)
                else  # if added_lines > 14.5
                   return 0.65 # (0.65 out of 1.0)
                end               else  # if Comments_before > 38.0
                 return 0.375 # (0.375 out of 1.0)
              end             end           end         else  # if Comments_diff > 0.5
           return 0.0 # (0.0 out of 1.0)
        end       else  # if Comments_before > 64.5
         return 0.7692307692307693 # (0.7692307692307693 out of 1.0)
      end     else  # if Single comments_before > 102.5
      case when Single comments_before <= 205.5 then
         return 0.03333333333333333 # (0.03333333333333333 out of 1.0)
      else  # if Single comments_before > 205.5
         return 0.5652173913043478 # (0.5652173913043478 out of 1.0)
      end     end   else  # if LOC_diff > 60.0
     return 1.0 # (1.0 out of 1.0)
  end )