create or replace function Tree_default (using-constant-test int64, simplifiable-if-statement int64, Comments_after int64, same_day_duration_avg_diff int64, Single comments_before int64, one_file_fix_rate_diff int64, too-many-boolean-expressions int64, Single comments_diff int64, high_McCabe_sum_before int64, pointless-statement int64, bugs_diff int64, McCabe_max_before int64, length_diff int64, LOC_diff int64, N2_diff int64, superfluous-parens int64, too-many-nested-blocks int64, effort_diff int64, cur_count_x int64, high_McCabe_max_before int64, comparison-of-constants int64, SLOC_diff int64, hunks_num int64, high_McCabe_max_diff int64, prev_count int64, McCabe_sum_after int64, cur_count_y int64, refactor_mle_diff int64, too-many-return-statements int64, too-many-statements int64, too-many-lines int64, only_removal int64, removed_lines int64, cur_count int64, volume_diff int64, is_refactor int64, prev_count_y int64, calculated_length_diff int64, Simplify-boolean-expression int64, h1_diff int64, McCabe_max_diff int64, wildcard-import int64, McCabe_sum_before int64, line-too-long int64, N1_diff int64, too-many-branches int64, h2_diff int64, McCabe_max_after int64, unnecessary-pass int64, avg_coupling_code_size_cut_diff int64, high_ccp_group int64, vocabulary_diff int64, try-except-raise int64, broad-exception-caught int64, simplifiable-condition int64, LLOC_before int64, added_functions int64, LLOC_diff int64, difficulty_diff int64, McCabe_sum_diff int64, Multi_diff int64, massive_change int64, mostly_delete int64, Comments_before int64, changed_lines int64, Comments_diff int64, time_diff int64, Blank_before int64, high_McCabe_sum_diff int64, added_lines int64, prev_count_x int64, unnecessary-semicolon int64, Blank_diff int64, modified_McCabe_max_diff int64, Single comments_after int64, LOC_before int64, simplifiable-if-expression int64, SLOC_before int64) as (
  case when high_ccp_group <= 0.5 then
    case when Comments_diff <= -21.0 then
      case when same_day_duration_avg_diff <= -33.64265823364258 then
        case when Multi_diff <= 3.5 then
           return 0.0 # (0.0 out of 4.0)
        else  # if Multi_diff > 3.5
           return 1.0 # (3.0 out of 3.0)
        end       else  # if same_day_duration_avg_diff > -33.64265823364258
        case when length_diff <= -13.0 then
           return 1.0 # (26.0 out of 26.0)
        else  # if length_diff > -13.0
           return 0.0 # (0.0 out of 1.0)
        end       end     else  # if Comments_diff > -21.0
      case when SLOC_diff <= 38.0 then
        case when Comments_after <= 6.5 then
          case when one_file_fix_rate_diff <= -0.0555555559694767 then
             return 1.0 # (10.0 out of 10.0)
          else  # if one_file_fix_rate_diff > -0.0555555559694767
            case when McCabe_sum_after <= 39.5 then
              case when McCabe_max_after <= 8.5 then
                case when McCabe_sum_before <= 0.5 then
                   return 1.0 # (2.0 out of 2.0)
                else  # if McCabe_sum_before > 0.5
                  case when LLOC_before <= 365.0 then
                    case when avg_coupling_code_size_cut_diff <= 1.4801586866378784 then
                       return 0.0 # (0.0 out of 10.0)
                    else  # if avg_coupling_code_size_cut_diff > 1.4801586866378784
                      case when McCabe_max_after <= 5.0 then
                         return 0.0 # (0.0 out of 1.0)
                      else  # if McCabe_max_after > 5.0
                         return 1.0 # (1.0 out of 1.0)
                      end                     end                   else  # if LLOC_before > 365.0
                     return 1.0 # (1.0 out of 1.0)
                  end                 end               else  # if McCabe_max_after > 8.5
                 return 1.0 # (2.0 out of 2.0)
              end             else  # if McCabe_sum_after > 39.5
               return 1.0 # (3.0 out of 3.0)
            end           end         else  # if Comments_after > 6.5
          case when one_file_fix_rate_diff <= 0.9166666567325592 then
            case when McCabe_sum_after <= 369.0 then
              case when McCabe_max_diff <= -0.5 then
                case when avg_coupling_code_size_cut_diff <= 0.18065998703241348 then
                  case when McCabe_sum_before <= 335.5 then
                    case when Blank_before <= 211.5 then
                      case when too-many-nested-blocks <= 0.5 then
                        case when changed_lines <= 21.5 then
                          case when h2_diff <= -4.5 then
                             return 1.0 # (1.0 out of 1.0)
                          else  # if h2_diff > -4.5
                             return 0.0 # (0.0 out of 4.0)
                          end                         else  # if changed_lines > 21.5
                           return 0.0 # (0.0 out of 59.0)
                        end                       else  # if too-many-nested-blocks > 0.5
                        case when high_McCabe_max_before <= 0.5 then
                           return 0.0 # (0.0 out of 2.0)
                        else  # if high_McCabe_max_before > 0.5
                           return 1.0 # (1.0 out of 1.0)
                        end                       end                     else  # if Blank_before > 211.5
                      case when one_file_fix_rate_diff <= 0.08055555634200573 then
                         return 1.0 # (2.0 out of 2.0)
                      else  # if one_file_fix_rate_diff > 0.08055555634200573
                         return 0.0 # (0.0 out of 5.0)
                      end                     end                   else  # if McCabe_sum_before > 335.5
                     return 1.0 # (1.0 out of 1.0)
                  end                 else  # if avg_coupling_code_size_cut_diff > 0.18065998703241348
                  case when same_day_duration_avg_diff <= -19.88888931274414 then
                    case when Blank_diff <= -4.5 then
                      case when LLOC_diff <= -320.5 then
                         return 1.0 # (1.0 out of 1.0)
                      else  # if LLOC_diff > -320.5
                         return 0.0 # (0.0 out of 2.0)
                      end                     else  # if Blank_diff > -4.5
                       return 1.0 # (4.0 out of 4.0)
                    end                   else  # if same_day_duration_avg_diff > -19.88888931274414
                    case when avg_coupling_code_size_cut_diff <= 0.2668016254901886 then
                       return 1.0 # (1.0 out of 1.0)
                    else  # if avg_coupling_code_size_cut_diff > 0.2668016254901886
                      case when Multi_diff <= 3.5 then
                         return 0.0 # (0.0 out of 11.0)
                      else  # if Multi_diff > 3.5
                         return 1.0 # (1.0 out of 1.0)
                      end                     end                   end                 end               else  # if McCabe_max_diff > -0.5
                case when modified_McCabe_max_diff <= -0.5 then
                  case when one_file_fix_rate_diff <= -0.02463235380128026 then
                    case when LLOC_before <= 911.5 then
                       return 0.0 # (0.0 out of 8.0)
                    else  # if LLOC_before > 911.5
                       return 1.0 # (2.0 out of 2.0)
                    end                   else  # if one_file_fix_rate_diff > -0.02463235380128026
                    case when Comments_before <= 62.0 then
                      case when N1_diff <= 3.5 then
                        case when McCabe_max_after <= 7.0 then
                           return 0.0 # (0.0 out of 1.0)
                        else  # if McCabe_max_after > 7.0
                           return 1.0 # (15.0 out of 15.0)
                        end                       else  # if N1_diff > 3.5
                        case when LOC_diff <= -18.5 then
                           return 1.0 # (1.0 out of 1.0)
                        else  # if LOC_diff > -18.5
                           return 0.0 # (0.0 out of 2.0)
                        end                       end                     else  # if Comments_before > 62.0
                      case when same_day_duration_avg_diff <= 116.66111373901367 then
                        case when LLOC_diff <= -2.0 then
                           return 0.0 # (0.0 out of 7.0)
                        else  # if LLOC_diff > -2.0
                           return 1.0 # (1.0 out of 1.0)
                        end                       else  # if same_day_duration_avg_diff > 116.66111373901367
                         return 1.0 # (2.0 out of 2.0)
                      end                     end                   end                 else  # if modified_McCabe_max_diff > -0.5
                  case when McCabe_sum_before <= 175.5 then
                    case when added_lines <= 116.5 then
                      case when McCabe_max_after <= 41.0 then
                        case when SLOC_before <= 121.0 then
                          case when Blank_diff <= 3.0 then
                             return 1.0 # (4.0 out of 4.0)
                          else  # if Blank_diff > 3.0
                             return 0.0 # (0.0 out of 1.0)
                          end                         else  # if SLOC_before > 121.0
                          case when McCabe_sum_after <= 101.0 then
                            case when same_day_duration_avg_diff <= -23.587565422058105 then
                              case when one_file_fix_rate_diff <= 0.2916666716337204 then
                                case when Comments_before <= 22.5 then
                                  case when added_lines <= 1.0 then
                                     return 0.0 # (0.0 out of 1.0)
                                  else  # if added_lines > 1.0
                                     return 1.0 # (3.0 out of 3.0)
                                  end                                 else  # if Comments_before > 22.5
                                  case when avg_coupling_code_size_cut_diff <= -0.06302521377801895 then
                                    case when same_day_duration_avg_diff <= -143.37105560302734 then
                                       return 0.0 # (0.0 out of 2.0)
                                    else  # if same_day_duration_avg_diff > -143.37105560302734
                                      case when refactor_mle_diff <= -0.2383088544011116 then
                                         return 0.0 # (0.0 out of 1.0)
                                      else  # if refactor_mle_diff > -0.2383088544011116
                                         return 1.0 # (3.0 out of 3.0)
                                      end                                     end                                   else  # if avg_coupling_code_size_cut_diff > -0.06302521377801895
                                     return 0.0 # (0.0 out of 13.0)
                                  end                                 end                               else  # if one_file_fix_rate_diff > 0.2916666716337204
                                 return 1.0 # (3.0 out of 3.0)
                              end                             else  # if same_day_duration_avg_diff > -23.587565422058105
                              case when SLOC_before <= 211.5 then
                                case when refactor_mle_diff <= 0.10774999856948853 then
                                   return 0.0 # (0.0 out of 4.0)
                                else  # if refactor_mle_diff > 0.10774999856948853
                                   return 1.0 # (2.0 out of 2.0)
                                end                               else  # if SLOC_before > 211.5
                                 return 0.0 # (0.0 out of 34.0)
                              end                             end                           else  # if McCabe_sum_after > 101.0
                            case when SLOC_before <= 642.5 then
                              case when McCabe_sum_before <= 133.5 then
                                case when LLOC_before <= 257.0 then
                                   return 0.0 # (0.0 out of 3.0)
                                else  # if LLOC_before > 257.0
                                  case when SLOC_diff <= 4.5 then
                                     return 1.0 # (7.0 out of 7.0)
                                  else  # if SLOC_diff > 4.5
                                     return 0.0 # (0.0 out of 2.0)
                                  end                                 end                               else  # if McCabe_sum_before > 133.5
                                 return 0.0 # (0.0 out of 12.0)
                              end                             else  # if SLOC_before > 642.5
                               return 1.0 # (6.0 out of 6.0)
                            end                           end                         end                       else  # if McCabe_max_after > 41.0
                         return 1.0 # (4.0 out of 4.0)
                      end                     else  # if added_lines > 116.5
                      case when LLOC_before <= 557.0 then
                         return 1.0 # (6.0 out of 6.0)
                      else  # if LLOC_before > 557.0
                         return 0.0 # (0.0 out of 1.0)
                      end                     end                   else  # if McCabe_sum_before > 175.5
                    case when same_day_duration_avg_diff <= -219.61111450195312 then
                       return 1.0 # (1.0 out of 1.0)
                    else  # if same_day_duration_avg_diff > -219.61111450195312
                      case when McCabe_max_after <= 62.0 then
                        case when Blank_before <= 96.5 then
                          case when added_lines <= 6.5 then
                             return 0.0 # (0.0 out of 2.0)
                          else  # if added_lines > 6.5
                             return 1.0 # (1.0 out of 1.0)
                          end                         else  # if Blank_before > 96.5
                          case when too-many-return-statements <= 0.5 then
                             return 0.0 # (0.0 out of 44.0)
                          else  # if too-many-return-statements > 0.5
                            case when LLOC_before <= 665.5 then
                               return 0.0 # (0.0 out of 3.0)
                            else  # if LLOC_before > 665.5
                               return 1.0 # (1.0 out of 1.0)
                            end                           end                         end                       else  # if McCabe_max_after > 62.0
                        case when McCabe_sum_before <= 202.0 then
                           return 0.0 # (0.0 out of 1.0)
                        else  # if McCabe_sum_before > 202.0
                           return 1.0 # (1.0 out of 1.0)
                        end                       end                     end                   end                 end               end             else  # if McCabe_sum_after > 369.0
              case when avg_coupling_code_size_cut_diff <= -0.04989034961909056 then
                case when SLOC_diff <= 7.5 then
                   return 1.0 # (11.0 out of 11.0)
                else  # if SLOC_diff > 7.5
                   return 0.0 # (0.0 out of 2.0)
                end               else  # if avg_coupling_code_size_cut_diff > -0.04989034961909056
                case when added_lines <= 119.0 then
                  case when McCabe_sum_after <= 374.0 then
                     return 1.0 # (2.0 out of 2.0)
                  else  # if McCabe_sum_after > 374.0
                    case when LLOC_before <= 4535.0 then
                      case when one_file_fix_rate_diff <= -0.875 then
                         return 1.0 # (1.0 out of 1.0)
                      else  # if one_file_fix_rate_diff > -0.875
                         return 0.0 # (0.0 out of 16.0)
                      end                     else  # if LLOC_before > 4535.0
                       return 1.0 # (1.0 out of 1.0)
                    end                   end                 else  # if added_lines > 119.0
                  case when Single comments_diff <= -3.5 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if Single comments_diff > -3.5
                     return 1.0 # (5.0 out of 5.0)
                  end                 end               end             end           else  # if one_file_fix_rate_diff > 0.9166666567325592
            case when Blank_before <= 31.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if Blank_before > 31.5
               return 1.0 # (6.0 out of 6.0)
            end           end         end       else  # if SLOC_diff > 38.0
        case when Blank_before <= 80.0 then
           return 1.0 # (19.0 out of 19.0)
        else  # if Blank_before > 80.0
          case when same_day_duration_avg_diff <= 72.3214282989502 then
            case when h2_diff <= 19.0 then
              case when LOC_before <= 647.5 then
                 return 0.0 # (0.0 out of 4.0)
              else  # if LOC_before > 647.5
                case when length_diff <= -11.5 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if length_diff > -11.5
                  case when avg_coupling_code_size_cut_diff <= -2.333333373069763 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if avg_coupling_code_size_cut_diff > -2.333333373069763
                     return 1.0 # (14.0 out of 14.0)
                  end                 end               end             else  # if h2_diff > 19.0
              case when added_functions <= 1.5 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if added_functions > 1.5
                 return 0.0 # (0.0 out of 7.0)
              end             end           else  # if same_day_duration_avg_diff > 72.3214282989502
             return 0.0 # (0.0 out of 6.0)
          end         end       end     end   else  # if high_ccp_group > 0.5
    case when changed_lines <= 312.5 then
      case when refactor_mle_diff <= -0.0790850818157196 then
        case when added_lines <= 59.5 then
          case when hunks_num <= 3.5 then
            case when avg_coupling_code_size_cut_diff <= 0.5259740427136421 then
              case when avg_coupling_code_size_cut_diff <= -5.0 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if avg_coupling_code_size_cut_diff > -5.0
                 return 1.0 # (12.0 out of 12.0)
              end             else  # if avg_coupling_code_size_cut_diff > 0.5259740427136421
              case when Comments_after <= 25.5 then
                 return 0.0 # (0.0 out of 6.0)
              else  # if Comments_after > 25.5
                 return 1.0 # (2.0 out of 2.0)
              end             end           else  # if hunks_num > 3.5
            case when Single comments_after <= 1.5 then
               return 1.0 # (1.0 out of 1.0)
            else  # if Single comments_after > 1.5
               return 0.0 # (0.0 out of 9.0)
            end           end         else  # if added_lines > 59.5
           return 1.0 # (12.0 out of 12.0)
        end       else  # if refactor_mle_diff > -0.0790850818157196
        case when vocabulary_diff <= -15.5 then
           return 0.0 # (0.0 out of 2.0)
        else  # if vocabulary_diff > -15.5
          case when avg_coupling_code_size_cut_diff <= -0.9416666626930237 then
            case when refactor_mle_diff <= 0.0420738086104393 then
               return 1.0 # (7.0 out of 7.0)
            else  # if refactor_mle_diff > 0.0420738086104393
              case when McCabe_sum_before <= 135.0 then
                 return 1.0 # (2.0 out of 2.0)
              else  # if McCabe_sum_before > 135.0
                 return 0.0 # (0.0 out of 5.0)
              end             end           else  # if avg_coupling_code_size_cut_diff > -0.9416666626930237
            case when wildcard-import <= 0.5 then
              case when refactor_mle_diff <= -0.0413585864007473 then
                case when Blank_diff <= -0.5 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if Blank_diff > -0.5
                   return 1.0 # (2.0 out of 2.0)
                end               else  # if refactor_mle_diff > -0.0413585864007473
                case when hunks_num <= 12.5 then
                   return 1.0 # (50.0 out of 50.0)
                else  # if hunks_num > 12.5
                  case when vocabulary_diff <= 2.0 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if vocabulary_diff > 2.0
                     return 1.0 # (2.0 out of 2.0)
                  end                 end               end             else  # if wildcard-import > 0.5
               return 0.0 # (0.0 out of 1.0)
            end           end         end       end     else  # if changed_lines > 312.5
      case when refactor_mle_diff <= 0.09177327528595924 then
        case when McCabe_sum_diff <= -36.5 then
          case when is_refactor <= 0.5 then
             return 1.0 # (2.0 out of 2.0)
          else  # if is_refactor > 0.5
             return 0.0 # (0.0 out of 1.0)
          end         else  # if McCabe_sum_diff > -36.5
           return 0.0 # (0.0 out of 13.0)
        end       else  # if refactor_mle_diff > 0.09177327528595924
         return 1.0 # (5.0 out of 5.0)
      end     end   end )