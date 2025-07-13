create or replace function Tree_default (LOC_diff int64, Comments_after int64, volume_diff int64, LOC_before int64, McCabe_max_diff int64, Blank_diff int64, unnecessary-pass int64, McCabe_max_before int64, prev_count_x int64, prev_count_y int64, N2_diff int64, LLOC_before int64, prev_count int64, too-many-branches int64, added_functions int64, length_diff int64, h2_diff int64, removed_lines int64, too-many-nested-blocks int64, comparison-of-constants int64, bugs_diff int64, N1_diff int64, Comments_diff int64, line-too-long int64, McCabe_sum_diff int64, superfluous-parens int64, Multi_diff int64, changed_lines int64, McCabe_sum_before int64, calculated_length_diff int64, Single comments_after int64, time_diff int64, Single comments_diff int64, Comments_before int64, added_lines int64, effort_diff int64, refactor_mle_diff int64, Blank_before int64, too-many-return-statements int64, pointless-statement int64, too-many-statements int64, cur_count_y int64, unnecessary-semicolon int64, cur_count_x int64, using-constant-test int64, McCabe_sum_after int64, McCabe_max_after int64, too-many-lines int64, LLOC_diff int64, difficulty_diff int64, simplifiable-if-statement int64, vocabulary_diff int64, SLOC_before int64, modified_McCabe_max_diff int64, wildcard-import int64, one_file_fix_rate_diff int64, simplifiable-condition int64, SLOC_diff int64, h1_diff int64, same_day_duration_avg_diff int64, Single comments_before int64, cur_count int64, try-except-raise int64, Simplify-boolean-expression int64, simplifiable-if-expression int64, broad-exception-caught int64, hunks_num int64, too-many-boolean-expressions int64, avg_coupling_code_size_cut_diff int64) as (
  case when SLOC_diff <= 38.0 then
    case when hunks_num <= 11.5 then
      case when Single comments_diff <= -2.5 then
        case when hunks_num <= 1.5 then
          case when Single comments_diff <= -974.0 then
             return 1.0 # (1.0 out of 1.0)
          else  # if Single comments_diff > -974.0
             return 0.0 # (0.0 out of 12.0)
          end         else  # if hunks_num > 1.5
          case when added_lines <= 22.0 then
             return 0.0 # (0.0 out of 4.0)
          else  # if added_lines > 22.0
            case when McCabe_max_before <= 19.5 then
              case when unnecessary-semicolon <= 0.5 then
                case when refactor_mle_diff <= 0.6105833351612091 then
                   return 1.0 # (45.0 out of 45.0)
                else  # if refactor_mle_diff > 0.6105833351612091
                   return 0.0 # (0.0 out of 1.0)
                end               else  # if unnecessary-semicolon > 0.5
                 return 0.0 # (0.0 out of 1.0)
              end             else  # if McCabe_max_before > 19.5
              case when SLOC_diff <= -46.5 then
                case when Single comments_before <= 50.0 then
                  case when Comments_before <= 42.5 then
                     return 1.0 # (4.0 out of 4.0)
                  else  # if Comments_before > 42.5
                     return 0.0 # (0.0 out of 4.0)
                  end                 else  # if Single comments_before > 50.0
                  case when Blank_before <= 304.0 then
                     return 1.0 # (19.0 out of 19.0)
                  else  # if Blank_before > 304.0
                     return 0.0 # (0.0 out of 1.0)
                  end                 end               else  # if SLOC_diff > -46.5
                case when one_file_fix_rate_diff <= 0.02380952425301075 then
                  case when McCabe_sum_before <= 65.0 then
                     return 1.0 # (1.0 out of 1.0)
                  else  # if McCabe_sum_before > 65.0
                     return 0.0 # (0.0 out of 9.0)
                  end                 else  # if one_file_fix_rate_diff > 0.02380952425301075
                  case when Comments_before <= 15.0 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if Comments_before > 15.0
                     return 1.0 # (3.0 out of 3.0)
                  end                 end               end             end           end         end       else  # if Single comments_diff > -2.5
        case when same_day_duration_avg_diff <= -0.05050504952669144 then
          case when same_day_duration_avg_diff <= -40.4897518157959 then
            case when Blank_before <= 328.0 then
              case when LLOC_diff <= -6.5 then
                case when same_day_duration_avg_diff <= -332.5 then
                  case when N1_diff <= -14.0 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if N1_diff > -14.0
                     return 1.0 # (2.0 out of 2.0)
                  end                 else  # if same_day_duration_avg_diff > -332.5
                   return 0.0 # (0.0 out of 19.0)
                end               else  # if LLOC_diff > -6.5
                case when removed_lines <= 49.5 then
                  case when refactor_mle_diff <= -0.1262214295566082 then
                    case when SLOC_diff <= -1.0 then
                       return 1.0 # (4.0 out of 4.0)
                    else  # if SLOC_diff > -1.0
                      case when avg_coupling_code_size_cut_diff <= -0.7385912835597992 then
                        case when avg_coupling_code_size_cut_diff <= -0.88591268658638 then
                          case when same_day_duration_avg_diff <= -247.6547622680664 then
                            case when cur_count_x <= 0.5 then
                               return 0.0 # (0.0 out of 1.0)
                            else  # if cur_count_x > 0.5
                              case when one_file_fix_rate_diff <= 0.550000011920929 then
                                 return 1.0 # (6.0 out of 6.0)
                              else  # if one_file_fix_rate_diff > 0.550000011920929
                                 return 0.0 # (0.0 out of 1.0)
                              end                             end                           else  # if same_day_duration_avg_diff > -247.6547622680664
                            case when prev_count_x <= 1.5 then
                              case when one_file_fix_rate_diff <= 0.09880952537059784 then
                                case when avg_coupling_code_size_cut_diff <= -3.225000023841858 then
                                  case when avg_coupling_code_size_cut_diff <= -4.0 then
                                     return 0.0 # (0.0 out of 1.0)
                                  else  # if avg_coupling_code_size_cut_diff > -4.0
                                     return 1.0 # (2.0 out of 2.0)
                                  end                                 else  # if avg_coupling_code_size_cut_diff > -3.225000023841858
                                  case when same_day_duration_avg_diff <= -54.118953704833984 then
                                     return 0.0 # (0.0 out of 6.0)
                                  else  # if same_day_duration_avg_diff > -54.118953704833984
                                    case when same_day_duration_avg_diff <= -46.60497856140137 then
                                       return 1.0 # (1.0 out of 1.0)
                                    else  # if same_day_duration_avg_diff > -46.60497856140137
                                       return 0.0 # (0.0 out of 1.0)
                                    end                                   end                                 end                               else  # if one_file_fix_rate_diff > 0.09880952537059784
                                case when same_day_duration_avg_diff <= -143.50833129882812 then
                                   return 0.0 # (0.0 out of 1.0)
                                else  # if same_day_duration_avg_diff > -143.50833129882812
                                   return 1.0 # (5.0 out of 5.0)
                                end                               end                             else  # if prev_count_x > 1.5
                               return 0.0 # (0.0 out of 6.0)
                            end                           end                         else  # if avg_coupling_code_size_cut_diff > -0.88591268658638
                           return 1.0 # (4.0 out of 4.0)
                        end                       else  # if avg_coupling_code_size_cut_diff > -0.7385912835597992
                        case when prev_count_x <= 8.5 then
                          case when avg_coupling_code_size_cut_diff <= 2.0666667222976685 then
                            case when pointless-statement <= 0.5 then
                              case when one_file_fix_rate_diff <= -0.5178571343421936 then
                                case when superfluous-parens <= 0.5 then
                                   return 1.0 # (2.0 out of 2.0)
                                else  # if superfluous-parens > 0.5
                                   return 0.0 # (0.0 out of 1.0)
                                end                               else  # if one_file_fix_rate_diff > -0.5178571343421936
                                case when modified_McCabe_max_diff <= -0.5 then
                                   return 1.0 # (1.0 out of 1.0)
                                else  # if modified_McCabe_max_diff > -0.5
                                  case when length_diff <= 1.5 then
                                    case when same_day_duration_avg_diff <= -321.94444274902344 then
                                      case when same_day_duration_avg_diff <= -379.1666717529297 then
                                         return 0.0 # (0.0 out of 4.0)
                                      else  # if same_day_duration_avg_diff > -379.1666717529297
                                         return 1.0 # (3.0 out of 3.0)
                                      end                                     else  # if same_day_duration_avg_diff > -321.94444274902344
                                      case when refactor_mle_diff <= -0.2815866768360138 then
                                        case when same_day_duration_avg_diff <= -75.625 then
                                          case when refactor_mle_diff <= -0.362124502658844 then
                                             return 0.0 # (0.0 out of 14.0)
                                          else  # if refactor_mle_diff > -0.362124502658844
                                            case when prev_count_x <= 0.5 then
                                               return 1.0 # (1.0 out of 1.0)
                                            else  # if prev_count_x > 0.5
                                               return 0.0 # (0.0 out of 3.0)
                                            end                                           end                                         else  # if same_day_duration_avg_diff > -75.625
                                          case when line-too-long <= 0.5 then
                                            case when too-many-statements <= 0.5 then
                                               return 0.0 # (0.0 out of 6.0)
                                            else  # if too-many-statements > 0.5
                                               return 1.0 # (1.0 out of 1.0)
                                            end                                           else  # if line-too-long > 0.5
                                             return 1.0 # (3.0 out of 3.0)
                                          end                                         end                                       else  # if refactor_mle_diff > -0.2815866768360138
                                         return 0.0 # (0.0 out of 41.0)
                                      end                                     end                                   else  # if length_diff > 1.5
                                     return 1.0 # (1.0 out of 1.0)
                                  end                                 end                               end                             else  # if pointless-statement > 0.5
                               return 1.0 # (2.0 out of 2.0)
                            end                           else  # if avg_coupling_code_size_cut_diff > 2.0666667222976685
                            case when same_day_duration_avg_diff <= -157.84722137451172 then
                               return 0.0 # (0.0 out of 3.0)
                            else  # if same_day_duration_avg_diff > -157.84722137451172
                              case when avg_coupling_code_size_cut_diff <= 2.757575750350952 then
                                 return 1.0 # (5.0 out of 5.0)
                              else  # if avg_coupling_code_size_cut_diff > 2.757575750350952
                                case when avg_coupling_code_size_cut_diff <= 3.007002830505371 then
                                   return 0.0 # (0.0 out of 2.0)
                                else  # if avg_coupling_code_size_cut_diff > 3.007002830505371
                                  case when LOC_before <= 347.0 then
                                     return 1.0 # (2.0 out of 2.0)
                                  else  # if LOC_before > 347.0
                                     return 0.0 # (0.0 out of 1.0)
                                  end                                 end                               end                             end                           end                         else  # if prev_count_x > 8.5
                          case when refactor_mle_diff <= -0.4341536611318588 then
                             return 0.0 # (0.0 out of 1.0)
                          else  # if refactor_mle_diff > -0.4341536611318588
                            case when one_file_fix_rate_diff <= -0.2983821779489517 then
                               return 0.0 # (0.0 out of 1.0)
                            else  # if one_file_fix_rate_diff > -0.2983821779489517
                               return 1.0 # (5.0 out of 5.0)
                            end                           end                         end                       end                     end                   else  # if refactor_mle_diff > -0.1262214295566082
                    case when one_file_fix_rate_diff <= 0.6904762089252472 then
                      case when refactor_mle_diff <= -0.032713472843170166 then
                        case when prev_count_x <= 1.5 then
                          case when avg_coupling_code_size_cut_diff <= -1.4741379022598267 then
                            case when avg_coupling_code_size_cut_diff <= -2.485714316368103 then
                               return 1.0 # (1.0 out of 1.0)
                            else  # if avg_coupling_code_size_cut_diff > -2.485714316368103
                               return 0.0 # (0.0 out of 6.0)
                            end                           else  # if avg_coupling_code_size_cut_diff > -1.4741379022598267
                            case when one_file_fix_rate_diff <= -0.3928571492433548 then
                               return 0.0 # (0.0 out of 3.0)
                            else  # if one_file_fix_rate_diff > -0.3928571492433548
                              case when same_day_duration_avg_diff <= -122.95580673217773 then
                                 return 1.0 # (8.0 out of 8.0)
                              else  # if same_day_duration_avg_diff > -122.95580673217773
                                case when same_day_duration_avg_diff <= -94.91666793823242 then
                                   return 0.0 # (0.0 out of 5.0)
                                else  # if same_day_duration_avg_diff > -94.91666793823242
                                  case when same_day_duration_avg_diff <= -57.0706787109375 then
                                    case when too-many-lines <= 0.5 then
                                      case when avg_coupling_code_size_cut_diff <= -0.6346697509288788 then
                                        case when too-many-boolean-expressions <= 0.5 then
                                           return 1.0 # (1.0 out of 1.0)
                                        else  # if too-many-boolean-expressions > 0.5
                                           return 0.0 # (0.0 out of 1.0)
                                        end                                       else  # if avg_coupling_code_size_cut_diff > -0.6346697509288788
                                         return 1.0 # (9.0 out of 9.0)
                                      end                                     else  # if too-many-lines > 0.5
                                       return 0.0 # (0.0 out of 1.0)
                                    end                                   else  # if same_day_duration_avg_diff > -57.0706787109375
                                    case when one_file_fix_rate_diff <= 0.042171720415353775 then
                                      case when same_day_duration_avg_diff <= -52.0512809753418 then
                                         return 0.0 # (0.0 out of 1.0)
                                      else  # if same_day_duration_avg_diff > -52.0512809753418
                                         return 1.0 # (3.0 out of 3.0)
                                      end                                     else  # if one_file_fix_rate_diff > 0.042171720415353775
                                       return 0.0 # (0.0 out of 3.0)
                                    end                                   end                                 end                               end                             end                           end                         else  # if prev_count_x > 1.5
                          case when unnecessary-pass <= 0.5 then
                             return 1.0 # (12.0 out of 12.0)
                          else  # if unnecessary-pass > 0.5
                             return 0.0 # (0.0 out of 1.0)
                          end                         end                       else  # if refactor_mle_diff > -0.032713472843170166
                        case when prev_count_x <= 1.5 then
                          case when hunks_num <= 2.5 then
                            case when one_file_fix_rate_diff <= -0.19523809850215912 then
                              case when one_file_fix_rate_diff <= -0.40833333134651184 then
                                case when same_day_duration_avg_diff <= -91.3452377319336 then
                                  case when too-many-branches <= 0.5 then
                                     return 0.0 # (0.0 out of 4.0)
                                  else  # if too-many-branches > 0.5
                                    case when avg_coupling_code_size_cut_diff <= -0.38461536169052124 then
                                       return 0.0 # (0.0 out of 1.0)
                                    else  # if avg_coupling_code_size_cut_diff > -0.38461536169052124
                                       return 1.0 # (2.0 out of 2.0)
                                    end                                   end                                 else  # if same_day_duration_avg_diff > -91.3452377319336
                                  case when cur_count_x <= 0.5 then
                                    case when McCabe_max_before <= 3.0 then
                                       return 0.0 # (0.0 out of 3.0)
                                    else  # if McCabe_max_before > 3.0
                                       return 1.0 # (1.0 out of 1.0)
                                    end                                   else  # if cur_count_x > 0.5
                                     return 1.0 # (6.0 out of 6.0)
                                  end                                 end                               else  # if one_file_fix_rate_diff > -0.40833333134651184
                                 return 1.0 # (10.0 out of 10.0)
                              end                             else  # if one_file_fix_rate_diff > -0.19523809850215912
                              case when too-many-lines <= 0.5 then
                                case when refactor_mle_diff <= 0.14565899968147278 then
                                  case when refactor_mle_diff <= 0.09309868142008781 then
                                    case when too-many-statements <= 0.5 then
                                      case when refactor_mle_diff <= -0.015226878225803375 then
                                        case when same_day_duration_avg_diff <= -56.95123100280762 then
                                           return 0.0 # (0.0 out of 4.0)
                                        else  # if same_day_duration_avg_diff > -56.95123100280762
                                           return 1.0 # (1.0 out of 1.0)
                                        end                                       else  # if refactor_mle_diff > -0.015226878225803375
                                        case when McCabe_max_after <= 18.0 then
                                          case when unnecessary-pass <= 0.5 then
                                            case when same_day_duration_avg_diff <= -359.39772033691406 then
                                               return 0.0 # (0.0 out of 1.0)
                                            else  # if same_day_duration_avg_diff > -359.39772033691406
                                              case when same_day_duration_avg_diff <= -126.30345916748047 then
                                                 return 1.0 # (11.0 out of 11.0)
                                              else  # if same_day_duration_avg_diff > -126.30345916748047
                                                case when same_day_duration_avg_diff <= -55.596256256103516 then
                                                  case when hunks_num <= 0.5 then
                                                     return 0.0 # (0.0 out of 5.0)
                                                  else  # if hunks_num > 0.5
                                                     return 1.0 # (3.0 out of 3.0)
                                                  end                                                 else  # if same_day_duration_avg_diff > -55.596256256103516
                                                  case when avg_coupling_code_size_cut_diff <= 1.5 then
                                                     return 1.0 # (10.0 out of 10.0)
                                                  else  # if avg_coupling_code_size_cut_diff > 1.5
                                                    case when same_day_duration_avg_diff <= -45.89583396911621 then
                                                       return 1.0 # (1.0 out of 1.0)
                                                    else  # if same_day_duration_avg_diff > -45.89583396911621
                                                       return 0.0 # (0.0 out of 2.0)
                                                    end                                                   end                                                 end                                               end                                             end                                           else  # if unnecessary-pass > 0.5
                                             return 0.0 # (0.0 out of 2.0)
                                          end                                         else  # if McCabe_max_after > 18.0
                                           return 0.0 # (0.0 out of 2.0)
                                        end                                       end                                     else  # if too-many-statements > 0.5
                                      case when same_day_duration_avg_diff <= -232.01587677001953 then
                                         return 1.0 # (1.0 out of 1.0)
                                      else  # if same_day_duration_avg_diff > -232.01587677001953
                                         return 0.0 # (0.0 out of 9.0)
                                      end                                     end                                   else  # if refactor_mle_diff > 0.09309868142008781
                                    case when avg_coupling_code_size_cut_diff <= -4.545454502105713 then
                                       return 1.0 # (1.0 out of 1.0)
                                    else  # if avg_coupling_code_size_cut_diff > -4.545454502105713
                                       return 0.0 # (0.0 out of 14.0)
                                    end                                   end                                 else  # if refactor_mle_diff > 0.14565899968147278
                                  case when cur_count_x <= 1.5 then
                                    case when avg_coupling_code_size_cut_diff <= 3.649999976158142 then
                                      case when same_day_duration_avg_diff <= -146.26428985595703 then
                                        case when same_day_duration_avg_diff <= -190.5625 then
                                          case when line-too-long <= 0.5 then
                                             return 1.0 # (7.0 out of 7.0)
                                          else  # if line-too-long > 0.5
                                             return 0.0 # (0.0 out of 1.0)
                                          end                                         else  # if same_day_duration_avg_diff > -190.5625
                                          case when avg_coupling_code_size_cut_diff <= 2.449999988079071 then
                                             return 0.0 # (0.0 out of 5.0)
                                          else  # if avg_coupling_code_size_cut_diff > 2.449999988079071
                                             return 1.0 # (1.0 out of 1.0)
                                          end                                         end                                       else  # if same_day_duration_avg_diff > -146.26428985595703
                                        case when Blank_before <= 229.5 then
                                          case when avg_coupling_code_size_cut_diff <= 2.375 then
                                            case when line-too-long <= 0.5 then
                                               return 1.0 # (12.0 out of 12.0)
                                            else  # if line-too-long > 0.5
                                              case when same_day_duration_avg_diff <= -66.95394515991211 then
                                                 return 1.0 # (3.0 out of 3.0)
                                              else  # if same_day_duration_avg_diff > -66.95394515991211
                                                 return 0.0 # (0.0 out of 1.0)
                                              end                                             end                                           else  # if avg_coupling_code_size_cut_diff > 2.375
                                            case when too-many-statements <= 0.5 then
                                               return 1.0 # (1.0 out of 1.0)
                                            else  # if too-many-statements > 0.5
                                               return 0.0 # (0.0 out of 1.0)
                                            end                                           end                                         else  # if Blank_before > 229.5
                                           return 0.0 # (0.0 out of 1.0)
                                        end                                       end                                     else  # if avg_coupling_code_size_cut_diff > 3.649999976158142
                                       return 0.0 # (0.0 out of 1.0)
                                    end                                   else  # if cur_count_x > 1.5
                                    case when refactor_mle_diff <= 0.17524176090955734 then
                                       return 1.0 # (2.0 out of 2.0)
                                    else  # if refactor_mle_diff > 0.17524176090955734
                                       return 0.0 # (0.0 out of 5.0)
                                    end                                   end                                 end                               else  # if too-many-lines > 0.5
                                case when avg_coupling_code_size_cut_diff <= 0.3618220128118992 then
                                  case when same_day_duration_avg_diff <= -122.46449279785156 then
                                     return 0.0 # (0.0 out of 2.0)
                                  else  # if same_day_duration_avg_diff > -122.46449279785156
                                     return 1.0 # (1.0 out of 1.0)
                                  end                                 else  # if avg_coupling_code_size_cut_diff > 0.3618220128118992
                                   return 0.0 # (0.0 out of 6.0)
                                end                               end                             end                           else  # if hunks_num > 2.5
                             return 0.0 # (0.0 out of 7.0)
                          end                         else  # if prev_count_x > 1.5
                          case when cur_count_x <= 24.5 then
                            case when avg_coupling_code_size_cut_diff <= 0.9019005596637726 then
                              case when one_file_fix_rate_diff <= 0.2500000074505806 then
                                case when one_file_fix_rate_diff <= -0.949999988079071 then
                                   return 1.0 # (1.0 out of 1.0)
                                else  # if one_file_fix_rate_diff > -0.949999988079071
                                  case when prev_count_y <= 2.5 then
                                    case when avg_coupling_code_size_cut_diff <= -3.5128204822540283 then
                                       return 1.0 # (1.0 out of 1.0)
                                    else  # if avg_coupling_code_size_cut_diff > -3.5128204822540283
                                      case when refactor_mle_diff <= 0.4899231940507889 then
                                        case when avg_coupling_code_size_cut_diff <= -0.8712121248245239 then
                                          case when avg_coupling_code_size_cut_diff <= -1.125 then
                                             return 0.0 # (0.0 out of 4.0)
                                          else  # if avg_coupling_code_size_cut_diff > -1.125
                                             return 1.0 # (2.0 out of 2.0)
                                          end                                         else  # if avg_coupling_code_size_cut_diff > -0.8712121248245239
                                          case when same_day_duration_avg_diff <= -481.9247283935547 then
                                            case when prev_count_x <= 3.5 then
                                               return 1.0 # (1.0 out of 1.0)
                                            else  # if prev_count_x > 3.5
                                               return 0.0 # (0.0 out of 1.0)
                                            end                                           else  # if same_day_duration_avg_diff > -481.9247283935547
                                             return 0.0 # (0.0 out of 15.0)
                                          end                                         end                                       else  # if refactor_mle_diff > 0.4899231940507889
                                         return 1.0 # (1.0 out of 1.0)
                                      end                                     end                                   else  # if prev_count_y > 2.5
                                     return 1.0 # (1.0 out of 1.0)
                                  end                                 end                               else  # if one_file_fix_rate_diff > 0.2500000074505806
                                case when simplifiable-condition <= 0.5 then
                                   return 1.0 # (3.0 out of 3.0)
                                else  # if simplifiable-condition > 0.5
                                   return 0.0 # (0.0 out of 1.0)
                                end                               end                             else  # if avg_coupling_code_size_cut_diff > 0.9019005596637726
                              case when one_file_fix_rate_diff <= -0.3029411807656288 then
                                 return 1.0 # (1.0 out of 1.0)
                              else  # if one_file_fix_rate_diff > -0.3029411807656288
                                 return 0.0 # (0.0 out of 16.0)
                              end                             end                           else  # if cur_count_x > 24.5
                             return 1.0 # (4.0 out of 4.0)
                          end                         end                       end                     else  # if one_file_fix_rate_diff > 0.6904762089252472
                      case when Single comments_before <= 32.0 then
                         return 0.0 # (0.0 out of 9.0)
                      else  # if Single comments_before > 32.0
                         return 1.0 # (1.0 out of 1.0)
                      end                     end                   end                 else  # if removed_lines > 49.5
                  case when Comments_diff <= -1.5 then
                     return 0.0 # (0.0 out of 2.0)
                  else  # if Comments_diff > -1.5
                     return 1.0 # (9.0 out of 9.0)
                  end                 end               end             else  # if Blank_before > 328.0
              case when Comments_after <= 559.5 then
                 return 1.0 # (8.0 out of 8.0)
              else  # if Comments_after > 559.5
                 return 0.0 # (0.0 out of 1.0)
              end             end           else  # if same_day_duration_avg_diff > -40.4897518157959
            case when one_file_fix_rate_diff <= -0.40238095819950104 then
              case when same_day_duration_avg_diff <= -28.716666221618652 then
                case when avg_coupling_code_size_cut_diff <= 0.5508145391941071 then
                  case when h1_diff <= -2.0 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if h1_diff > -2.0
                     return 1.0 # (2.0 out of 2.0)
                  end                 else  # if avg_coupling_code_size_cut_diff > 0.5508145391941071
                   return 0.0 # (0.0 out of 3.0)
                end               else  # if same_day_duration_avg_diff > -28.716666221618652
                case when refactor_mle_diff <= 0.1280944049358368 then
                  case when superfluous-parens <= 0.5 then
                    case when one_file_fix_rate_diff <= -0.550000011920929 then
                       return 1.0 # (19.0 out of 19.0)
                    else  # if one_file_fix_rate_diff > -0.550000011920929
                      case when line-too-long <= 0.5 then
                        case when avg_coupling_code_size_cut_diff <= -0.3680555522441864 then
                           return 0.0 # (0.0 out of 1.0)
                        else  # if avg_coupling_code_size_cut_diff > -0.3680555522441864
                          case when avg_coupling_code_size_cut_diff <= 0.5263157784938812 then
                             return 1.0 # (10.0 out of 10.0)
                          else  # if avg_coupling_code_size_cut_diff > 0.5263157784938812
                             return 0.0 # (0.0 out of 1.0)
                          end                         end                       else  # if line-too-long > 0.5
                         return 0.0 # (0.0 out of 1.0)
                      end                     end                   else  # if superfluous-parens > 0.5
                     return 0.0 # (0.0 out of 1.0)
                  end                 else  # if refactor_mle_diff > 0.1280944049358368
                  case when refactor_mle_diff <= 0.5572525337338448 then
                     return 0.0 # (0.0 out of 2.0)
                  else  # if refactor_mle_diff > 0.5572525337338448
                     return 1.0 # (1.0 out of 1.0)
                  end                 end               end             else  # if one_file_fix_rate_diff > -0.40238095819950104
              case when one_file_fix_rate_diff <= -0.28312864899635315 then
                case when too-many-statements <= 0.5 then
                   return 0.0 # (0.0 out of 12.0)
                else  # if too-many-statements > 0.5
                   return 1.0 # (2.0 out of 2.0)
                end               else  # if one_file_fix_rate_diff > -0.28312864899635315
                case when Comments_after <= 43.5 then
                  case when same_day_duration_avg_diff <= -11.298230171203613 then
                    case when McCabe_max_before <= 48.5 then
                      case when same_day_duration_avg_diff <= -14.866071701049805 then
                        case when SLOC_before <= 269.5 then
                          case when Comments_after <= 9.0 then
                            case when one_file_fix_rate_diff <= 0.550000011920929 then
                              case when refactor_mle_diff <= 0.3337487280368805 then
                                case when prev_count_x <= 5.5 then
                                  case when cur_count_x <= 0.5 then
                                    case when same_day_duration_avg_diff <= -16.713558197021484 then
                                      case when refactor_mle_diff <= -0.4625631272792816 then
                                         return 0.0 # (0.0 out of 1.0)
                                      else  # if refactor_mle_diff > -0.4625631272792816
                                        case when LLOC_diff <= -1.5 then
                                           return 0.0 # (0.0 out of 1.0)
                                        else  # if LLOC_diff > -1.5
                                           return 1.0 # (18.0 out of 18.0)
                                        end                                       end                                     else  # if same_day_duration_avg_diff > -16.713558197021484
                                      case when avg_coupling_code_size_cut_diff <= -0.12053571688011289 then
                                         return 0.0 # (0.0 out of 3.0)
                                      else  # if avg_coupling_code_size_cut_diff > -0.12053571688011289
                                         return 1.0 # (1.0 out of 1.0)
                                      end                                     end                                   else  # if cur_count_x > 0.5
                                    case when one_file_fix_rate_diff <= -0.24166666716337204 then
                                       return 0.0 # (0.0 out of 3.0)
                                    else  # if one_file_fix_rate_diff > -0.24166666716337204
                                      case when one_file_fix_rate_diff <= -0.018145160749554634 then
                                        case when one_file_fix_rate_diff <= -0.10458839312195778 then
                                          case when one_file_fix_rate_diff <= -0.18614719063043594 then
                                             return 1.0 # (4.0 out of 4.0)
                                          else  # if one_file_fix_rate_diff > -0.18614719063043594
                                             return 0.0 # (0.0 out of 4.0)
                                          end                                         else  # if one_file_fix_rate_diff > -0.10458839312195778
                                           return 1.0 # (9.0 out of 9.0)
                                        end                                       else  # if one_file_fix_rate_diff > -0.018145160749554634
                                        case when same_day_duration_avg_diff <= -18.204914093017578 then
                                          case when prev_count_x <= 1.5 then
                                            case when one_file_fix_rate_diff <= 0.050735294818878174 then
                                              case when refactor_mle_diff <= -0.4310000091791153 then
                                                 return 1.0 # (4.0 out of 4.0)
                                              else  # if refactor_mle_diff > -0.4310000091791153
                                                case when refactor_mle_diff <= -0.16493679955601692 then
                                                   return 0.0 # (0.0 out of 8.0)
                                                else  # if refactor_mle_diff > -0.16493679955601692
                                                  case when one_file_fix_rate_diff <= 0.002923976629972458 then
                                                    case when refactor_mle_diff <= 0.07183333486318588 then
                                                      case when avg_coupling_code_size_cut_diff <= 0.07828282564878464 then
                                                         return 1.0 # (5.0 out of 5.0)
                                                      else  # if avg_coupling_code_size_cut_diff > 0.07828282564878464
                                                         return 0.0 # (0.0 out of 1.0)
                                                      end                                                     else  # if refactor_mle_diff > 0.07183333486318588
                                                      case when same_day_duration_avg_diff <= -32.77083396911621 then
                                                         return 0.0 # (0.0 out of 2.0)
                                                      else  # if same_day_duration_avg_diff > -32.77083396911621
                                                         return 1.0 # (1.0 out of 1.0)
                                                      end                                                     end                                                   else  # if one_file_fix_rate_diff > 0.002923976629972458
                                                     return 0.0 # (0.0 out of 4.0)
                                                  end                                                 end                                               end                                             else  # if one_file_fix_rate_diff > 0.050735294818878174
                                              case when refactor_mle_diff <= -0.35740233957767487 then
                                                 return 0.0 # (0.0 out of 3.0)
                                              else  # if refactor_mle_diff > -0.35740233957767487
                                                case when refactor_mle_diff <= -0.13386353105306625 then
                                                  case when one_file_fix_rate_diff <= 0.2777777835726738 then
                                                     return 1.0 # (11.0 out of 11.0)
                                                  else  # if one_file_fix_rate_diff > 0.2777777835726738
                                                    case when refactor_mle_diff <= -0.2431282103061676 then
                                                       return 1.0 # (1.0 out of 1.0)
                                                    else  # if refactor_mle_diff > -0.2431282103061676
                                                       return 0.0 # (0.0 out of 1.0)
                                                    end                                                   end                                                 else  # if refactor_mle_diff > -0.13386353105306625
                                                  case when one_file_fix_rate_diff <= 0.12426740303635597 then
                                                     return 0.0 # (0.0 out of 3.0)
                                                  else  # if one_file_fix_rate_diff > 0.12426740303635597
                                                    case when refactor_mle_diff <= -0.0793882180005312 then
                                                       return 0.0 # (0.0 out of 2.0)
                                                    else  # if refactor_mle_diff > -0.0793882180005312
                                                      case when too-many-branches <= 0.5 then
                                                         return 1.0 # (6.0 out of 6.0)
                                                      else  # if too-many-branches > 0.5
                                                         return 0.0 # (0.0 out of 1.0)
                                                      end                                                     end                                                   end                                                 end                                               end                                             end                                           else  # if prev_count_x > 1.5
                                            case when cur_count_x <= 6.5 then
                                               return 0.0 # (0.0 out of 8.0)
                                            else  # if cur_count_x > 6.5
                                               return 1.0 # (1.0 out of 1.0)
                                            end                                           end                                         else  # if same_day_duration_avg_diff > -18.204914093017578
                                          case when broad-exception-caught <= 0.5 then
                                             return 1.0 # (7.0 out of 7.0)
                                          else  # if broad-exception-caught > 0.5
                                             return 0.0 # (0.0 out of 1.0)
                                          end                                         end                                       end                                     end                                   end                                 else  # if prev_count_x > 5.5
                                  case when cur_count_x <= 62.5 then
                                     return 1.0 # (13.0 out of 13.0)
                                  else  # if cur_count_x > 62.5
                                     return 0.0 # (0.0 out of 1.0)
                                  end                                 end                               else  # if refactor_mle_diff > 0.3337487280368805
                                 return 0.0 # (0.0 out of 3.0)
                              end                             else  # if one_file_fix_rate_diff > 0.550000011920929
                               return 1.0 # (7.0 out of 7.0)
                            end                           else  # if Comments_after > 9.0
                             return 0.0 # (0.0 out of 4.0)
                          end                         else  # if SLOC_before > 269.5
                           return 1.0 # (8.0 out of 8.0)
                        end                       else  # if same_day_duration_avg_diff > -14.866071701049805
                        case when prev_count_x <= 3.5 then
                           return 1.0 # (18.0 out of 18.0)
                        else  # if prev_count_x > 3.5
                          case when prev_count_x <= 7.0 then
                             return 0.0 # (0.0 out of 2.0)
                          else  # if prev_count_x > 7.0
                             return 1.0 # (2.0 out of 2.0)
                          end                         end                       end                     else  # if McCabe_max_before > 48.5
                       return 0.0 # (0.0 out of 4.0)
                    end                   else  # if same_day_duration_avg_diff > -11.298230171203613
                    case when N2_diff <= -0.5 then
                       return 1.0 # (3.0 out of 3.0)
                    else  # if N2_diff > -0.5
                      case when same_day_duration_avg_diff <= -9.206862926483154 then
                        case when avg_coupling_code_size_cut_diff <= 1.699572592973709 then
                          case when too-many-boolean-expressions <= 0.5 then
                             return 0.0 # (0.0 out of 9.0)
                          else  # if too-many-boolean-expressions > 0.5
                             return 1.0 # (1.0 out of 1.0)
                          end                         else  # if avg_coupling_code_size_cut_diff > 1.699572592973709
                           return 1.0 # (1.0 out of 1.0)
                        end                       else  # if same_day_duration_avg_diff > -9.206862926483154
                        case when avg_coupling_code_size_cut_diff <= 1.6347222328186035 then
                          case when same_day_duration_avg_diff <= -7.0254902839660645 then
                            case when avg_coupling_code_size_cut_diff <= -0.5888888835906982 then
                              case when refactor_mle_diff <= 0.07668044790625572 then
                                 return 0.0 # (0.0 out of 2.0)
                              else  # if refactor_mle_diff > 0.07668044790625572
                                 return 1.0 # (1.0 out of 1.0)
                              end                             else  # if avg_coupling_code_size_cut_diff > -0.5888888835906982
                              case when refactor_mle_diff <= -0.28742697834968567 then
                                 return 0.0 # (0.0 out of 1.0)
                              else  # if refactor_mle_diff > -0.28742697834968567
                                 return 1.0 # (11.0 out of 11.0)
                              end                             end                           else  # if same_day_duration_avg_diff > -7.0254902839660645
                            case when refactor_mle_diff <= -0.036737619899213314 then
                              case when same_day_duration_avg_diff <= -4.914396286010742 then
                                case when too-many-statements <= 0.5 then
                                   return 0.0 # (0.0 out of 4.0)
                                else  # if too-many-statements > 0.5
                                   return 1.0 # (3.0 out of 3.0)
                                end                               else  # if same_day_duration_avg_diff > -4.914396286010742
                                 return 1.0 # (9.0 out of 9.0)
                              end                             else  # if refactor_mle_diff > -0.036737619899213314
                              case when refactor_mle_diff <= 0.2617799639701843 then
                                case when prev_count_x <= 1.5 then
                                  case when same_day_duration_avg_diff <= -1.981944501399994 then
                                     return 0.0 # (0.0 out of 12.0)
                                  else  # if same_day_duration_avg_diff > -1.981944501399994
                                    case when same_day_duration_avg_diff <= -1.2545183300971985 then
                                       return 1.0 # (2.0 out of 2.0)
                                    else  # if same_day_duration_avg_diff > -1.2545183300971985
                                       return 0.0 # (0.0 out of 3.0)
                                    end                                   end                                 else  # if prev_count_x > 1.5
                                  case when refactor_mle_diff <= 0.004320802167057991 then
                                     return 0.0 # (0.0 out of 3.0)
                                  else  # if refactor_mle_diff > 0.004320802167057991
                                     return 1.0 # (3.0 out of 3.0)
                                  end                                 end                               else  # if refactor_mle_diff > 0.2617799639701843
                                case when too-many-lines <= 0.5 then
                                  case when one_file_fix_rate_diff <= 0.5500000007450581 then
                                     return 1.0 # (5.0 out of 5.0)
                                  else  # if one_file_fix_rate_diff > 0.5500000007450581
                                     return 0.0 # (0.0 out of 1.0)
                                  end                                 else  # if too-many-lines > 0.5
                                   return 0.0 # (0.0 out of 2.0)
                                end                               end                             end                           end                         else  # if avg_coupling_code_size_cut_diff > 1.6347222328186035
                          case when one_file_fix_rate_diff <= -0.0486111119389534 then
                             return 1.0 # (1.0 out of 1.0)
                          else  # if one_file_fix_rate_diff > -0.0486111119389534
                             return 0.0 # (0.0 out of 7.0)
                          end                         end                       end                     end                   end                 else  # if Comments_after > 43.5
                  case when changed_lines <= 7.5 then
                     return 1.0 # (4.0 out of 4.0)
                  else  # if changed_lines > 7.5
                    case when LLOC_before <= 608.0 then
                      case when vocabulary_diff <= -16.5 then
                         return 1.0 # (1.0 out of 1.0)
                      else  # if vocabulary_diff > -16.5
                        case when same_day_duration_avg_diff <= -37.585784912109375 then
                           return 1.0 # (1.0 out of 1.0)
                        else  # if same_day_duration_avg_diff > -37.585784912109375
                           return 0.0 # (0.0 out of 20.0)
                        end                       end                     else  # if LLOC_before > 608.0
                      case when avg_coupling_code_size_cut_diff <= 0.20000000298023224 then
                         return 1.0 # (4.0 out of 4.0)
                      else  # if avg_coupling_code_size_cut_diff > 0.20000000298023224
                        case when LOC_diff <= 36.0 then
                           return 0.0 # (0.0 out of 4.0)
                        else  # if LOC_diff > 36.0
                           return 1.0 # (1.0 out of 1.0)
                        end                       end                     end                   end                 end               end             end           end         else  # if same_day_duration_avg_diff > -0.05050504952669144
          case when McCabe_max_before <= 51.0 then
            case when McCabe_max_diff <= -5.5 then
               return 0.0 # (0.0 out of 23.0)
            else  # if McCabe_max_diff > -5.5
              case when McCabe_max_after <= 34.0 then
                case when McCabe_sum_after <= 101.0 then
                  case when Comments_before <= 102.0 then
                    case when LOC_before <= 956.5 then
                      case when prev_count_y <= 1.5 then
                        case when one_file_fix_rate_diff <= 0.26713287830352783 then
                          case when cur_count_x <= 66.5 then
                            case when cur_count_x <= 19.0 then
                              case when one_file_fix_rate_diff <= -0.6547619104385376 then
                                case when refactor_mle_diff <= 0.2049209102988243 then
                                  case when same_day_duration_avg_diff <= 296.1388854980469 then
                                    case when same_day_duration_avg_diff <= 1.0833333730697632 then
                                      case when cur_count_x <= 3.5 then
                                         return 0.0 # (0.0 out of 1.0)
                                      else  # if cur_count_x > 3.5
                                         return 1.0 # (1.0 out of 1.0)
                                      end                                     else  # if same_day_duration_avg_diff > 1.0833333730697632
                                      case when too-many-statements <= 0.5 then
                                        case when refactor_mle_diff <= -0.1157674603164196 then
                                          case when refactor_mle_diff <= -0.15718823671340942 then
                                             return 0.0 # (0.0 out of 5.0)
                                          else  # if refactor_mle_diff > -0.15718823671340942
                                             return 1.0 # (1.0 out of 1.0)
                                          end                                         else  # if refactor_mle_diff > -0.1157674603164196
                                           return 0.0 # (0.0 out of 18.0)
                                        end                                       else  # if too-many-statements > 0.5
                                        case when one_file_fix_rate_diff <= -0.875 then
                                           return 1.0 # (1.0 out of 1.0)
                                        else  # if one_file_fix_rate_diff > -0.875
                                           return 0.0 # (0.0 out of 2.0)
                                        end                                       end                                     end                                   else  # if same_day_duration_avg_diff > 296.1388854980469
                                     return 1.0 # (1.0 out of 1.0)
                                  end                                 else  # if refactor_mle_diff > 0.2049209102988243
                                  case when avg_coupling_code_size_cut_diff <= 0.5698757767677307 then
                                     return 1.0 # (3.0 out of 3.0)
                                  else  # if avg_coupling_code_size_cut_diff > 0.5698757767677307
                                    case when superfluous-parens <= 0.5 then
                                       return 0.0 # (0.0 out of 3.0)
                                    else  # if superfluous-parens > 0.5
                                       return 1.0 # (1.0 out of 1.0)
                                    end                                   end                                 end                               else  # if one_file_fix_rate_diff > -0.6547619104385376
                                case when one_file_fix_rate_diff <= -0.5857143104076385 then
                                  case when cur_count_x <= 2.5 then
                                     return 1.0 # (8.0 out of 8.0)
                                  else  # if cur_count_x > 2.5
                                     return 0.0 # (0.0 out of 2.0)
                                  end                                 else  # if one_file_fix_rate_diff > -0.5857143104076385
                                  case when avg_coupling_code_size_cut_diff <= -4.083333253860474 then
                                     return 0.0 # (0.0 out of 7.0)
                                  else  # if avg_coupling_code_size_cut_diff > -4.083333253860474
                                    case when McCabe_sum_before <= 27.0 then
                                      case when prev_count_y <= 0.5 then
                                        case when refactor_mle_diff <= -0.5653376579284668 then
                                          case when refactor_mle_diff <= -0.9274788498878479 then
                                            case when avg_coupling_code_size_cut_diff <= 0.16386555135250092 then
                                               return 0.0 # (0.0 out of 2.0)
                                            else  # if avg_coupling_code_size_cut_diff > 0.16386555135250092
                                               return 1.0 # (1.0 out of 1.0)
                                            end                                           else  # if refactor_mle_diff > -0.9274788498878479
                                             return 1.0 # (6.0 out of 6.0)
                                          end                                         else  # if refactor_mle_diff > -0.5653376579284668
                                          case when refactor_mle_diff <= -0.39430592954158783 then
                                            case when avg_coupling_code_size_cut_diff <= 1.7202380895614624 then
                                               return 0.0 # (0.0 out of 11.0)
                                            else  # if avg_coupling_code_size_cut_diff > 1.7202380895614624
                                              case when avg_coupling_code_size_cut_diff <= 2.5 then
                                                 return 1.0 # (1.0 out of 1.0)
                                              else  # if avg_coupling_code_size_cut_diff > 2.5
                                                 return 0.0 # (0.0 out of 1.0)
                                              end                                             end                                           else  # if refactor_mle_diff > -0.39430592954158783
                                            case when one_file_fix_rate_diff <= 0.1665591448545456 then
                                              case when one_file_fix_rate_diff <= 0.014087301678955555 then
                                                case when too-many-boolean-expressions <= 0.5 then
                                                  case when refactor_mle_diff <= 0.17309515923261642 then
                                                    case when cur_count_x <= 5.5 then
                                                      case when refactor_mle_diff <= 0.05809994228184223 then
                                                        case when avg_coupling_code_size_cut_diff <= 3.5 then
                                                          case when line-too-long <= 0.5 then
                                                            case when one_file_fix_rate_diff <= -0.3452381044626236 then
                                                              case when too-many-statements <= 0.5 then
                                                                 return 0.0 # (0.0 out of 15.0)
                                                              else  # if too-many-statements > 0.5
                                                                case when one_file_fix_rate_diff <= -0.4722222238779068 then
                                                                   return 1.0 # (2.0 out of 2.0)
                                                                else  # if one_file_fix_rate_diff > -0.4722222238779068
                                                                   return 0.0 # (0.0 out of 1.0)
                                                                end                                                               end                                                             else  # if one_file_fix_rate_diff > -0.3452381044626236
                                                              case when same_day_duration_avg_diff <= 65.07936477661133 then
                                                                case when same_day_duration_avg_diff <= 59.9512825012207 then
                                                                  case when unnecessary-pass <= 0.5 then
                                                                    case when same_day_duration_avg_diff <= 11.724137783050537 then
                                                                      case when avg_coupling_code_size_cut_diff <= -0.11250000074505806 then
                                                                        case when same_day_duration_avg_diff <= 0.36789771914482117 then
                                                                           return 0.0 # (0.0 out of 1.0)
                                                                        else  # if same_day_duration_avg_diff > 0.36789771914482117
                                                                           return 1.0 # (9.0 out of 9.0)
                                                                        end                                                                       else  # if avg_coupling_code_size_cut_diff > -0.11250000074505806
                                                                        case when one_file_fix_rate_diff <= -0.1339285746216774 then
                                                                          case when one_file_fix_rate_diff <= -0.3095238208770752 then
                                                                             return 0.0 # (0.0 out of 1.0)
                                                                          else  # if one_file_fix_rate_diff > -0.3095238208770752
                                                                             return 1.0 # (6.0 out of 6.0)
                                                                          end                                                                         else  # if one_file_fix_rate_diff > -0.1339285746216774
                                                                          case when refactor_mle_diff <= -0.272966668009758 then
                                                                            case when same_day_duration_avg_diff <= 3.2916667461395264 then
                                                                               return 0.0 # (0.0 out of 1.0)
                                                                            else  # if same_day_duration_avg_diff > 3.2916667461395264
                                                                               return 1.0 # (3.0 out of 3.0)
                                                                            end                                                                           else  # if refactor_mle_diff > -0.272966668009758
                                                                            case when same_day_duration_avg_diff <= 3.5714285373687744 then
                                                                              case when avg_coupling_code_size_cut_diff <= 0.06666667014360428 then
                                                                                 return 0.0 # (0.0 out of 3.0)
                                                                              else  # if avg_coupling_code_size_cut_diff > 0.06666667014360428
                                                                                case when avg_coupling_code_size_cut_diff <= 1.324999988079071 then
                                                                                   return 1.0 # (5.0 out of 5.0)
                                                                                else  # if avg_coupling_code_size_cut_diff > 1.324999988079071
                                                                                   return 0.0 # (0.0 out of 1.0)
                                                                                end                                                                               end                                                                             else  # if same_day_duration_avg_diff > 3.5714285373687744
                                                                               return 0.0 # (0.0 out of 10.0)
                                                                            end                                                                           end                                                                         end                                                                       end                                                                     else  # if same_day_duration_avg_diff > 11.724137783050537
                                                                      case when avg_coupling_code_size_cut_diff <= 1.6458333134651184 then
                                                                        case when one_file_fix_rate_diff <= -0.03409090917557478 then
                                                                          case when one_file_fix_rate_diff <= -0.1458333358168602 then
                                                                            case when prev_count_x <= 0.5 then
                                                                               return 0.0 # (0.0 out of 4.0)
                                                                            else  # if prev_count_x > 0.5
                                                                              case when superfluous-parens <= 0.5 then
                                                                                 return 1.0 # (3.0 out of 3.0)
                                                                              else  # if superfluous-parens > 0.5
                                                                                 return 0.0 # (0.0 out of 2.0)
                                                                              end                                                                             end                                                                           else  # if one_file_fix_rate_diff > -0.1458333358168602
                                                                             return 1.0 # (4.0 out of 4.0)
                                                                          end                                                                         else  # if one_file_fix_rate_diff > -0.03409090917557478
                                                                          case when unnecessary-semicolon <= 0.5 then
                                                                            case when refactor_mle_diff <= 0.0061571430414915085 then
                                                                              case when avg_coupling_code_size_cut_diff <= -0.27521009743213654 then
                                                                                case when avg_coupling_code_size_cut_diff <= -1.4222221970558167 then
                                                                                   return 0.0 # (0.0 out of 6.0)
                                                                                else  # if avg_coupling_code_size_cut_diff > -1.4222221970558167
                                                                                  case when refactor_mle_diff <= -0.19391316175460815 then
                                                                                     return 0.0 # (0.0 out of 2.0)
                                                                                  else  # if refactor_mle_diff > -0.19391316175460815
                                                                                    case when simplifiable-if-expression <= 0.5 then
                                                                                       return 1.0 # (4.0 out of 4.0)
                                                                                    else  # if simplifiable-if-expression > 0.5
                                                                                       return 0.0 # (0.0 out of 1.0)
                                                                                    end                                                                                   end                                                                                 end                                                                               else  # if avg_coupling_code_size_cut_diff > -0.27521009743213654
                                                                                case when avg_coupling_code_size_cut_diff <= 1.1201298534870148 then
                                                                                   return 0.0 # (0.0 out of 11.0)
                                                                                else  # if avg_coupling_code_size_cut_diff > 1.1201298534870148
                                                                                  case when avg_coupling_code_size_cut_diff <= 1.5982142686843872 then
                                                                                     return 1.0 # (1.0 out of 1.0)
                                                                                  else  # if avg_coupling_code_size_cut_diff > 1.5982142686843872
                                                                                     return 0.0 # (0.0 out of 1.0)
                                                                                  end                                                                                 end                                                                               end                                                                             else  # if refactor_mle_diff > 0.0061571430414915085
                                                                               return 1.0 # (1.0 out of 1.0)
                                                                            end                                                                           else  # if unnecessary-semicolon > 0.5
                                                                             return 1.0 # (1.0 out of 1.0)
                                                                          end                                                                         end                                                                       else  # if avg_coupling_code_size_cut_diff > 1.6458333134651184
                                                                        case when same_day_duration_avg_diff <= 31.050538539886475 then
                                                                           return 0.0 # (0.0 out of 1.0)
                                                                        else  # if same_day_duration_avg_diff > 31.050538539886475
                                                                           return 1.0 # (4.0 out of 4.0)
                                                                        end                                                                       end                                                                     end                                                                   else  # if unnecessary-pass > 0.5
                                                                     return 1.0 # (4.0 out of 4.0)
                                                                  end                                                                 else  # if same_day_duration_avg_diff > 59.9512825012207
                                                                   return 1.0 # (4.0 out of 4.0)
                                                                end                                                               else  # if same_day_duration_avg_diff > 65.07936477661133
                                                                case when one_file_fix_rate_diff <= -0.13051948323845863 then
                                                                  case when avg_coupling_code_size_cut_diff <= -0.7126786410808563 then
                                                                     return 0.0 # (0.0 out of 1.0)
                                                                  else  # if avg_coupling_code_size_cut_diff > -0.7126786410808563
                                                                     return 1.0 # (5.0 out of 5.0)
                                                                  end                                                                 else  # if one_file_fix_rate_diff > -0.13051948323845863
                                                                  case when same_day_duration_avg_diff <= 229.58333587646484 then
                                                                    case when prev_count_x <= 4.5 then
                                                                      case when pointless-statement <= 0.5 then
                                                                        case when superfluous-parens <= 0.5 then
                                                                           return 0.0 # (0.0 out of 19.0)
                                                                        else  # if superfluous-parens > 0.5
                                                                          case when refactor_mle_diff <= -0.015672726556658745 then
                                                                             return 0.0 # (0.0 out of 4.0)
                                                                          else  # if refactor_mle_diff > -0.015672726556658745
                                                                            case when same_day_duration_avg_diff <= 117.61666488647461 then
                                                                               return 0.0 # (0.0 out of 1.0)
                                                                            else  # if same_day_duration_avg_diff > 117.61666488647461
                                                                               return 1.0 # (1.0 out of 1.0)
                                                                            end                                                                           end                                                                         end                                                                       else  # if pointless-statement > 0.5
                                                                        case when same_day_duration_avg_diff <= 118.41470718383789 then
                                                                           return 1.0 # (1.0 out of 1.0)
                                                                        else  # if same_day_duration_avg_diff > 118.41470718383789
                                                                           return 0.0 # (0.0 out of 1.0)
                                                                        end                                                                       end                                                                     else  # if prev_count_x > 4.5
                                                                       return 1.0 # (1.0 out of 1.0)
                                                                    end                                                                   else  # if same_day_duration_avg_diff > 229.58333587646484
                                                                    case when avg_coupling_code_size_cut_diff <= -0.2777777910232544 then
                                                                       return 0.0 # (0.0 out of 2.0)
                                                                    else  # if avg_coupling_code_size_cut_diff > -0.2777777910232544
                                                                       return 1.0 # (3.0 out of 3.0)
                                                                    end                                                                   end                                                                 end                                                               end                                                             end                                                           else  # if line-too-long > 0.5
                                                            case when refactor_mle_diff <= 0.023402715101838112 then
                                                              case when one_file_fix_rate_diff <= -0.0833333358168602 then
                                                                 return 1.0 # (7.0 out of 7.0)
                                                              else  # if one_file_fix_rate_diff > -0.0833333358168602
                                                                case when refactor_mle_diff <= -0.15149664878845215 then
                                                                  case when same_day_duration_avg_diff <= 244.1666717529297 then
                                                                    case when cur_count_x <= 0.5 then
                                                                       return 0.0 # (0.0 out of 1.0)
                                                                    else  # if cur_count_x > 0.5
                                                                       return 1.0 # (9.0 out of 9.0)
                                                                    end                                                                   else  # if same_day_duration_avg_diff > 244.1666717529297
                                                                     return 0.0 # (0.0 out of 1.0)
                                                                  end                                                                 else  # if refactor_mle_diff > -0.15149664878845215
                                                                  case when refactor_mle_diff <= -0.03591666743159294 then
                                                                     return 0.0 # (0.0 out of 5.0)
                                                                  else  # if refactor_mle_diff > -0.03591666743159294
                                                                    case when prev_count_x <= 0.5 then
                                                                      case when same_day_duration_avg_diff <= 84.16388702392578 then
                                                                         return 0.0 # (0.0 out of 3.0)
                                                                      else  # if same_day_duration_avg_diff > 84.16388702392578
                                                                         return 1.0 # (1.0 out of 1.0)
                                                                      end                                                                     else  # if prev_count_x > 0.5
                                                                       return 1.0 # (4.0 out of 4.0)
                                                                    end                                                                   end                                                                 end                                                               end                                                             else  # if refactor_mle_diff > 0.023402715101838112
                                                               return 0.0 # (0.0 out of 3.0)
                                                            end                                                           end                                                         else  # if avg_coupling_code_size_cut_diff > 3.5
                                                           return 0.0 # (0.0 out of 5.0)
                                                        end                                                       else  # if refactor_mle_diff > 0.05809994228184223
                                                        case when avg_coupling_code_size_cut_diff <= 1.2178571820259094 then
                                                          case when superfluous-parens <= 0.5 then
                                                            case when refactor_mle_diff <= 0.0804171934723854 then
                                                               return 1.0 # (3.0 out of 3.0)
                                                            else  # if refactor_mle_diff > 0.0804171934723854
                                                              case when avg_coupling_code_size_cut_diff <= -0.5307539701461792 then
                                                                case when same_day_duration_avg_diff <= 114.98059463500977 then
                                                                  case when refactor_mle_diff <= 0.13557476550340652 then
                                                                     return 0.0 # (0.0 out of 2.0)
                                                                  else  # if refactor_mle_diff > 0.13557476550340652
                                                                    case when avg_coupling_code_size_cut_diff <= -1.2229118943214417 then
                                                                       return 0.0 # (0.0 out of 1.0)
                                                                    else  # if avg_coupling_code_size_cut_diff > -1.2229118943214417
                                                                       return 1.0 # (2.0 out of 2.0)
                                                                    end                                                                   end                                                                 else  # if same_day_duration_avg_diff > 114.98059463500977
                                                                   return 1.0 # (3.0 out of 3.0)
                                                                end                                                               else  # if avg_coupling_code_size_cut_diff > -0.5307539701461792
                                                                case when simplifiable-if-expression <= 0.5 then
                                                                  case when broad-exception-caught <= 0.5 then
                                                                    case when same_day_duration_avg_diff <= 106.63181686401367 then
                                                                       return 0.0 # (0.0 out of 10.0)
                                                                    else  # if same_day_duration_avg_diff > 106.63181686401367
                                                                      case when same_day_duration_avg_diff <= 167.19393920898438 then
                                                                         return 1.0 # (1.0 out of 1.0)
                                                                      else  # if same_day_duration_avg_diff > 167.19393920898438
                                                                         return 0.0 # (0.0 out of 5.0)
                                                                      end                                                                     end                                                                   else  # if broad-exception-caught > 0.5
                                                                     return 1.0 # (1.0 out of 1.0)
                                                                  end                                                                 else  # if simplifiable-if-expression > 0.5
                                                                   return 1.0 # (1.0 out of 1.0)
                                                                end                                                               end                                                             end                                                           else  # if superfluous-parens > 0.5
                                                             return 1.0 # (5.0 out of 5.0)
                                                          end                                                         else  # if avg_coupling_code_size_cut_diff > 1.2178571820259094
                                                           return 1.0 # (11.0 out of 11.0)
                                                        end                                                       end                                                     else  # if cur_count_x > 5.5
                                                      case when same_day_duration_avg_diff <= 208.43333435058594 then
                                                         return 0.0 # (0.0 out of 9.0)
                                                      else  # if same_day_duration_avg_diff > 208.43333435058594
                                                         return 1.0 # (1.0 out of 1.0)
                                                      end                                                     end                                                   else  # if refactor_mle_diff > 0.17309515923261642
                                                    case when avg_coupling_code_size_cut_diff <= 0.6194171905517578 then
                                                      case when same_day_duration_avg_diff <= 367.4166717529297 then
                                                        case when one_file_fix_rate_diff <= -0.3512820601463318 then
                                                          case when same_day_duration_avg_diff <= 45.76128387451172 then
                                                             return 1.0 # (3.0 out of 3.0)
                                                          else  # if same_day_duration_avg_diff > 45.76128387451172
                                                            case when superfluous-parens <= 0.5 then
                                                               return 0.0 # (0.0 out of 3.0)
                                                            else  # if superfluous-parens > 0.5
                                                               return 1.0 # (1.0 out of 1.0)
                                                            end                                                           end                                                         else  # if one_file_fix_rate_diff > -0.3512820601463318
                                                          case when simplifiable-if-expression <= 0.5 then
                                                            case when avg_coupling_code_size_cut_diff <= -0.7596153914928436 then
                                                              case when avg_coupling_code_size_cut_diff <= -1.2545787692070007 then
                                                                 return 0.0 # (0.0 out of 7.0)
                                                              else  # if avg_coupling_code_size_cut_diff > -1.2545787692070007
                                                                case when refactor_mle_diff <= 0.27036920189857483 then
                                                                   return 0.0 # (0.0 out of 3.0)
                                                                else  # if refactor_mle_diff > 0.27036920189857483
                                                                   return 1.0 # (3.0 out of 3.0)
                                                                end                                                               end                                                             else  # if avg_coupling_code_size_cut_diff > -0.7596153914928436
                                                              case when same_day_duration_avg_diff <= 163.58333587646484 then
                                                                 return 0.0 # (0.0 out of 28.0)
                                                              else  # if same_day_duration_avg_diff > 163.58333587646484
                                                                 return 1.0 # (1.0 out of 1.0)
                                                              end                                                             end                                                           else  # if simplifiable-if-expression > 0.5
                                                             return 1.0 # (1.0 out of 1.0)
                                                          end                                                         end                                                       else  # if same_day_duration_avg_diff > 367.4166717529297
                                                         return 1.0 # (2.0 out of 2.0)
                                                      end                                                     else  # if avg_coupling_code_size_cut_diff > 0.6194171905517578
                                                      case when same_day_duration_avg_diff <= 65.5250015258789 then
                                                        case when cur_count_x <= 11.5 then
                                                          case when avg_coupling_code_size_cut_diff <= 1.9285714030265808 then
                                                             return 1.0 # (8.0 out of 8.0)
                                                          else  # if avg_coupling_code_size_cut_diff > 1.9285714030265808
                                                            case when one_file_fix_rate_diff <= -0.04545454680919647 then
                                                               return 0.0 # (0.0 out of 1.0)
                                                            else  # if one_file_fix_rate_diff > -0.04545454680919647
                                                              case when avg_coupling_code_size_cut_diff <= 2.149999976158142 then
                                                                case when refactor_mle_diff <= 0.272966668009758 then
                                                                   return 1.0 # (2.0 out of 2.0)
                                                                else  # if refactor_mle_diff > 0.272966668009758
                                                                   return 0.0 # (0.0 out of 1.0)
                                                                end                                                               else  # if avg_coupling_code_size_cut_diff > 2.149999976158142
                                                                 return 1.0 # (2.0 out of 2.0)
                                                              end                                                             end                                                           end                                                         else  # if cur_count_x > 11.5
                                                           return 0.0 # (0.0 out of 1.0)
                                                        end                                                       else  # if same_day_duration_avg_diff > 65.5250015258789
                                                        case when avg_coupling_code_size_cut_diff <= 2.5 then
                                                           return 0.0 # (0.0 out of 6.0)
                                                        else  # if avg_coupling_code_size_cut_diff > 2.5
                                                           return 1.0 # (1.0 out of 1.0)
                                                        end                                                       end                                                     end                                                   end                                                 else  # if too-many-boolean-expressions > 0.5
                                                  case when prev_count_x <= 1.5 then
                                                     return 0.0 # (0.0 out of 10.0)
                                                  else  # if prev_count_x > 1.5
                                                    case when avg_coupling_code_size_cut_diff <= -0.21540075913071632 then
                                                       return 1.0 # (1.0 out of 1.0)
                                                    else  # if avg_coupling_code_size_cut_diff > -0.21540075913071632
                                                       return 0.0 # (0.0 out of 1.0)
                                                    end                                                   end                                                 end                                               else  # if one_file_fix_rate_diff > 0.014087301678955555
                                                case when refactor_mle_diff <= 0.31954948604106903 then
                                                  case when same_day_duration_avg_diff <= 3.594209909439087 then
                                                    case when simplifiable-if-expression <= 0.5 then
                                                       return 1.0 # (3.0 out of 3.0)
                                                    else  # if simplifiable-if-expression > 0.5
                                                       return 0.0 # (0.0 out of 1.0)
                                                    end                                                   else  # if same_day_duration_avg_diff > 3.594209909439087
                                                    case when pointless-statement <= 0.5 then
                                                      case when cur_count_x <= 0.5 then
                                                        case when avg_coupling_code_size_cut_diff <= -0.39004287123680115 then
                                                           return 0.0 # (0.0 out of 2.0)
                                                        else  # if avg_coupling_code_size_cut_diff > -0.39004287123680115
                                                           return 1.0 # (1.0 out of 1.0)
                                                        end                                                       else  # if cur_count_x > 0.5
                                                         return 0.0 # (0.0 out of 33.0)
                                                      end                                                     else  # if pointless-statement > 0.5
                                                       return 1.0 # (1.0 out of 1.0)
                                                    end                                                   end                                                 else  # if refactor_mle_diff > 0.31954948604106903
                                                   return 1.0 # (3.0 out of 3.0)
                                                end                                               end                                             else  # if one_file_fix_rate_diff > 0.1665591448545456
                                              case when one_file_fix_rate_diff <= 0.170634925365448 then
                                                 return 1.0 # (8.0 out of 8.0)
                                              else  # if one_file_fix_rate_diff > 0.170634925365448
                                                case when avg_coupling_code_size_cut_diff <= -0.8137820661067963 then
                                                   return 0.0 # (0.0 out of 5.0)
                                                else  # if avg_coupling_code_size_cut_diff > -0.8137820661067963
                                                  case when too-many-statements <= 0.5 then
                                                    case when prev_count_x <= 0.5 then
                                                       return 1.0 # (5.0 out of 5.0)
                                                    else  # if prev_count_x > 0.5
                                                      case when refactor_mle_diff <= 0.13468749821186066 then
                                                        case when one_file_fix_rate_diff <= 0.24188034981489182 then
                                                           return 0.0 # (0.0 out of 4.0)
                                                        else  # if one_file_fix_rate_diff > 0.24188034981489182
                                                           return 1.0 # (1.0 out of 1.0)
                                                        end                                                       else  # if refactor_mle_diff > 0.13468749821186066
                                                         return 1.0 # (3.0 out of 3.0)
                                                      end                                                     end                                                   else  # if too-many-statements > 0.5
                                                    case when prev_count_x <= 6.5 then
                                                       return 0.0 # (0.0 out of 4.0)
                                                    else  # if prev_count_x > 6.5
                                                       return 1.0 # (1.0 out of 1.0)
                                                    end                                                   end                                                 end                                               end                                             end                                           end                                         end                                       else  # if prev_count_y > 0.5
                                        case when hunks_num <= 3.5 then
                                          case when added_lines <= 14.5 then
                                            case when one_file_fix_rate_diff <= -0.05263157933950424 then
                                              case when one_file_fix_rate_diff <= -0.1180555559694767 then
                                                 return 1.0 # (4.0 out of 4.0)
                                              else  # if one_file_fix_rate_diff > -0.1180555559694767
                                                 return 0.0 # (0.0 out of 2.0)
                                              end                                             else  # if one_file_fix_rate_diff > -0.05263157933950424
                                               return 1.0 # (12.0 out of 12.0)
                                            end                                           else  # if added_lines > 14.5
                                             return 0.0 # (0.0 out of 1.0)
                                          end                                         else  # if hunks_num > 3.5
                                           return 0.0 # (0.0 out of 2.0)
                                        end                                       end                                     else  # if McCabe_sum_before > 27.0
                                      case when modified_McCabe_max_diff <= -3.5 then
                                         return 1.0 # (2.0 out of 2.0)
                                      else  # if modified_McCabe_max_diff > -3.5
                                        case when Blank_diff <= 6.5 then
                                          case when refactor_mle_diff <= 0.1929549053311348 then
                                             return 0.0 # (0.0 out of 17.0)
                                          else  # if refactor_mle_diff > 0.1929549053311348
                                            case when LOC_diff <= 2.5 then
                                               return 1.0 # (1.0 out of 1.0)
                                            else  # if LOC_diff > 2.5
                                               return 0.0 # (0.0 out of 1.0)
                                            end                                           end                                         else  # if Blank_diff > 6.5
                                           return 1.0 # (1.0 out of 1.0)
                                        end                                       end                                     end                                   end                                 end                               end                             else  # if cur_count_x > 19.0
                              case when one_file_fix_rate_diff <= 0.19239510595798492 then
                                case when same_day_duration_avg_diff <= 187.33333587646484 then
                                   return 1.0 # (12.0 out of 12.0)
                                else  # if same_day_duration_avg_diff > 187.33333587646484
                                   return 0.0 # (0.0 out of 1.0)
                                end                               else  # if one_file_fix_rate_diff > 0.19239510595798492
                                 return 0.0 # (0.0 out of 1.0)
                              end                             end                           else  # if cur_count_x > 66.5
                            case when refactor_mle_diff <= -0.26578332483768463 then
                               return 1.0 # (1.0 out of 1.0)
                            else  # if refactor_mle_diff > -0.26578332483768463
                               return 0.0 # (0.0 out of 12.0)
                            end                           end                         else  # if one_file_fix_rate_diff > 0.26713287830352783
                          case when too-many-lines <= 0.5 then
                            case when try-except-raise <= 0.5 then
                              case when broad-exception-caught <= 0.5 then
                                case when simplifiable-if-statement <= 0.5 then
                                  case when same_day_duration_avg_diff <= 48.272727966308594 then
                                    case when same_day_duration_avg_diff <= 21.48488998413086 then
                                      case when cur_count_x <= 24.5 then
                                        case when too-many-branches <= 0.5 then
                                           return 0.0 # (0.0 out of 9.0)
                                        else  # if too-many-branches > 0.5
                                          case when one_file_fix_rate_diff <= 0.3095238208770752 then
                                             return 1.0 # (1.0 out of 1.0)
                                          else  # if one_file_fix_rate_diff > 0.3095238208770752
                                             return 0.0 # (0.0 out of 2.0)
                                          end                                         end                                       else  # if cur_count_x > 24.5
                                         return 1.0 # (1.0 out of 1.0)
                                      end                                     else  # if same_day_duration_avg_diff > 21.48488998413086
                                      case when same_day_duration_avg_diff <= 32.24666690826416 then
                                         return 1.0 # (3.0 out of 3.0)
                                      else  # if same_day_duration_avg_diff > 32.24666690826416
                                        case when avg_coupling_code_size_cut_diff <= 0.3949275314807892 then
                                          case when vocabulary_diff <= -1.0 then
                                             return 0.0 # (0.0 out of 1.0)
                                          else  # if vocabulary_diff > -1.0
                                             return 1.0 # (2.0 out of 2.0)
                                          end                                         else  # if avg_coupling_code_size_cut_diff > 0.3949275314807892
                                           return 0.0 # (0.0 out of 3.0)
                                        end                                       end                                     end                                   else  # if same_day_duration_avg_diff > 48.272727966308594
                                    case when refactor_mle_diff <= 0.059519048780202866 then
                                       return 0.0 # (0.0 out of 17.0)
                                    else  # if refactor_mle_diff > 0.059519048780202866
                                      case when refactor_mle_diff <= 0.06996753253042698 then
                                         return 1.0 # (1.0 out of 1.0)
                                      else  # if refactor_mle_diff > 0.06996753253042698
                                        case when avg_coupling_code_size_cut_diff <= -0.009344596415758133 then
                                          case when cur_count_x <= 1.5 then
                                            case when avg_coupling_code_size_cut_diff <= -0.43593189865350723 then
                                               return 0.0 # (0.0 out of 5.0)
                                            else  # if avg_coupling_code_size_cut_diff > -0.43593189865350723
                                               return 1.0 # (1.0 out of 1.0)
                                            end                                           else  # if cur_count_x > 1.5
                                             return 1.0 # (1.0 out of 1.0)
                                          end                                         else  # if avg_coupling_code_size_cut_diff > -0.009344596415758133
                                           return 0.0 # (0.0 out of 8.0)
                                        end                                       end                                     end                                   end                                 else  # if simplifiable-if-statement > 0.5
                                   return 1.0 # (1.0 out of 1.0)
                                end                               else  # if broad-exception-caught > 0.5
                                case when same_day_duration_avg_diff <= 9.726190567016602 then
                                   return 0.0 # (0.0 out of 1.0)
                                else  # if same_day_duration_avg_diff > 9.726190567016602
                                   return 1.0 # (2.0 out of 2.0)
                                end                               end                             else  # if try-except-raise > 0.5
                               return 1.0 # (1.0 out of 1.0)
                            end                           else  # if too-many-lines > 0.5
                             return 1.0 # (1.0 out of 1.0)
                          end                         end                       else  # if prev_count_y > 1.5
                        case when N1_diff <= 3.0 then
                           return 1.0 # (6.0 out of 6.0)
                        else  # if N1_diff > 3.0
                           return 0.0 # (0.0 out of 1.0)
                        end                       end                     else  # if LOC_before > 956.5
                       return 1.0 # (5.0 out of 5.0)
                    end                   else  # if Comments_before > 102.0
                     return 0.0 # (0.0 out of 11.0)
                  end                 else  # if McCabe_sum_after > 101.0
                  case when Blank_diff <= -4.5 then
                     return 1.0 # (8.0 out of 8.0)
                  else  # if Blank_diff > -4.5
                    case when SLOC_before <= 583.5 then
                      case when McCabe_max_after <= 28.5 then
                        case when McCabe_sum_after <= 112.5 then
                           return 1.0 # (1.0 out of 1.0)
                        else  # if McCabe_sum_after > 112.5
                           return 0.0 # (0.0 out of 9.0)
                        end                       else  # if McCabe_max_after > 28.5
                         return 1.0 # (2.0 out of 2.0)
                      end                     else  # if SLOC_before > 583.5
                      case when McCabe_max_diff <= -0.5 then
                         return 0.0 # (0.0 out of 5.0)
                      else  # if McCabe_max_diff > -0.5
                        case when SLOC_before <= 1625.0 then
                          case when Comments_before <= 20.5 then
                             return 0.0 # (0.0 out of 1.0)
                          else  # if Comments_before > 20.5
                            case when try-except-raise <= 0.5 then
                               return 1.0 # (19.0 out of 19.0)
                            else  # if try-except-raise > 0.5
                               return 0.0 # (0.0 out of 1.0)
                            end                           end                         else  # if SLOC_before > 1625.0
                          case when h2_diff <= 0.5 then
                             return 0.0 # (0.0 out of 5.0)
                          else  # if h2_diff > 0.5
                            case when modified_McCabe_max_diff <= 3.0 then
                               return 1.0 # (2.0 out of 2.0)
                            else  # if modified_McCabe_max_diff > 3.0
                               return 0.0 # (0.0 out of 1.0)
                            end                           end                         end                       end                     end                   end                 end               else  # if McCabe_max_after > 34.0
                case when same_day_duration_avg_diff <= 99.22575759887695 then
                   return 0.0 # (0.0 out of 19.0)
                else  # if same_day_duration_avg_diff > 99.22575759887695
                  case when McCabe_sum_after <= 442.5 then
                     return 1.0 # (2.0 out of 2.0)
                  else  # if McCabe_sum_after > 442.5
                     return 0.0 # (0.0 out of 1.0)
                  end                 end               end             end           else  # if McCabe_max_before > 51.0
             return 1.0 # (11.0 out of 11.0)
          end         end       end     else  # if hunks_num > 11.5
      case when Comments_after <= 213.0 then
        case when McCabe_max_before <= 15.5 then
          case when hunks_num <= 14.5 then
             return 0.0 # (0.0 out of 4.0)
          else  # if hunks_num > 14.5
            case when removed_lines <= 94.0 then
               return 1.0 # (6.0 out of 6.0)
            else  # if removed_lines > 94.0
              case when Single comments_before <= 51.0 then
                 return 0.0 # (0.0 out of 2.0)
              else  # if Single comments_before > 51.0
                 return 1.0 # (1.0 out of 1.0)
              end             end           end         else  # if McCabe_max_before > 15.5
          case when SLOC_before <= 436.0 then
            case when removed_lines <= 143.0 then
               return 1.0 # (3.0 out of 3.0)
            else  # if removed_lines > 143.0
               return 0.0 # (0.0 out of 1.0)
            end           else  # if SLOC_before > 436.0
            case when Multi_diff <= -31.0 then
               return 1.0 # (1.0 out of 1.0)
            else  # if Multi_diff > -31.0
              case when LOC_before <= 1957.0 then
                 return 0.0 # (0.0 out of 71.0)
              else  # if LOC_before > 1957.0
                case when Comments_before <= 175.0 then
                   return 0.0 # (0.0 out of 2.0)
                else  # if Comments_before > 175.0
                   return 1.0 # (1.0 out of 1.0)
                end               end             end           end         end       else  # if Comments_after > 213.0
        case when Blank_before <= 1139.5 then
          case when removed_lines <= 48.0 then
             return 0.0 # (0.0 out of 1.0)
          else  # if removed_lines > 48.0
             return 1.0 # (7.0 out of 7.0)
          end         else  # if Blank_before > 1139.5
           return 0.0 # (0.0 out of 2.0)
        end       end     end   else  # if SLOC_diff > 38.0
    case when avg_coupling_code_size_cut_diff <= -1.1746032238006592 then
       return 0.0 # (0.0 out of 5.0)
    else  # if avg_coupling_code_size_cut_diff > -1.1746032238006592
      case when length_diff <= 36.0 then
        case when Multi_diff <= -5.0 then
           return 0.0 # (0.0 out of 2.0)
        else  # if Multi_diff > -5.0
          case when SLOC_before <= 2855.0 then
            case when vocabulary_diff <= -35.0 then
               return 0.0 # (0.0 out of 1.0)
            else  # if vocabulary_diff > -35.0
              case when avg_coupling_code_size_cut_diff <= -0.7708333432674408 then
                case when N1_diff <= 6.0 then
                   return 1.0 # (2.0 out of 2.0)
                else  # if N1_diff > 6.0
                   return 0.0 # (0.0 out of 1.0)
                end               else  # if avg_coupling_code_size_cut_diff > -0.7708333432674408
                 return 1.0 # (44.0 out of 44.0)
              end             end           else  # if SLOC_before > 2855.0
             return 0.0 # (0.0 out of 2.0)
          end         end       else  # if length_diff > 36.0
        case when LOC_before <= 578.5 then
           return 1.0 # (1.0 out of 1.0)
        else  # if LOC_before > 578.5
           return 0.0 # (0.0 out of 5.0)
        end       end     end   end )