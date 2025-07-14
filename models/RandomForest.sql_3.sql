create or replace function RandomForest_3 (hunks_num int64, McCabe_sum_after int64, added_lines int64, cur_count_y int64, changed_lines int64, N1_diff int64, added_functions int64, Single comments_before int64, McCabe_max_after int64, calculated_length_diff int64, h1_diff int64, difficulty_diff int64, too-many-nested-blocks int64, modified_McCabe_max_diff int64, removed_lines int64, prev_count int64, Blank_diff int64, prev_count_x int64, h2_diff int64, LLOC_before int64, Multi_diff int64, volume_diff int64, same_day_duration_avg_diff int64, N2_diff int64, one_file_fix_rate_diff int64, Comments_after int64, massive_change int64, Single comments_diff int64, Comments_before int64, SLOC_before int64, prev_count_y int64, vocabulary_diff int64, LOC_before int64, McCabe_sum_diff int64, high_ccp_group int64, McCabe_sum_before int64, is_refactor int64, cur_count_x int64, refactor_mle_diff int64, time_diff int64, bugs_diff int64, avg_coupling_code_size_cut_diff int64, LLOC_diff int64, Single comments_after int64, too-many-branches int64, McCabe_max_diff int64, too-many-statements int64, mostly_delete int64, effort_diff int64, length_diff int64, Blank_before int64, SLOC_diff int64, McCabe_max_before int64, LOC_diff int64, cur_count int64, too-many-return-statements int64, only_removal int64, Comments_diff int64) as (
  case when Blank_before <= 42.5 then
     return 0.88 # (22.0 out of 25.0)
  else  # if Blank_before > 42.5
    case when Comments_diff <= -7.5 then
      case when McCabe_max_before <= 18.5 then
         return 0.6666666666666666 # (10.0 out of 15.0)
      else  # if McCabe_max_before > 18.5
         return 0.9333333333333333 # (14.0 out of 15.0)
      end     else  # if Comments_diff > -7.5
      case when N2_diff <= -27.0 then
         return 0.0 # (0.0 out of 19.0)
      else  # if N2_diff > -27.0
        case when high_ccp_group <= 0.5 then
          case when avg_coupling_code_size_cut_diff <= -1.4954545497894287 then
             return 0.0 # (0.0 out of 26.0)
          else  # if avg_coupling_code_size_cut_diff > -1.4954545497894287
            case when SLOC_before <= 668.5 then
              case when Comments_before <= 18.5 then
                 return 0.1 # (2.0 out of 20.0)
              else  # if Comments_before > 18.5
                case when McCabe_sum_diff <= -1.5 then
                   return 0.8823529411764706 # (15.0 out of 17.0)
                else  # if McCabe_sum_diff > -1.5
                   return 0.35 # (7.0 out of 20.0)
                end               end             else  # if SLOC_before > 668.5
              case when SLOC_before <= 1167.5 then
                 return 0.11764705882352941 # (2.0 out of 17.0)
              else  # if SLOC_before > 1167.5
                 return 0.09523809523809523 # (2.0 out of 21.0)
              end             end           end         else  # if high_ccp_group > 0.5
          case when McCabe_max_after <= 21.5 then
             return 0.875 # (14.0 out of 16.0)
          else  # if McCabe_max_after > 21.5
             return 0.2777777777777778 # (5.0 out of 18.0)
          end         end       end     end   end )