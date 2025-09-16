create or replace function Tree_default (low_McCabe_sum_before int64, changed_lines int64, low_McCabe_max_diff int64, try-except-raise int64, Comments_before int64, high_McCabe_sum_diff int64, low_McCabe_max_before int64, Multi_diff int64, effort_diff int64, difficulty_diff int64, only_removal int64, length_diff int64, comparison-of-constants int64, LOC_diff int64, h2_diff int64, line-too-long int64, h1_diff int64, using-constant-test int64, broad-exception-caught int64, time_diff int64, calculated_length_diff int64, too-many-branches int64, SLOC_before int64, low_ccp_group int64, avg_coupling_code_size_cut_diff int64, new_function int64, wildcard-import int64, McCabe_max_before int64, superfluous-parens int64, low_McCabe_sum_diff int64, pointless-statement int64, one_file_fix_rate_diff int64, cur_count_x int64, same_day_duration_avg_diff int64, too-many-nested-blocks int64, simplifiable-condition int64, too-many-lines int64, SLOC_diff int64, cur_count_y int64, LLOC_before int64, Comments_after int64, high_ccp_group int64, bugs_diff int64, unnecessary-pass int64, prev_count_x int64, massive_change int64, McCabe_max_after int64, removed_lines int64, Comments_diff int64, Single comments_diff int64, too-many-statements int64, Simplify-boolean-expression int64, is_refactor int64, refactor_mle_diff int64, added_lines int64, mostly_delete int64, volume_diff int64, too-many-boolean-expressions int64, N2_diff int64, Blank_before int64, vocabulary_diff int64, McCabe_sum_before int64, high_McCabe_sum_before int64, N1_diff int64, LOC_before int64, LLOC_diff int64, high_McCabe_max_diff int64, simplifiable-if-statement int64, prev_count_y int64, hunks_num int64, Blank_diff int64, prev_count int64, Single comments_before int64, McCabe_max_diff int64, McCabe_sum_diff int64, modified_McCabe_max_diff int64, McCabe_sum_after int64, too-many-return-statements int64, Single comments_after int64, unnecessary-semicolon int64, added_functions int64, cur_count int64, simplifiable-if-expression int64, high_McCabe_max_before int64) as (
  case when low_ccp_group <= 0.5 then
    case when LLOC_before <= 190.5 then
      case when refactor_mle_diff <= -0.2524428591132164 then
        case when same_day_duration_avg_diff <= -32.88675308227539 then
          case when Blank_diff <= -11.0 then
             return 0.0 # (0.0 out of 1.0)
          else  # if Blank_diff > -11.0
             return 1.0 # (1.0 out of 1.0)
          end         else  # if same_day_duration_avg_diff > -32.88675308227539
           return 0.0 # (0.0 out of 1.0)
        end       else  # if refactor_mle_diff > -0.2524428591132164
        case when Single comments_diff <= 0.5 then
          case when high_McCabe_max_diff <= 0.5 then
            case when wildcard-import <= 0.5 then
              case when too-many-nested-blocks <= 0.5 then
                case when refactor_mle_diff <= -0.16559473425149918 then
                  case when SLOC_diff <= -19.5 then
                    case when Comments_before <= 1.0 then
                       return 1.0 # (1.0 out of 1.0)
                    else  # if Comments_before > 1.0
                       return 0.0 # (0.0 out of 1.0)
                    end                   else  # if SLOC_diff > -19.5
                     return 1.0 # (1.0 out of 1.0)
                  end                 else  # if refactor_mle_diff > -0.16559473425149918
                  case when hunks_num <= 7.5 then
                     return 1.0 # (1.0 out of 1.0)
                  else  # if hunks_num > 7.5
                    case when Single comments_after <= 4.5 then
                       return 0.0 # (0.0 out of 1.0)
                    else  # if Single comments_after > 4.5
                       return 1.0 # (1.0 out of 1.0)
                    end                   end                 end               else  # if too-many-nested-blocks > 0.5
                case when refactor_mle_diff <= -0.015392857603728771 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if refactor_mle_diff > -0.015392857603728771
                   return 1.0 # (1.0 out of 1.0)
                end               end             else  # if wildcard-import > 0.5
               return 0.0 # (0.0 out of 1.0)
            end           else  # if high_McCabe_max_diff > 0.5
             return 0.0 # (0.0 out of 1.0)
          end         else  # if Single comments_diff > 0.5
          case when Single comments_before <= 5.0 then
             return 0.0 # (0.0 out of 1.0)
          else  # if Single comments_before > 5.0
            case when McCabe_sum_after <= 48.0 then
               return 1.0 # (1.0 out of 1.0)
            else  # if McCabe_sum_after > 48.0
               return 0.0 # (0.0 out of 1.0)
            end           end         end       end     else  # if LLOC_before > 190.5
      case when changed_lines <= 136.5 then
        case when high_ccp_group <= 0.5 then
          case when SLOC_diff <= -17.5 then
            case when SLOC_before <= 971.5 then
              case when McCabe_sum_after <= 59.0 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if McCabe_sum_after > 59.0
                case when Multi_diff <= -29.0 then
                  case when McCabe_sum_after <= 128.0 then
                     return 1.0 # (1.0 out of 1.0)
                  else  # if McCabe_sum_after > 128.0
                     return 0.0 # (0.0 out of 1.0)
                  end                 else  # if Multi_diff > -29.0
                  case when modified_McCabe_max_diff <= -6.5 then
                    case when Blank_before <= 132.0 then
                       return 0.0 # (0.0 out of 1.0)
                    else  # if Blank_before > 132.0
                       return 1.0 # (1.0 out of 1.0)
                    end                   else  # if modified_McCabe_max_diff > -6.5
                     return 0.0 # (0.0 out of 1.0)
                  end                 end               end             else  # if SLOC_before > 971.5
              case when avg_coupling_code_size_cut_diff <= 0.5571428574621677 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if avg_coupling_code_size_cut_diff > 0.5571428574621677
                 return 0.0 # (0.0 out of 1.0)
              end             end           else  # if SLOC_diff > -17.5
            case when SLOC_before <= 1510.0 then
              case when SLOC_before <= 593.0 then
                case when one_file_fix_rate_diff <= 0.3282051384449005 then
                  case when Comments_after <= 37.0 then
                    case when McCabe_max_before <= 11.5 then
                      case when Comments_after <= 32.0 then
                         return 0.0 # (0.0 out of 1.0)
                      else  # if Comments_after > 32.0
                         return 1.0 # (1.0 out of 1.0)
                      end                     else  # if McCabe_max_before > 11.5
                      case when refactor_mle_diff <= -0.06143488921225071 then
                         return 1.0 # (1.0 out of 1.0)
                      else  # if refactor_mle_diff > -0.06143488921225071
                        case when Single comments_before <= 16.0 then
                          case when LOC_before <= 644.0 then
                             return 1.0 # (1.0 out of 1.0)
                          else  # if LOC_before > 644.0
                             return 0.0 # (0.0 out of 1.0)
                          end                         else  # if Single comments_before > 16.0
                           return 0.0 # (0.0 out of 1.0)
                        end                       end                     end                   else  # if Comments_after > 37.0
                     return 0.0 # (0.0 out of 1.0)
                  end                 else  # if one_file_fix_rate_diff > 0.3282051384449005
                  case when Comments_diff <= -0.5 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if Comments_diff > -0.5
                    case when Blank_before <= 152.0 then
                       return 1.0 # (1.0 out of 1.0)
                    else  # if Blank_before > 152.0
                       return 0.0 # (0.0 out of 1.0)
                    end                   end                 end               else  # if SLOC_before > 593.0
                case when avg_coupling_code_size_cut_diff <= -1.516233742237091 then
                  case when length_diff <= -8.0 then
                     return 1.0 # (1.0 out of 1.0)
                  else  # if length_diff > -8.0
                     return 0.0 # (0.0 out of 1.0)
                  end                 else  # if avg_coupling_code_size_cut_diff > -1.516233742237091
                  case when hunks_num <= 15.5 then
                    case when wildcard-import <= 0.5 then
                      case when same_day_duration_avg_diff <= 252.57142639160156 then
                        case when SLOC_before <= 632.5 then
                          case when SLOC_before <= 620.5 then
                             return 1.0 # (1.0 out of 1.0)
                          else  # if SLOC_before > 620.5
                             return 0.0 # (0.0 out of 1.0)
                          end                         else  # if SLOC_before > 632.5
                           return 1.0 # (1.0 out of 1.0)
                        end                       else  # if same_day_duration_avg_diff > 252.57142639160156
                         return 0.0 # (0.0 out of 1.0)
                      end                     else  # if wildcard-import > 0.5
                       return 0.0 # (0.0 out of 1.0)
                    end                   else  # if hunks_num > 15.5
                     return 0.0 # (0.0 out of 1.0)
                  end                 end               end             else  # if SLOC_before > 1510.0
              case when added_functions <= 1.5 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if added_functions > 1.5
                 return 1.0 # (1.0 out of 1.0)
              end             end           end         else  # if high_ccp_group > 0.5
          case when Single comments_diff <= 2.5 then
            case when McCabe_max_diff <= 0.5 then
              case when Single comments_after <= 16.0 then
                case when avg_coupling_code_size_cut_diff <= 0.7045454680919647 then
                  case when Single comments_after <= 14.0 then
                     return 1.0 # (1.0 out of 1.0)
                  else  # if Single comments_after > 14.0
                     return 0.0 # (0.0 out of 1.0)
                  end                 else  # if avg_coupling_code_size_cut_diff > 0.7045454680919647
                   return 0.0 # (0.0 out of 1.0)
                end               else  # if Single comments_after > 16.0
                case when simplifiable-if-statement <= 0.5 then
                  case when refactor_mle_diff <= 0.181182861328125 then
                    case when Multi_diff <= -4.5 then
                       return 0.0 # (0.0 out of 1.0)
                    else  # if Multi_diff > -4.5
                      case when avg_coupling_code_size_cut_diff <= -5.0 then
                        case when avg_coupling_code_size_cut_diff <= -7.25 then
                           return 1.0 # (1.0 out of 1.0)
                        else  # if avg_coupling_code_size_cut_diff > -7.25
                           return 0.0 # (0.0 out of 1.0)
                        end                       else  # if avg_coupling_code_size_cut_diff > -5.0
                        case when hunks_num <= 10.0 then
                           return 1.0 # (1.0 out of 1.0)
                        else  # if hunks_num > 10.0
                          case when LLOC_before <= 1033.0 then
                             return 0.0 # (0.0 out of 1.0)
                          else  # if LLOC_before > 1033.0
                             return 1.0 # (1.0 out of 1.0)
                          end                         end                       end                     end                   else  # if refactor_mle_diff > 0.181182861328125
                    case when McCabe_max_after <= 21.0 then
                       return 1.0 # (1.0 out of 1.0)
                    else  # if McCabe_max_after > 21.0
                       return 0.0 # (0.0 out of 1.0)
                    end                   end                 else  # if simplifiable-if-statement > 0.5
                   return 0.0 # (0.0 out of 1.0)
                end               end             else  # if McCabe_max_diff > 0.5
               return 0.0 # (0.0 out of 1.0)
            end           else  # if Single comments_diff > 2.5
             return 0.0 # (0.0 out of 1.0)
          end         end       else  # if changed_lines > 136.5
        case when removed_lines <= 197.0 then
          case when Comments_before <= 376.0 then
            case when one_file_fix_rate_diff <= 0.26944445073604584 then
              case when Blank_before <= 70.5 then
                case when McCabe_max_after <= 19.5 then
                   return 1.0 # (1.0 out of 1.0)
                else  # if McCabe_max_after > 19.5
                   return 0.0 # (0.0 out of 1.0)
                end               else  # if Blank_before > 70.5
                case when hunks_num <= 11.5 then
                  case when McCabe_sum_before <= 130.0 then
                    case when Blank_before <= 156.5 then
                      case when modified_McCabe_max_diff <= 1.5 then
                         return 1.0 # (1.0 out of 1.0)
                      else  # if modified_McCabe_max_diff > 1.5
                         return 0.0 # (0.0 out of 1.0)
                      end                     else  # if Blank_before > 156.5
                      case when McCabe_max_before <= 18.0 then
                         return 1.0 # (1.0 out of 1.0)
                      else  # if McCabe_max_before > 18.0
                         return 0.0 # (0.0 out of 1.0)
                      end                     end                   else  # if McCabe_sum_before > 130.0
                    case when removed_lines <= 1.5 then
                      case when LLOC_diff <= -147.5 then
                         return 0.0 # (0.0 out of 1.0)
                      else  # if LLOC_diff > -147.5
                         return 1.0 # (1.0 out of 1.0)
                      end                     else  # if removed_lines > 1.5
                       return 1.0 # (1.0 out of 1.0)
                    end                   end                 else  # if hunks_num > 11.5
                  case when refactor_mle_diff <= -0.19458577036857605 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if refactor_mle_diff > -0.19458577036857605
                    case when McCabe_max_diff <= -4.0 then
                      case when added_lines <= 312.5 then
                         return 0.0 # (0.0 out of 1.0)
                      else  # if added_lines > 312.5
                         return 1.0 # (1.0 out of 1.0)
                      end                     else  # if McCabe_max_diff > -4.0
                      case when too-many-lines <= 0.5 then
                         return 1.0 # (1.0 out of 1.0)
                      else  # if too-many-lines > 0.5
                         return 0.0 # (0.0 out of 1.0)
                      end                     end                   end                 end               end             else  # if one_file_fix_rate_diff > 0.26944445073604584
              case when Single comments_diff <= -7.5 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if Single comments_diff > -7.5
                 return 0.0 # (0.0 out of 1.0)
              end             end           else  # if Comments_before > 376.0
             return 0.0 # (0.0 out of 1.0)
          end         else  # if removed_lines > 197.0
          case when SLOC_diff <= 62.5 then
            case when N1_diff <= -67.0 then
               return 1.0 # (1.0 out of 1.0)
            else  # if N1_diff > -67.0
               return 0.0 # (0.0 out of 1.0)
            end           else  # if SLOC_diff > 62.5
            case when LLOC_diff <= 94.5 then
              case when same_day_duration_avg_diff <= 34.03783130645752 then
                case when hunks_num <= 64.5 then
                   return 1.0 # (1.0 out of 1.0)
                else  # if hunks_num > 64.5
                   return 0.0 # (0.0 out of 1.0)
                end               else  # if same_day_duration_avg_diff > 34.03783130645752
                 return 0.0 # (0.0 out of 1.0)
              end             else  # if LLOC_diff > 94.5
               return 0.0 # (0.0 out of 1.0)
            end           end         end       end     end   else  # if low_ccp_group > 0.5
    case when Comments_diff <= 20.5 then
      case when Single comments_diff <= -17.0 then
        case when added_lines <= 163.0 then
           return 0.0 # (0.0 out of 1.0)
        else  # if added_lines > 163.0
           return 1.0 # (1.0 out of 1.0)
        end       else  # if Single comments_diff > -17.0
        case when Blank_before <= 562.0 then
          case when Single comments_after <= 1.0 then
            case when low_McCabe_max_before <= 0.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if low_McCabe_max_before > 0.5
               return 1.0 # (1.0 out of 1.0)
            end           else  # if Single comments_after > 1.0
            case when same_day_duration_avg_diff <= 658.5833282470703 then
              case when McCabe_sum_before <= 18.5 then
                case when McCabe_max_before <= 6.0 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if McCabe_max_before > 6.0
                   return 1.0 # (1.0 out of 1.0)
                end               else  # if McCabe_sum_before > 18.5
                case when McCabe_max_before <= 5.5 then
                  case when Comments_before <= 69.5 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if Comments_before > 69.5
                     return 1.0 # (1.0 out of 1.0)
                  end                 else  # if McCabe_max_before > 5.5
                  case when too-many-statements <= 0.5 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if too-many-statements > 0.5
                    case when avg_coupling_code_size_cut_diff <= 0.9880972504615784 then
                      case when McCabe_max_after <= 27.5 then
                         return 0.0 # (0.0 out of 1.0)
                      else  # if McCabe_max_after > 27.5
                         return 1.0 # (1.0 out of 1.0)
                      end                     else  # if avg_coupling_code_size_cut_diff > 0.9880972504615784
                       return 1.0 # (1.0 out of 1.0)
                    end                   end                 end               end             else  # if same_day_duration_avg_diff > 658.5833282470703
               return 1.0 # (1.0 out of 1.0)
            end           end         else  # if Blank_before > 562.0
          case when Comments_diff <= -5.0 then
             return 0.0 # (0.0 out of 1.0)
          else  # if Comments_diff > -5.0
             return 1.0 # (1.0 out of 1.0)
          end         end       end     else  # if Comments_diff > 20.5
      case when Comments_before <= 506.0 then
         return 1.0 # (1.0 out of 1.0)
      else  # if Comments_before > 506.0
         return 0.0 # (0.0 out of 1.0)
      end     end   end )