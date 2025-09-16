create or replace function RandomForest_9 (low_McCabe_sum_before int64, changed_lines int64, low_McCabe_max_diff int64, try-except-raise int64, Comments_before int64, high_McCabe_sum_diff int64, low_McCabe_max_before int64, Multi_diff int64, effort_diff int64, difficulty_diff int64, only_removal int64, length_diff int64, comparison-of-constants int64, LOC_diff int64, h2_diff int64, line-too-long int64, h1_diff int64, using-constant-test int64, broad-exception-caught int64, time_diff int64, calculated_length_diff int64, too-many-branches int64, SLOC_before int64, low_ccp_group int64, avg_coupling_code_size_cut_diff int64, new_function int64, wildcard-import int64, McCabe_max_before int64, superfluous-parens int64, low_McCabe_sum_diff int64, pointless-statement int64, one_file_fix_rate_diff int64, cur_count_x int64, same_day_duration_avg_diff int64, too-many-nested-blocks int64, simplifiable-condition int64, too-many-lines int64, SLOC_diff int64, cur_count_y int64, LLOC_before int64, Comments_after int64, high_ccp_group int64, bugs_diff int64, unnecessary-pass int64, prev_count_x int64, massive_change int64, McCabe_max_after int64, removed_lines int64, Comments_diff int64, Single comments_diff int64, too-many-statements int64, Simplify-boolean-expression int64, is_refactor int64, refactor_mle_diff int64, added_lines int64, mostly_delete int64, volume_diff int64, too-many-boolean-expressions int64, N2_diff int64, Blank_before int64, vocabulary_diff int64, McCabe_sum_before int64, high_McCabe_sum_before int64, N1_diff int64, LOC_before int64, LLOC_diff int64, high_McCabe_max_diff int64, simplifiable-if-statement int64, prev_count_y int64, hunks_num int64, Blank_diff int64, prev_count int64, Single comments_before int64, McCabe_max_diff int64, McCabe_sum_diff int64, modified_McCabe_max_diff int64, McCabe_sum_after int64, too-many-return-statements int64, Single comments_after int64, unnecessary-semicolon int64, added_functions int64, cur_count int64, simplifiable-if-expression int64, high_McCabe_max_before int64) as (
  case when Single comments_diff <= -4.5 then
    case when McCabe_max_after <= 20.0 then
      case when McCabe_sum_diff <= -25.0 then
        case when McCabe_sum_after <= 91.5 then
           return 0.8666666666666667 # (0.8666666666666667 out of 1.0)
        else  # if McCabe_sum_after > 91.5
           return 1.0 # (1.0 out of 1.0)
        end       else  # if McCabe_sum_diff > -25.0
        case when McCabe_max_after <= 7.0 then
           return 0.8148148148148148 # (0.8148148148148148 out of 1.0)
        else  # if McCabe_max_after > 7.0
           return 0.23529411764705882 # (0.23529411764705882 out of 1.0)
        end       end     else  # if McCabe_max_after > 20.0
       return 0.36363636363636365 # (0.36363636363636365 out of 1.0)
    end   else  # if Single comments_diff > -4.5
    case when changed_lines <= 13.0 then
      case when refactor_mle_diff <= -0.15069085359573364 then
         return 0.4838709677419355 # (0.4838709677419355 out of 1.0)
      else  # if refactor_mle_diff > -0.15069085359573364
        case when McCabe_max_before <= 6.5 then
           return 0.875 # (0.875 out of 1.0)
        else  # if McCabe_max_before > 6.5
          case when only_removal <= 0.5 then
            case when McCabe_max_after <= 20.5 then
               return 0.4666666666666667 # (0.4666666666666667 out of 1.0)
            else  # if McCabe_max_after > 20.5
               return 0.7037037037037037 # (0.7037037037037037 out of 1.0)
            end           else  # if only_removal > 0.5
             return 0.8823529411764706 # (0.8823529411764706 out of 1.0)
          end         end       end     else  # if changed_lines > 13.0
      case when removed_lines <= 10.5 then
        case when SLOC_before <= 215.5 then
           return 0.0 # (0.0 out of 1.0)
        else  # if SLOC_before > 215.5
          case when McCabe_sum_after <= 193.5 then
            case when Comments_after <= 26.5 then
               return 0.2727272727272727 # (0.2727272727272727 out of 1.0)
            else  # if Comments_after > 26.5
              case when Single comments_before <= 110.5 then
                 return 0.11764705882352941 # (0.11764705882352941 out of 1.0)
              else  # if Single comments_before > 110.5
                 return 0.0 # (0.0 out of 1.0)
              end             end           else  # if McCabe_sum_after > 193.5
             return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
          end         end       else  # if removed_lines > 10.5
        case when vocabulary_diff <= -21.0 then
           return 0.03571428571428571 # (0.03571428571428571 out of 1.0)
        else  # if vocabulary_diff > -21.0
          case when Single comments_before <= 188.0 then
            case when Comments_diff <= 1.5 then
              case when low_ccp_group <= 0.5 then
                case when Single comments_after <= 59.0 then
                  case when changed_lines <= 128.5 then
                    case when McCabe_max_before <= 15.5 then
                       return 0.9259259259259259 # (0.9259259259259259 out of 1.0)
                    else  # if McCabe_max_before > 15.5
                       return 0.5 # (0.5 out of 1.0)
                    end                   else  # if changed_lines > 128.5
                     return 0.9375 # (0.9375 out of 1.0)
                  end                 else  # if Single comments_after > 59.0
                  case when Comments_before <= 101.0 then
                     return 0.5 # (0.5 out of 1.0)
                  else  # if Comments_before > 101.0
                     return 0.15789473684210525 # (0.15789473684210525 out of 1.0)
                  end                 end               else  # if low_ccp_group > 0.5
                case when same_day_duration_avg_diff <= -6.920258522033691 then
                   return 0.09090909090909091 # (0.09090909090909091 out of 1.0)
                else  # if same_day_duration_avg_diff > -6.920258522033691
                   return 0.058823529411764705 # (0.058823529411764705 out of 1.0)
                end               end             else  # if Comments_diff > 1.5
              case when McCabe_max_before <= 27.5 then
                case when refactor_mle_diff <= -0.009472527541220188 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if refactor_mle_diff > -0.009472527541220188
                   return 0.14285714285714285 # (0.14285714285714285 out of 1.0)
                end               else  # if McCabe_max_before > 27.5
                 return 0.4117647058823529 # (0.4117647058823529 out of 1.0)
              end             end           else  # if Single comments_before > 188.0
            case when SLOC_before <= 1589.5 then
               return 0.8636363636363636 # (0.8636363636363636 out of 1.0)
            else  # if SLOC_before > 1589.5
               return 0.5416666666666666 # (0.5416666666666666 out of 1.0)
            end           end         end       end     end   end )