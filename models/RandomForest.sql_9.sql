create or replace function RandomForest_9 (McCabe_sum_before int64, changed_lines int64, prev_count_y int64, mostly_delete int64, h1_diff int64, too-many-lines int64, low_McCabe_sum_before int64, length_diff int64, LOC_before int64, simplifiable-if-expression int64, added_functions int64, broad-exception-caught int64, simplifiable-condition int64, prev_count_x int64, McCabe_max_diff int64, SLOC_before int64, LLOC_before int64, low_McCabe_max_diff int64, bugs_diff int64, same_day_duration_avg_diff int64, cur_count_x int64, only_removal int64, McCabe_max_after int64, Single comments_after int64, low_ccp_group int64, one_file_fix_rate_diff int64, effort_diff int64, difficulty_diff int64, removed_lines int64, Comments_diff int64, too-many-boolean-expressions int64, refactor_mle_diff int64, high_McCabe_max_before int64, hunks_num int64, LOC_diff int64, SLOC_diff int64, cur_count_y int64, vocabulary_diff int64, using-constant-test int64, Simplify-boolean-expression int64, low_McCabe_max_before int64, high_McCabe_sum_diff int64, high_McCabe_sum_before int64, McCabe_max_before int64, Comments_after int64, McCabe_sum_diff int64, unnecessary-pass int64, avg_coupling_code_size_cut_diff int64, simplifiable-if-statement int64, is_refactor int64, volume_diff int64, added_lines int64, high_McCabe_max_diff int64, superfluous-parens int64, cur_count int64, low_McCabe_sum_diff int64, calculated_length_diff int64, Multi_diff int64, N2_diff int64, h2_diff int64, Single comments_before int64, McCabe_sum_after int64, N1_diff int64, too-many-statements int64, comparison-of-constants int64, pointless-statement int64, time_diff int64, prev_count int64, Single comments_diff int64, massive_change int64, Blank_diff int64, too-many-nested-blocks int64, Comments_before int64, modified_McCabe_max_diff int64, LLOC_diff int64, Blank_before int64, try-except-raise int64, too-many-branches int64, too-many-return-statements int64, unnecessary-semicolon int64, wildcard-import int64, high_ccp_group int64, line-too-long int64) as (
  case when Single comments_after <= 4.5 then
    case when McCabe_sum_before <= 30.5 then
       return 0.9545454545454546 # (0.9545454545454546 out of 1.0)
    else  # if McCabe_sum_before > 30.5
       return 0.8 # (0.8 out of 1.0)
    end   else  # if Single comments_after > 4.5
    case when too-many-return-statements <= 0.5 then
      case when same_day_duration_avg_diff <= 277.68055725097656 then
        case when Comments_diff <= -2.5 then
          case when Comments_before <= 43.0 then
            case when LOC_before <= 300.0 then
               return 1.0 # (1.0 out of 1.0)
            else  # if LOC_before > 300.0
               return 0.8095238095238095 # (0.8095238095238095 out of 1.0)
            end           else  # if Comments_before > 43.0
            case when Comments_diff <= -20.5 then
              case when low_McCabe_max_diff <= 0.5 then
                 return 0.26666666666666666 # (0.26666666666666666 out of 1.0)
              else  # if low_McCabe_max_diff > 0.5
                 return 0.92 # (0.92 out of 1.0)
              end             else  # if Comments_diff > -20.5
              case when low_ccp_group <= 0.5 then
                 return 0.53125 # (0.53125 out of 1.0)
              else  # if low_ccp_group > 0.5
                 return 0.13636363636363635 # (0.13636363636363635 out of 1.0)
              end             end           end         else  # if Comments_diff > -2.5
          case when LLOC_before <= 879.0 then
            case when vocabulary_diff <= -2.5 then
              case when McCabe_sum_after <= 127.5 then
                case when LLOC_before <= 353.5 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if LLOC_before > 353.5
                   return 0.13333333333333333 # (0.13333333333333333 out of 1.0)
                end               else  # if McCabe_sum_after > 127.5
                 return 0.0 # (0.0 out of 1.0)
              end             else  # if vocabulary_diff > -2.5
              case when low_ccp_group <= 0.5 then
                case when Comments_after <= 62.5 then
                  case when same_day_duration_avg_diff <= 38.014957427978516 then
                    case when Single comments_before <= 20.5 then
                       return 0.43478260869565216 # (0.43478260869565216 out of 1.0)
                    else  # if Single comments_before > 20.5
                      case when Comments_before <= 46.5 then
                        case when changed_lines <= 28.0 then
                           return 0.76 # (0.76 out of 1.0)
                        else  # if changed_lines > 28.0
                           return 0.9523809523809523 # (0.9523809523809523 out of 1.0)
                        end                       else  # if Comments_before > 46.5
                         return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
                      end                     end                   else  # if same_day_duration_avg_diff > 38.014957427978516
                     return 0.17647058823529413 # (0.17647058823529413 out of 1.0)
                  end                 else  # if Comments_after > 62.5
                  case when high_ccp_group <= 0.5 then
                     return 0.24242424242424243 # (0.24242424242424243 out of 1.0)
                  else  # if high_ccp_group > 0.5
                     return 0.42857142857142855 # (0.42857142857142855 out of 1.0)
                  end                 end               else  # if low_ccp_group > 0.5
                case when Comments_diff <= 4.5 then
                  case when LLOC_diff <= 1.5 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if LLOC_diff > 1.5
                     return 0.2777777777777778 # (0.2777777777777778 out of 1.0)
                  end                 else  # if Comments_diff > 4.5
                   return 0.5 # (0.5 out of 1.0)
                end               end             end           else  # if LLOC_before > 879.0
            case when McCabe_sum_before <= 634.0 then
              case when added_lines <= 4.5 then
                 return 0.3888888888888889 # (0.3888888888888889 out of 1.0)
              else  # if added_lines > 4.5
                case when McCabe_sum_after <= 379.5 then
                   return 0.782608695652174 # (0.782608695652174 out of 1.0)
                else  # if McCabe_sum_after > 379.5
                   return 0.9411764705882353 # (0.9411764705882353 out of 1.0)
                end               end             else  # if McCabe_sum_before > 634.0
               return 0.4 # (0.4 out of 1.0)
            end           end         end       else  # if same_day_duration_avg_diff > 277.68055725097656
         return 0.0 # (0.0 out of 1.0)
      end     else  # if too-many-return-statements > 0.5
       return 0.0 # (0.0 out of 1.0)
    end   end )