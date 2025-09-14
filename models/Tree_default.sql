create or replace function Tree_default (low_McCabe_max_before int64, LLOC_before int64, low_McCabe_sum_diff int64, modified_McCabe_max_diff int64, bugs_diff int64, McCabe_max_before int64, Single comments_before int64, prev_count_y int64, added_lines int64, LLOC_diff int64, N2_diff int64, added_functions int64, prev_count int64, too-many-boolean-expressions int64, SLOC_diff int64, mostly_delete int64, time_diff int64, calculated_length_diff int64, McCabe_max_after int64, Comments_diff int64, line-too-long int64, McCabe_sum_after int64, one_file_fix_rate_diff int64, h1_diff int64, high_McCabe_max_diff int64, too-many-branches int64, SLOC_before int64, cur_count_y int64, prev_count_x int64, McCabe_sum_before int64, Comments_after int64, wildcard-import int64, unnecessary-semicolon int64, same_day_duration_avg_diff int64, effort_diff int64, too-many-statements int64, broad-exception-caught int64, LOC_before int64, cur_count int64, Comments_before int64, using-constant-test int64, LOC_diff int64, high_McCabe_sum_diff int64, only_removal int64, superfluous-parens int64, try-except-raise int64, Blank_before int64, McCabe_max_diff int64, N1_diff int64, massive_change int64, refactor_mle_diff int64, pointless-statement int64, too-many-lines int64, simplifiable-if-statement int64, high_McCabe_sum_before int64, vocabulary_diff int64, removed_lines int64, difficulty_diff int64, Simplify-boolean-expression int64, avg_coupling_code_size_cut_diff int64, Single comments_after int64, low_ccp_group int64, Multi_diff int64, is_refactor int64, hunks_num int64, Single comments_diff int64, length_diff int64, unnecessary-pass int64, Blank_diff int64, h2_diff int64, changed_lines int64, cur_count_x int64, low_McCabe_max_diff int64, high_McCabe_max_before int64, high_ccp_group int64, too-many-nested-blocks int64, McCabe_sum_diff int64, volume_diff int64, comparison-of-constants int64, too-many-return-statements int64, simplifiable-condition int64, simplifiable-if-expression int64, low_McCabe_sum_before int64) as (
  case when low_ccp_group <= 0.5 then
    case when Comments_before <= 369.0 then
      case when same_day_duration_avg_diff <= 382.5833282470703 then
        case when prev_count <= 4.5 then
          case when Comments_diff <= 87.5 then
            case when McCabe_sum_after <= 60.5 then
              case when same_day_duration_avg_diff <= 293.0722351074219 then
                case when unnecessary-pass <= 0.5 then
                  case when wildcard-import <= 0.5 then
                    case when too-many-return-statements <= 0.5 then
                      case when too-many-nested-blocks <= 0.5 then
                        case when hunks_num <= 30.0 then
                          case when Comments_after <= 81.5 then
                            case when Blank_diff <= -72.0 then
                               return 0.0 # (0.0 out of 1.0)
                            else  # if Blank_diff > -72.0
                              case when avg_coupling_code_size_cut_diff <= 6.5 then
                                case when using-constant-test <= 0.5 then
                                  case when McCabe_max_diff <= 2.0 then
                                    case when refactor_mle_diff <= -0.3004685714840889 then
                                      case when McCabe_sum_after <= 32.5 then
                                        case when same_day_duration_avg_diff <= -135.3222198486328 then
                                           return 1.0 # (1.0 out of 1.0)
                                        else  # if same_day_duration_avg_diff > -135.3222198486328
                                           return 0.0 # (0.0 out of 1.0)
                                        end                                       else  # if McCabe_sum_after > 32.5
                                         return 1.0 # (1.0 out of 1.0)
                                      end                                     else  # if refactor_mle_diff > -0.3004685714840889
                                      case when LOC_before <= 156.5 then
                                        case when SLOC_before <= 115.5 then
                                          case when N1_diff <= -7.0 then
                                             return 0.0 # (0.0 out of 1.0)
                                          else  # if N1_diff > -7.0
                                             return 1.0 # (1.0 out of 1.0)
                                          end                                         else  # if SLOC_before > 115.5
                                           return 0.0 # (0.0 out of 1.0)
                                        end                                       else  # if LOC_before > 156.5
                                         return 1.0 # (1.0 out of 1.0)
                                      end                                     end                                   else  # if McCabe_max_diff > 2.0
                                     return 0.0 # (0.0 out of 1.0)
                                  end                                 else  # if using-constant-test > 0.5
                                   return 0.0 # (0.0 out of 1.0)
                                end                               else  # if avg_coupling_code_size_cut_diff > 6.5
                                 return 0.0 # (0.0 out of 1.0)
                              end                             end                           else  # if Comments_after > 81.5
                            case when LLOC_before <= 408.5 then
                              case when same_day_duration_avg_diff <= -74.17856979370117 then
                                 return 0.0 # (0.0 out of 1.0)
                              else  # if same_day_duration_avg_diff > -74.17856979370117
                                 return 1.0 # (1.0 out of 1.0)
                              end                             else  # if LLOC_before > 408.5
                               return 0.0 # (0.0 out of 1.0)
                            end                           end                         else  # if hunks_num > 30.0
                           return 0.0 # (0.0 out of 1.0)
                        end                       else  # if too-many-nested-blocks > 0.5
                         return 0.0 # (0.0 out of 1.0)
                      end                     else  # if too-many-return-statements > 0.5
                       return 0.0 # (0.0 out of 1.0)
                    end                   else  # if wildcard-import > 0.5
                     return 0.0 # (0.0 out of 1.0)
                  end                 else  # if unnecessary-pass > 0.5
                   return 0.0 # (0.0 out of 1.0)
                end               else  # if same_day_duration_avg_diff > 293.0722351074219
                 return 0.0 # (0.0 out of 1.0)
              end             else  # if McCabe_sum_after > 60.5
              case when LLOC_before <= 521.0 then
                case when SLOC_before <= 880.5 then
                  case when avg_coupling_code_size_cut_diff <= -0.18333333730697632 then
                    case when McCabe_sum_before <= 175.0 then
                      case when McCabe_sum_diff <= 3.0 then
                        case when prev_count <= 1.5 then
                          case when removed_lines <= 0.5 then
                             return 0.0 # (0.0 out of 1.0)
                          else  # if removed_lines > 0.5
                            case when Single comments_after <= 11.5 then
                               return 0.0 # (0.0 out of 1.0)
                            else  # if Single comments_after > 11.5
                              case when Multi_diff <= 5.0 then
                                case when high_McCabe_max_diff <= 0.5 then
                                  case when avg_coupling_code_size_cut_diff <= -0.23026315867900848 then
                                    case when SLOC_before <= 703.5 then
                                      case when too-many-statements <= 0.5 then
                                         return 1.0 # (1.0 out of 1.0)
                                      else  # if too-many-statements > 0.5
                                        case when Single comments_diff <= -4.0 then
                                           return 0.0 # (0.0 out of 1.0)
                                        else  # if Single comments_diff > -4.0
                                          case when N2_diff <= -1.0 then
                                             return 1.0 # (1.0 out of 1.0)
                                          else  # if N2_diff > -1.0
                                             return 0.0 # (0.0 out of 1.0)
                                          end                                         end                                       end                                     else  # if SLOC_before > 703.5
                                       return 0.0 # (0.0 out of 1.0)
                                    end                                   else  # if avg_coupling_code_size_cut_diff > -0.23026315867900848
                                     return 0.0 # (0.0 out of 1.0)
                                  end                                 else  # if high_McCabe_max_diff > 0.5
                                   return 0.0 # (0.0 out of 1.0)
                                end                               else  # if Multi_diff > 5.0
                                 return 0.0 # (0.0 out of 1.0)
                              end                             end                           end                         else  # if prev_count > 1.5
                           return 0.0 # (0.0 out of 1.0)
                        end                       else  # if McCabe_sum_diff > 3.0
                         return 0.0 # (0.0 out of 1.0)
                      end                     else  # if McCabe_sum_before > 175.0
                       return 0.0 # (0.0 out of 1.0)
                    end                   else  # if avg_coupling_code_size_cut_diff > -0.18333333730697632
                    case when refactor_mle_diff <= -0.14642616361379623 then
                      case when too-many-lines <= 0.5 then
                        case when avg_coupling_code_size_cut_diff <= -0.0062500000931327016 then
                           return 1.0 # (1.0 out of 1.0)
                        else  # if avg_coupling_code_size_cut_diff > -0.0062500000931327016
                           return 0.0 # (0.0 out of 1.0)
                        end                       else  # if too-many-lines > 0.5
                         return 1.0 # (1.0 out of 1.0)
                      end                     else  # if refactor_mle_diff > -0.14642616361379623
                      case when Single comments_after <= 58.5 then
                        case when Blank_before <= 162.0 then
                          case when avg_coupling_code_size_cut_diff <= -0.0357142873108387 then
                            case when length_diff <= 4.5 then
                               return 0.0 # (0.0 out of 1.0)
                            else  # if length_diff > 4.5
                               return 1.0 # (1.0 out of 1.0)
                            end                           else  # if avg_coupling_code_size_cut_diff > -0.0357142873108387
                            case when wildcard-import <= 0.5 then
                              case when Blank_before <= 30.0 then
                                 return 0.0 # (0.0 out of 1.0)
                              else  # if Blank_before > 30.0
                                case when Comments_diff <= -11.0 then
                                   return 0.0 # (0.0 out of 1.0)
                                else  # if Comments_diff > -11.0
                                  case when one_file_fix_rate_diff <= -0.9000000059604645 then
                                     return 0.0 # (0.0 out of 1.0)
                                  else  # if one_file_fix_rate_diff > -0.9000000059604645
                                    case when N1_diff <= -32.5 then
                                      case when McCabe_sum_diff <= -64.5 then
                                         return 1.0 # (1.0 out of 1.0)
                                      else  # if McCabe_sum_diff > -64.5
                                         return 0.0 # (0.0 out of 1.0)
                                      end                                     else  # if N1_diff > -32.5
                                      case when McCabe_max_before <= 10.0 then
                                        case when Comments_before <= 14.0 then
                                           return 1.0 # (1.0 out of 1.0)
                                        else  # if Comments_before > 14.0
                                           return 0.0 # (0.0 out of 1.0)
                                        end                                       else  # if McCabe_max_before > 10.0
                                         return 1.0 # (1.0 out of 1.0)
                                      end                                     end                                   end                                 end                               end                             else  # if wildcard-import > 0.5
                               return 0.0 # (0.0 out of 1.0)
                            end                           end                         else  # if Blank_before > 162.0
                          case when Single comments_after <= 32.5 then
                             return 0.0 # (0.0 out of 1.0)
                          else  # if Single comments_after > 32.5
                             return 1.0 # (1.0 out of 1.0)
                          end                         end                       else  # if Single comments_after > 58.5
                        case when Blank_before <= 111.5 then
                          case when SLOC_diff <= -3.0 then
                             return 1.0 # (1.0 out of 1.0)
                          else  # if SLOC_diff > -3.0
                             return 0.0 # (0.0 out of 1.0)
                          end                         else  # if Blank_before > 111.5
                          case when too-many-branches <= 0.5 then
                             return 1.0 # (1.0 out of 1.0)
                          else  # if too-many-branches > 0.5
                             return 0.0 # (0.0 out of 1.0)
                          end                         end                       end                     end                   end                 else  # if SLOC_before > 880.5
                  case when McCabe_sum_diff <= -6.5 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if McCabe_sum_diff > -6.5
                     return 1.0 # (1.0 out of 1.0)
                  end                 end               else  # if LLOC_before > 521.0
                case when McCabe_sum_after <= 101.5 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if McCabe_sum_after > 101.5
                  case when SLOC_before <= 572.5 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if SLOC_before > 572.5
                    case when refactor_mle_diff <= 0.7046507894992828 then
                      case when modified_McCabe_max_diff <= 8.0 then
                        case when SLOC_diff <= -17.0 then
                          case when modified_McCabe_max_diff <= 0.5 then
                            case when hunks_num <= 1.5 then
                               return 0.0 # (0.0 out of 1.0)
                            else  # if hunks_num > 1.5
                              case when one_file_fix_rate_diff <= -0.10833333805203438 then
                                case when hunks_num <= 7.0 then
                                  case when added_lines <= 41.0 then
                                     return 0.0 # (0.0 out of 1.0)
                                  else  # if added_lines > 41.0
                                     return 1.0 # (1.0 out of 1.0)
                                  end                                 else  # if hunks_num > 7.0
                                   return 0.0 # (0.0 out of 1.0)
                                end                               else  # if one_file_fix_rate_diff > -0.10833333805203438
                                case when one_file_fix_rate_diff <= 0.7333333492279053 then
                                  case when too-many-boolean-expressions <= 0.5 then
                                    case when McCabe_max_diff <= -6.0 then
                                      case when SLOC_before <= 904.0 then
                                         return 0.0 # (0.0 out of 1.0)
                                      else  # if SLOC_before > 904.0
                                         return 1.0 # (1.0 out of 1.0)
                                      end                                     else  # if McCabe_max_diff > -6.0
                                       return 1.0 # (1.0 out of 1.0)
                                    end                                   else  # if too-many-boolean-expressions > 0.5
                                     return 0.0 # (0.0 out of 1.0)
                                  end                                 else  # if one_file_fix_rate_diff > 0.7333333492279053
                                   return 0.0 # (0.0 out of 1.0)
                                end                               end                             end                           else  # if modified_McCabe_max_diff > 0.5
                             return 0.0 # (0.0 out of 1.0)
                          end                         else  # if SLOC_diff > -17.0
                          case when Blank_before <= 95.5 then
                             return 0.0 # (0.0 out of 1.0)
                          else  # if Blank_before > 95.5
                            case when hunks_num <= 58.5 then
                              case when same_day_duration_avg_diff <= -347.4583282470703 then
                                 return 0.0 # (0.0 out of 1.0)
                              else  # if same_day_duration_avg_diff > -347.4583282470703
                                case when Comments_after <= 11.0 then
                                   return 0.0 # (0.0 out of 1.0)
                                else  # if Comments_after > 11.0
                                  case when McCabe_max_before <= 78.5 then
                                    case when one_file_fix_rate_diff <= -0.8214285671710968 then
                                      case when LOC_diff <= 35.5 then
                                         return 1.0 # (1.0 out of 1.0)
                                      else  # if LOC_diff > 35.5
                                         return 0.0 # (0.0 out of 1.0)
                                      end                                     else  # if one_file_fix_rate_diff > -0.8214285671710968
                                      case when refactor_mle_diff <= 0.3217107057571411 then
                                         return 1.0 # (1.0 out of 1.0)
                                      else  # if refactor_mle_diff > 0.3217107057571411
                                        case when SLOC_before <= 960.0 then
                                           return 0.0 # (0.0 out of 1.0)
                                        else  # if SLOC_before > 960.0
                                           return 1.0 # (1.0 out of 1.0)
                                        end                                       end                                     end                                   else  # if McCabe_max_before > 78.5
                                    case when changed_lines <= 24.0 then
                                       return 0.0 # (0.0 out of 1.0)
                                    else  # if changed_lines > 24.0
                                       return 1.0 # (1.0 out of 1.0)
                                    end                                   end                                 end                               end                             else  # if hunks_num > 58.5
                               return 0.0 # (0.0 out of 1.0)
                            end                           end                         end                       else  # if modified_McCabe_max_diff > 8.0
                         return 0.0 # (0.0 out of 1.0)
                      end                     else  # if refactor_mle_diff > 0.7046507894992828
                       return 0.0 # (0.0 out of 1.0)
                    end                   end                 end               end             end           else  # if Comments_diff > 87.5
             return 0.0 # (0.0 out of 1.0)
          end         else  # if prev_count > 4.5
           return 0.0 # (0.0 out of 1.0)
        end       else  # if same_day_duration_avg_diff > 382.5833282470703
         return 0.0 # (0.0 out of 1.0)
      end     else  # if Comments_before > 369.0
      case when prev_count_x <= 1.5 then
         return 0.0 # (0.0 out of 1.0)
      else  # if prev_count_x > 1.5
        case when McCabe_max_after <= 92.0 then
           return 1.0 # (1.0 out of 1.0)
        else  # if McCabe_max_after > 92.0
           return 0.0 # (0.0 out of 1.0)
        end       end     end   else  # if low_ccp_group > 0.5
    case when same_day_duration_avg_diff <= 5.808960437774658 then
      case when same_day_duration_avg_diff <= -33.06060600280762 then
         return 0.0 # (0.0 out of 1.0)
      else  # if same_day_duration_avg_diff > -33.06060600280762
        case when same_day_duration_avg_diff <= -22.13083267211914 then
          case when LOC_diff <= 7.0 then
            case when removed_lines <= 6.0 then
               return 0.0 # (0.0 out of 1.0)
            else  # if removed_lines > 6.0
              case when simplifiable-if-statement <= 0.5 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if simplifiable-if-statement > 0.5
                 return 0.0 # (0.0 out of 1.0)
              end             end           else  # if LOC_diff > 7.0
             return 0.0 # (0.0 out of 1.0)
          end         else  # if same_day_duration_avg_diff > -22.13083267211914
          case when added_lines <= 3.5 then
            case when Blank_before <= 61.0 then
               return 0.0 # (0.0 out of 1.0)
            else  # if Blank_before > 61.0
               return 1.0 # (1.0 out of 1.0)
            end           else  # if added_lines > 3.5
             return 0.0 # (0.0 out of 1.0)
          end         end       end     else  # if same_day_duration_avg_diff > 5.808960437774658
      case when Comments_before <= 21.5 then
         return 0.0 # (0.0 out of 1.0)
      else  # if Comments_before > 21.5
        case when Blank_diff <= 2.0 then
          case when removed_lines <= 16.5 then
            case when unnecessary-semicolon <= 0.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if unnecessary-semicolon > 0.5
               return 1.0 # (1.0 out of 1.0)
            end           else  # if removed_lines > 16.5
            case when LLOC_diff <= -573.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if LLOC_diff > -573.5
              case when avg_coupling_code_size_cut_diff <= 2.666666626930237 then
                case when removed_lines <= 61.0 then
                  case when SLOC_diff <= 16.5 then
                     return 1.0 # (1.0 out of 1.0)
                  else  # if SLOC_diff > 16.5
                     return 0.0 # (0.0 out of 1.0)
                  end                 else  # if removed_lines > 61.0
                   return 1.0 # (1.0 out of 1.0)
                end               else  # if avg_coupling_code_size_cut_diff > 2.666666626930237
                 return 0.0 # (0.0 out of 1.0)
              end             end           end         else  # if Blank_diff > 2.0
           return 0.0 # (0.0 out of 1.0)
        end       end     end   end )