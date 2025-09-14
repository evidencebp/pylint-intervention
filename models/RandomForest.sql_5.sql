create or replace function RandomForest_5 (is_refactor int64, McCabe_max_before int64, N1_diff int64, high_McCabe_sum_before int64, same_day_duration_avg_diff int64, Comments_before int64, hunks_num int64, added_lines int64, prev_count int64, low_McCabe_max_before int64, high_McCabe_max_diff int64, vocabulary_diff int64, modified_McCabe_max_diff int64, avg_coupling_code_size_cut_diff int64, too-many-nested-blocks int64, low_McCabe_max_diff int64, changed_lines int64, effort_diff int64, removed_lines int64, Blank_before int64, SLOC_diff int64, length_diff int64, low_ccp_group int64, calculated_length_diff int64, McCabe_max_diff int64, McCabe_max_after int64, LOC_diff int64, too-many-return-statements int64, Single comments_after int64, McCabe_sum_diff int64, LLOC_diff int64, too-many-statements int64, Comments_after int64, low_McCabe_sum_diff int64, McCabe_sum_before int64, difficulty_diff int64, Single comments_before int64, massive_change int64, prev_count_x int64, refactor_mle_diff int64, cur_count_y int64, N2_diff int64, prev_count_y int64, Single comments_diff int64, cur_count int64, high_McCabe_max_before int64, one_file_fix_rate_diff int64, h1_diff int64, low_McCabe_sum_before int64, time_diff int64, LOC_before int64, SLOC_before int64, too-many-branches int64, volume_diff int64, McCabe_sum_after int64, mostly_delete int64, Multi_diff int64, high_McCabe_sum_diff int64, Blank_diff int64, bugs_diff int64, h2_diff int64, cur_count_x int64, added_functions int64, LLOC_before int64, high_ccp_group int64, Comments_diff int64, only_removal int64) as (
  case when LOC_diff <= -114.5 then
    case when Blank_before <= 151.0 then
       return 0.8888888888888888 # (0.8888888888888888 out of 1.0)
    else  # if Blank_before > 151.0
       return 0.3888888888888889 # (0.3888888888888889 out of 1.0)
    end   else  # if LOC_diff > -114.5
    case when LOC_before <= 293.0 then
       return 0.75 # (0.75 out of 1.0)
    else  # if LOC_before > 293.0
      case when LLOC_diff <= -34.5 then
         return 0.1 # (0.1 out of 1.0)
      else  # if LLOC_diff > -34.5
        case when N1_diff <= -0.5 then
          case when refactor_mle_diff <= -0.08936133608222008 then
             return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
          else  # if refactor_mle_diff > -0.08936133608222008
            case when refactor_mle_diff <= 0.02565476205199957 then
               return 0.25 # (0.25 out of 1.0)
            else  # if refactor_mle_diff > 0.02565476205199957
               return 0.5 # (0.5 out of 1.0)
            end           end         else  # if N1_diff > -0.5
          case when N1_diff <= 0.5 then
            case when Blank_before <= 151.0 then
              case when hunks_num <= 5.5 then
                 return 0.3181818181818182 # (0.3181818181818182 out of 1.0)
              else  # if hunks_num > 5.5
                 return 0.11764705882352941 # (0.11764705882352941 out of 1.0)
              end             else  # if Blank_before > 151.0
               return 0.08333333333333333 # (0.08333333333333333 out of 1.0)
            end           else  # if N1_diff > 0.5
             return 0.5 # (0.5 out of 1.0)
          end         end       end     end   end )