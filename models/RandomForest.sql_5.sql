create or replace function RandomForest_5 (prev_count int64, simplifiable-if-expression int64, N1_diff int64, cur_count int64, wildcard-import int64, too-many-return-statements int64, low_McCabe_max_diff int64, length_diff int64, volume_diff int64, high_McCabe_sum_diff int64, high_McCabe_max_before int64, simplifiable-condition int64, Blank_before int64, high_ccp_group int64, McCabe_max_before int64, bugs_diff int64, too-many-nested-blocks int64, refactor_mle_diff int64, difficulty_diff int64, LLOC_diff int64, LOC_diff int64, simplifiable-if-statement int64, one_file_fix_rate_diff int64, SLOC_before int64, LOC_before int64, mostly_delete int64, changed_lines int64, Single comments_before int64, removed_lines int64, added_functions int64, h1_diff int64, effort_diff int64, hunks_num int64, Multi_diff int64, same_day_duration_avg_diff int64, N2_diff int64, cur_count_y int64, Comments_diff int64, modified_McCabe_max_diff int64, h2_diff int64, time_diff int64, LLOC_before int64, calculated_length_diff int64, Single comments_after int64, massive_change int64, McCabe_sum_before int64, too-many-boolean-expressions int64, Simplify-boolean-expression int64, line-too-long int64, superfluous-parens int64, low_ccp_group int64, McCabe_max_diff int64, comparison-of-constants int64, high_McCabe_sum_before int64, low_McCabe_sum_diff int64, avg_coupling_code_size_cut_diff int64, is_refactor int64, Single comments_diff int64, unnecessary-semicolon int64, added_lines int64, prev_count_y int64, try-except-raise int64, low_McCabe_sum_before int64, vocabulary_diff int64, too-many-branches int64, McCabe_sum_after int64, broad-exception-caught int64, prev_count_x int64, only_removal int64, McCabe_max_after int64, pointless-statement int64, low_McCabe_max_before int64, too-many-lines int64, McCabe_sum_diff int64, high_McCabe_max_diff int64, using-constant-test int64, SLOC_diff int64, Blank_diff int64, Comments_after int64, cur_count_x int64, unnecessary-pass int64, too-many-statements int64, Comments_before int64) as (
  case when refactor_mle_diff <= 0.5782583355903625 then
    case when Comments_after <= 8.5 then
      case when SLOC_before <= 156.5 then
        case when added_lines <= 6.5 then
           return 1.0 # (1.0 out of 1.0)
        else  # if added_lines > 6.5
           return 0.36363636363636365 # (0.36363636363636365 out of 1.0)
        end       else  # if SLOC_before > 156.5
         return 0.9230769230769231 # (0.9230769230769231 out of 1.0)
      end     else  # if Comments_after > 8.5
      case when high_ccp_group <= 0.5 then
        case when length_diff <= -199.0 then
           return 0.95 # (0.95 out of 1.0)
        else  # if length_diff > -199.0
          case when Comments_diff <= 20.5 then
            case when low_McCabe_max_before <= 0.5 then
              case when low_ccp_group <= 0.5 then
                case when changed_lines <= 135.0 then
                  case when SLOC_before <= 261.0 then
                     return 0.19047619047619047 # (0.19047619047619047 out of 1.0)
                  else  # if SLOC_before > 261.0
                    case when Comments_before <= 197.5 then
                      case when LLOC_diff <= -29.5 then
                         return 0.1111111111111111 # (0.1111111111111111 out of 1.0)
                      else  # if LLOC_diff > -29.5
                        case when McCabe_max_after <= 26.5 then
                          case when Blank_before <= 149.5 then
                             return 0.25 # (0.25 out of 1.0)
                          else  # if Blank_before > 149.5
                             return 0.6785714285714286 # (0.6785714285714286 out of 1.0)
                          end                         else  # if McCabe_max_after > 26.5
                           return 0.8214285714285714 # (0.8214285714285714 out of 1.0)
                        end                       end                     else  # if Comments_before > 197.5
                       return 0.058823529411764705 # (0.058823529411764705 out of 1.0)
                    end                   end                 else  # if changed_lines > 135.0
                  case when refactor_mle_diff <= -0.18887000530958176 then
                     return 0.29411764705882354 # (0.29411764705882354 out of 1.0)
                  else  # if refactor_mle_diff > -0.18887000530958176
                    case when Single comments_diff <= -0.5 then
                       return 0.8928571428571429 # (0.8928571428571429 out of 1.0)
                    else  # if Single comments_diff > -0.5
                       return 0.7083333333333334 # (0.7083333333333334 out of 1.0)
                    end                   end                 end               else  # if low_ccp_group > 0.5
                case when h2_diff <= -9.0 then
                   return 0.23809523809523808 # (0.23809523809523808 out of 1.0)
                else  # if h2_diff > -9.0
                  case when Comments_after <= 217.5 then
                    case when Single comments_after <= 13.0 then
                       return 0.06666666666666667 # (0.06666666666666667 out of 1.0)
                    else  # if Single comments_after > 13.0
                       return 0.0 # (0.0 out of 1.0)
                    end                   else  # if Comments_after > 217.5
                     return 0.1111111111111111 # (0.1111111111111111 out of 1.0)
                  end                 end               end             else  # if low_McCabe_max_before > 0.5
              case when length_diff <= -8.5 then
                 return 0.7692307692307693 # (0.7692307692307693 out of 1.0)
              else  # if length_diff > -8.5
                case when McCabe_max_after <= 7.5 then
                   return 0.53125 # (0.53125 out of 1.0)
                else  # if McCabe_max_after > 7.5
                  case when removed_lines <= 17.0 then
                     return 0.1875 # (0.1875 out of 1.0)
                  else  # if removed_lines > 17.0
                     return 0.5294117647058824 # (0.5294117647058824 out of 1.0)
                  end                 end               end             end           else  # if Comments_diff > 20.5
             return 0.9 # (0.9 out of 1.0)
          end         end       else  # if high_ccp_group > 0.5
        case when N2_diff <= -29.0 then
           return 0.2631578947368421 # (0.2631578947368421 out of 1.0)
        else  # if N2_diff > -29.0
          case when McCabe_sum_before <= 135.0 then
             return 1.0 # (1.0 out of 1.0)
          else  # if McCabe_sum_before > 135.0
            case when LOC_before <= 1009.0 then
               return 0.36363636363636365 # (0.36363636363636365 out of 1.0)
            else  # if LOC_before > 1009.0
               return 0.95 # (0.95 out of 1.0)
            end           end         end       end     end   else  # if refactor_mle_diff > 0.5782583355903625
     return 0.13636363636363635 # (0.13636363636363635 out of 1.0)
  end )