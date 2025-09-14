create or replace function RandomForest_7 (is_refactor int64, McCabe_max_before int64, N1_diff int64, high_McCabe_sum_before int64, same_day_duration_avg_diff int64, Comments_before int64, hunks_num int64, added_lines int64, prev_count int64, low_McCabe_max_before int64, high_McCabe_max_diff int64, vocabulary_diff int64, modified_McCabe_max_diff int64, avg_coupling_code_size_cut_diff int64, too-many-nested-blocks int64, low_McCabe_max_diff int64, changed_lines int64, effort_diff int64, removed_lines int64, Blank_before int64, SLOC_diff int64, length_diff int64, low_ccp_group int64, calculated_length_diff int64, McCabe_max_diff int64, McCabe_max_after int64, LOC_diff int64, too-many-return-statements int64, Single comments_after int64, McCabe_sum_diff int64, LLOC_diff int64, too-many-statements int64, Comments_after int64, low_McCabe_sum_diff int64, McCabe_sum_before int64, difficulty_diff int64, Single comments_before int64, massive_change int64, prev_count_x int64, refactor_mle_diff int64, cur_count_y int64, N2_diff int64, prev_count_y int64, Single comments_diff int64, cur_count int64, high_McCabe_max_before int64, one_file_fix_rate_diff int64, h1_diff int64, low_McCabe_sum_before int64, time_diff int64, LOC_before int64, SLOC_before int64, too-many-branches int64, volume_diff int64, McCabe_sum_after int64, mostly_delete int64, Multi_diff int64, high_McCabe_sum_diff int64, Blank_diff int64, bugs_diff int64, h2_diff int64, cur_count_x int64, added_functions int64, LLOC_before int64, high_ccp_group int64, Comments_diff int64, only_removal int64) as (
  case when hunks_num <= 11.5 then
    case when LOC_diff <= -114.5 then
      case when McCabe_sum_diff <= -33.5 then
         return 0.9444444444444444 # (0.9444444444444444 out of 1.0)
      else  # if McCabe_sum_diff > -33.5
         return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
      end     else  # if LOC_diff > -114.5
      case when refactor_mle_diff <= 0.17010866105556488 then
        case when Blank_before <= 37.0 then
           return 0.8333333333333334 # (0.8333333333333334 out of 1.0)
        else  # if Blank_before > 37.0
          case when removed_lines <= 58.5 then
            case when McCabe_max_before <= 20.5 then
              case when vocabulary_diff <= -0.5 then
                 return 0.631578947368421 # (0.631578947368421 out of 1.0)
              else  # if vocabulary_diff > -0.5
                 return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
              end             else  # if McCabe_max_before > 20.5
               return 0.2413793103448276 # (0.2413793103448276 out of 1.0)
            end           else  # if removed_lines > 58.5
             return 0.7894736842105263 # (0.7894736842105263 out of 1.0)
          end         end       else  # if refactor_mle_diff > 0.17010866105556488
        case when LLOC_before <= 329.5 then
           return 0.35714285714285715 # (0.35714285714285715 out of 1.0)
        else  # if LLOC_before > 329.5
           return 0.10526315789473684 # (0.10526315789473684 out of 1.0)
        end       end     end   else  # if hunks_num > 11.5
    case when removed_lines <= 62.5 then
       return 0.0 # (0.0 out of 1.0)
    else  # if removed_lines > 62.5
       return 0.2608695652173913 # (0.2608695652173913 out of 1.0)
    end   end )