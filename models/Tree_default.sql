create or replace function Tree_default (prev_count int64, prev_count_x int64, prev_count_y int64, using-constant-test int64, Comments_diff int64, massive_change int64, McCabe_max_after int64, Comments_before int64, too-many-statements int64, cur_count_x int64, h1_diff int64, McCabe_sum_diff int64, LLOC_before int64, McCabe_sum_before int64, high_McCabe_max_before int64, avg_coupling_code_size_cut_diff int64, is_refactor int64, N2_diff int64, too-many-branches int64, SLOC_before int64, too-many-nested-blocks int64, too-many-lines int64, bugs_diff int64, time_diff int64, Single comments_after int64, simplifiable-condition int64, Multi_diff int64, high_McCabe_sum_before int64, low_ccp_group int64, refactor_mle_diff int64, low_McCabe_max_diff int64, SLOC_diff int64, changed_lines int64, hunks_num int64, McCabe_sum_after int64, cur_count_y int64, one_file_fix_rate_diff int64, low_McCabe_sum_before int64, modified_McCabe_max_diff int64, superfluous-parens int64, mostly_delete int64, added_functions int64, Comments_after int64, N1_diff int64, McCabe_max_diff int64, simplifiable-if-statement int64, LOC_before int64, low_McCabe_max_before int64, McCabe_max_before int64, try-except-raise int64, line-too-long int64, unnecessary-semicolon int64, wildcard-import int64, difficulty_diff int64, Simplify-boolean-expression int64, cur_count int64, low_McCabe_sum_diff int64, pointless-statement int64, length_diff int64, broad-exception-caught int64, h2_diff int64, high_McCabe_sum_diff int64, only_removal int64, comparison-of-constants int64, Single comments_diff int64, too-many-boolean-expressions int64, Blank_before int64, calculated_length_diff int64, Single comments_before int64, removed_lines int64, simplifiable-if-expression int64, LOC_diff int64, volume_diff int64, high_McCabe_max_diff int64, high_ccp_group int64, same_day_duration_avg_diff int64, Blank_diff int64, effort_diff int64, too-many-return-statements int64, added_lines int64, unnecessary-pass int64, vocabulary_diff int64, LLOC_diff int64) as (
  case when high_ccp_group <= 0.5 then
    case when h1_diff <= -4.5 then
      case when Comments_diff <= -3.0 then
         return 1.0 # (1.0 out of 1.0)
      else  # if Comments_diff > -3.0
        case when vocabulary_diff <= -35.0 then
           return 0.0 # (0.0 out of 1.0)
        else  # if vocabulary_diff > -35.0
           return 1.0 # (1.0 out of 1.0)
        end       end     else  # if h1_diff > -4.5
      case when low_ccp_group <= 0.5 then
        case when Comments_before <= 23.5 then
          case when one_file_fix_rate_diff <= 0.08472222462296486 then
            case when McCabe_max_after <= 10.5 then
              case when Blank_before <= 17.0 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if Blank_before > 17.0
                case when same_day_duration_avg_diff <= 24.81666660308838 then
                  case when one_file_fix_rate_diff <= -0.0555555559694767 then
                    case when removed_lines <= 4.5 then
                       return 0.0 # (0.0 out of 1.0)
                    else  # if removed_lines > 4.5
                       return 1.0 # (1.0 out of 1.0)
                    end                   else  # if one_file_fix_rate_diff > -0.0555555559694767
                    case when refactor_mle_diff <= -0.7473824322223663 then
                       return 1.0 # (1.0 out of 1.0)
                    else  # if refactor_mle_diff > -0.7473824322223663
                      case when Blank_diff <= -0.5 then
                         return 1.0 # (1.0 out of 1.0)
                      else  # if Blank_diff > -0.5
                        case when avg_coupling_code_size_cut_diff <= 3.8166667819023132 then
                           return 0.0 # (0.0 out of 1.0)
                        else  # if avg_coupling_code_size_cut_diff > 3.8166667819023132
                           return 1.0 # (1.0 out of 1.0)
                        end                       end                     end                   end                 else  # if same_day_duration_avg_diff > 24.81666660308838
                   return 1.0 # (1.0 out of 1.0)
                end               end             else  # if McCabe_max_after > 10.5
               return 1.0 # (1.0 out of 1.0)
            end           else  # if one_file_fix_rate_diff > 0.08472222462296486
            case when Single comments_before <= 20.5 then
              case when same_day_duration_avg_diff <= -135.3222198486328 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if same_day_duration_avg_diff > -135.3222198486328
                case when too-many-lines <= 0.5 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if too-many-lines > 0.5
                   return 1.0 # (1.0 out of 1.0)
                end               end             else  # if Single comments_before > 20.5
               return 1.0 # (1.0 out of 1.0)
            end           end         else  # if Comments_before > 23.5
          case when one_file_fix_rate_diff <= 0.9166666567325592 then
            case when McCabe_max_after <= 47.5 then
              case when same_day_duration_avg_diff <= -606.5000152587891 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if same_day_duration_avg_diff > -606.5000152587891
                case when Single comments_after <= 2.5 then
                   return 1.0 # (1.0 out of 1.0)
                else  # if Single comments_after > 2.5
                  case when McCabe_max_diff <= 6.5 then
                    case when Blank_diff <= 17.5 then
                      case when h1_diff <= -2.5 then
                         return 1.0 # (1.0 out of 1.0)
                      else  # if h1_diff > -2.5
                        case when same_day_duration_avg_diff <= -125.05807876586914 then
                          case when McCabe_max_before <= 18.0 then
                             return 1.0 # (1.0 out of 1.0)
                          else  # if McCabe_max_before > 18.0
                            case when too-many-statements <= 0.5 then
                              case when LOC_diff <= 1.5 then
                                 return 0.0 # (0.0 out of 1.0)
                              else  # if LOC_diff > 1.5
                                 return 1.0 # (1.0 out of 1.0)
                              end                             else  # if too-many-statements > 0.5
                               return 1.0 # (1.0 out of 1.0)
                            end                           end                         else  # if same_day_duration_avg_diff > -125.05807876586914
                          case when LLOC_before <= 47.0 then
                             return 1.0 # (1.0 out of 1.0)
                          else  # if LLOC_before > 47.0
                            case when superfluous-parens <= 0.5 then
                              case when McCabe_sum_before <= 1502.0 then
                                case when Multi_diff <= -5.0 then
                                  case when too-many-branches <= 0.5 then
                                    case when McCabe_sum_before <= 63.5 then
                                       return 1.0 # (1.0 out of 1.0)
                                    else  # if McCabe_sum_before > 63.5
                                      case when one_file_fix_rate_diff <= 0.4333333447575569 then
                                        case when same_day_duration_avg_diff <= 177.3311996459961 then
                                          case when Multi_diff <= -6.5 then
                                            case when one_file_fix_rate_diff <= -0.4166666716337204 then
                                              case when Comments_diff <= -14.0 then
                                                 return 0.0 # (0.0 out of 1.0)
                                              else  # if Comments_diff > -14.0
                                                 return 1.0 # (1.0 out of 1.0)
                                              end                                             else  # if one_file_fix_rate_diff > -0.4166666716337204
                                               return 0.0 # (0.0 out of 1.0)
                                            end                                           else  # if Multi_diff > -6.5
                                             return 1.0 # (1.0 out of 1.0)
                                          end                                         else  # if same_day_duration_avg_diff > 177.3311996459961
                                           return 1.0 # (1.0 out of 1.0)
                                        end                                       else  # if one_file_fix_rate_diff > 0.4333333447575569
                                         return 1.0 # (1.0 out of 1.0)
                                      end                                     end                                   else  # if too-many-branches > 0.5
                                     return 1.0 # (1.0 out of 1.0)
                                  end                                 else  # if Multi_diff > -5.0
                                  case when unnecessary-semicolon <= 0.5 then
                                    case when McCabe_max_before <= 7.5 then
                                      case when same_day_duration_avg_diff <= 57.499664306640625 then
                                        case when too-many-lines <= 0.5 then
                                          case when LLOC_before <= 1212.5 then
                                             return 0.0 # (0.0 out of 1.0)
                                          else  # if LLOC_before > 1212.5
                                             return 1.0 # (1.0 out of 1.0)
                                          end                                         else  # if too-many-lines > 0.5
                                           return 1.0 # (1.0 out of 1.0)
                                        end                                       else  # if same_day_duration_avg_diff > 57.499664306640625
                                         return 1.0 # (1.0 out of 1.0)
                                      end                                     else  # if McCabe_max_before > 7.5
                                      case when Blank_before <= 38.0 then
                                         return 1.0 # (1.0 out of 1.0)
                                      else  # if Blank_before > 38.0
                                        case when SLOC_diff <= -16.0 then
                                          case when LLOC_diff <= -1.5 then
                                             return 0.0 # (0.0 out of 1.0)
                                          else  # if LLOC_diff > -1.5
                                             return 1.0 # (1.0 out of 1.0)
                                          end                                         else  # if SLOC_diff > -16.0
                                          case when length_diff <= -15.0 then
                                            case when refactor_mle_diff <= 0.3678737282752991 then
                                               return 1.0 # (1.0 out of 1.0)
                                            else  # if refactor_mle_diff > 0.3678737282752991
                                               return 0.0 # (0.0 out of 1.0)
                                            end                                           else  # if length_diff > -15.0
                                            case when Blank_diff <= -4.0 then
                                               return 1.0 # (1.0 out of 1.0)
                                            else  # if Blank_diff > -4.0
                                              case when too-many-boolean-expressions <= 0.5 then
                                                case when hunks_num <= 3.5 then
                                                  case when one_file_fix_rate_diff <= 0.3928571492433548 then
                                                    case when Single comments_after <= 57.0 then
                                                       return 0.0 # (0.0 out of 1.0)
                                                    else  # if Single comments_after > 57.0
                                                      case when LLOC_before <= 427.5 then
                                                         return 1.0 # (1.0 out of 1.0)
                                                      else  # if LLOC_before > 427.5
                                                        case when simplifiable-if-expression <= 0.5 then
                                                           return 0.0 # (0.0 out of 1.0)
                                                        else  # if simplifiable-if-expression > 0.5
                                                           return 1.0 # (1.0 out of 1.0)
                                                        end                                                       end                                                     end                                                   else  # if one_file_fix_rate_diff > 0.3928571492433548
                                                     return 1.0 # (1.0 out of 1.0)
                                                  end                                                 else  # if hunks_num > 3.5
                                                   return 0.0 # (0.0 out of 1.0)
                                                end                                               else  # if too-many-boolean-expressions > 0.5
                                                 return 1.0 # (1.0 out of 1.0)
                                              end                                             end                                           end                                         end                                       end                                     end                                   else  # if unnecessary-semicolon > 0.5
                                     return 1.0 # (1.0 out of 1.0)
                                  end                                 end                               else  # if McCabe_sum_before > 1502.0
                                 return 1.0 # (1.0 out of 1.0)
                              end                             else  # if superfluous-parens > 0.5
                              case when McCabe_sum_before <= 274.0 then
                                case when LOC_diff <= 26.0 then
                                   return 0.0 # (0.0 out of 1.0)
                                else  # if LOC_diff > 26.0
                                   return 1.0 # (1.0 out of 1.0)
                                end                               else  # if McCabe_sum_before > 274.0
                                case when McCabe_max_after <= 33.5 then
                                   return 1.0 # (1.0 out of 1.0)
                                else  # if McCabe_max_after > 33.5
                                   return 0.0 # (0.0 out of 1.0)
                                end                               end                             end                           end                         end                       end                     else  # if Blank_diff > 17.5
                      case when Single comments_diff <= 9.5 then
                         return 1.0 # (1.0 out of 1.0)
                      else  # if Single comments_diff > 9.5
                        case when N1_diff <= 6.5 then
                           return 1.0 # (1.0 out of 1.0)
                        else  # if N1_diff > 6.5
                           return 0.0 # (0.0 out of 1.0)
                        end                       end                     end                   else  # if McCabe_max_diff > 6.5
                     return 1.0 # (1.0 out of 1.0)
                  end                 end               end             else  # if McCabe_max_after > 47.5
              case when McCabe_max_before <= 78.5 then
                case when McCabe_max_diff <= 4.5 then
                   return 1.0 # (1.0 out of 1.0)
                else  # if McCabe_max_diff > 4.5
                   return 0.0 # (0.0 out of 1.0)
                end               else  # if McCabe_max_before > 78.5
                case when hunks_num <= 8.5 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if hunks_num > 8.5
                   return 1.0 # (1.0 out of 1.0)
                end               end             end           else  # if one_file_fix_rate_diff > 0.9166666567325592
             return 1.0 # (1.0 out of 1.0)
          end         end       else  # if low_ccp_group > 0.5
        case when Comments_diff <= 20.5 then
          case when added_lines <= 649.5 then
            case when Blank_before <= 557.0 then
              case when Single comments_diff <= -42.5 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if Single comments_diff > -42.5
                case when same_day_duration_avg_diff <= 624.5 then
                  case when unnecessary-semicolon <= 0.5 then
                    case when too-many-statements <= 0.5 then
                      case when hunks_num <= 28.0 then
                         return 0.0 # (0.0 out of 1.0)
                      else  # if hunks_num > 28.0
                        case when Blank_before <= 186.0 then
                           return 1.0 # (1.0 out of 1.0)
                        else  # if Blank_before > 186.0
                           return 0.0 # (0.0 out of 1.0)
                        end                       end                     else  # if too-many-statements > 0.5
                      case when added_lines <= 4.5 then
                         return 1.0 # (1.0 out of 1.0)
                      else  # if added_lines > 4.5
                        case when Comments_before <= 54.0 then
                           return 0.0 # (0.0 out of 1.0)
                        else  # if Comments_before > 54.0
                          case when length_diff <= -4.0 then
                             return 0.0 # (0.0 out of 1.0)
                          else  # if length_diff > -4.0
                             return 1.0 # (1.0 out of 1.0)
                          end                         end                       end                     end                   else  # if unnecessary-semicolon > 0.5
                    case when vocabulary_diff <= -1.0 then
                       return 0.0 # (0.0 out of 1.0)
                    else  # if vocabulary_diff > -1.0
                       return 1.0 # (1.0 out of 1.0)
                    end                   end                 else  # if same_day_duration_avg_diff > 624.5
                   return 1.0 # (1.0 out of 1.0)
                end               end             else  # if Blank_before > 557.0
              case when McCabe_max_before <= 28.5 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if McCabe_max_before > 28.5
                 return 0.0 # (0.0 out of 1.0)
              end             end           else  # if added_lines > 649.5
             return 1.0 # (1.0 out of 1.0)
          end         else  # if Comments_diff > 20.5
          case when LLOC_before <= 413.0 then
             return 1.0 # (1.0 out of 1.0)
          else  # if LLOC_before > 413.0
             return 0.0 # (0.0 out of 1.0)
          end         end       end     end   else  # if high_ccp_group > 0.5
    case when McCabe_sum_before <= 135.5 then
      case when removed_lines <= 360.5 then
        case when refactor_mle_diff <= -0.02819955162703991 then
          case when LOC_diff <= -30.5 then
            case when removed_lines <= 36.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if removed_lines > 36.5
               return 1.0 # (1.0 out of 1.0)
            end           else  # if LOC_diff > -30.5
             return 1.0 # (1.0 out of 1.0)
          end         else  # if refactor_mle_diff > -0.02819955162703991
           return 1.0 # (1.0 out of 1.0)
        end       else  # if removed_lines > 360.5
         return 0.0 # (0.0 out of 1.0)
      end     else  # if McCabe_sum_before > 135.5
      case when McCabe_sum_after <= 195.5 then
        case when avg_coupling_code_size_cut_diff <= 2.02692312002182 then
          case when one_file_fix_rate_diff <= 0.4833333343267441 then
            case when McCabe_max_before <= 18.5 then
               return 1.0 # (1.0 out of 1.0)
            else  # if McCabe_max_before > 18.5
              case when same_day_duration_avg_diff <= -95.55833053588867 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if same_day_duration_avg_diff > -95.55833053588867
                case when same_day_duration_avg_diff <= 167.82575607299805 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if same_day_duration_avg_diff > 167.82575607299805
                   return 1.0 # (1.0 out of 1.0)
                end               end             end           else  # if one_file_fix_rate_diff > 0.4833333343267441
             return 1.0 # (1.0 out of 1.0)
          end         else  # if avg_coupling_code_size_cut_diff > 2.02692312002182
           return 1.0 # (1.0 out of 1.0)
        end       else  # if McCabe_sum_after > 195.5
        case when McCabe_sum_after <= 242.0 then
           return 1.0 # (1.0 out of 1.0)
        else  # if McCabe_sum_after > 242.0
          case when SLOC_before <= 1436.0 then
            case when LOC_before <= 1500.0 then
               return 1.0 # (1.0 out of 1.0)
            else  # if LOC_before > 1500.0
               return 0.0 # (0.0 out of 1.0)
            end           else  # if SLOC_before > 1436.0
            case when LOC_before <= 7100.5 then
               return 1.0 # (1.0 out of 1.0)
            else  # if LOC_before > 7100.5
               return 0.0 # (0.0 out of 1.0)
            end           end         end       end     end   end )