create or replace function Tree_default (SLOC_before int64, simplifiable-condition int64, bugs_diff int64, Blank_before int64, LLOC_diff int64, try-except-raise int64, LLOC_before int64, changed_lines int64, h2_diff int64, prev_count_x int64, too-many-lines int64, cur_count_y int64, Comments_before int64, McCabe_sum_after int64, cur_count_x int64, vocabulary_diff int64, Single comments_before int64, N2_diff int64, high_ccp_group int64, massive_change int64, added_lines int64, prev_count int64, refactor_mle_diff int64, superfluous-parens int64, avg_coupling_code_size_cut_diff int64, McCabe_sum_diff int64, LOC_before int64, too-many-return-statements int64, too-many-branches int64, too-many-nested-blocks int64, difficulty_diff int64, time_diff int64, Single comments_after int64, calculated_length_diff int64, Simplify-boolean-expression int64, unnecessary-semicolon int64, mostly_delete int64, effort_diff int64, Multi_diff int64, McCabe_max_diff int64, is_refactor int64, only_removal int64, LOC_diff int64, one_file_fix_rate_diff int64, Comments_after int64, comparison-of-constants int64, McCabe_max_after int64, length_diff int64, simplifiable-if-statement int64, removed_lines int64, unnecessary-pass int64, Comments_diff int64, cur_count int64, same_day_duration_avg_diff int64, hunks_num int64, N1_diff int64, line-too-long int64, volume_diff int64, using-constant-test int64, too-many-boolean-expressions int64, modified_McCabe_max_diff int64, h1_diff int64, added_functions int64, SLOC_diff int64, too-many-statements int64, pointless-statement int64, wildcard-import int64, McCabe_max_before int64, prev_count_y int64, broad-exception-caught int64, Blank_diff int64, McCabe_sum_before int64, simplifiable-if-expression int64, Single comments_diff int64) as (
  case when Comments_after <= 5.5 then
    case when Single comments_after <= 1.5 then
       return 1.0 # (23.0 out of 23.0)
    else  # if Single comments_after > 1.5
      case when SLOC_before <= 176.5 then
        case when LOC_diff <= 3.0 then
          case when Comments_diff <= -2.0 then
             return 1.0 # (2.0 out of 2.0)
          else  # if Comments_diff > -2.0
            case when hunks_num <= 0.5 then
               return 1.0 # (1.0 out of 1.0)
            else  # if hunks_num > 0.5
               return 0.0 # (0.0 out of 18.0)
            end           end         else  # if LOC_diff > 3.0
           return 1.0 # (7.0 out of 7.0)
        end       else  # if SLOC_before > 176.5
         return 1.0 # (10.0 out of 10.0)
      end     end   else  # if Comments_after > 5.5
    case when high_ccp_group <= 0.5 then
      case when Comments_diff <= -21.0 then
        case when McCabe_max_after <= 10.5 then
           return 1.0 # (17.0 out of 17.0)
        else  # if McCabe_max_after > 10.5
          case when avg_coupling_code_size_cut_diff <= -1.3936507999897003 then
             return 1.0 # (9.0 out of 9.0)
          else  # if avg_coupling_code_size_cut_diff > -1.3936507999897003
            case when h2_diff <= -272.0 then
               return 1.0 # (1.0 out of 1.0)
            else  # if h2_diff > -272.0
               return 0.0 # (0.0 out of 27.0)
            end           end         end       else  # if Comments_diff > -21.0
        case when Single comments_diff <= 22.5 then
          case when changed_lines <= 137.0 then
            case when too-many-boolean-expressions <= 0.5 then
              case when refactor_mle_diff <= -0.6840274930000305 then
                 return 1.0 # (2.0 out of 2.0)
              else  # if refactor_mle_diff > -0.6840274930000305
                case when avg_coupling_code_size_cut_diff <= 4.757142901420593 then
                  case when refactor_mle_diff <= 0.800428569316864 then
                    case when LOC_diff <= 88.5 then
                      case when LLOC_before <= 35.5 then
                         return 1.0 # (2.0 out of 2.0)
                      else  # if LLOC_before > 35.5
                        case when changed_lines <= 32.0 then
                          case when Multi_diff <= 0.5 then
                            case when one_file_fix_rate_diff <= 0.4848484843969345 then
                              case when LLOC_before <= 4535.0 then
                                case when hunks_num <= 11.0 then
                                  case when one_file_fix_rate_diff <= -0.9000000059604645 then
                                     return 1.0 # (1.0 out of 1.0)
                                  else  # if one_file_fix_rate_diff > -0.9000000059604645
                                    case when Comments_diff <= -4.5 then
                                       return 1.0 # (1.0 out of 1.0)
                                    else  # if Comments_diff > -4.5
                                      case when avg_coupling_code_size_cut_diff <= 1.4633458256721497 then
                                        case when one_file_fix_rate_diff <= -0.269696980714798 then
                                          case when Comments_after <= 26.0 then
                                             return 1.0 # (3.0 out of 3.0)
                                          else  # if Comments_after > 26.0
                                            case when one_file_fix_rate_diff <= -0.3021284192800522 then
                                               return 0.0 # (0.0 out of 24.0)
                                            else  # if one_file_fix_rate_diff > -0.3021284192800522
                                               return 1.0 # (3.0 out of 3.0)
                                            end                                           end                                         else  # if one_file_fix_rate_diff > -0.269696980714798
                                          case when refactor_mle_diff <= 0.4358186274766922 then
                                            case when SLOC_before <= 632.5 then
                                              case when McCabe_sum_after <= 18.0 then
                                                 return 1.0 # (1.0 out of 1.0)
                                              else  # if McCabe_sum_after > 18.0
                                                 return 0.0 # (0.0 out of 102.0)
                                              end                                             else  # if SLOC_before > 632.5
                                              case when SLOC_before <= 709.5 then
                                                case when h2_diff <= -10.5 then
                                                   return 0.0 # (0.0 out of 3.0)
                                                else  # if h2_diff > -10.5
                                                   return 1.0 # (4.0 out of 4.0)
                                                end                                               else  # if SLOC_before > 709.5
                                                case when SLOC_diff <= -5.0 then
                                                   return 1.0 # (1.0 out of 1.0)
                                                else  # if SLOC_diff > -5.0
                                                  case when refactor_mle_diff <= -0.23551326990127563 then
                                                     return 1.0 # (1.0 out of 1.0)
                                                  else  # if refactor_mle_diff > -0.23551326990127563
                                                    case when simplifiable-if-expression <= 0.5 then
                                                       return 0.0 # (0.0 out of 69.0)
                                                    else  # if simplifiable-if-expression > 0.5
                                                       return 1.0 # (1.0 out of 1.0)
                                                    end                                                   end                                                 end                                               end                                             end                                           else  # if refactor_mle_diff > 0.4358186274766922
                                            case when McCabe_max_diff <= -3.0 then
                                               return 0.0 # (0.0 out of 3.0)
                                            else  # if McCabe_max_diff > -3.0
                                               return 1.0 # (2.0 out of 2.0)
                                            end                                           end                                         end                                       else  # if avg_coupling_code_size_cut_diff > 1.4633458256721497
                                        case when McCabe_max_after <= 19.5 then
                                          case when too-many-nested-blocks <= 0.5 then
                                            case when LOC_before <= 1946.5 then
                                               return 0.0 # (0.0 out of 15.0)
                                            else  # if LOC_before > 1946.5
                                               return 1.0 # (1.0 out of 1.0)
                                            end                                           else  # if too-many-nested-blocks > 0.5
                                             return 1.0 # (1.0 out of 1.0)
                                          end                                         else  # if McCabe_max_after > 19.5
                                           return 1.0 # (3.0 out of 3.0)
                                        end                                       end                                     end                                   end                                 else  # if hunks_num > 11.0
                                   return 1.0 # (1.0 out of 1.0)
                                end                               else  # if LLOC_before > 4535.0
                                 return 1.0 # (1.0 out of 1.0)
                              end                             else  # if one_file_fix_rate_diff > 0.4848484843969345
                              case when avg_coupling_code_size_cut_diff <= 0.1111111119389534 then
                                case when same_day_duration_avg_diff <= -24.245237469673157 then
                                   return 0.0 # (0.0 out of 9.0)
                                else  # if same_day_duration_avg_diff > -24.245237469673157
                                  case when SLOC_before <= 226.5 then
                                     return 0.0 # (0.0 out of 3.0)
                                  else  # if SLOC_before > 226.5
                                     return 1.0 # (3.0 out of 3.0)
                                  end                                 end                               else  # if avg_coupling_code_size_cut_diff > 0.1111111119389534
                                 return 1.0 # (3.0 out of 3.0)
                              end                             end                           else  # if Multi_diff > 0.5
                            case when Blank_diff <= -0.5 then
                               return 0.0 # (0.0 out of 3.0)
                            else  # if Blank_diff > -0.5
                               return 1.0 # (5.0 out of 5.0)
                            end                           end                         else  # if changed_lines > 32.0
                          case when SLOC_diff <= -110.0 then
                             return 1.0 # (1.0 out of 1.0)
                          else  # if SLOC_diff > -110.0
                            case when McCabe_sum_after <= 59.0 then
                              case when McCabe_max_after <= 14.5 then
                                case when SLOC_diff <= 12.5 then
                                  case when same_day_duration_avg_diff <= -155.63448333740234 then
                                     return 1.0 # (2.0 out of 2.0)
                                  else  # if same_day_duration_avg_diff > -155.63448333740234
                                    case when McCabe_sum_diff <= 2.5 then
                                      case when McCabe_sum_after <= 54.5 then
                                         return 0.0 # (0.0 out of 66.0)
                                      else  # if McCabe_sum_after > 54.5
                                         return 1.0 # (1.0 out of 1.0)
                                      end                                     else  # if McCabe_sum_diff > 2.5
                                       return 1.0 # (1.0 out of 1.0)
                                    end                                   end                                 else  # if SLOC_diff > 12.5
                                   return 1.0 # (2.0 out of 2.0)
                                end                               else  # if McCabe_max_after > 14.5
                                 return 1.0 # (4.0 out of 4.0)
                              end                             else  # if McCabe_sum_after > 59.0
                              case when one_file_fix_rate_diff <= 0.2291666641831398 then
                                case when Multi_diff <= -29.0 then
                                  case when Comments_after <= 58.5 then
                                     return 1.0 # (1.0 out of 1.0)
                                  else  # if Comments_after > 58.5
                                     return 0.0 # (0.0 out of 3.0)
                                  end                                 else  # if Multi_diff > -29.0
                                  case when prev_count_x <= 2.5 then
                                    case when changed_lines <= 52.5 then
                                      case when changed_lines <= 51.5 then
                                        case when changed_lines <= 48.5 then
                                           return 0.0 # (0.0 out of 75.0)
                                        else  # if changed_lines > 48.5
                                          case when avg_coupling_code_size_cut_diff <= -0.862500011920929 then
                                             return 0.0 # (0.0 out of 9.0)
                                          else  # if avg_coupling_code_size_cut_diff > -0.862500011920929
                                             return 1.0 # (2.0 out of 2.0)
                                          end                                         end                                       else  # if changed_lines > 51.5
                                         return 1.0 # (1.0 out of 1.0)
                                      end                                     else  # if changed_lines > 52.5
                                       return 0.0 # (0.0 out of 177.0)
                                    end                                   else  # if prev_count_x > 2.5
                                    case when Single comments_after <= 149.5 then
                                       return 0.0 # (0.0 out of 6.0)
                                    else  # if Single comments_after > 149.5
                                       return 1.0 # (1.0 out of 1.0)
                                    end                                   end                                 end                               else  # if one_file_fix_rate_diff > 0.2291666641831398
                                case when McCabe_max_diff <= -1.0 then
                                   return 1.0 # (2.0 out of 2.0)
                                else  # if McCabe_max_diff > -1.0
                                  case when Comments_after <= 123.5 then
                                    case when changed_lines <= 97.5 then
                                       return 0.0 # (0.0 out of 27.0)
                                    else  # if changed_lines > 97.5
                                       return 1.0 # (1.0 out of 1.0)
                                    end                                   else  # if Comments_after > 123.5
                                     return 1.0 # (1.0 out of 1.0)
                                  end                                 end                               end                             end                           end                         end                       end                     else  # if LOC_diff > 88.5
                       return 1.0 # (2.0 out of 2.0)
                    end                   else  # if refactor_mle_diff > 0.800428569316864
                     return 1.0 # (2.0 out of 2.0)
                  end                 else  # if avg_coupling_code_size_cut_diff > 4.757142901420593
                   return 1.0 # (2.0 out of 2.0)
                end               end             else  # if too-many-boolean-expressions > 0.5
               return 1.0 # (3.0 out of 3.0)
            end           else  # if changed_lines > 137.0
            case when LOC_before <= 314.0 then
               return 1.0 # (8.0 out of 8.0)
            else  # if LOC_before > 314.0
              case when McCabe_max_diff <= 2.5 then
                case when Single comments_diff <= 0.5 then
                  case when modified_McCabe_max_diff <= -19.5 then
                     return 1.0 # (6.0 out of 6.0)
                  else  # if modified_McCabe_max_diff > -19.5
                    case when removed_lines <= 483.0 then
                      case when Comments_before <= 24.5 then
                        case when McCabe_max_before <= 7.5 then
                           return 0.0 # (0.0 out of 3.0)
                        else  # if McCabe_max_before > 7.5
                           return 1.0 # (6.0 out of 6.0)
                        end                       else  # if Comments_before > 24.5
                        case when Comments_before <= 220.5 then
                          case when same_day_duration_avg_diff <= 104.67727279663086 then
                            case when refactor_mle_diff <= 0.47111472487449646 then
                              case when LOC_before <= 370.5 then
                                 return 1.0 # (1.0 out of 1.0)
                              else  # if LOC_before > 370.5
                                case when Multi_diff <= -18.5 then
                                  case when McCabe_max_after <= 19.5 then
                                     return 0.0 # (0.0 out of 6.0)
                                  else  # if McCabe_max_after > 19.5
                                     return 1.0 # (2.0 out of 2.0)
                                  end                                 else  # if Multi_diff > -18.5
                                  case when Blank_diff <= -68.0 then
                                     return 1.0 # (1.0 out of 1.0)
                                  else  # if Blank_diff > -68.0
                                    case when LOC_diff <= 90.5 then
                                       return 0.0 # (0.0 out of 69.0)
                                    else  # if LOC_diff > 90.5
                                      case when McCabe_sum_before <= 363.5 then
                                         return 1.0 # (1.0 out of 1.0)
                                      else  # if McCabe_sum_before > 363.5
                                         return 0.0 # (0.0 out of 3.0)
                                      end                                     end                                   end                                 end                               end                             else  # if refactor_mle_diff > 0.47111472487449646
                               return 1.0 # (1.0 out of 1.0)
                            end                           else  # if same_day_duration_avg_diff > 104.67727279663086
                            case when hunks_num <= 5.0 then
                               return 0.0 # (0.0 out of 9.0)
                            else  # if hunks_num > 5.0
                               return 1.0 # (6.0 out of 6.0)
                            end                           end                         else  # if Comments_before > 220.5
                          case when Comments_after <= 361.0 then
                             return 1.0 # (5.0 out of 5.0)
                          else  # if Comments_after > 361.0
                             return 0.0 # (0.0 out of 3.0)
                          end                         end                       end                     else  # if removed_lines > 483.0
                       return 1.0 # (4.0 out of 4.0)
                    end                   end                 else  # if Single comments_diff > 0.5
                  case when refactor_mle_diff <= 0.6677079349756241 then
                    case when avg_coupling_code_size_cut_diff <= -4.024999976158142 then
                       return 1.0 # (1.0 out of 1.0)
                    else  # if avg_coupling_code_size_cut_diff > -4.024999976158142
                      case when same_day_duration_avg_diff <= -587.5 then
                         return 1.0 # (1.0 out of 1.0)
                      else  # if same_day_duration_avg_diff > -587.5
                        case when McCabe_sum_after <= 839.5 then
                          case when modified_McCabe_max_diff <= 3.0 then
                             return 0.0 # (0.0 out of 75.0)
                          else  # if modified_McCabe_max_diff > 3.0
                            case when McCabe_sum_after <= 463.0 then
                               return 1.0 # (1.0 out of 1.0)
                            else  # if McCabe_sum_after > 463.0
                               return 0.0 # (0.0 out of 3.0)
                            end                           end                         else  # if McCabe_sum_after > 839.5
                          case when same_day_duration_avg_diff <= -12.407936573028564 then
                             return 0.0 # (0.0 out of 3.0)
                          else  # if same_day_duration_avg_diff > -12.407936573028564
                             return 1.0 # (1.0 out of 1.0)
                          end                         end                       end                     end                   else  # if refactor_mle_diff > 0.6677079349756241
                     return 1.0 # (1.0 out of 1.0)
                  end                 end               else  # if McCabe_max_diff > 2.5
                 return 1.0 # (6.0 out of 6.0)
              end             end           end         else  # if Single comments_diff > 22.5
          case when McCabe_max_after <= 9.0 then
             return 0.0 # (0.0 out of 6.0)
          else  # if McCabe_max_after > 9.0
             return 1.0 # (13.0 out of 13.0)
          end         end       end     else  # if high_ccp_group > 0.5
      case when LOC_before <= 729.0 then
        case when hunks_num <= 2.5 then
          case when McCabe_max_diff <= -4.5 then
             return 0.0 # (0.0 out of 9.0)
          else  # if McCabe_max_diff > -4.5
            case when avg_coupling_code_size_cut_diff <= -2.0833333134651184 then
               return 0.0 # (0.0 out of 3.0)
            else  # if avg_coupling_code_size_cut_diff > -2.0833333134651184
               return 1.0 # (9.0 out of 9.0)
            end           end         else  # if hunks_num > 2.5
           return 1.0 # (31.0 out of 31.0)
        end       else  # if LOC_before > 729.0
        case when McCabe_sum_after <= 196.0 then
          case when same_day_duration_avg_diff <= 161.342529296875 then
            case when one_file_fix_rate_diff <= 0.4833333343267441 then
              case when refactor_mle_diff <= 0.10783640667796135 then
                case when avg_coupling_code_size_cut_diff <= 3.3269230723381042 then
                  case when refactor_mle_diff <= -0.3437737971544266 then
                     return 1.0 # (1.0 out of 1.0)
                  else  # if refactor_mle_diff > -0.3437737971544266
                    case when McCabe_max_before <= 17.0 then
                      case when length_diff <= -4.5 then
                         return 1.0 # (1.0 out of 1.0)
                      else  # if length_diff > -4.5
                         return 0.0 # (0.0 out of 6.0)
                      end                     else  # if McCabe_max_before > 17.0
                       return 0.0 # (0.0 out of 81.0)
                    end                   end                 else  # if avg_coupling_code_size_cut_diff > 3.3269230723381042
                   return 1.0 # (1.0 out of 1.0)
                end               else  # if refactor_mle_diff > 0.10783640667796135
                case when Comments_after <= 63.5 then
                   return 1.0 # (5.0 out of 5.0)
                else  # if Comments_after > 63.5
                   return 0.0 # (0.0 out of 3.0)
                end               end             else  # if one_file_fix_rate_diff > 0.4833333343267441
               return 1.0 # (4.0 out of 4.0)
            end           else  # if same_day_duration_avg_diff > 161.342529296875
             return 1.0 # (4.0 out of 4.0)
          end         else  # if McCabe_sum_after > 196.0
          case when avg_coupling_code_size_cut_diff <= 0.019999999552965164 then
            case when LLOC_before <= 1140.5 then
              case when McCabe_sum_before <= 240.5 then
                case when McCabe_sum_before <= 214.5 then
                  case when SLOC_before <= 1084.0 then
                     return 1.0 # (1.0 out of 1.0)
                  else  # if SLOC_before > 1084.0
                     return 0.0 # (0.0 out of 3.0)
                  end                 else  # if McCabe_sum_before > 214.5
                   return 1.0 # (6.0 out of 6.0)
                end               else  # if McCabe_sum_before > 240.5
                case when hunks_num <= 0.5 then
                   return 1.0 # (1.0 out of 1.0)
                else  # if hunks_num > 0.5
                  case when added_functions <= 9.5 then
                     return 0.0 # (0.0 out of 18.0)
                  else  # if added_functions > 9.5
                     return 1.0 # (1.0 out of 1.0)
                  end                 end               end             else  # if LLOC_before > 1140.5
               return 1.0 # (5.0 out of 5.0)
            end           else  # if avg_coupling_code_size_cut_diff > 0.019999999552965164
             return 1.0 # (12.0 out of 12.0)
          end         end       end     end   end )