create or replace function RandomForest_0 (LOC_diff int64, Comments_after int64, volume_diff int64, LOC_before int64, McCabe_max_diff int64, Blank_diff int64, unnecessary-pass int64, McCabe_max_before int64, prev_count_x int64, prev_count_y int64, N2_diff int64, LLOC_before int64, prev_count int64, too-many-branches int64, added_functions int64, length_diff int64, h2_diff int64, removed_lines int64, too-many-nested-blocks int64, comparison-of-constants int64, bugs_diff int64, N1_diff int64, Comments_diff int64, line-too-long int64, McCabe_sum_diff int64, superfluous-parens int64, Multi_diff int64, changed_lines int64, McCabe_sum_before int64, calculated_length_diff int64, Single comments_after int64, time_diff int64, Single comments_diff int64, Comments_before int64, added_lines int64, effort_diff int64, refactor_mle_diff int64, Blank_before int64, too-many-return-statements int64, pointless-statement int64, too-many-statements int64, cur_count_y int64, unnecessary-semicolon int64, cur_count_x int64, using-constant-test int64, McCabe_sum_after int64, McCabe_max_after int64, too-many-lines int64, LLOC_diff int64, difficulty_diff int64, simplifiable-if-statement int64, vocabulary_diff int64, SLOC_before int64, modified_McCabe_max_diff int64, wildcard-import int64, one_file_fix_rate_diff int64, simplifiable-condition int64, SLOC_diff int64, h1_diff int64, same_day_duration_avg_diff int64, Single comments_before int64, cur_count int64, try-except-raise int64, Simplify-boolean-expression int64, simplifiable-if-expression int64, broad-exception-caught int64, hunks_num int64, too-many-boolean-expressions int64, avg_coupling_code_size_cut_diff int64) as (
  case when hunks_num <= 10.5 then
    case when Blank_diff <= -52.0 then
       return 0.875 # (21.0 out of 24.0)
    else  # if Blank_diff > -52.0
      case when prev_count_x <= 20.0 then
        case when prev_count_x <= 3.5 then
          case when pointless-statement <= 0.5 then
            case when cur_count <= 0.5 then
              case when Single comments_diff <= 21.0 then
                case when Blank_diff <= -12.5 then
                   return 0.7307692307692307 # (19.0 out of 26.0)
                else  # if Blank_diff > -12.5
                  case when N2_diff <= -25.0 then
                     return 0.22727272727272727 # (5.0 out of 22.0)
                  else  # if N2_diff > -25.0
                    case when SLOC_diff <= -39.5 then
                       return 0.16 # (4.0 out of 25.0)
                    else  # if SLOC_diff > -39.5
                      case when Single comments_diff <= 2.5 then
                        case when one_file_fix_rate_diff <= 0.7638888955116272 then
                          case when same_day_duration_avg_diff <= 9.157827854156494 then
                            case when Blank_before <= 266.0 then
                              case when McCabe_sum_before <= 191.5 then
                                case when McCabe_sum_diff <= -0.5 then
                                  case when changed_lines <= 47.0 then
                                     return 0.043478260869565216 # (1.0 out of 23.0)
                                  else  # if changed_lines > 47.0
                                     return 0.4117647058823529 # (7.0 out of 17.0)
                                  end                                 else  # if McCabe_sum_diff > -0.5
                                  case when Comments_before <= 37.5 then
                                    case when cur_count_x <= 2.5 then
                                      case when refactor_mle_diff <= -0.2513136565685272 then
                                        case when one_file_fix_rate_diff <= -0.08493589982390404 then
                                           return 0.15789473684210525 # (3.0 out of 19.0)
                                        else  # if one_file_fix_rate_diff > -0.08493589982390404
                                          case when refactor_mle_diff <= -0.5553842186927795 then
                                             return 0.75 # (12.0 out of 16.0)
                                          else  # if refactor_mle_diff > -0.5553842186927795
                                             return 0.2727272727272727 # (12.0 out of 44.0)
                                          end                                         end                                       else  # if refactor_mle_diff > -0.2513136565685272
                                        case when hunks_num <= 0.5 then
                                          case when simplifiable-if-expression <= 0.5 then
                                            case when Blank_before <= 40.0 then
                                              case when too-many-branches <= 0.5 then
                                                case when same_day_duration_avg_diff <= -25.851388931274414 then
                                                   return 0.44081632653061226 # (108.0 out of 245.0)
                                                else  # if same_day_duration_avg_diff > -25.851388931274414
                                                  case when same_day_duration_avg_diff <= -5.301136255264282 then
                                                    case when refactor_mle_diff <= -0.022762672044336796 then
                                                       return 0.7096774193548387 # (22.0 out of 31.0)
                                                    else  # if refactor_mle_diff > -0.022762672044336796
                                                       return 0.8666666666666667 # (39.0 out of 45.0)
                                                    end                                                   else  # if same_day_duration_avg_diff > -5.301136255264282
                                                    case when too-many-statements <= 0.5 then
                                                       return 0.43859649122807015 # (25.0 out of 57.0)
                                                    else  # if too-many-statements > 0.5
                                                       return 0.6 # (18.0 out of 30.0)
                                                    end                                                   end                                                 end                                               else  # if too-many-branches > 0.5
                                                 return 0.6808510638297872 # (32.0 out of 47.0)
                                              end                                             else  # if Blank_before > 40.0
                                               return 0.2857142857142857 # (4.0 out of 14.0)
                                            end                                           else  # if simplifiable-if-expression > 0.5
                                             return 0.4444444444444444 # (8.0 out of 18.0)
                                          end                                         else  # if hunks_num > 0.5
                                           return 0.7586206896551724 # (22.0 out of 29.0)
                                        end                                       end                                     else  # if cur_count_x > 2.5
                                       return 0.18518518518518517 # (5.0 out of 27.0)
                                    end                                   else  # if Comments_before > 37.5
                                     return 0.18518518518518517 # (5.0 out of 27.0)
                                  end                                 end                               else  # if McCabe_sum_before > 191.5
                                 return 0.9090909090909091 # (30.0 out of 33.0)
                              end                             else  # if Blank_before > 266.0
                               return 0.2222222222222222 # (6.0 out of 27.0)
                            end                           else  # if same_day_duration_avg_diff > 9.157827854156494
                            case when LOC_before <= 17.0 then
                              case when cur_count_x <= 0.5 then
                                 return 0.4838709677419355 # (15.0 out of 31.0)
                              else  # if cur_count_x > 0.5
                                case when avg_coupling_code_size_cut_diff <= -2.908333420753479 then
                                   return 0.058823529411764705 # (1.0 out of 17.0)
                                else  # if avg_coupling_code_size_cut_diff > -2.908333420753479
                                  case when too-many-statements <= 0.5 then
                                    case when refactor_mle_diff <= -0.2921983152627945 then
                                      case when avg_coupling_code_size_cut_diff <= 0.0833333358168602 then
                                         return 0.5263157894736842 # (10.0 out of 19.0)
                                      else  # if avg_coupling_code_size_cut_diff > 0.0833333358168602
                                         return 0.5294117647058824 # (9.0 out of 17.0)
                                      end                                     else  # if refactor_mle_diff > -0.2921983152627945
                                      case when line-too-long <= 0.5 then
                                        case when cur_count_x <= 1.5 then
                                          case when superfluous-parens <= 0.5 then
                                             return 0.2835820895522388 # (38.0 out of 134.0)
                                          else  # if superfluous-parens > 0.5
                                            case when same_day_duration_avg_diff <= 43.75 then
                                               return 0.21428571428571427 # (6.0 out of 28.0)
                                            else  # if same_day_duration_avg_diff > 43.75
                                               return 0.782608695652174 # (18.0 out of 23.0)
                                            end                                           end                                         else  # if cur_count_x > 1.5
                                          case when avg_coupling_code_size_cut_diff <= 0.16152745857834816 then
                                             return 0.26666666666666666 # (4.0 out of 15.0)
                                          else  # if avg_coupling_code_size_cut_diff > 0.16152745857834816
                                             return 0.10526315789473684 # (2.0 out of 19.0)
                                          end                                         end                                       else  # if line-too-long > 0.5
                                        case when one_file_fix_rate_diff <= -0.04692082107067108 then
                                           return 0.38095238095238093 # (8.0 out of 21.0)
                                        else  # if one_file_fix_rate_diff > -0.04692082107067108
                                           return 0.5 # (12.0 out of 24.0)
                                        end                                       end                                     end                                   else  # if too-many-statements > 0.5
                                    case when avg_coupling_code_size_cut_diff <= -0.25824176520109177 then
                                       return 0.6666666666666666 # (12.0 out of 18.0)
                                    else  # if avg_coupling_code_size_cut_diff > -0.25824176520109177
                                      case when avg_coupling_code_size_cut_diff <= 0.4689514487981796 then
                                         return 0.15 # (3.0 out of 20.0)
                                      else  # if avg_coupling_code_size_cut_diff > 0.4689514487981796
                                         return 0.1 # (2.0 out of 20.0)
                                      end                                     end                                   end                                 end                               end                             else  # if LOC_before > 17.0
                              case when Single comments_after <= 18.5 then
                                 return 0.696969696969697 # (23.0 out of 33.0)
                              else  # if Single comments_after > 18.5
                                case when avg_coupling_code_size_cut_diff <= 0.34166666865348816 then
                                  case when avg_coupling_code_size_cut_diff <= -0.17607759311795235 then
                                     return 0.5416666666666666 # (13.0 out of 24.0)
                                  else  # if avg_coupling_code_size_cut_diff > -0.17607759311795235
                                     return 0.13793103448275862 # (4.0 out of 29.0)
                                  end                                 else  # if avg_coupling_code_size_cut_diff > 0.34166666865348816
                                   return 0.8333333333333334 # (15.0 out of 18.0)
                                end                               end                             end                           end                         else  # if one_file_fix_rate_diff > 0.7638888955116272
                           return 0.6842105263157895 # (26.0 out of 38.0)
                        end                       else  # if Single comments_diff > 2.5
                         return 0.0 # (0.0 out of 20.0)
                      end                     end                   end                 end               else  # if Single comments_diff > 21.0
                 return 0.8888888888888888 # (16.0 out of 18.0)
              end             else  # if cur_count > 0.5
               return 0.8888888888888888 # (24.0 out of 27.0)
            end           else  # if pointless-statement > 0.5
             return 0.7317073170731707 # (30.0 out of 41.0)
          end         else  # if prev_count_x > 3.5
          case when added_lines <= 0.5 then
            case when refactor_mle_diff <= 0.16145890206098557 then
              case when avg_coupling_code_size_cut_diff <= -0.9886363744735718 then
                 return 0.7 # (14.0 out of 20.0)
              else  # if avg_coupling_code_size_cut_diff > -0.9886363744735718
                case when prev_count_x <= 7.5 then
                  case when same_day_duration_avg_diff <= 7.059090614318848 then
                     return 0.0 # (0.0 out of 25.0)
                  else  # if same_day_duration_avg_diff > 7.059090614318848
                     return 0.07142857142857142 # (1.0 out of 14.0)
                  end                 else  # if prev_count_x > 7.5
                   return 0.4117647058823529 # (14.0 out of 34.0)
                end               end             else  # if refactor_mle_diff > 0.16145890206098557
               return 0.6 # (12.0 out of 20.0)
            end           else  # if added_lines > 0.5
             return 0.0 # (0.0 out of 21.0)
          end         end       else  # if prev_count_x > 20.0
        case when refactor_mle_diff <= 0.004684782586991787 then
          case when avg_coupling_code_size_cut_diff <= -0.7190476357936859 then
             return 0.5833333333333334 # (7.0 out of 12.0)
          else  # if avg_coupling_code_size_cut_diff > -0.7190476357936859
             return 0.6666666666666666 # (8.0 out of 12.0)
          end         else  # if refactor_mle_diff > 0.004684782586991787
           return 0.8518518518518519 # (23.0 out of 27.0)
        end       end     end   else  # if hunks_num > 10.5
    case when SLOC_before <= 406.5 then
       return 0.8461538461538461 # (11.0 out of 13.0)
    else  # if SLOC_before > 406.5
      case when SLOC_before <= 979.0 then
        case when added_lines <= 215.0 then
          case when LOC_diff <= -20.0 then
             return 0.05555555555555555 # (1.0 out of 18.0)
          else  # if LOC_diff > -20.0
             return 0.0 # (0.0 out of 42.0)
          end         else  # if added_lines > 215.0
           return 0.21739130434782608 # (5.0 out of 23.0)
        end       else  # if SLOC_before > 979.0
        case when McCabe_sum_diff <= -3.0 then
           return 0.1111111111111111 # (2.0 out of 18.0)
        else  # if McCabe_sum_diff > -3.0
           return 0.7142857142857143 # (15.0 out of 21.0)
        end       end     end   end )