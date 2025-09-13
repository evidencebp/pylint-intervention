create or replace function Tree_ms50 (prev_count int64, simplifiable-if-expression int64, N1_diff int64, cur_count int64, wildcard-import int64, too-many-return-statements int64, low_McCabe_max_diff int64, length_diff int64, volume_diff int64, high_McCabe_sum_diff int64, high_McCabe_max_before int64, simplifiable-condition int64, Blank_before int64, high_ccp_group int64, McCabe_max_before int64, bugs_diff int64, too-many-nested-blocks int64, refactor_mle_diff int64, difficulty_diff int64, LLOC_diff int64, LOC_diff int64, simplifiable-if-statement int64, one_file_fix_rate_diff int64, SLOC_before int64, LOC_before int64, mostly_delete int64, changed_lines int64, Single comments_before int64, removed_lines int64, added_functions int64, h1_diff int64, effort_diff int64, hunks_num int64, Multi_diff int64, same_day_duration_avg_diff int64, N2_diff int64, cur_count_y int64, Comments_diff int64, modified_McCabe_max_diff int64, h2_diff int64, time_diff int64, LLOC_before int64, calculated_length_diff int64, Single comments_after int64, massive_change int64, McCabe_sum_before int64, too-many-boolean-expressions int64, Simplify-boolean-expression int64, line-too-long int64, superfluous-parens int64, low_ccp_group int64, McCabe_max_diff int64, comparison-of-constants int64, high_McCabe_sum_before int64, low_McCabe_sum_diff int64, avg_coupling_code_size_cut_diff int64, is_refactor int64, Single comments_diff int64, unnecessary-semicolon int64, added_lines int64, prev_count_y int64, try-except-raise int64, low_McCabe_sum_before int64, vocabulary_diff int64, too-many-branches int64, McCabe_sum_after int64, broad-exception-caught int64, prev_count_x int64, only_removal int64, McCabe_max_after int64, pointless-statement int64, low_McCabe_max_before int64, too-many-lines int64, McCabe_sum_diff int64, high_McCabe_max_diff int64, using-constant-test int64, SLOC_diff int64, Blank_diff int64, Comments_after int64, cur_count_x int64, unnecessary-pass int64, too-many-statements int64, Comments_before int64) as (
  case when low_ccp_group <= 0.5 then
    case when Blank_before <= 53.5 then
      case when Blank_diff <= -1.5 then
         return 0.4 # (0.4 out of 1.0)
      else  # if Blank_diff > -1.5
        case when refactor_mle_diff <= -0.20850324630737305 then
           return 0.6 # (0.6 out of 1.0)
        else  # if refactor_mle_diff > -0.20850324630737305
          case when refactor_mle_diff <= 0.2076636329293251 then
            case when McCabe_sum_after <= 35.0 then
               return 1.0 # (1.0 out of 1.0)
            else  # if McCabe_sum_after > 35.0
               return 0.8333333333333334 # (0.8333333333333334 out of 1.0)
            end           else  # if refactor_mle_diff > 0.2076636329293251
             return 0.7 # (0.7 out of 1.0)
          end         end       end     else  # if Blank_before > 53.5
      case when Comments_before <= 405.0 then
        case when prev_count_y <= 4.5 then
          case when refactor_mle_diff <= -0.10912862047553062 then
            case when removed_lines <= 158.5 then
              case when one_file_fix_rate_diff <= 0.34166666865348816 then
                case when removed_lines <= 1.5 then
                   return 0.2222222222222222 # (0.2222222222222222 out of 1.0)
                else  # if removed_lines > 1.5
                  case when LOC_before <= 1136.0 then
                    case when Comments_before <= 29.0 then
                       return 0.9375 # (0.9375 out of 1.0)
                    else  # if Comments_before > 29.0
                      case when refactor_mle_diff <= -0.20215881615877151 then
                         return 0.17647058823529413 # (0.17647058823529413 out of 1.0)
                      else  # if refactor_mle_diff > -0.20215881615877151
                         return 0.6 # (0.6 out of 1.0)
                      end                     end                   else  # if LOC_before > 1136.0
                    case when LOC_before <= 1893.0 then
                       return 1.0 # (1.0 out of 1.0)
                    else  # if LOC_before > 1893.0
                       return 0.8 # (0.8 out of 1.0)
                    end                   end                 end               else  # if one_file_fix_rate_diff > 0.34166666865348816
                 return 0.058823529411764705 # (0.058823529411764705 out of 1.0)
              end             else  # if removed_lines > 158.5
               return 0.05555555555555555 # (0.05555555555555555 out of 1.0)
            end           else  # if refactor_mle_diff > -0.10912862047553062
            case when refactor_mle_diff <= 0.5782583355903625 then
              case when Blank_diff <= -40.0 then
                case when h1_diff <= -5.0 then
                   return 0.9 # (0.9 out of 1.0)
                else  # if h1_diff > -5.0
                   return 1.0 # (1.0 out of 1.0)
                end               else  # if Blank_diff > -40.0
                case when Blank_diff <= -26.5 then
                   return 0.2 # (0.2 out of 1.0)
                else  # if Blank_diff > -26.5
                  case when Comments_diff <= 6.0 then
                    case when McCabe_sum_diff <= 8.5 then
                      case when high_ccp_group <= 0.5 then
                        case when changed_lines <= 160.0 then
                          case when one_file_fix_rate_diff <= 0.1114766076207161 then
                            case when LOC_before <= 803.0 then
                              case when SLOC_diff <= 0.5 then
                                 return 0.7 # (0.7 out of 1.0)
                              else  # if SLOC_diff > 0.5
                                 return 0.23076923076923078 # (0.23076923076923078 out of 1.0)
                              end                             else  # if LOC_before > 803.0
                              case when McCabe_sum_before <= 138.5 then
                                 return 1.0 # (1.0 out of 1.0)
                              else  # if McCabe_sum_before > 138.5
                                 return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
                              end                             end                           else  # if one_file_fix_rate_diff > 0.1114766076207161
                            case when same_day_duration_avg_diff <= 3.0796958655118942 then
                               return 0.5384615384615384 # (0.5384615384615384 out of 1.0)
                            else  # if same_day_duration_avg_diff > 3.0796958655118942
                               return 0.1 # (0.1 out of 1.0)
                            end                           end                         else  # if changed_lines > 160.0
                           return 1.0 # (1.0 out of 1.0)
                        end                       else  # if high_ccp_group > 0.5
                        case when N2_diff <= -3.0 then
                           return 0.6923076923076923 # (0.6923076923076923 out of 1.0)
                        else  # if N2_diff > -3.0
                          case when Single comments_after <= 119.0 then
                             return 1.0 # (1.0 out of 1.0)
                          else  # if Single comments_after > 119.0
                             return 0.9 # (0.9 out of 1.0)
                          end                         end                       end                     else  # if McCabe_sum_diff > 8.5
                       return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
                    end                   else  # if Comments_diff > 6.0
                     return 0.25 # (0.25 out of 1.0)
                  end                 end               end             else  # if refactor_mle_diff > 0.5782583355903625
               return 0.2631578947368421 # (0.2631578947368421 out of 1.0)
            end           end         else  # if prev_count_y > 4.5
           return 0.0 # (0.0 out of 1.0)
        end       else  # if Comments_before > 405.0
         return 0.0625 # (0.0625 out of 1.0)
      end     end   else  # if low_ccp_group > 0.5
    case when Single comments_diff <= 20.5 then
      case when Single comments_diff <= -18.5 then
         return 1.0 # (1.0 out of 1.0)
      else  # if Single comments_diff > -18.5
        case when added_lines <= 12.5 then
          case when same_day_duration_avg_diff <= -30.548755645751953 then
             return 0.0 # (0.0 out of 1.0)
          else  # if same_day_duration_avg_diff > -30.548755645751953
            case when LLOC_diff <= 1.0 then
               return 0.2 # (0.2 out of 1.0)
            else  # if LLOC_diff > 1.0
               return 0.7 # (0.7 out of 1.0)
            end           end         else  # if added_lines > 12.5
          case when refactor_mle_diff <= -0.2031647190451622 then
            case when McCabe_max_diff <= -1.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if McCabe_max_diff > -1.5
               return 0.3 # (0.3 out of 1.0)
            end           else  # if refactor_mle_diff > -0.2031647190451622
             return 0.0 # (0.0 out of 1.0)
          end         end       end     else  # if Single comments_diff > 20.5
       return 0.9411764705882353 # (0.9411764705882353 out of 1.0)
    end   end )