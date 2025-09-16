create or replace function RandomForest_8 (low_McCabe_sum_before int64, changed_lines int64, low_McCabe_max_diff int64, try-except-raise int64, Comments_before int64, high_McCabe_sum_diff int64, low_McCabe_max_before int64, Multi_diff int64, effort_diff int64, difficulty_diff int64, only_removal int64, length_diff int64, comparison-of-constants int64, LOC_diff int64, h2_diff int64, line-too-long int64, h1_diff int64, using-constant-test int64, broad-exception-caught int64, time_diff int64, calculated_length_diff int64, too-many-branches int64, SLOC_before int64, low_ccp_group int64, avg_coupling_code_size_cut_diff int64, new_function int64, wildcard-import int64, McCabe_max_before int64, superfluous-parens int64, low_McCabe_sum_diff int64, pointless-statement int64, one_file_fix_rate_diff int64, cur_count_x int64, same_day_duration_avg_diff int64, too-many-nested-blocks int64, simplifiable-condition int64, too-many-lines int64, SLOC_diff int64, cur_count_y int64, LLOC_before int64, Comments_after int64, high_ccp_group int64, bugs_diff int64, unnecessary-pass int64, prev_count_x int64, massive_change int64, McCabe_max_after int64, removed_lines int64, Comments_diff int64, Single comments_diff int64, too-many-statements int64, Simplify-boolean-expression int64, is_refactor int64, refactor_mle_diff int64, added_lines int64, mostly_delete int64, volume_diff int64, too-many-boolean-expressions int64, N2_diff int64, Blank_before int64, vocabulary_diff int64, McCabe_sum_before int64, high_McCabe_sum_before int64, N1_diff int64, LOC_before int64, LLOC_diff int64, high_McCabe_max_diff int64, simplifiable-if-statement int64, prev_count_y int64, hunks_num int64, Blank_diff int64, prev_count int64, Single comments_before int64, McCabe_max_diff int64, McCabe_sum_diff int64, modified_McCabe_max_diff int64, McCabe_sum_after int64, too-many-return-statements int64, Single comments_after int64, unnecessary-semicolon int64, added_functions int64, cur_count int64, simplifiable-if-expression int64, high_McCabe_max_before int64) as (
  case when high_ccp_group <= 0.5 then
    case when LLOC_diff <= -92.5 then
      case when McCabe_max_diff <= -4.5 then
         return 0.5294117647058824 # (0.5294117647058824 out of 1.0)
      else  # if McCabe_max_diff > -4.5
         return 0.7777777777777778 # (0.7777777777777778 out of 1.0)
      end     else  # if LLOC_diff > -92.5
      case when low_ccp_group <= 0.5 then
        case when added_functions <= 1.5 then
          case when low_McCabe_sum_diff <= 0.5 then
            case when LOC_diff <= -0.5 then
              case when hunks_num <= 1.5 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if hunks_num > 1.5
                case when hunks_num <= 3.5 then
                   return 0.4 # (0.4 out of 1.0)
                else  # if hunks_num > 3.5
                   return 0.06666666666666667 # (0.06666666666666667 out of 1.0)
                end               end             else  # if LOC_diff > -0.5
              case when Blank_before <= 365.5 then
                case when Single comments_after <= 3.5 then
                   return 0.9375 # (0.9375 out of 1.0)
                else  # if Single comments_after > 3.5
                  case when McCabe_sum_diff <= 0.5 then
                    case when Comments_after <= 125.5 then
                      case when refactor_mle_diff <= 0.019644059240818024 then
                         return 0.391304347826087 # (0.391304347826087 out of 1.0)
                      else  # if refactor_mle_diff > 0.019644059240818024
                         return 0.3888888888888889 # (0.3888888888888889 out of 1.0)
                      end                     else  # if Comments_after > 125.5
                       return 0.8125 # (0.8125 out of 1.0)
                    end                   else  # if McCabe_sum_diff > 0.5
                     return 0.25 # (0.25 out of 1.0)
                  end                 end               else  # if Blank_before > 365.5
                 return 0.058823529411764705 # (0.058823529411764705 out of 1.0)
              end             end           else  # if low_McCabe_sum_diff > 0.5
            case when McCabe_sum_before <= 254.5 then
               return 0.16 # (0.16 out of 1.0)
            else  # if McCabe_sum_before > 254.5
               return 0.0 # (0.0 out of 1.0)
            end           end         else  # if added_functions > 1.5
          case when McCabe_max_after <= 12.0 then
             return 0.8421052631578947 # (0.8421052631578947 out of 1.0)
          else  # if McCabe_max_after > 12.0
             return 0.5294117647058824 # (0.5294117647058824 out of 1.0)
          end         end       else  # if low_ccp_group > 0.5
        case when N1_diff <= -4.5 then
           return 0.45454545454545453 # (0.45454545454545453 out of 1.0)
        else  # if N1_diff > -4.5
          case when same_day_duration_avg_diff <= -0.3958333432674408 then
             return 0.0 # (0.0 out of 1.0)
          else  # if same_day_duration_avg_diff > -0.3958333432674408
            case when McCabe_sum_diff <= -0.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if McCabe_sum_diff > -0.5
              case when Comments_before <= 54.0 then
                 return 0.08571428571428572 # (0.08571428571428572 out of 1.0)
              else  # if Comments_before > 54.0
                 return 0.5 # (0.5 out of 1.0)
              end             end           end         end       end     end   else  # if high_ccp_group > 0.5
    case when avg_coupling_code_size_cut_diff <= -1.1597222089767456 then
       return 0.3181818181818182 # (0.3181818181818182 out of 1.0)
    else  # if avg_coupling_code_size_cut_diff > -1.1597222089767456
      case when Blank_diff <= -1.5 then
        case when added_lines <= 64.5 then
           return 0.4 # (0.4 out of 1.0)
        else  # if added_lines > 64.5
           return 0.8571428571428571 # (0.8571428571428571 out of 1.0)
        end       else  # if Blank_diff > -1.5
        case when avg_coupling_code_size_cut_diff <= 0.019999999552965164 then
          case when same_day_duration_avg_diff <= -62.2738094329834 then
             return 0.36363636363636365 # (0.36363636363636365 out of 1.0)
          else  # if same_day_duration_avg_diff > -62.2738094329834
             return 0.9642857142857143 # (0.9642857142857143 out of 1.0)
          end         else  # if avg_coupling_code_size_cut_diff > 0.019999999552965164
           return 0.9696969696969697 # (0.9696969696969697 out of 1.0)
        end       end     end   end )