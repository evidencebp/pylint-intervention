create or replace function RandomForest_2 (LOC_diff int64, Comments_after int64, volume_diff int64, LOC_before int64, McCabe_max_diff int64, Blank_diff int64, unnecessary-pass int64, McCabe_max_before int64, prev_count_x int64, prev_count_y int64, N2_diff int64, LLOC_before int64, prev_count int64, too-many-branches int64, added_functions int64, length_diff int64, h2_diff int64, removed_lines int64, too-many-nested-blocks int64, comparison-of-constants int64, bugs_diff int64, N1_diff int64, Comments_diff int64, line-too-long int64, McCabe_sum_diff int64, superfluous-parens int64, Multi_diff int64, changed_lines int64, McCabe_sum_before int64, calculated_length_diff int64, Single comments_after int64, time_diff int64, Single comments_diff int64, Comments_before int64, added_lines int64, effort_diff int64, refactor_mle_diff int64, Blank_before int64, too-many-return-statements int64, pointless-statement int64, too-many-statements int64, cur_count_y int64, unnecessary-semicolon int64, cur_count_x int64, using-constant-test int64, McCabe_sum_after int64, McCabe_max_after int64, too-many-lines int64, LLOC_diff int64, difficulty_diff int64, simplifiable-if-statement int64, vocabulary_diff int64, SLOC_before int64, modified_McCabe_max_diff int64, wildcard-import int64, one_file_fix_rate_diff int64, simplifiable-condition int64, SLOC_diff int64, h1_diff int64, same_day_duration_avg_diff int64, Single comments_before int64, cur_count int64, try-except-raise int64, Simplify-boolean-expression int64, simplifiable-if-expression int64, broad-exception-caught int64, hunks_num int64, too-many-boolean-expressions int64, avg_coupling_code_size_cut_diff int64) as (
  case when Single comments_diff <= -16.5 then
    case when LLOC_diff <= -327.5 then
       return 0.47368421052631576 # (9.0 out of 19.0)
    else  # if LLOC_diff > -327.5
       return 1.0 # (25.0 out of 25.0)
    end   else  # if Single comments_diff > -16.5
    case when McCabe_sum_diff <= -9.5 then
      case when refactor_mle_diff <= -0.06832268089056015 then
        case when removed_lines <= 11.0 then
           return 0.0 # (0.0 out of 20.0)
        else  # if removed_lines > 11.0
          case when McCabe_sum_before <= 232.5 then
             return 0.16 # (4.0 out of 25.0)
          else  # if McCabe_sum_before > 232.5
             return 0.0 # (0.0 out of 14.0)
          end         end       else  # if refactor_mle_diff > -0.06832268089056015
        case when hunks_num <= 12.0 then
          case when LOC_diff <= -95.5 then
             return 0.85 # (17.0 out of 20.0)
          else  # if LOC_diff > -95.5
             return 0.36363636363636365 # (8.0 out of 22.0)
          end         else  # if hunks_num > 12.0
           return 0.1 # (2.0 out of 20.0)
        end       end     else  # if McCabe_sum_diff > -9.5
      case when cur_count_y <= 0.5 then
        case when pointless-statement <= 0.5 then
          case when SLOC_diff <= 35.0 then
            case when same_day_duration_avg_diff <= -0.8374999761581421 then
              case when McCabe_max_after <= 8.0 then
                case when refactor_mle_diff <= 0.2355090007185936 then
                  case when McCabe_sum_after <= 6.5 then
                     return 0.5346715328467153 # (293.0 out of 548.0)
                  else  # if McCabe_sum_after > 6.5
                     return 0.8571428571428571 # (18.0 out of 21.0)
                  end                 else  # if refactor_mle_diff > 0.2355090007185936
                   return 0.359375 # (23.0 out of 64.0)
                end               else  # if McCabe_max_after > 8.0
                case when McCabe_sum_after <= 148.5 then
                  case when hunks_num <= 2.5 then
                     return 0.4444444444444444 # (8.0 out of 18.0)
                  else  # if hunks_num > 2.5
                    case when changed_lines <= 86.0 then
                      case when LLOC_before <= 335.0 then
                         return 0.23529411764705882 # (4.0 out of 17.0)
                      else  # if LLOC_before > 335.0
                         return 0.13333333333333333 # (2.0 out of 15.0)
                      end                     else  # if changed_lines > 86.0
                       return 0.047619047619047616 # (1.0 out of 21.0)
                    end                   end                 else  # if McCabe_sum_after > 148.5
                  case when Blank_before <= 162.5 then
                    case when refactor_mle_diff <= -0.059156863018870354 then
                       return 0.7 # (14.0 out of 20.0)
                    else  # if refactor_mle_diff > -0.059156863018870354
                       return 0.7777777777777778 # (14.0 out of 18.0)
                    end                   else  # if Blank_before > 162.5
                    case when LOC_diff <= 2.5 then
                       return 0.12 # (3.0 out of 25.0)
                    else  # if LOC_diff > 2.5
                       return 0.8571428571428571 # (12.0 out of 14.0)
                    end                   end                 end               end             else  # if same_day_duration_avg_diff > -0.8374999761581421
              case when McCabe_sum_before <= 357.0 then
                case when refactor_mle_diff <= -0.3475697785615921 then
                   return 0.2127659574468085 # (10.0 out of 47.0)
                else  # if refactor_mle_diff > -0.3475697785615921
                  case when SLOC_diff <= 1.5 then
                    case when prev_count <= 0.5 then
                      case when refactor_mle_diff <= -0.2921983152627945 then
                         return 0.7368421052631579 # (14.0 out of 19.0)
                      else  # if refactor_mle_diff > -0.2921983152627945
                        case when too-many-lines <= 0.5 then
                          case when too-many-statements <= 0.5 then
                            case when prev_count_x <= 33.5 then
                              case when prev_count_x <= 4.5 then
                                case when too-many-branches <= 0.5 then
                                   return 0.4080267558528428 # (122.0 out of 299.0)
                                else  # if too-many-branches > 0.5
                                  case when same_day_duration_avg_diff <= 32.62916660308838 then
                                     return 0.3181818181818182 # (7.0 out of 22.0)
                                  else  # if same_day_duration_avg_diff > 32.62916660308838
                                     return 0.55 # (11.0 out of 20.0)
                                  end                                 end                               else  # if prev_count_x > 4.5
                                case when avg_coupling_code_size_cut_diff <= -0.2817460373044014 then
                                   return 0.35714285714285715 # (5.0 out of 14.0)
                                else  # if avg_coupling_code_size_cut_diff > -0.2817460373044014
                                   return 0.3333333333333333 # (5.0 out of 15.0)
                                end                               end                             else  # if prev_count_x > 33.5
                               return 0.16666666666666666 # (3.0 out of 18.0)
                            end                           else  # if too-many-statements > 0.5
                            case when prev_count_x <= 0.5 then
                              case when one_file_fix_rate_diff <= -0.1190476231276989 then
                                 return 0.5294117647058824 # (9.0 out of 17.0)
                              else  # if one_file_fix_rate_diff > -0.1190476231276989
                                case when same_day_duration_avg_diff <= 38.04495620727539 then
                                   return 0.24 # (6.0 out of 25.0)
                                else  # if same_day_duration_avg_diff > 38.04495620727539
                                   return 0.0 # (0.0 out of 18.0)
                                end                               end                             else  # if prev_count_x > 0.5
                              case when same_day_duration_avg_diff <= 82.14285659790039 then
                                 return 0.5384615384615384 # (14.0 out of 26.0)
                              else  # if same_day_duration_avg_diff > 82.14285659790039
                                 return 0.2926829268292683 # (12.0 out of 41.0)
                              end                             end                           end                         else  # if too-many-lines > 0.5
                           return 0.5263157894736842 # (10.0 out of 19.0)
                        end                       end                     else  # if prev_count > 0.5
                      case when Single comments_after <= 29.5 then
                         return 0.7333333333333333 # (22.0 out of 30.0)
                      else  # if Single comments_after > 29.5
                        case when one_file_fix_rate_diff <= -0.001923076924867928 then
                           return 0.21739130434782608 # (5.0 out of 23.0)
                        else  # if one_file_fix_rate_diff > -0.001923076924867928
                          case when SLOC_diff <= -5.5 then
                             return 0.6666666666666666 # (12.0 out of 18.0)
                          else  # if SLOC_diff > -5.5
                             return 0.5 # (9.0 out of 18.0)
                          end                         end                       end                     end                   else  # if SLOC_diff > 1.5
                    case when SLOC_before <= 620.0 then
                      case when removed_lines <= 25.0 then
                         return 0.125 # (2.0 out of 16.0)
                      else  # if removed_lines > 25.0
                         return 0.0 # (0.0 out of 14.0)
                      end                     else  # if SLOC_before > 620.0
                       return 0.3125 # (5.0 out of 16.0)
                    end                   end                 end               else  # if McCabe_sum_before > 357.0
                 return 0.7142857142857143 # (20.0 out of 28.0)
              end             end           else  # if SLOC_diff > 35.0
            case when LOC_diff <= 66.0 then
               return 1.0 # (17.0 out of 17.0)
            else  # if LOC_diff > 66.0
              case when Blank_diff <= 12.0 then
                 return 0.3888888888888889 # (7.0 out of 18.0)
              else  # if Blank_diff > 12.0
                 return 0.7333333333333333 # (11.0 out of 15.0)
              end             end           end         else  # if pointless-statement > 0.5
          case when prev_count_x <= 0.5 then
             return 0.9411764705882353 # (16.0 out of 17.0)
          else  # if prev_count_x > 0.5
             return 0.7142857142857143 # (15.0 out of 21.0)
          end         end       else  # if cur_count_y > 0.5
         return 0.9565217391304348 # (22.0 out of 23.0)
      end     end   end )