create or replace function RandomForest_4 (is_refactor int64, McCabe_max_before int64, N1_diff int64, high_McCabe_sum_before int64, same_day_duration_avg_diff int64, Comments_before int64, hunks_num int64, added_lines int64, prev_count int64, low_McCabe_max_before int64, high_McCabe_max_diff int64, vocabulary_diff int64, modified_McCabe_max_diff int64, avg_coupling_code_size_cut_diff int64, too-many-nested-blocks int64, low_McCabe_max_diff int64, changed_lines int64, effort_diff int64, removed_lines int64, Blank_before int64, SLOC_diff int64, length_diff int64, low_ccp_group int64, calculated_length_diff int64, McCabe_max_diff int64, McCabe_max_after int64, LOC_diff int64, too-many-return-statements int64, Single comments_after int64, McCabe_sum_diff int64, LLOC_diff int64, too-many-statements int64, Comments_after int64, low_McCabe_sum_diff int64, McCabe_sum_before int64, difficulty_diff int64, Single comments_before int64, massive_change int64, prev_count_x int64, refactor_mle_diff int64, cur_count_y int64, N2_diff int64, prev_count_y int64, Single comments_diff int64, cur_count int64, high_McCabe_max_before int64, one_file_fix_rate_diff int64, h1_diff int64, low_McCabe_sum_before int64, time_diff int64, LOC_before int64, SLOC_before int64, too-many-branches int64, volume_diff int64, McCabe_sum_after int64, mostly_delete int64, Multi_diff int64, high_McCabe_sum_diff int64, Blank_diff int64, bugs_diff int64, h2_diff int64, cur_count_x int64, added_functions int64, LLOC_before int64, high_ccp_group int64, Comments_diff int64, only_removal int64) as (
  case when Comments_diff <= -4.5 then
    case when McCabe_max_diff <= -2.0 then
      case when low_McCabe_max_diff <= 0.5 then
         return 0.9583333333333334 # (0.9583333333333334 out of 1.0)
      else  # if low_McCabe_max_diff > 0.5
         return 0.5652173913043478 # (0.5652173913043478 out of 1.0)
      end     else  # if McCabe_max_diff > -2.0
       return 0.21052631578947367 # (0.21052631578947367 out of 1.0)
    end   else  # if Comments_diff > -4.5
    case when high_ccp_group <= 0.5 then
      case when McCabe_sum_after <= 179.5 then
        case when low_McCabe_max_before <= 0.5 then
          case when McCabe_sum_diff <= -6.0 then
             return 0.47619047619047616 # (0.47619047619047616 out of 1.0)
          else  # if McCabe_sum_diff > -6.0
            case when refactor_mle_diff <= -0.1785571426153183 then
               return 0.3076923076923077 # (0.3076923076923077 out of 1.0)
            else  # if refactor_mle_diff > -0.1785571426153183
               return 0.034482758620689655 # (0.034482758620689655 out of 1.0)
            end           end         else  # if low_McCabe_max_before > 0.5
          case when refactor_mle_diff <= -0.11903809756040573 then
             return 0.38095238095238093 # (0.38095238095238093 out of 1.0)
          else  # if refactor_mle_diff > -0.11903809756040573
             return 0.7647058823529411 # (0.7647058823529411 out of 1.0)
          end         end       else  # if McCabe_sum_after > 179.5
        case when same_day_duration_avg_diff <= 45.10416603088379 then
           return 0.05 # (0.05 out of 1.0)
        else  # if same_day_duration_avg_diff > 45.10416603088379
           return 0.26666666666666666 # (0.26666666666666666 out of 1.0)
        end       end     else  # if high_ccp_group > 0.5
      case when McCabe_sum_before <= 128.0 then
         return 0.7142857142857143 # (0.7142857142857143 out of 1.0)
      else  # if McCabe_sum_before > 128.0
         return 0.46153846153846156 # (0.46153846153846156 out of 1.0)
      end     end   end )