create or replace function RandomForest_7 (LOC_diff int64, Comments_after int64, volume_diff int64, LOC_before int64, McCabe_max_diff int64, Blank_diff int64, unnecessary-pass int64, McCabe_max_before int64, prev_count_x int64, prev_count_y int64, N2_diff int64, LLOC_before int64, prev_count int64, too-many-branches int64, added_functions int64, length_diff int64, h2_diff int64, removed_lines int64, too-many-nested-blocks int64, comparison-of-constants int64, bugs_diff int64, N1_diff int64, Comments_diff int64, line-too-long int64, McCabe_sum_diff int64, superfluous-parens int64, Multi_diff int64, changed_lines int64, McCabe_sum_before int64, calculated_length_diff int64, Single comments_after int64, time_diff int64, Single comments_diff int64, Comments_before int64, added_lines int64, effort_diff int64, refactor_mle_diff int64, Blank_before int64, too-many-return-statements int64, pointless-statement int64, too-many-statements int64, cur_count_y int64, unnecessary-semicolon int64, cur_count_x int64, using-constant-test int64, McCabe_sum_after int64, McCabe_max_after int64, too-many-lines int64, LLOC_diff int64, difficulty_diff int64, simplifiable-if-statement int64, vocabulary_diff int64, SLOC_before int64, modified_McCabe_max_diff int64, wildcard-import int64, one_file_fix_rate_diff int64, simplifiable-condition int64, SLOC_diff int64, h1_diff int64, same_day_duration_avg_diff int64, Single comments_before int64, cur_count int64, try-except-raise int64, Simplify-boolean-expression int64, simplifiable-if-expression int64, broad-exception-caught int64, hunks_num int64, too-many-boolean-expressions int64, avg_coupling_code_size_cut_diff int64) as (
  case when hunks_num <= 13.5 then
    case when LLOC_diff <= 1.5 then
      case when pointless-statement <= 0.5 then
        case when changed_lines <= 135.0 then
          case when too-many-boolean-expressions <= 0.5 then
            case when same_day_duration_avg_diff <= 7.510956287384033 then
              case when one_file_fix_rate_diff <= -0.025132276117801666 then
                case when refactor_mle_diff <= 0.05038394033908844 then
                  case when prev_count_x <= 1.5 then
                    case when Comments_after <= 39.0 then
                      case when same_day_duration_avg_diff <= -43.564626693725586 then
                         return 0.28205128205128205 # (11.0 out of 39.0)
                      else  # if same_day_duration_avg_diff > -43.564626693725586
                        case when same_day_duration_avg_diff <= -32.38319396972656 then
                           return 0.8 # (12.0 out of 15.0)
                        else  # if same_day_duration_avg_diff > -32.38319396972656
                           return 0.5686274509803921 # (29.0 out of 51.0)
                        end                       end                     else  # if Comments_after > 39.0
                       return 0.35714285714285715 # (5.0 out of 14.0)
                    end                   else  # if prev_count_x > 1.5
                     return 0.6792452830188679 # (36.0 out of 53.0)
                  end                 else  # if refactor_mle_diff > 0.05038394033908844
                  case when same_day_duration_avg_diff <= -84.84803771972656 then
                     return 0.5 # (8.0 out of 16.0)
                  else  # if same_day_duration_avg_diff > -84.84803771972656
                    case when one_file_fix_rate_diff <= -0.2547619119286537 then
                       return 0.5882352941176471 # (10.0 out of 17.0)
                    else  # if one_file_fix_rate_diff > -0.2547619119286537
                       return 0.8787878787878788 # (29.0 out of 33.0)
                    end                   end                 end               else  # if one_file_fix_rate_diff > -0.025132276117801666
                case when unnecessary-pass <= 0.5 then
                  case when SLOC_before <= 433.0 then
                    case when McCabe_max_after <= 12.5 then
                      case when too-many-lines <= 0.5 then
                        case when one_file_fix_rate_diff <= 0.2797619104385376 then
                          case when one_file_fix_rate_diff <= 0.20317460596561432 then
                            case when LLOC_diff <= -7.0 then
                               return 0.16666666666666666 # (2.0 out of 12.0)
                            else  # if LLOC_diff > -7.0
                              case when superfluous-parens <= 0.5 then
                                case when one_file_fix_rate_diff <= 0.12083333358168602 then
                                  case when same_day_duration_avg_diff <= 0.9656955003738403 then
                                    case when one_file_fix_rate_diff <= 0.0773809552192688 then
                                      case when too-many-branches <= 0.5 then
                                        case when line-too-long <= 0.5 then
                                          case when refactor_mle_diff <= 0.19839682430028915 then
                                            case when same_day_duration_avg_diff <= -7.950486660003662 then
                                              case when same_day_duration_avg_diff <= -41.52437400817871 then
                                                case when same_day_duration_avg_diff <= -108.54670333862305 then
                                                   return 0.4117647058823529 # (7.0 out of 17.0)
                                                else  # if same_day_duration_avg_diff > -108.54670333862305
                                                   return 0.3125 # (5.0 out of 16.0)
                                                end                                               else  # if same_day_duration_avg_diff > -41.52437400817871
                                                 return 0.6 # (9.0 out of 15.0)
                                              end                                             else  # if same_day_duration_avg_diff > -7.950486660003662
                                               return 0.2222222222222222 # (4.0 out of 18.0)
                                            end                                           else  # if refactor_mle_diff > 0.19839682430028915
                                             return 0.7857142857142857 # (11.0 out of 14.0)
                                          end                                         else  # if line-too-long > 0.5
                                          case when prev_count_x <= 2.5 then
                                             return 0.3611111111111111 # (13.0 out of 36.0)
                                          else  # if prev_count_x > 2.5
                                             return 0.19230769230769232 # (5.0 out of 26.0)
                                          end                                         end                                       else  # if too-many-branches > 0.5
                                         return 0.3333333333333333 # (7.0 out of 21.0)
                                      end                                     else  # if one_file_fix_rate_diff > 0.0773809552192688
                                       return 0.13636363636363635 # (3.0 out of 22.0)
                                    end                                   else  # if same_day_duration_avg_diff > 0.9656955003738403
                                     return 0.6538461538461539 # (17.0 out of 26.0)
                                  end                                 else  # if one_file_fix_rate_diff > 0.12083333358168602
                                  case when too-many-statements <= 0.5 then
                                     return 0.4 # (10.0 out of 25.0)
                                  else  # if too-many-statements > 0.5
                                     return 0.76 # (19.0 out of 25.0)
                                  end                                 end                               else  # if superfluous-parens > 0.5
                                 return 0.6078431372549019 # (31.0 out of 51.0)
                              end                             end                           else  # if one_file_fix_rate_diff > 0.20317460596561432
                             return 0.21052631578947367 # (4.0 out of 19.0)
                          end                         else  # if one_file_fix_rate_diff > 0.2797619104385376
                          case when cur_count_x <= 3.5 then
                            case when avg_coupling_code_size_cut_diff <= 0.8295454680919647 then
                              case when one_file_fix_rate_diff <= 0.6458333432674408 then
                                 return 0.6981132075471698 # (37.0 out of 53.0)
                              else  # if one_file_fix_rate_diff > 0.6458333432674408
                                 return 0.4666666666666667 # (7.0 out of 15.0)
                              end                             else  # if avg_coupling_code_size_cut_diff > 0.8295454680919647
                               return 0.4 # (8.0 out of 20.0)
                            end                           else  # if cur_count_x > 3.5
                             return 0.3125 # (5.0 out of 16.0)
                          end                         end                       else  # if too-many-lines > 0.5
                         return 0.25 # (7.0 out of 28.0)
                      end                     else  # if McCabe_max_after > 12.5
                       return 0.7222222222222222 # (13.0 out of 18.0)
                    end                   else  # if SLOC_before > 433.0
                    case when refactor_mle_diff <= 0.054954493418335915 then
                      case when vocabulary_diff <= -2.0 then
                         return 0.1 # (2.0 out of 20.0)
                      else  # if vocabulary_diff > -2.0
                        case when same_day_duration_avg_diff <= -46.558332443237305 then
                           return 0.22727272727272727 # (5.0 out of 22.0)
                        else  # if same_day_duration_avg_diff > -46.558332443237305
                           return 0.21428571428571427 # (3.0 out of 14.0)
                        end                       end                     else  # if refactor_mle_diff > 0.054954493418335915
                       return 0.5714285714285714 # (8.0 out of 14.0)
                    end                   end                 else  # if unnecessary-pass > 0.5
                  case when one_file_fix_rate_diff <= 0.055555556900799274 then
                     return 0.5555555555555556 # (10.0 out of 18.0)
                  else  # if one_file_fix_rate_diff > 0.055555556900799274
                     return 0.68 # (17.0 out of 25.0)
                  end                 end               end             else  # if same_day_duration_avg_diff > 7.510956287384033
              case when McCabe_sum_diff <= -11.0 then
                 return 0.0 # (0.0 out of 25.0)
              else  # if McCabe_sum_diff > -11.0
                case when McCabe_sum_before <= 99.5 then
                  case when added_lines <= 23.0 then
                    case when added_lines <= 3.0 then
                      case when prev_count_x <= 18.0 then
                        case when prev_count_x <= 1.5 then
                          case when same_day_duration_avg_diff <= 22.34083843231201 then
                            case when refactor_mle_diff <= 0.06065925769507885 then
                              case when one_file_fix_rate_diff <= -0.02500000037252903 then
                                 return 0.2857142857142857 # (6.0 out of 21.0)
                              else  # if one_file_fix_rate_diff > -0.02500000037252903
                                 return 0.13636363636363635 # (3.0 out of 22.0)
                              end                             else  # if refactor_mle_diff > 0.06065925769507885
                               return 0.4 # (10.0 out of 25.0)
                            end                           else  # if same_day_duration_avg_diff > 22.34083843231201
                            case when too-many-statements <= 0.5 then
                               return 0.4473684210526316 # (85.0 out of 190.0)
                            else  # if too-many-statements > 0.5
                               return 0.5285714285714286 # (37.0 out of 70.0)
                            end                           end                         else  # if prev_count_x > 1.5
                           return 0.23129251700680273 # (34.0 out of 147.0)
                        end                       else  # if prev_count_x > 18.0
                         return 0.72 # (18.0 out of 25.0)
                      end                     else  # if added_lines > 3.0
                       return 0.0 # (0.0 out of 23.0)
                    end                   else  # if added_lines > 23.0
                     return 0.6428571428571429 # (9.0 out of 14.0)
                  end                 else  # if McCabe_sum_before > 99.5
                  case when N2_diff <= -3.5 then
                     return 0.8 # (12.0 out of 15.0)
                  else  # if N2_diff > -3.5
                    case when same_day_duration_avg_diff <= 51.09544372558594 then
                       return 0.15789473684210525 # (3.0 out of 19.0)
                    else  # if same_day_duration_avg_diff > 51.09544372558594
                       return 0.6521739130434783 # (15.0 out of 23.0)
                    end                   end                 end               end             end           else  # if too-many-boolean-expressions > 0.5
            case when refactor_mle_diff <= -0.031073163263499737 then
               return 0.25 # (5.0 out of 20.0)
            else  # if refactor_mle_diff > -0.031073163263499737
               return 0.0625 # (1.0 out of 16.0)
            end           end         else  # if changed_lines > 135.0
          case when Comments_diff <= 0.5 then
            case when hunks_num <= 2.5 then
               return 0.42857142857142855 # (6.0 out of 14.0)
            else  # if hunks_num > 2.5
              case when McCabe_max_diff <= -3.0 then
                 return 1.0 # (35.0 out of 35.0)
              else  # if McCabe_max_diff > -3.0
                 return 0.7 # (21.0 out of 30.0)
              end             end           else  # if Comments_diff > 0.5
             return 0.38461538461538464 # (10.0 out of 26.0)
          end         end       else  # if pointless-statement > 0.5
         return 0.7435897435897436 # (29.0 out of 39.0)
      end     else  # if LLOC_diff > 1.5
      case when cur_count_y <= 0.5 then
        case when McCabe_max_before <= 11.5 then
          case when same_day_duration_avg_diff <= 10.757922649383545 then
             return 0.7142857142857143 # (10.0 out of 14.0)
          else  # if same_day_duration_avg_diff > 10.757922649383545
             return 0.8571428571428571 # (18.0 out of 21.0)
          end         else  # if McCabe_max_before > 11.5
          case when vocabulary_diff <= 0.5 then
             return 0.6666666666666666 # (18.0 out of 27.0)
          else  # if vocabulary_diff > 0.5
             return 0.2692307692307692 # (7.0 out of 26.0)
          end         end       else  # if cur_count_y > 0.5
         return 1.0 # (19.0 out of 19.0)
      end     end   else  # if hunks_num > 13.5
    case when vocabulary_diff <= -2.0 then
      case when McCabe_sum_before <= 150.5 then
         return 0.0 # (0.0 out of 13.0)
      else  # if McCabe_sum_before > 150.5
         return 0.1111111111111111 # (3.0 out of 27.0)
      end     else  # if vocabulary_diff > -2.0
      case when LOC_before <= 1076.0 then
         return 0.125 # (2.0 out of 16.0)
      else  # if LOC_before > 1076.0
         return 0.5714285714285714 # (8.0 out of 14.0)
      end     end   end )