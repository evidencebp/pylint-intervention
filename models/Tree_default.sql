create or replace function Tree_default (h1_diff int64, simplifiable-if-statement int64, McCabe_max_after int64, McCabe_sum_before int64, Single comments_before int64, low_McCabe_max_diff int64, high_ccp_group int64, pointless-statement int64, too-many-branches int64, high_McCabe_max_before int64, superfluous-parens int64, Multi_diff int64, wildcard-import int64, high_McCabe_sum_before int64, LLOC_before int64, cur_count int64, unnecessary-semicolon int64, Comments_after int64, mostly_delete int64, simplifiable-condition int64, avg_coupling_code_size_cut_diff int64, added_functions int64, McCabe_max_diff int64, McCabe_sum_diff int64, LLOC_diff int64, LOC_before int64, Comments_diff int64, prev_count_x int64, effort_diff int64, try-except-raise int64, difficulty_diff int64, line-too-long int64, Simplify-boolean-expression int64, SLOC_diff int64, McCabe_sum_after int64, refactor_mle_diff int64, one_file_fix_rate_diff int64, is_refactor int64, too-many-lines int64, too-many-boolean-expressions int64, Single comments_diff int64, low_McCabe_sum_diff int64, cur_count_y int64, comparison-of-constants int64, Comments_before int64, too-many-return-statements int64, vocabulary_diff int64, massive_change int64, hunks_num int64, modified_McCabe_max_diff int64, high_McCabe_sum_diff int64, N2_diff int64, broad-exception-caught int64, length_diff int64, unnecessary-pass int64, time_diff int64, changed_lines int64, Single comments_after int64, h2_diff int64, low_McCabe_sum_before int64, cur_count_x int64, McCabe_max_before int64, using-constant-test int64, added_lines int64, same_day_duration_avg_diff int64, prev_count_y int64, Blank_diff int64, LOC_diff int64, only_removal int64, low_McCabe_max_before int64, bugs_diff int64, too-many-statements int64, simplifiable-if-expression int64, calculated_length_diff int64, volume_diff int64, Blank_before int64, high_McCabe_max_diff int64, SLOC_before int64, too-many-nested-blocks int64, removed_lines int64, low_ccp_group int64, N1_diff int64, prev_count int64) as (
  case when high_ccp_group <= 0.5 then
    case when Single comments_diff <= -18.5 then
      case when hunks_num <= 11.0 then
        case when removed_lines <= 2.5 then
           return 0.0 # (0.0 out of 1.0)
        else  # if removed_lines > 2.5
           return 1.0 # (1.0 out of 1.0)
        end       else  # if hunks_num > 11.0
        case when McCabe_max_diff <= -4.5 then
           return 1.0 # (1.0 out of 1.0)
        else  # if McCabe_max_diff > -4.5
           return 0.0 # (0.0 out of 1.0)
        end       end     else  # if Single comments_diff > -18.5
      case when low_ccp_group <= 0.5 then
        case when low_McCabe_sum_before <= 0.5 then
          case when SLOC_diff <= 36.5 then
            case when same_day_duration_avg_diff <= -128.49257278442383 then
              case when changed_lines <= 526.0 then
                case when Comments_before <= 77.5 then
                   return 1.0 # (1.0 out of 1.0)
                else  # if Comments_before > 77.5
                  case when vocabulary_diff <= -2.5 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if vocabulary_diff > -2.5
                    case when Comments_after <= 342.0 then
                       return 1.0 # (1.0 out of 1.0)
                    else  # if Comments_after > 342.0
                       return 0.0 # (0.0 out of 1.0)
                    end                   end                 end               else  # if changed_lines > 526.0
                 return 0.0 # (0.0 out of 1.0)
              end             else  # if same_day_duration_avg_diff > -128.49257278442383
              case when superfluous-parens <= 0.5 then
                case when Single comments_after <= 7.0 then
                   return 1.0 # (1.0 out of 1.0)
                else  # if Single comments_after > 7.0
                  case when added_lines <= 74.0 then
                    case when added_lines <= 67.0 then
                      case when Single comments_before <= 95.5 then
                        case when Single comments_after <= 62.5 then
                          case when h2_diff <= 12.5 then
                            case when McCabe_max_before <= 51.0 then
                              case when Blank_before <= 55.0 then
                                case when removed_lines <= 28.0 then
                                   return 1.0 # (1.0 out of 1.0)
                                else  # if removed_lines > 28.0
                                   return 0.0 # (0.0 out of 1.0)
                                end                               else  # if Blank_before > 55.0
                                case when Comments_after <= 57.0 then
                                  case when only_removal <= 0.5 then
                                     return 0.0 # (0.0 out of 1.0)
                                  else  # if only_removal > 0.5
                                    case when McCabe_sum_before <= 157.5 then
                                       return 1.0 # (1.0 out of 1.0)
                                    else  # if McCabe_sum_before > 157.5
                                       return 0.0 # (0.0 out of 1.0)
                                    end                                   end                                 else  # if Comments_after > 57.0
                                  case when one_file_fix_rate_diff <= 0.02500000037252903 then
                                     return 0.0 # (0.0 out of 1.0)
                                  else  # if one_file_fix_rate_diff > 0.02500000037252903
                                     return 1.0 # (1.0 out of 1.0)
                                  end                                 end                               end                             else  # if McCabe_max_before > 51.0
                               return 1.0 # (1.0 out of 1.0)
                            end                           else  # if h2_diff > 12.5
                             return 1.0 # (1.0 out of 1.0)
                          end                         else  # if Single comments_after > 62.5
                          case when McCabe_max_diff <= -0.5 then
                             return 0.0 # (0.0 out of 1.0)
                          else  # if McCabe_max_diff > -0.5
                            case when Comments_diff <= -1.0 then
                               return 0.0 # (0.0 out of 1.0)
                            else  # if Comments_diff > -1.0
                               return 1.0 # (1.0 out of 1.0)
                            end                           end                         end                       else  # if Single comments_before > 95.5
                        case when hunks_num <= 7.5 then
                          case when avg_coupling_code_size_cut_diff <= 1.4666666984558105 then
                             return 0.0 # (0.0 out of 1.0)
                          else  # if avg_coupling_code_size_cut_diff > 1.4666666984558105
                            case when one_file_fix_rate_diff <= 0.1111111119389534 then
                               return 1.0 # (1.0 out of 1.0)
                            else  # if one_file_fix_rate_diff > 0.1111111119389534
                               return 0.0 # (0.0 out of 1.0)
                            end                           end                         else  # if hunks_num > 7.5
                          case when avg_coupling_code_size_cut_diff <= 0.05358585715293884 then
                            case when Comments_before <= 111.5 then
                               return 0.0 # (0.0 out of 1.0)
                            else  # if Comments_before > 111.5
                               return 1.0 # (1.0 out of 1.0)
                            end                           else  # if avg_coupling_code_size_cut_diff > 0.05358585715293884
                             return 0.0 # (0.0 out of 1.0)
                          end                         end                       end                     else  # if added_lines > 67.0
                       return 1.0 # (1.0 out of 1.0)
                    end                   else  # if added_lines > 74.0
                    case when Single comments_diff <= -6.5 then
                      case when McCabe_sum_diff <= -25.0 then
                         return 1.0 # (1.0 out of 1.0)
                      else  # if McCabe_sum_diff > -25.0
                         return 0.0 # (0.0 out of 1.0)
                      end                     else  # if Single comments_diff > -6.5
                       return 0.0 # (0.0 out of 1.0)
                    end                   end                 end               else  # if superfluous-parens > 0.5
                case when McCabe_sum_after <= 105.0 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if McCabe_sum_after > 105.0
                  case when removed_lines <= 19.0 then
                    case when removed_lines <= 5.0 then
                      case when Comments_before <= 103.5 then
                         return 0.0 # (0.0 out of 1.0)
                      else  # if Comments_before > 103.5
                         return 1.0 # (1.0 out of 1.0)
                      end                     else  # if removed_lines > 5.0
                       return 0.0 # (0.0 out of 1.0)
                    end                   else  # if removed_lines > 19.0
                     return 1.0 # (1.0 out of 1.0)
                  end                 end               end             end           else  # if SLOC_diff > 36.5
            case when mostly_delete <= 0.5 then
              case when Multi_diff <= -5.0 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if Multi_diff > -5.0
                case when McCabe_max_before <= 52.0 then
                   return 1.0 # (1.0 out of 1.0)
                else  # if McCabe_max_before > 52.0
                   return 0.0 # (0.0 out of 1.0)
                end               end             else  # if mostly_delete > 0.5
              case when Comments_before <= 135.0 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if Comments_before > 135.0
                case when Single comments_after <= 440.5 then
                   return 1.0 # (1.0 out of 1.0)
                else  # if Single comments_after > 440.5
                   return 0.0 # (0.0 out of 1.0)
                end               end             end           end         else  # if low_McCabe_sum_before > 0.5
          case when Single comments_before <= 39.5 then
            case when refactor_mle_diff <= -0.11903809756040573 then
              case when McCabe_sum_diff <= -0.5 then
                case when N2_diff <= -4.5 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if N2_diff > -4.5
                   return 1.0 # (1.0 out of 1.0)
                end               else  # if McCabe_sum_diff > -0.5
                case when one_file_fix_rate_diff <= 0.375 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if one_file_fix_rate_diff > 0.375
                   return 1.0 # (1.0 out of 1.0)
                end               end             else  # if refactor_mle_diff > -0.11903809756040573
              case when same_day_duration_avg_diff <= -7.148529529571533 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if same_day_duration_avg_diff > -7.148529529571533
                case when changed_lines <= 16.5 then
                  case when refactor_mle_diff <= 0.08536038920283318 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if refactor_mle_diff > 0.08536038920283318
                     return 1.0 # (1.0 out of 1.0)
                  end                 else  # if changed_lines > 16.5
                  case when Single comments_diff <= 0.5 then
                     return 1.0 # (1.0 out of 1.0)
                  else  # if Single comments_diff > 0.5
                     return 0.0 # (0.0 out of 1.0)
                  end                 end               end             end           else  # if Single comments_before > 39.5
            case when LOC_before <= 847.0 then
              case when LLOC_before <= 265.0 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if LLOC_before > 265.0
                 return 1.0 # (1.0 out of 1.0)
              end             else  # if LOC_before > 847.0
               return 1.0 # (1.0 out of 1.0)
            end           end         end       else  # if low_ccp_group > 0.5
        case when Comments_diff <= 20.5 then
          case when Blank_before <= 562.0 then
            case when unnecessary-semicolon <= 0.5 then
              case when added_functions <= 58.0 then
                case when changed_lines <= 15.5 then
                  case when removed_lines <= 5.0 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if removed_lines > 5.0
                    case when Comments_before <= 39.5 then
                      case when LLOC_before <= 61.0 then
                         return 0.0 # (0.0 out of 1.0)
                      else  # if LLOC_before > 61.0
                         return 1.0 # (1.0 out of 1.0)
                      end                     else  # if Comments_before > 39.5
                       return 0.0 # (0.0 out of 1.0)
                    end                   end                 else  # if changed_lines > 15.5
                  case when one_file_fix_rate_diff <= 0.2916666716337204 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if one_file_fix_rate_diff > 0.2916666716337204
                    case when modified_McCabe_max_diff <= 0.5 then
                       return 0.0 # (0.0 out of 1.0)
                    else  # if modified_McCabe_max_diff > 0.5
                       return 1.0 # (1.0 out of 1.0)
                    end                   end                 end               else  # if added_functions > 58.0
                 return 1.0 # (1.0 out of 1.0)
              end             else  # if unnecessary-semicolon > 0.5
              case when McCabe_sum_diff <= 0.5 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if McCabe_sum_diff > 0.5
                 return 0.0 # (0.0 out of 1.0)
              end             end           else  # if Blank_before > 562.0
            case when SLOC_before <= 2402.0 then
               return 1.0 # (1.0 out of 1.0)
            else  # if SLOC_before > 2402.0
               return 0.0 # (0.0 out of 1.0)
            end           end         else  # if Comments_diff > 20.5
          case when modified_McCabe_max_diff <= 2.0 then
             return 1.0 # (1.0 out of 1.0)
          else  # if modified_McCabe_max_diff > 2.0
             return 0.0 # (0.0 out of 1.0)
          end         end       end     end   else  # if high_ccp_group > 0.5
    case when Comments_diff <= 10.5 then
      case when SLOC_diff <= -245.5 then
         return 0.0 # (0.0 out of 1.0)
      else  # if SLOC_diff > -245.5
        case when McCabe_max_diff <= 0.5 then
          case when added_functions <= 6.5 then
            case when one_file_fix_rate_diff <= 0.3764881044626236 then
              case when same_day_duration_avg_diff <= 40.77809524536133 then
                case when hunks_num <= 58.5 then
                  case when h2_diff <= -64.0 then
                    case when avg_coupling_code_size_cut_diff <= 0.13333334028720856 then
                       return 1.0 # (1.0 out of 1.0)
                    else  # if avg_coupling_code_size_cut_diff > 0.13333334028720856
                       return 0.0 # (0.0 out of 1.0)
                    end                   else  # if h2_diff > -64.0
                    case when Single comments_diff <= 2.5 then
                      case when same_day_duration_avg_diff <= -397.7916717529297 then
                        case when changed_lines <= 78.5 then
                           return 0.0 # (0.0 out of 1.0)
                        else  # if changed_lines > 78.5
                           return 1.0 # (1.0 out of 1.0)
                        end                       else  # if same_day_duration_avg_diff > -397.7916717529297
                         return 1.0 # (1.0 out of 1.0)
                      end                     else  # if Single comments_diff > 2.5
                      case when McCabe_sum_before <= 54.0 then
                         return 0.0 # (0.0 out of 1.0)
                      else  # if McCabe_sum_before > 54.0
                         return 1.0 # (1.0 out of 1.0)
                      end                     end                   end                 else  # if hunks_num > 58.5
                   return 0.0 # (0.0 out of 1.0)
                end               else  # if same_day_duration_avg_diff > 40.77809524536133
                case when same_day_duration_avg_diff <= 157.625 then
                  case when Blank_before <= 207.0 then
                    case when Single comments_diff <= -6.0 then
                       return 1.0 # (1.0 out of 1.0)
                    else  # if Single comments_diff > -6.0
                       return 0.0 # (0.0 out of 1.0)
                    end                   else  # if Blank_before > 207.0
                     return 1.0 # (1.0 out of 1.0)
                  end                 else  # if same_day_duration_avg_diff > 157.625
                  case when SLOC_diff <= -29.0 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if SLOC_diff > -29.0
                     return 1.0 # (1.0 out of 1.0)
                  end                 end               end             else  # if one_file_fix_rate_diff > 0.3764881044626236
              case when one_file_fix_rate_diff <= 0.4833333343267441 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if one_file_fix_rate_diff > 0.4833333343267441
                 return 1.0 # (1.0 out of 1.0)
              end             end           else  # if added_functions > 6.5
             return 0.0 # (0.0 out of 1.0)
          end         else  # if McCabe_max_diff > 0.5
          case when Comments_before <= 59.5 then
            case when SLOC_before <= 152.0 then
               return 0.0 # (0.0 out of 1.0)
            else  # if SLOC_before > 152.0
               return 1.0 # (1.0 out of 1.0)
            end           else  # if Comments_before > 59.5
             return 0.0 # (0.0 out of 1.0)
          end         end       end     else  # if Comments_diff > 10.5
      case when high_McCabe_sum_diff <= 0.5 then
         return 0.0 # (0.0 out of 1.0)
      else  # if high_McCabe_sum_diff > 0.5
         return 1.0 # (1.0 out of 1.0)
      end     end   end )