create or replace function Tree_default (prev_count int64, simplifiable-if-expression int64, N1_diff int64, cur_count int64, wildcard-import int64, too-many-return-statements int64, low_McCabe_max_diff int64, length_diff int64, volume_diff int64, high_McCabe_sum_diff int64, high_McCabe_max_before int64, simplifiable-condition int64, Blank_before int64, high_ccp_group int64, McCabe_max_before int64, bugs_diff int64, too-many-nested-blocks int64, refactor_mle_diff int64, difficulty_diff int64, LLOC_diff int64, LOC_diff int64, simplifiable-if-statement int64, one_file_fix_rate_diff int64, SLOC_before int64, LOC_before int64, mostly_delete int64, changed_lines int64, Single comments_before int64, removed_lines int64, added_functions int64, h1_diff int64, effort_diff int64, hunks_num int64, Multi_diff int64, same_day_duration_avg_diff int64, N2_diff int64, cur_count_y int64, Comments_diff int64, modified_McCabe_max_diff int64, h2_diff int64, time_diff int64, LLOC_before int64, calculated_length_diff int64, Single comments_after int64, massive_change int64, McCabe_sum_before int64, too-many-boolean-expressions int64, Simplify-boolean-expression int64, line-too-long int64, superfluous-parens int64, low_ccp_group int64, McCabe_max_diff int64, comparison-of-constants int64, high_McCabe_sum_before int64, low_McCabe_sum_diff int64, avg_coupling_code_size_cut_diff int64, is_refactor int64, Single comments_diff int64, unnecessary-semicolon int64, added_lines int64, prev_count_y int64, try-except-raise int64, low_McCabe_sum_before int64, vocabulary_diff int64, too-many-branches int64, McCabe_sum_after int64, broad-exception-caught int64, prev_count_x int64, only_removal int64, McCabe_max_after int64, pointless-statement int64, low_McCabe_max_before int64, too-many-lines int64, McCabe_sum_diff int64, high_McCabe_max_diff int64, using-constant-test int64, SLOC_diff int64, Blank_diff int64, Comments_after int64, cur_count_x int64, unnecessary-pass int64, too-many-statements int64, Comments_before int64) as (
  case when low_ccp_group <= 0.5 then
    case when Blank_before <= 53.5 then
      case when Blank_diff <= -1.5 then
        case when Single comments_after <= 17.5 then
          case when refactor_mle_diff <= 0.03984033688902855 then
            case when Comments_diff <= -8.5 then
               return 1.0 # (1.0 out of 1.0)
            else  # if Comments_diff > -8.5
               return 0.0 # (0.0 out of 1.0)
            end           else  # if refactor_mle_diff > 0.03984033688902855
             return 1.0 # (1.0 out of 1.0)
          end         else  # if Single comments_after > 17.5
          case when same_day_duration_avg_diff <= 273.1416702270508 then
             return 1.0 # (1.0 out of 1.0)
          else  # if same_day_duration_avg_diff > 273.1416702270508
             return 0.0 # (0.0 out of 1.0)
          end         end       else  # if Blank_diff > -1.5
        case when refactor_mle_diff <= -0.20850324630737305 then
          case when LOC_before <= 219.0 then
             return 0.0 # (0.0 out of 1.0)
          else  # if LOC_before > 219.0
             return 1.0 # (1.0 out of 1.0)
          end         else  # if refactor_mle_diff > -0.20850324630737305
          case when Multi_diff <= -0.5 then
            case when length_diff <= 43.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if length_diff > 43.5
               return 1.0 # (1.0 out of 1.0)
            end           else  # if Multi_diff > -0.5
            case when McCabe_max_diff <= 2.0 then
              case when wildcard-import <= 0.5 then
                case when hunks_num <= 7.5 then
                   return 1.0 # (1.0 out of 1.0)
                else  # if hunks_num > 7.5
                  case when Single comments_before <= 6.5 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if Single comments_before > 6.5
                     return 1.0 # (1.0 out of 1.0)
                  end                 end               else  # if wildcard-import > 0.5
                 return 0.0 # (0.0 out of 1.0)
              end             else  # if McCabe_max_diff > 2.0
               return 0.0 # (0.0 out of 1.0)
            end           end         end       end     else  # if Blank_before > 53.5
      case when Comments_before <= 405.0 then
        case when prev_count_x <= 4.5 then
          case when refactor_mle_diff <= -0.10912862047553062 then
            case when removed_lines <= 158.5 then
              case when one_file_fix_rate_diff <= 0.34166666865348816 then
                case when removed_lines <= 1.5 then
                  case when one_file_fix_rate_diff <= 0.0555555559694767 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if one_file_fix_rate_diff > 0.0555555559694767
                     return 1.0 # (1.0 out of 1.0)
                  end                 else  # if removed_lines > 1.5
                  case when Blank_before <= 60.5 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if Blank_before > 60.5
                    case when McCabe_max_after <= 24.5 then
                      case when McCabe_max_after <= 20.0 then
                        case when removed_lines <= 3.0 then
                           return 0.0 # (0.0 out of 1.0)
                        else  # if removed_lines > 3.0
                          case when same_day_duration_avg_diff <= 123.60416412353516 then
                            case when SLOC_before <= 559.5 then
                               return 1.0 # (1.0 out of 1.0)
                            else  # if SLOC_before > 559.5
                              case when McCabe_sum_before <= 124.5 then
                                case when McCabe_sum_after <= 36.5 then
                                   return 1.0 # (1.0 out of 1.0)
                                else  # if McCabe_sum_after > 36.5
                                   return 0.0 # (0.0 out of 1.0)
                                end                               else  # if McCabe_sum_before > 124.5
                                case when McCabe_max_after <= 18.5 then
                                   return 1.0 # (1.0 out of 1.0)
                                else  # if McCabe_max_after > 18.5
                                   return 0.0 # (0.0 out of 1.0)
                                end                               end                             end                           else  # if same_day_duration_avg_diff > 123.60416412353516
                             return 0.0 # (0.0 out of 1.0)
                          end                         end                       else  # if McCabe_max_after > 20.0
                         return 0.0 # (0.0 out of 1.0)
                      end                     else  # if McCabe_max_after > 24.5
                      case when one_file_fix_rate_diff <= -0.75 then
                         return 0.0 # (0.0 out of 1.0)
                      else  # if one_file_fix_rate_diff > -0.75
                         return 1.0 # (1.0 out of 1.0)
                      end                     end                   end                 end               else  # if one_file_fix_rate_diff > 0.34166666865348816
                case when low_McCabe_sum_before <= 0.5 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if low_McCabe_sum_before > 0.5
                   return 1.0 # (1.0 out of 1.0)
                end               end             else  # if removed_lines > 158.5
              case when hunks_num <= 41.0 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if hunks_num > 41.0
                 return 1.0 # (1.0 out of 1.0)
              end             end           else  # if refactor_mle_diff > -0.10912862047553062
            case when refactor_mle_diff <= 0.5782583355903625 then
              case when LOC_diff <= -262.0 then
                case when same_day_duration_avg_diff <= -244.94510650634766 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if same_day_duration_avg_diff > -244.94510650634766
                   return 1.0 # (1.0 out of 1.0)
                end               else  # if LOC_diff > -262.0
                case when McCabe_sum_after <= 354.5 then
                  case when Comments_diff <= 6.0 then
                    case when McCabe_sum_after <= 294.0 then
                      case when Blank_diff <= -28.5 then
                        case when low_McCabe_max_before <= 0.5 then
                           return 0.0 # (0.0 out of 1.0)
                        else  # if low_McCabe_max_before > 0.5
                           return 1.0 # (1.0 out of 1.0)
                        end                       else  # if Blank_diff > -28.5
                        case when SLOC_before <= 579.0 then
                          case when McCabe_sum_after <= 170.0 then
                            case when superfluous-parens <= 0.5 then
                              case when modified_McCabe_max_diff <= -0.5 then
                                case when LOC_before <= 858.5 then
                                  case when SLOC_before <= 158.5 then
                                     return 0.0 # (0.0 out of 1.0)
                                  else  # if SLOC_before > 158.5
                                     return 1.0 # (1.0 out of 1.0)
                                  end                                 else  # if LOC_before > 858.5
                                   return 0.0 # (0.0 out of 1.0)
                                end                               else  # if modified_McCabe_max_diff > -0.5
                                case when hunks_num <= 11.5 then
                                  case when refactor_mle_diff <= -0.04683160223066807 then
                                     return 1.0 # (1.0 out of 1.0)
                                  else  # if refactor_mle_diff > -0.04683160223066807
                                    case when McCabe_sum_after <= 46.5 then
                                      case when removed_lines <= 6.0 then
                                         return 1.0 # (1.0 out of 1.0)
                                      else  # if removed_lines > 6.0
                                         return 0.0 # (0.0 out of 1.0)
                                      end                                     else  # if McCabe_sum_after > 46.5
                                      case when changed_lines <= 1.5 then
                                         return 1.0 # (1.0 out of 1.0)
                                      else  # if changed_lines > 1.5
                                         return 0.0 # (0.0 out of 1.0)
                                      end                                     end                                   end                                 else  # if hunks_num > 11.5
                                   return 1.0 # (1.0 out of 1.0)
                                end                               end                             else  # if superfluous-parens > 0.5
                               return 1.0 # (1.0 out of 1.0)
                            end                           else  # if McCabe_sum_after > 170.0
                            case when McCabe_sum_after <= 253.5 then
                               return 0.0 # (0.0 out of 1.0)
                            else  # if McCabe_sum_after > 253.5
                               return 1.0 # (1.0 out of 1.0)
                            end                           end                         else  # if SLOC_before > 579.0
                          case when SLOC_before <= 1120.0 then
                            case when McCabe_max_diff <= -4.5 then
                              case when McCabe_max_after <= 15.0 then
                                 return 1.0 # (1.0 out of 1.0)
                              else  # if McCabe_max_after > 15.0
                                 return 0.0 # (0.0 out of 1.0)
                              end                             else  # if McCabe_max_diff > -4.5
                              case when Comments_before <= 12.0 then
                                 return 0.0 # (0.0 out of 1.0)
                              else  # if Comments_before > 12.0
                                case when h2_diff <= -21.5 then
                                   return 0.0 # (0.0 out of 1.0)
                                else  # if h2_diff > -21.5
                                  case when prev_count_x <= 1.5 then
                                     return 1.0 # (1.0 out of 1.0)
                                  else  # if prev_count_x > 1.5
                                    case when only_removal <= 0.5 then
                                       return 0.0 # (0.0 out of 1.0)
                                    else  # if only_removal > 0.5
                                       return 1.0 # (1.0 out of 1.0)
                                    end                                   end                                 end                               end                             end                           else  # if SLOC_before > 1120.0
                            case when LOC_before <= 1727.5 then
                               return 0.0 # (0.0 out of 1.0)
                            else  # if LOC_before > 1727.5
                              case when Multi_diff <= -26.5 then
                                 return 0.0 # (0.0 out of 1.0)
                              else  # if Multi_diff > -26.5
                                 return 1.0 # (1.0 out of 1.0)
                              end                             end                           end                         end                       end                     else  # if McCabe_sum_after > 294.0
                       return 0.0 # (0.0 out of 1.0)
                    end                   else  # if Comments_diff > 6.0
                    case when McCabe_max_diff <= 0.5 then
                       return 0.0 # (0.0 out of 1.0)
                    else  # if McCabe_max_diff > 0.5
                       return 1.0 # (1.0 out of 1.0)
                    end                   end                 else  # if McCabe_sum_after > 354.5
                  case when try-except-raise <= 0.5 then
                    case when simplifiable-condition <= 0.5 then
                       return 1.0 # (1.0 out of 1.0)
                    else  # if simplifiable-condition > 0.5
                       return 0.0 # (0.0 out of 1.0)
                    end                   else  # if try-except-raise > 0.5
                     return 0.0 # (0.0 out of 1.0)
                  end                 end               end             else  # if refactor_mle_diff > 0.5782583355903625
              case when Single comments_after <= 51.5 then
                case when SLOC_diff <= 13.0 then
                   return 1.0 # (1.0 out of 1.0)
                else  # if SLOC_diff > 13.0
                   return 0.0 # (0.0 out of 1.0)
                end               else  # if Single comments_after > 51.5
                case when same_day_duration_avg_diff <= -68.11666870117188 then
                   return 1.0 # (1.0 out of 1.0)
                else  # if same_day_duration_avg_diff > -68.11666870117188
                   return 0.0 # (0.0 out of 1.0)
                end               end             end           end         else  # if prev_count_x > 4.5
           return 0.0 # (0.0 out of 1.0)
        end       else  # if Comments_before > 405.0
        case when refactor_mle_diff <= -0.46093055605888367 then
           return 1.0 # (1.0 out of 1.0)
        else  # if refactor_mle_diff > -0.46093055605888367
           return 0.0 # (0.0 out of 1.0)
        end       end     end   else  # if low_ccp_group > 0.5
    case when Single comments_diff <= 20.5 then
      case when Single comments_diff <= -18.5 then
         return 1.0 # (1.0 out of 1.0)
      else  # if Single comments_diff > -18.5
        case when Blank_before <= 562.0 then
          case when McCabe_sum_after <= 19.0 then
            case when McCabe_max_before <= 6.0 then
               return 0.0 # (0.0 out of 1.0)
            else  # if McCabe_max_before > 6.0
              case when Multi_diff <= -4.5 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if Multi_diff > -4.5
                 return 1.0 # (1.0 out of 1.0)
              end             end           else  # if McCabe_sum_after > 19.0
            case when same_day_duration_avg_diff <= 658.5833282470703 then
              case when McCabe_max_before <= 5.5 then
                case when LOC_before <= 752.0 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if LOC_before > 752.0
                   return 1.0 # (1.0 out of 1.0)
                end               else  # if McCabe_max_before > 5.5
                case when refactor_mle_diff <= 0.4760225862264633 then
                  case when one_file_fix_rate_diff <= 0.4833333343267441 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if one_file_fix_rate_diff > 0.4833333343267441
                    case when same_day_duration_avg_diff <= -44.07256507873535 then
                       return 0.0 # (0.0 out of 1.0)
                    else  # if same_day_duration_avg_diff > -44.07256507873535
                       return 1.0 # (1.0 out of 1.0)
                    end                   end                 else  # if refactor_mle_diff > 0.4760225862264633
                  case when Blank_before <= 92.0 then
                     return 1.0 # (1.0 out of 1.0)
                  else  # if Blank_before > 92.0
                     return 0.0 # (0.0 out of 1.0)
                  end                 end               end             else  # if same_day_duration_avg_diff > 658.5833282470703
               return 1.0 # (1.0 out of 1.0)
            end           end         else  # if Blank_before > 562.0
          case when LLOC_before <= 2129.0 then
             return 1.0 # (1.0 out of 1.0)
          else  # if LLOC_before > 2129.0
             return 0.0 # (0.0 out of 1.0)
          end         end       end     else  # if Single comments_diff > 20.5
      case when N1_diff <= 2.5 then
         return 1.0 # (1.0 out of 1.0)
      else  # if N1_diff > 2.5
         return 0.0 # (0.0 out of 1.0)
      end     end   end )