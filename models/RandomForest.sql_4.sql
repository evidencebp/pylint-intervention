create or replace function RandomForest_4 (McCabe_sum_before int64, changed_lines int64, prev_count_y int64, mostly_delete int64, h1_diff int64, too-many-lines int64, low_McCabe_sum_before int64, length_diff int64, LOC_before int64, simplifiable-if-expression int64, added_functions int64, broad-exception-caught int64, simplifiable-condition int64, prev_count_x int64, McCabe_max_diff int64, SLOC_before int64, LLOC_before int64, low_McCabe_max_diff int64, bugs_diff int64, same_day_duration_avg_diff int64, cur_count_x int64, only_removal int64, McCabe_max_after int64, Single comments_after int64, low_ccp_group int64, one_file_fix_rate_diff int64, effort_diff int64, difficulty_diff int64, removed_lines int64, Comments_diff int64, too-many-boolean-expressions int64, refactor_mle_diff int64, high_McCabe_max_before int64, hunks_num int64, LOC_diff int64, SLOC_diff int64, cur_count_y int64, vocabulary_diff int64, using-constant-test int64, Simplify-boolean-expression int64, low_McCabe_max_before int64, high_McCabe_sum_diff int64, high_McCabe_sum_before int64, McCabe_max_before int64, Comments_after int64, McCabe_sum_diff int64, unnecessary-pass int64, avg_coupling_code_size_cut_diff int64, simplifiable-if-statement int64, is_refactor int64, volume_diff int64, added_lines int64, high_McCabe_max_diff int64, superfluous-parens int64, cur_count int64, low_McCabe_sum_diff int64, calculated_length_diff int64, Multi_diff int64, N2_diff int64, h2_diff int64, Single comments_before int64, McCabe_sum_after int64, N1_diff int64, too-many-statements int64, comparison-of-constants int64, pointless-statement int64, time_diff int64, prev_count int64, Single comments_diff int64, massive_change int64, Blank_diff int64, too-many-nested-blocks int64, Comments_before int64, modified_McCabe_max_diff int64, LLOC_diff int64, Blank_before int64, try-except-raise int64, too-many-branches int64, too-many-return-statements int64, unnecessary-semicolon int64, wildcard-import int64, high_ccp_group int64, line-too-long int64) as (
  case when Single comments_diff <= -4.5 then
    case when high_McCabe_max_before <= 0.5 then
      case when one_file_fix_rate_diff <= 0.16111111640930176 then
        case when Single comments_before <= 94.0 then
          case when LOC_before <= 1074.0 then
             return 0.9285714285714286 # (0.9285714285714286 out of 1.0)
          else  # if LOC_before > 1074.0
             return 1.0 # (1.0 out of 1.0)
          end         else  # if Single comments_before > 94.0
           return 0.7391304347826086 # (0.7391304347826086 out of 1.0)
        end       else  # if one_file_fix_rate_diff > 0.16111111640930176
         return 0.3076923076923077 # (0.3076923076923077 out of 1.0)
      end     else  # if high_McCabe_max_before > 0.5
       return 0.36363636363636365 # (0.36363636363636365 out of 1.0)
    end   else  # if Single comments_diff > -4.5
    case when Blank_before <= 16.0 then
       return 0.9130434782608695 # (0.9130434782608695 out of 1.0)
    else  # if Blank_before > 16.0
      case when added_lines <= 1.5 then
        case when LLOC_before <= 382.5 then
           return 0.7714285714285715 # (0.7714285714285715 out of 1.0)
        else  # if LLOC_before > 382.5
          case when removed_lines <= 0.5 then
             return 0.2 # (0.2 out of 1.0)
          else  # if removed_lines > 0.5
             return 0.625 # (0.625 out of 1.0)
          end         end       else  # if added_lines > 1.5
        case when low_ccp_group <= 0.5 then
          case when LLOC_diff <= -47.0 then
            case when SLOC_diff <= -85.0 then
               return 0.07692307692307693 # (0.07692307692307693 out of 1.0)
            else  # if SLOC_diff > -85.0
               return 0.0 # (0.0 out of 1.0)
            end           else  # if LLOC_diff > -47.0
            case when McCabe_sum_before <= 67.5 then
              case when same_day_duration_avg_diff <= 3.0332791805267334 then
                case when McCabe_sum_diff <= -1.5 then
                   return 0.8125 # (0.8125 out of 1.0)
                else  # if McCabe_sum_diff > -1.5
                   return 0.6 # (0.6 out of 1.0)
                end               else  # if same_day_duration_avg_diff > 3.0332791805267334
                 return 0.4 # (0.4 out of 1.0)
              end             else  # if McCabe_sum_before > 67.5
              case when modified_McCabe_max_diff <= -0.5 then
                case when one_file_fix_rate_diff <= -0.09761904925107956 then
                   return 0.7 # (0.7 out of 1.0)
                else  # if one_file_fix_rate_diff > -0.09761904925107956
                  case when Comments_before <= 89.5 then
                     return 0.25806451612903225 # (0.25806451612903225 out of 1.0)
                  else  # if Comments_before > 89.5
                     return 0.7142857142857143 # (0.7142857142857143 out of 1.0)
                  end                 end               else  # if modified_McCabe_max_diff > -0.5
                case when high_McCabe_max_before <= 0.5 then
                  case when Single comments_after <= 75.5 then
                    case when McCabe_sum_after <= 134.0 then
                       return 0.42857142857142855 # (0.42857142857142855 out of 1.0)
                    else  # if McCabe_sum_after > 134.0
                       return 0.16666666666666666 # (0.16666666666666666 out of 1.0)
                    end                   else  # if Single comments_after > 75.5
                    case when Comments_before <= 118.5 then
                       return 0.0 # (0.0 out of 1.0)
                    else  # if Comments_before > 118.5
                       return 0.23529411764705882 # (0.23529411764705882 out of 1.0)
                    end                   end                 else  # if high_McCabe_max_before > 0.5
                  case when LOC_before <= 1436.0 then
                     return 0.2 # (0.2 out of 1.0)
                  else  # if LOC_before > 1436.0
                     return 0.6363636363636364 # (0.6363636363636364 out of 1.0)
                  end                 end               end             end           end         else  # if low_ccp_group > 0.5
          case when McCabe_sum_after <= 271.5 then
            case when N1_diff <= -3.5 then
               return 0.13333333333333333 # (0.13333333333333333 out of 1.0)
            else  # if N1_diff > -3.5
               return 0.0 # (0.0 out of 1.0)
            end           else  # if McCabe_sum_after > 271.5
             return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
          end         end       end     end   end )