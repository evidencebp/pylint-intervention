create or replace function RandomForest_8 (LOC_diff int64, Comments_after int64, volume_diff int64, LOC_before int64, McCabe_max_diff int64, Blank_diff int64, unnecessary-pass int64, McCabe_max_before int64, prev_count_x int64, prev_count_y int64, N2_diff int64, LLOC_before int64, prev_count int64, too-many-branches int64, added_functions int64, length_diff int64, h2_diff int64, removed_lines int64, too-many-nested-blocks int64, comparison-of-constants int64, bugs_diff int64, N1_diff int64, Comments_diff int64, line-too-long int64, McCabe_sum_diff int64, superfluous-parens int64, Multi_diff int64, changed_lines int64, McCabe_sum_before int64, calculated_length_diff int64, Single comments_after int64, time_diff int64, Single comments_diff int64, Comments_before int64, added_lines int64, effort_diff int64, refactor_mle_diff int64, Blank_before int64, too-many-return-statements int64, pointless-statement int64, too-many-statements int64, cur_count_y int64, unnecessary-semicolon int64, cur_count_x int64, using-constant-test int64, McCabe_sum_after int64, McCabe_max_after int64, too-many-lines int64, LLOC_diff int64, difficulty_diff int64, simplifiable-if-statement int64, vocabulary_diff int64, SLOC_before int64, modified_McCabe_max_diff int64, wildcard-import int64, one_file_fix_rate_diff int64, simplifiable-condition int64, SLOC_diff int64, h1_diff int64, same_day_duration_avg_diff int64, Single comments_before int64, cur_count int64, try-except-raise int64, Simplify-boolean-expression int64, simplifiable-if-expression int64, broad-exception-caught int64, hunks_num int64, too-many-boolean-expressions int64, avg_coupling_code_size_cut_diff int64) as (
  case when same_day_duration_avg_diff <= -65.9481201171875 then
    case when h2_diff <= 0.5 then
      case when McCabe_max_diff <= -1.5 then
         return 0.5909090909090909 # (13.0 out of 22.0)
      else  # if McCabe_max_diff > -1.5
        case when LOC_before <= 1001.5 then
          case when cur_count_x <= 0.5 then
            case when McCabe_max_after <= 7.5 then
              case when avg_coupling_code_size_cut_diff <= 0.20416667312383652 then
                 return 0.6842105263157895 # (13.0 out of 19.0)
              else  # if avg_coupling_code_size_cut_diff > 0.20416667312383652
                 return 0.5454545454545454 # (6.0 out of 11.0)
              end             else  # if McCabe_max_after > 7.5
               return 0.41379310344827586 # (12.0 out of 29.0)
            end           else  # if cur_count_x > 0.5
            case when prev_count_x <= 8.5 then
              case when avg_coupling_code_size_cut_diff <= -0.7576389014720917 then
                case when avg_coupling_code_size_cut_diff <= -1.550000011920929 then
                   return 0.25 # (7.0 out of 28.0)
                else  # if avg_coupling_code_size_cut_diff > -1.550000011920929
                   return 0.6 # (12.0 out of 20.0)
                end               else  # if avg_coupling_code_size_cut_diff > -0.7576389014720917
                case when line-too-long <= 0.5 then
                  case when cur_count_x <= 1.5 then
                     return 0.31 # (31.0 out of 100.0)
                  else  # if cur_count_x > 1.5
                     return 0.047619047619047616 # (1.0 out of 21.0)
                  end                 else  # if line-too-long > 0.5
                  case when refactor_mle_diff <= -0.014366666786372662 then
                     return 0.05263157894736842 # (1.0 out of 19.0)
                  else  # if refactor_mle_diff > -0.014366666786372662
                     return 0.16 # (4.0 out of 25.0)
                  end                 end               end             else  # if prev_count_x > 8.5
               return 0.5 # (10.0 out of 20.0)
            end           end         else  # if LOC_before > 1001.5
           return 0.0 # (0.0 out of 35.0)
        end       end     else  # if h2_diff > 0.5
       return 0.7916666666666666 # (19.0 out of 24.0)
    end   else  # if same_day_duration_avg_diff > -65.9481201171875
    case when prev_count_x <= 64.5 then
      case when modified_McCabe_max_diff <= -23.5 then
         return 1.0 # (17.0 out of 17.0)
      else  # if modified_McCabe_max_diff > -23.5
        case when changed_lines <= 350.5 then
          case when same_day_duration_avg_diff <= -11.644011974334717 then
            case when McCabe_max_after <= 6.5 then
              case when cur_count_x <= 11.5 then
                case when changed_lines <= 48.0 then
                  case when too-many-branches <= 0.5 then
                    case when one_file_fix_rate_diff <= 0.207341268658638 then
                       return 0.5833333333333334 # (119.0 out of 204.0)
                    else  # if one_file_fix_rate_diff > 0.207341268658638
                       return 0.7777777777777778 # (35.0 out of 45.0)
                    end                   else  # if too-many-branches > 0.5
                     return 0.8095238095238095 # (17.0 out of 21.0)
                  end                 else  # if changed_lines > 48.0
                   return 1.0 # (15.0 out of 15.0)
                end               else  # if cur_count_x > 11.5
                 return 1.0 # (21.0 out of 21.0)
              end             else  # if McCabe_max_after > 6.5
              case when refactor_mle_diff <= -0.14789215475320816 then
                 return 0.1935483870967742 # (6.0 out of 31.0)
              else  # if refactor_mle_diff > -0.14789215475320816
                case when McCabe_max_after <= 21.5 then
                  case when SLOC_before <= 599.0 then
                     return 0.3448275862068966 # (10.0 out of 29.0)
                  else  # if SLOC_before > 599.0
                     return 0.7857142857142857 # (11.0 out of 14.0)
                  end                 else  # if McCabe_max_after > 21.5
                  case when SLOC_before <= 691.0 then
                     return 0.5 # (8.0 out of 16.0)
                  else  # if SLOC_before > 691.0
                     return 0.8823529411764706 # (15.0 out of 17.0)
                  end                 end               end             end           else  # if same_day_duration_avg_diff > -11.644011974334717
            case when LOC_diff <= -113.5 then
               return 0.8888888888888888 # (24.0 out of 27.0)
            else  # if LOC_diff > -113.5
              case when refactor_mle_diff <= 0.18000096827745438 then
                case when avg_coupling_code_size_cut_diff <= 1.227543294429779 then
                  case when Single comments_diff <= -2.5 then
                     return 0.8333333333333334 # (20.0 out of 24.0)
                  else  # if Single comments_diff > -2.5
                    case when changed_lines <= 74.5 then
                      case when Comments_before <= 25.0 then
                        case when superfluous-parens <= 0.5 then
                          case when cur_count_x <= 11.0 then
                            case when same_day_duration_avg_diff <= 147.5952377319336 then
                              case when same_day_duration_avg_diff <= 63.73611068725586 then
                                case when cur_count_x <= 3.5 then
                                  case when avg_coupling_code_size_cut_diff <= 0.7750000059604645 then
                                    case when Single comments_before <= 5.0 then
                                      case when refactor_mle_diff <= -0.09476111829280853 then
                                         return 0.6666666666666666 # (40.0 out of 60.0)
                                      else  # if refactor_mle_diff > -0.09476111829280853
                                        case when same_day_duration_avg_diff <= -2.5723443031311035 then
                                           return 0.2 # (4.0 out of 20.0)
                                        else  # if same_day_duration_avg_diff > -2.5723443031311035
                                           return 0.4666666666666667 # (49.0 out of 105.0)
                                        end                                       end                                     else  # if Single comments_before > 5.0
                                       return 0.16666666666666666 # (3.0 out of 18.0)
                                    end                                   else  # if avg_coupling_code_size_cut_diff > 0.7750000059604645
                                     return 0.23076923076923078 # (3.0 out of 13.0)
                                  end                                 else  # if cur_count_x > 3.5
                                   return 0.17647058823529413 # (3.0 out of 17.0)
                                end                               else  # if same_day_duration_avg_diff > 63.73611068725586
                                case when line-too-long <= 0.5 then
                                  case when avg_coupling_code_size_cut_diff <= -0.22584033757448196 then
                                     return 0.0 # (0.0 out of 22.0)
                                  else  # if avg_coupling_code_size_cut_diff > -0.22584033757448196
                                     return 0.05263157894736842 # (1.0 out of 19.0)
                                  end                                 else  # if line-too-long > 0.5
                                   return 0.21428571428571427 # (3.0 out of 14.0)
                                end                               end                             else  # if same_day_duration_avg_diff > 147.5952377319336
                               return 0.5862068965517241 # (34.0 out of 58.0)
                            end                           else  # if cur_count_x > 11.0
                             return 0.8095238095238095 # (17.0 out of 21.0)
                          end                         else  # if superfluous-parens > 0.5
                          case when one_file_fix_rate_diff <= 0.043417368084192276 then
                            case when prev_count_x <= 0.5 then
                               return 0.30434782608695654 # (7.0 out of 23.0)
                            else  # if prev_count_x > 0.5
                               return 0.32 # (8.0 out of 25.0)
                            end                           else  # if one_file_fix_rate_diff > 0.043417368084192276
                             return 0.16 # (4.0 out of 25.0)
                          end                         end                       else  # if Comments_before > 25.0
                        case when Single comments_diff <= 0.5 then
                          case when refactor_mle_diff <= -0.09686616435647011 then
                             return 0.7368421052631579 # (14.0 out of 19.0)
                          else  # if refactor_mle_diff > -0.09686616435647011
                            case when McCabe_sum_after <= 103.5 then
                               return 0.25 # (4.0 out of 16.0)
                            else  # if McCabe_sum_after > 103.5
                               return 0.4375 # (7.0 out of 16.0)
                            end                           end                         else  # if Single comments_diff > 0.5
                           return 0.85 # (17.0 out of 20.0)
                        end                       end                     else  # if changed_lines > 74.5
                      case when SLOC_diff <= 2.5 then
                         return 0.0 # (0.0 out of 30.0)
                      else  # if SLOC_diff > 2.5
                         return 0.45454545454545453 # (10.0 out of 22.0)
                      end                     end                   end                 else  # if avg_coupling_code_size_cut_diff > 1.227543294429779
                  case when hunks_num <= 1.5 then
                    case when avg_coupling_code_size_cut_diff <= 3.285714268684387 then
                      case when one_file_fix_rate_diff <= 0.08571428805589676 then
                        case when refactor_mle_diff <= -0.09266811236739159 then
                           return 0.5357142857142857 # (15.0 out of 28.0)
                        else  # if refactor_mle_diff > -0.09266811236739159
                          case when cur_count_x <= 0.5 then
                             return 1.0 # (12.0 out of 12.0)
                          else  # if cur_count_x > 0.5
                             return 0.8205128205128205 # (32.0 out of 39.0)
                          end                         end                       else  # if one_file_fix_rate_diff > 0.08571428805589676
                         return 0.5789473684210527 # (11.0 out of 19.0)
                      end                     else  # if avg_coupling_code_size_cut_diff > 3.285714268684387
                       return 0.26666666666666666 # (4.0 out of 15.0)
                    end                   else  # if hunks_num > 1.5
                     return 0.2777777777777778 # (5.0 out of 18.0)
                  end                 end               else  # if refactor_mle_diff > 0.18000096827745438
                case when McCabe_sum_before <= 135.0 then
                  case when refactor_mle_diff <= 0.3114452213048935 then
                    case when prev_count_x <= 1.5 then
                      case when superfluous-parens <= 0.5 then
                        case when avg_coupling_code_size_cut_diff <= -0.17882118374109268 then
                           return 0.35294117647058826 # (6.0 out of 17.0)
                        else  # if avg_coupling_code_size_cut_diff > -0.17882118374109268
                           return 0.07692307692307693 # (2.0 out of 26.0)
                        end                       else  # if superfluous-parens > 0.5
                         return 0.6 # (12.0 out of 20.0)
                      end                     else  # if prev_count_x > 1.5
                       return 0.19230769230769232 # (5.0 out of 26.0)
                    end                   else  # if refactor_mle_diff > 0.3114452213048935
                     return 0.453125 # (29.0 out of 64.0)
                  end                 else  # if McCabe_sum_before > 135.0
                  case when LLOC_diff <= -1.0 then
                     return 0.0 # (0.0 out of 19.0)
                  else  # if LLOC_diff > -1.0
                     return 0.3076923076923077 # (4.0 out of 13.0)
                  end                 end               end             end           end         else  # if changed_lines > 350.5
          case when Comments_before <= 105.5 then
            case when prev_count <= 1.5 then
               return 0.25925925925925924 # (7.0 out of 27.0)
            else  # if prev_count > 1.5
               return 0.0 # (0.0 out of 16.0)
            end           else  # if Comments_before > 105.5
             return 0.5 # (11.0 out of 22.0)
          end         end       end     else  # if prev_count_x > 64.5
       return 0.09090909090909091 # (2.0 out of 22.0)
    end   end )