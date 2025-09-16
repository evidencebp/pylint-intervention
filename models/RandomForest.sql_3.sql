create or replace function RandomForest_3 (low_McCabe_sum_before int64, changed_lines int64, low_McCabe_max_diff int64, try-except-raise int64, Comments_before int64, high_McCabe_sum_diff int64, low_McCabe_max_before int64, Multi_diff int64, effort_diff int64, difficulty_diff int64, only_removal int64, length_diff int64, comparison-of-constants int64, LOC_diff int64, h2_diff int64, line-too-long int64, h1_diff int64, using-constant-test int64, broad-exception-caught int64, time_diff int64, calculated_length_diff int64, too-many-branches int64, SLOC_before int64, low_ccp_group int64, avg_coupling_code_size_cut_diff int64, new_function int64, wildcard-import int64, McCabe_max_before int64, superfluous-parens int64, low_McCabe_sum_diff int64, pointless-statement int64, one_file_fix_rate_diff int64, cur_count_x int64, same_day_duration_avg_diff int64, too-many-nested-blocks int64, simplifiable-condition int64, too-many-lines int64, SLOC_diff int64, cur_count_y int64, LLOC_before int64, Comments_after int64, high_ccp_group int64, bugs_diff int64, unnecessary-pass int64, prev_count_x int64, massive_change int64, McCabe_max_after int64, removed_lines int64, Comments_diff int64, Single comments_diff int64, too-many-statements int64, Simplify-boolean-expression int64, is_refactor int64, refactor_mle_diff int64, added_lines int64, mostly_delete int64, volume_diff int64, too-many-boolean-expressions int64, N2_diff int64, Blank_before int64, vocabulary_diff int64, McCabe_sum_before int64, high_McCabe_sum_before int64, N1_diff int64, LOC_before int64, LLOC_diff int64, high_McCabe_max_diff int64, simplifiable-if-statement int64, prev_count_y int64, hunks_num int64, Blank_diff int64, prev_count int64, Single comments_before int64, McCabe_max_diff int64, McCabe_sum_diff int64, modified_McCabe_max_diff int64, McCabe_sum_after int64, too-many-return-statements int64, Single comments_after int64, unnecessary-semicolon int64, added_functions int64, cur_count int64, simplifiable-if-expression int64, high_McCabe_max_before int64) as (
  case when length_diff <= 26.5 then
    case when added_lines <= 1.5 then
      case when added_functions <= 0.5 then
        case when LLOC_before <= 357.5 then
           return 0.43333333333333335 # (0.43333333333333335 out of 1.0)
        else  # if LLOC_before > 357.5
          case when SLOC_before <= 741.0 then
             return 0.875 # (0.875 out of 1.0)
          else  # if SLOC_before > 741.0
             return 0.5384615384615384 # (0.5384615384615384 out of 1.0)
          end         end       else  # if added_functions > 0.5
         return 0.9285714285714286 # (0.9285714285714286 out of 1.0)
      end     else  # if added_lines > 1.5
      case when low_ccp_group <= 0.5 then
        case when Comments_diff <= 3.5 then
          case when N1_diff <= -7.5 then
            case when McCabe_sum_diff <= -24.0 then
              case when Comments_after <= 35.5 then
                 return 0.4666666666666667 # (0.4666666666666667 out of 1.0)
              else  # if Comments_after > 35.5
                 return 0.9 # (0.9 out of 1.0)
              end             else  # if McCabe_sum_diff > -24.0
              case when LOC_diff <= -75.5 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if LOC_diff > -75.5
                case when McCabe_sum_after <= 77.5 then
                   return 0.6363636363636364 # (0.6363636363636364 out of 1.0)
                else  # if McCabe_sum_after > 77.5
                   return 0.2727272727272727 # (0.2727272727272727 out of 1.0)
                end               end             end           else  # if N1_diff > -7.5
            case when added_lines <= 38.5 then
              case when SLOC_before <= 224.5 then
                 return 0.8181818181818182 # (0.8181818181818182 out of 1.0)
              else  # if SLOC_before > 224.5
                case when McCabe_sum_after <= 158.5 then
                  case when added_lines <= 7.5 then
                     return 0.1 # (0.1 out of 1.0)
                  else  # if added_lines > 7.5
                    case when Comments_diff <= -0.5 then
                       return 0.21739130434782608 # (0.21739130434782608 out of 1.0)
                    else  # if Comments_diff > -0.5
                       return 0.6818181818181818 # (0.6818181818181818 out of 1.0)
                    end                   end                 else  # if McCabe_sum_after > 158.5
                  case when changed_lines <= 25.5 then
                     return 0.5882352941176471 # (0.5882352941176471 out of 1.0)
                  else  # if changed_lines > 25.5
                     return 0.7142857142857143 # (0.7142857142857143 out of 1.0)
                  end                 end               end             else  # if added_lines > 38.5
              case when LOC_diff <= -81.5 then
                 return 0.42857142857142855 # (0.42857142857142855 out of 1.0)
              else  # if LOC_diff > -81.5
                case when vocabulary_diff <= -0.5 then
                   return 0.625 # (0.625 out of 1.0)
                else  # if vocabulary_diff > -0.5
                  case when avg_coupling_code_size_cut_diff <= 0.2904761955142021 then
                     return 1.0 # (1.0 out of 1.0)
                  else  # if avg_coupling_code_size_cut_diff > 0.2904761955142021
                     return 0.7692307692307693 # (0.7692307692307693 out of 1.0)
                  end                 end               end             end           end         else  # if Comments_diff > 3.5
          case when LLOC_before <= 429.5 then
             return 0.23076923076923078 # (0.23076923076923078 out of 1.0)
          else  # if LLOC_before > 429.5
             return 0.125 # (0.125 out of 1.0)
          end         end       else  # if low_ccp_group > 0.5
        case when h2_diff <= -28.5 then
           return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
        else  # if h2_diff > -28.5
          case when new_function <= 0.5 then
            case when LLOC_diff <= -0.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if LLOC_diff > -0.5
               return 0.13333333333333333 # (0.13333333333333333 out of 1.0)
            end           else  # if new_function > 0.5
             return 0.20689655172413793 # (0.20689655172413793 out of 1.0)
          end         end       end     end   else  # if length_diff > 26.5
     return 0.04 # (0.04 out of 1.0)
  end )