create or replace function Tree_ms50 (low_McCabe_max_before int64, LLOC_before int64, low_McCabe_sum_diff int64, modified_McCabe_max_diff int64, bugs_diff int64, McCabe_max_before int64, Single comments_before int64, prev_count_y int64, added_lines int64, LLOC_diff int64, N2_diff int64, added_functions int64, prev_count int64, too-many-boolean-expressions int64, SLOC_diff int64, mostly_delete int64, time_diff int64, calculated_length_diff int64, McCabe_max_after int64, Comments_diff int64, line-too-long int64, McCabe_sum_after int64, one_file_fix_rate_diff int64, h1_diff int64, high_McCabe_max_diff int64, too-many-branches int64, SLOC_before int64, cur_count_y int64, prev_count_x int64, McCabe_sum_before int64, Comments_after int64, wildcard-import int64, unnecessary-semicolon int64, same_day_duration_avg_diff int64, effort_diff int64, too-many-statements int64, broad-exception-caught int64, LOC_before int64, cur_count int64, Comments_before int64, using-constant-test int64, LOC_diff int64, high_McCabe_sum_diff int64, only_removal int64, superfluous-parens int64, try-except-raise int64, Blank_before int64, McCabe_max_diff int64, N1_diff int64, massive_change int64, refactor_mle_diff int64, pointless-statement int64, too-many-lines int64, simplifiable-if-statement int64, high_McCabe_sum_before int64, vocabulary_diff int64, removed_lines int64, difficulty_diff int64, Simplify-boolean-expression int64, avg_coupling_code_size_cut_diff int64, Single comments_after int64, low_ccp_group int64, Multi_diff int64, is_refactor int64, hunks_num int64, Single comments_diff int64, length_diff int64, unnecessary-pass int64, Blank_diff int64, h2_diff int64, changed_lines int64, cur_count_x int64, low_McCabe_max_diff int64, high_McCabe_max_before int64, high_ccp_group int64, too-many-nested-blocks int64, McCabe_sum_diff int64, volume_diff int64, comparison-of-constants int64, too-many-return-statements int64, simplifiable-condition int64, simplifiable-if-expression int64, low_McCabe_sum_before int64) as (
  case when low_ccp_group <= 0.5 then
    case when Comments_before <= 369.0 then
      case when same_day_duration_avg_diff <= 310.1000061035156 then
        case when prev_count_x <= 3.5 then
          case when McCabe_sum_after <= 60.5 then
            case when Comments_after <= 51.0 then
              case when SLOC_before <= 153.0 then
                case when SLOC_before <= 112.5 then
                  case when Comments_after <= 5.0 then
                     return 1.0 # (1.0 out of 1.0)
                  else  # if Comments_after > 5.0
                     return 0.9230769230769231 # (0.9230769230769231 out of 1.0)
                  end                 else  # if SLOC_before > 112.5
                   return 0.625 # (0.625 out of 1.0)
                end               else  # if SLOC_before > 153.0
                case when changed_lines <= 19.5 then
                   return 0.8181818181818182 # (0.8181818181818182 out of 1.0)
                else  # if changed_lines > 19.5
                  case when Multi_diff <= -5.0 then
                     return 0.9642857142857143 # (0.9642857142857143 out of 1.0)
                  else  # if Multi_diff > -5.0
                     return 1.0 # (1.0 out of 1.0)
                  end                 end               end             else  # if Comments_after > 51.0
               return 0.75 # (0.75 out of 1.0)
            end           else  # if McCabe_sum_after > 60.5
            case when LLOC_before <= 521.0 then
              case when refactor_mle_diff <= -0.1126132495701313 then
                case when SLOC_before <= 664.0 then
                  case when Single comments_diff <= 0.5 then
                    case when changed_lines <= 119.5 then
                      case when hunks_num <= 2.5 then
                         return 0.8181818181818182 # (0.8181818181818182 out of 1.0)
                      else  # if hunks_num > 2.5
                         return 0.23076923076923078 # (0.23076923076923078 out of 1.0)
                      end                     else  # if changed_lines > 119.5
                       return 0.9310344827586207 # (0.9310344827586207 out of 1.0)
                    end                   else  # if Single comments_diff > 0.5
                     return 0.0 # (0.0 out of 1.0)
                  end                 else  # if SLOC_before > 664.0
                   return 0.0 # (0.0 out of 1.0)
                end               else  # if refactor_mle_diff > -0.1126132495701313
                case when Single comments_after <= 58.5 then
                  case when McCabe_sum_after <= 181.0 then
                    case when hunks_num <= 6.5 then
                      case when refactor_mle_diff <= 0.16808952391147614 then
                        case when added_lines <= 10.5 then
                           return 0.975 # (0.975 out of 1.0)
                        else  # if added_lines > 10.5
                           return 0.75 # (0.75 out of 1.0)
                        end                       else  # if refactor_mle_diff > 0.16808952391147614
                         return 0.5769230769230769 # (0.5769230769230769 out of 1.0)
                      end                     else  # if hunks_num > 6.5
                      case when SLOC_before <= 377.0 then
                         return 0.9642857142857143 # (0.9642857142857143 out of 1.0)
                      else  # if SLOC_before > 377.0
                         return 1.0 # (1.0 out of 1.0)
                      end                     end                   else  # if McCabe_sum_after > 181.0
                     return 0.42857142857142855 # (0.42857142857142855 out of 1.0)
                  end                 else  # if Single comments_after > 58.5
                  case when Blank_before <= 112.0 then
                     return 0.14285714285714285 # (0.14285714285714285 out of 1.0)
                  else  # if Blank_before > 112.0
                     return 0.8571428571428571 # (0.8571428571428571 out of 1.0)
                  end                 end               end             else  # if LLOC_before > 521.0
              case when added_lines <= 380.0 then
                case when LOC_before <= 1629.0 then
                  case when LOC_before <= 1372.5 then
                    case when one_file_fix_rate_diff <= -0.0055555556900799274 then
                       return 0.7272727272727273 # (0.7272727272727273 out of 1.0)
                    else  # if one_file_fix_rate_diff > -0.0055555556900799274
                      case when avg_coupling_code_size_cut_diff <= -0.28958334028720856 then
                         return 0.84375 # (0.84375 out of 1.0)
                      else  # if avg_coupling_code_size_cut_diff > -0.28958334028720856
                         return 1.0 # (1.0 out of 1.0)
                      end                     end                   else  # if LOC_before > 1372.5
                     return 0.5714285714285714 # (0.5714285714285714 out of 1.0)
                  end                 else  # if LOC_before > 1629.0
                  case when one_file_fix_rate_diff <= 0.06111111305654049 then
                    case when refactor_mle_diff <= -0.049152785912156105 then
                       return 0.9642857142857143 # (0.9642857142857143 out of 1.0)
                    else  # if refactor_mle_diff > -0.049152785912156105
                       return 1.0 # (1.0 out of 1.0)
                    end                   else  # if one_file_fix_rate_diff > 0.06111111305654049
                     return 0.9130434782608695 # (0.9130434782608695 out of 1.0)
                  end                 end               else  # if added_lines > 380.0
                 return 0.5714285714285714 # (0.5714285714285714 out of 1.0)
              end             end           end         else  # if prev_count_x > 3.5
           return 0.25 # (0.25 out of 1.0)
        end       else  # if same_day_duration_avg_diff > 310.1000061035156
         return 0.21428571428571427 # (0.21428571428571427 out of 1.0)
      end     else  # if Comments_before > 369.0
       return 0.2608695652173913 # (0.2608695652173913 out of 1.0)
    end   else  # if low_ccp_group > 0.5
    case when same_day_duration_avg_diff <= 5.808960437774658 then
      case when same_day_duration_avg_diff <= -33.06060600280762 then
         return 0.0 # (0.0 out of 1.0)
      else  # if same_day_duration_avg_diff > -33.06060600280762
        case when same_day_duration_avg_diff <= -21.621904373168945 then
           return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
        else  # if same_day_duration_avg_diff > -21.621904373168945
          case when avg_coupling_code_size_cut_diff <= 2.220446049250313e-16 then
             return 0.42857142857142855 # (0.42857142857142855 out of 1.0)
          else  # if avg_coupling_code_size_cut_diff > 2.220446049250313e-16
             return 0.0 # (0.0 out of 1.0)
          end         end       end     else  # if same_day_duration_avg_diff > 5.808960437774658
      case when Comments_before <= 21.5 then
         return 0.0 # (0.0 out of 1.0)
      else  # if Comments_before > 21.5
        case when Blank_diff <= 2.0 then
          case when removed_lines <= 16.5 then
             return 0.42857142857142855 # (0.42857142857142855 out of 1.0)
          else  # if removed_lines > 16.5
            case when McCabe_max_before <= 14.0 then
               return 1.0 # (1.0 out of 1.0)
            else  # if McCabe_max_before > 14.0
               return 0.8571428571428571 # (0.8571428571428571 out of 1.0)
            end           end         else  # if Blank_diff > 2.0
           return 0.0 # (0.0 out of 1.0)
        end       end     end   end )