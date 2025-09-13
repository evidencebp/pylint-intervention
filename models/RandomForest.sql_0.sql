create or replace function RandomForest_0 (prev_count int64, simplifiable-if-expression int64, N1_diff int64, cur_count int64, wildcard-import int64, too-many-return-statements int64, low_McCabe_max_diff int64, length_diff int64, volume_diff int64, high_McCabe_sum_diff int64, high_McCabe_max_before int64, simplifiable-condition int64, Blank_before int64, high_ccp_group int64, McCabe_max_before int64, bugs_diff int64, too-many-nested-blocks int64, refactor_mle_diff int64, difficulty_diff int64, LLOC_diff int64, LOC_diff int64, simplifiable-if-statement int64, one_file_fix_rate_diff int64, SLOC_before int64, LOC_before int64, mostly_delete int64, changed_lines int64, Single comments_before int64, removed_lines int64, added_functions int64, h1_diff int64, effort_diff int64, hunks_num int64, Multi_diff int64, same_day_duration_avg_diff int64, N2_diff int64, cur_count_y int64, Comments_diff int64, modified_McCabe_max_diff int64, h2_diff int64, time_diff int64, LLOC_before int64, calculated_length_diff int64, Single comments_after int64, massive_change int64, McCabe_sum_before int64, too-many-boolean-expressions int64, Simplify-boolean-expression int64, line-too-long int64, superfluous-parens int64, low_ccp_group int64, McCabe_max_diff int64, comparison-of-constants int64, high_McCabe_sum_before int64, low_McCabe_sum_diff int64, avg_coupling_code_size_cut_diff int64, is_refactor int64, Single comments_diff int64, unnecessary-semicolon int64, added_lines int64, prev_count_y int64, try-except-raise int64, low_McCabe_sum_before int64, vocabulary_diff int64, too-many-branches int64, McCabe_sum_after int64, broad-exception-caught int64, prev_count_x int64, only_removal int64, McCabe_max_after int64, pointless-statement int64, low_McCabe_max_before int64, too-many-lines int64, McCabe_sum_diff int64, high_McCabe_max_diff int64, using-constant-test int64, SLOC_diff int64, Blank_diff int64, Comments_after int64, cur_count_x int64, unnecessary-pass int64, too-many-statements int64, Comments_before int64) as (
  case when one_file_fix_rate_diff <= -0.19526144117116928 then
    case when refactor_mle_diff <= -0.13566047698259354 then
       return 0.32 # (0.32 out of 1.0)
    else  # if refactor_mle_diff > -0.13566047698259354
      case when LLOC_before <= 1099.0 then
        case when added_lines <= 19.5 then
           return 1.0 # (1.0 out of 1.0)
        else  # if added_lines > 19.5
          case when Multi_diff <= -1.0 then
             return 0.8823529411764706 # (0.8823529411764706 out of 1.0)
          else  # if Multi_diff > -1.0
            case when LLOC_before <= 243.0 then
               return 0.5294117647058824 # (0.5294117647058824 out of 1.0)
            else  # if LLOC_before > 243.0
               return 0.8333333333333334 # (0.8333333333333334 out of 1.0)
            end           end         end       else  # if LLOC_before > 1099.0
         return 0.4666666666666667 # (0.4666666666666667 out of 1.0)
      end     end   else  # if one_file_fix_rate_diff > -0.19526144117116928
    case when low_ccp_group <= 0.5 then
      case when low_McCabe_sum_before <= 0.5 then
        case when added_lines <= 56.5 then
          case when same_day_duration_avg_diff <= 55.74989318847656 then
            case when Single comments_before <= 102.0 then
              case when McCabe_sum_before <= 131.0 then
                 return 0.6206896551724138 # (0.6206896551724138 out of 1.0)
              else  # if McCabe_sum_before > 131.0
                case when SLOC_before <= 613.5 then
                   return 0.07692307692307693 # (0.07692307692307693 out of 1.0)
                else  # if SLOC_before > 613.5
                   return 0.5 # (0.5 out of 1.0)
                end               end             else  # if Single comments_before > 102.0
              case when LOC_before <= 2398.0 then
                 return 0.07142857142857142 # (0.07142857142857142 out of 1.0)
              else  # if LOC_before > 2398.0
                 return 0.16666666666666666 # (0.16666666666666666 out of 1.0)
              end             end           else  # if same_day_duration_avg_diff > 55.74989318847656
             return 0.6 # (0.6 out of 1.0)
          end         else  # if added_lines > 56.5
          case when length_diff <= -55.0 then
            case when refactor_mle_diff <= -0.17260468006134033 then
               return 0.13636363636363635 # (0.13636363636363635 out of 1.0)
            else  # if refactor_mle_diff > -0.17260468006134033
              case when same_day_duration_avg_diff <= -8.067888975143433 then
                 return 0.7857142857142857 # (0.7857142857142857 out of 1.0)
              else  # if same_day_duration_avg_diff > -8.067888975143433
                 return 0.21428571428571427 # (0.21428571428571427 out of 1.0)
              end             end           else  # if length_diff > -55.0
            case when Comments_after <= 46.0 then
               return 0.896551724137931 # (0.896551724137931 out of 1.0)
            else  # if Comments_after > 46.0
              case when McCabe_sum_before <= 281.5 then
                 return 0.5 # (0.5 out of 1.0)
              else  # if McCabe_sum_before > 281.5
                 return 0.7058823529411765 # (0.7058823529411765 out of 1.0)
              end             end           end         end       else  # if low_McCabe_sum_before > 0.5
        case when Single comments_after <= 36.5 then
          case when LOC_before <= 213.5 then
             return 0.6428571428571429 # (0.6428571428571429 out of 1.0)
          else  # if LOC_before > 213.5
            case when McCabe_sum_after <= 47.5 then
               return 1.0 # (1.0 out of 1.0)
            else  # if McCabe_sum_after > 47.5
               return 0.8666666666666667 # (0.8666666666666667 out of 1.0)
            end           end         else  # if Single comments_after > 36.5
           return 0.375 # (0.375 out of 1.0)
        end       end     else  # if low_ccp_group > 0.5
      case when LLOC_diff <= -42.5 then
         return 0.6875 # (0.6875 out of 1.0)
      else  # if LLOC_diff > -42.5
        case when Comments_before <= 246.0 then
          case when Single comments_before <= 19.0 then
             return 0.13333333333333333 # (0.13333333333333333 out of 1.0)
          else  # if Single comments_before > 19.0
            case when LLOC_diff <= -8.5 then
               return 0.06666666666666667 # (0.06666666666666667 out of 1.0)
            else  # if LLOC_diff > -8.5
               return 0.0 # (0.0 out of 1.0)
            end           end         else  # if Comments_before > 246.0
           return 0.7142857142857143 # (0.7142857142857143 out of 1.0)
        end       end     end   end )