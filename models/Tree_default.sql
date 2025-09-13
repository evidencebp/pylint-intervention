create or replace function Tree_default (h1_diff int64, SLOC_before int64, avg_coupling_code_size_cut_diff int64, Multi_diff int64, using-constant-test int64, high_McCabe_sum_diff int64, difficulty_diff int64, LLOC_diff int64, length_diff int64, Comments_after int64, McCabe_max_before int64, low_McCabe_sum_before int64, cur_count int64, LOC_before int64, low_McCabe_max_before int64, massive_change int64, too-many-return-statements int64, Comments_diff int64, added_lines int64, broad-exception-caught int64, comparison-of-constants int64, Single comments_diff int64, refactor_mle_diff int64, prev_count_x int64, McCabe_sum_before int64, modified_McCabe_max_diff int64, Simplify-boolean-expression int64, Blank_diff int64, added_functions int64, LLOC_before int64, cur_count_x int64, high_McCabe_sum_before int64, volume_diff int64, low_McCabe_max_diff int64, LOC_diff int64, calculated_length_diff int64, changed_lines int64, N2_diff int64, h2_diff int64, too-many-lines int64, unnecessary-pass int64, simplifiable-if-statement int64, prev_count int64, too-many-nested-blocks int64, Comments_before int64, SLOC_diff int64, McCabe_sum_after int64, bugs_diff int64, cur_count_y int64, Single comments_after int64, McCabe_max_diff int64, N1_diff int64, wildcard-import int64, McCabe_sum_diff int64, prev_count_y int64, superfluous-parens int64, hunks_num int64, try-except-raise int64, simplifiable-if-expression int64, McCabe_max_after int64, high_McCabe_max_diff int64, too-many-statements int64, simplifiable-condition int64, only_removal int64, unnecessary-semicolon int64, effort_diff int64, is_refactor int64, same_day_duration_avg_diff int64, one_file_fix_rate_diff int64, high_McCabe_max_before int64, vocabulary_diff int64, too-many-branches int64, mostly_delete int64, high_ccp_group int64, low_ccp_group int64, removed_lines int64, Single comments_before int64, low_McCabe_sum_diff int64, time_diff int64, Blank_before int64, line-too-long int64, too-many-boolean-expressions int64, pointless-statement int64) as (
  case when high_ccp_group <= 0.5 then
    case when Comments_diff <= -21.0 then
      case when McCabe_max_after <= 20.0 then
        case when hunks_num <= 14.0 then
          case when Comments_after <= 77.5 then
             return 1.0 # (1.0 out of 1.0)
          else  # if Comments_after > 77.5
             return 0.0 # (0.0 out of 1.0)
          end         else  # if hunks_num > 14.0
          case when Blank_before <= 120.0 then
             return 1.0 # (1.0 out of 1.0)
          else  # if Blank_before > 120.0
             return 0.0 # (0.0 out of 1.0)
          end         end       else  # if McCabe_max_after > 20.0
         return 0.0 # (0.0 out of 1.0)
      end     else  # if Comments_diff > -21.0
      case when SLOC_diff <= 38.0 then
        case when low_ccp_group <= 0.5 then
          case when Blank_before <= 40.5 then
            case when LOC_diff <= -12.5 then
              case when Single comments_after <= 19.5 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if Single comments_after > 19.5
                 return 1.0 # (1.0 out of 1.0)
              end             else  # if LOC_diff > -12.5
              case when hunks_num <= 6.5 then
                case when Blank_diff <= -5.5 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if Blank_diff > -5.5
                   return 1.0 # (1.0 out of 1.0)
                end               else  # if hunks_num > 6.5
                case when changed_lines <= 77.5 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if changed_lines > 77.5
                   return 1.0 # (1.0 out of 1.0)
                end               end             end           else  # if Blank_before > 40.5
            case when Comments_after <= 8.5 then
              case when SLOC_before <= 187.0 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if SLOC_before > 187.0
                 return 1.0 # (1.0 out of 1.0)
              end             else  # if Comments_after > 8.5
              case when N1_diff <= -50.5 then
                case when SLOC_before <= 2680.0 then
                   return 1.0 # (1.0 out of 1.0)
                else  # if SLOC_before > 2680.0
                   return 0.0 # (0.0 out of 1.0)
                end               else  # if N1_diff > -50.5
                case when N2_diff <= -18.0 then
                  case when changed_lines <= 80.5 then
                    case when Single comments_before <= 75.5 then
                       return 0.0 # (0.0 out of 1.0)
                    else  # if Single comments_before > 75.5
                       return 1.0 # (1.0 out of 1.0)
                    end                   else  # if changed_lines > 80.5
                    case when McCabe_sum_diff <= -74.5 then
                      case when hunks_num <= 16.5 then
                         return 0.0 # (0.0 out of 1.0)
                      else  # if hunks_num > 16.5
                         return 1.0 # (1.0 out of 1.0)
                      end                     else  # if McCabe_sum_diff > -74.5
                       return 0.0 # (0.0 out of 1.0)
                    end                   end                 else  # if N2_diff > -18.0
                  case when prev_count <= 2.5 then
                    case when LOC_before <= 589.0 then
                      case when vocabulary_diff <= -14.5 then
                         return 1.0 # (1.0 out of 1.0)
                      else  # if vocabulary_diff > -14.5
                        case when McCabe_max_before <= 2.0 then
                           return 1.0 # (1.0 out of 1.0)
                        else  # if McCabe_max_before > 2.0
                          case when too-many-branches <= 0.5 then
                            case when SLOC_diff <= 26.0 then
                              case when hunks_num <= 0.5 then
                                 return 1.0 # (1.0 out of 1.0)
                              else  # if hunks_num > 0.5
                                 return 0.0 # (0.0 out of 1.0)
                              end                             else  # if SLOC_diff > 26.0
                               return 1.0 # (1.0 out of 1.0)
                            end                           else  # if too-many-branches > 0.5
                            case when N2_diff <= 5.5 then
                               return 1.0 # (1.0 out of 1.0)
                            else  # if N2_diff > 5.5
                               return 0.0 # (0.0 out of 1.0)
                            end                           end                         end                       end                     else  # if LOC_before > 589.0
                      case when McCabe_sum_before <= 132.5 then
                        case when LOC_diff <= 12.5 then
                          case when SLOC_before <= 1081.5 then
                            case when removed_lines <= 0.5 then
                               return 0.0 # (0.0 out of 1.0)
                            else  # if removed_lines > 0.5
                              case when Blank_diff <= -5.5 then
                                case when Blank_diff <= -6.5 then
                                   return 1.0 # (1.0 out of 1.0)
                                else  # if Blank_diff > -6.5
                                   return 0.0 # (0.0 out of 1.0)
                                end                               else  # if Blank_diff > -5.5
                                 return 1.0 # (1.0 out of 1.0)
                              end                             end                           else  # if SLOC_before > 1081.5
                            case when LOC_before <= 1946.5 then
                               return 0.0 # (0.0 out of 1.0)
                            else  # if LOC_before > 1946.5
                               return 1.0 # (1.0 out of 1.0)
                            end                           end                         else  # if LOC_diff > 12.5
                          case when LLOC_diff <= 17.0 then
                             return 0.0 # (0.0 out of 1.0)
                          else  # if LLOC_diff > 17.0
                             return 1.0 # (1.0 out of 1.0)
                          end                         end                       else  # if McCabe_sum_before > 132.5
                        case when LOC_before <= 1595.5 then
                          case when Blank_before <= 78.0 then
                             return 1.0 # (1.0 out of 1.0)
                          else  # if Blank_before > 78.0
                            case when McCabe_max_before <= 5.5 then
                               return 1.0 # (1.0 out of 1.0)
                            else  # if McCabe_max_before > 5.5
                              case when modified_McCabe_max_diff <= -0.5 then
                                case when McCabe_sum_after <= 193.0 then
                                  case when same_day_duration_avg_diff <= 101.40909194946289 then
                                    case when same_day_duration_avg_diff <= -33.725951194763184 then
                                       return 1.0 # (1.0 out of 1.0)
                                    else  # if same_day_duration_avg_diff > -33.725951194763184
                                       return 0.0 # (0.0 out of 1.0)
                                    end                                   else  # if same_day_duration_avg_diff > 101.40909194946289
                                     return 1.0 # (1.0 out of 1.0)
                                  end                                 else  # if McCabe_sum_after > 193.0
                                   return 1.0 # (1.0 out of 1.0)
                                end                               else  # if modified_McCabe_max_diff > -0.5
                                case when Blank_before <= 104.0 then
                                  case when Comments_after <= 83.5 then
                                     return 1.0 # (1.0 out of 1.0)
                                  else  # if Comments_after > 83.5
                                     return 0.0 # (0.0 out of 1.0)
                                  end                                 else  # if Blank_before > 104.0
                                  case when Multi_diff <= -29.0 then
                                     return 1.0 # (1.0 out of 1.0)
                                  else  # if Multi_diff > -29.0
                                     return 0.0 # (0.0 out of 1.0)
                                  end                                 end                               end                             end                           end                         else  # if LOC_before > 1595.5
                          case when McCabe_sum_before <= 516.0 then
                            case when simplifiable-if-expression <= 0.5 then
                              case when Blank_diff <= -26.0 then
                                 return 0.0 # (0.0 out of 1.0)
                              else  # if Blank_diff > -26.0
                                 return 1.0 # (1.0 out of 1.0)
                              end                             else  # if simplifiable-if-expression > 0.5
                               return 0.0 # (0.0 out of 1.0)
                            end                           else  # if McCabe_sum_before > 516.0
                            case when refactor_mle_diff <= 0.05341019481420517 then
                               return 0.0 # (0.0 out of 1.0)
                            else  # if refactor_mle_diff > 0.05341019481420517
                              case when refactor_mle_diff <= 0.3678737282752991 then
                                 return 1.0 # (1.0 out of 1.0)
                              else  # if refactor_mle_diff > 0.3678737282752991
                                 return 0.0 # (0.0 out of 1.0)
                              end                             end                           end                         end                       end                     end                   else  # if prev_count > 2.5
                     return 0.0 # (0.0 out of 1.0)
                  end                 end               end             end           end         else  # if low_ccp_group > 0.5
          case when McCabe_sum_after <= 383.0 then
            case when unnecessary-semicolon <= 0.5 then
              case when same_day_duration_avg_diff <= 624.5 then
                case when Single comments_diff <= 24.5 then
                  case when refactor_mle_diff <= 0.4707983434200287 then
                    case when McCabe_sum_after <= 19.0 then
                      case when SLOC_before <= 380.5 then
                         return 0.0 # (0.0 out of 1.0)
                      else  # if SLOC_before > 380.5
                         return 1.0 # (1.0 out of 1.0)
                      end                     else  # if McCabe_sum_after > 19.0
                       return 0.0 # (0.0 out of 1.0)
                    end                   else  # if refactor_mle_diff > 0.4707983434200287
                    case when refactor_mle_diff <= 0.504281759262085 then
                       return 1.0 # (1.0 out of 1.0)
                    else  # if refactor_mle_diff > 0.504281759262085
                       return 0.0 # (0.0 out of 1.0)
                    end                   end                 else  # if Single comments_diff > 24.5
                   return 1.0 # (1.0 out of 1.0)
                end               else  # if same_day_duration_avg_diff > 624.5
                 return 1.0 # (1.0 out of 1.0)
              end             else  # if unnecessary-semicolon > 0.5
              case when Single comments_after <= 13.5 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if Single comments_after > 13.5
                 return 1.0 # (1.0 out of 1.0)
              end             end           else  # if McCabe_sum_after > 383.0
            case when same_day_duration_avg_diff <= 146.9840850830078 then
               return 1.0 # (1.0 out of 1.0)
            else  # if same_day_duration_avg_diff > 146.9840850830078
               return 0.0 # (0.0 out of 1.0)
            end           end         end       else  # if SLOC_diff > 38.0
        case when Blank_before <= 80.0 then
           return 1.0 # (1.0 out of 1.0)
        else  # if Blank_before > 80.0
          case when low_ccp_group <= 0.5 then
            case when LOC_before <= 731.0 then
               return 0.0 # (0.0 out of 1.0)
            else  # if LOC_before > 731.0
              case when hunks_num <= 64.5 then
                case when McCabe_sum_after <= 892.0 then
                   return 1.0 # (1.0 out of 1.0)
                else  # if McCabe_sum_after > 892.0
                   return 0.0 # (0.0 out of 1.0)
                end               else  # if hunks_num > 64.5
                 return 0.0 # (0.0 out of 1.0)
              end             end           else  # if low_ccp_group > 0.5
             return 0.0 # (0.0 out of 1.0)
          end         end       end     end   else  # if high_ccp_group > 0.5
    case when massive_change <= 0.5 then
      case when hunks_num <= 27.0 then
        case when one_file_fix_rate_diff <= 0.36666667461395264 then
          case when avg_coupling_code_size_cut_diff <= -0.9416666626930237 then
            case when LOC_before <= 996.0 then
              case when SLOC_before <= 165.5 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if SLOC_before > 165.5
                 return 1.0 # (1.0 out of 1.0)
              end             else  # if LOC_before > 996.0
              case when LLOC_before <= 1000.0 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if LLOC_before > 1000.0
                case when LLOC_diff <= 17.0 then
                   return 1.0 # (1.0 out of 1.0)
                else  # if LLOC_diff > 17.0
                   return 0.0 # (0.0 out of 1.0)
                end               end             end           else  # if avg_coupling_code_size_cut_diff > -0.9416666626930237
            case when same_day_duration_avg_diff <= 244.41666412353516 then
              case when wildcard-import <= 0.5 then
                case when hunks_num <= 11.5 then
                   return 1.0 # (1.0 out of 1.0)
                else  # if hunks_num > 11.5
                  case when N1_diff <= -3.0 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if N1_diff > -3.0
                     return 1.0 # (1.0 out of 1.0)
                  end                 end               else  # if wildcard-import > 0.5
                case when McCabe_sum_diff <= -1.0 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if McCabe_sum_diff > -1.0
                   return 1.0 # (1.0 out of 1.0)
                end               end             else  # if same_day_duration_avg_diff > 244.41666412353516
              case when high_McCabe_sum_before <= 0.5 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if high_McCabe_sum_before > 0.5
                 return 1.0 # (1.0 out of 1.0)
              end             end           end         else  # if one_file_fix_rate_diff > 0.36666667461395264
          case when one_file_fix_rate_diff <= 0.4833333343267441 then
             return 0.0 # (0.0 out of 1.0)
          else  # if one_file_fix_rate_diff > 0.4833333343267441
            case when SLOC_before <= 882.0 then
               return 1.0 # (1.0 out of 1.0)
            else  # if SLOC_before > 882.0
               return 0.0 # (0.0 out of 1.0)
            end           end         end       else  # if hunks_num > 27.0
         return 0.0 # (0.0 out of 1.0)
      end     else  # if massive_change > 0.5
      case when removed_lines <= 2.5 then
         return 1.0 # (1.0 out of 1.0)
      else  # if removed_lines > 2.5
        case when removed_lines <= 798.5 then
          case when refactor_mle_diff <= -0.30888332426548004 then
             return 1.0 # (1.0 out of 1.0)
          else  # if refactor_mle_diff > -0.30888332426548004
            case when same_day_duration_avg_diff <= -104.80535507202148 then
              case when vocabulary_diff <= -60.0 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if vocabulary_diff > -60.0
                 return 1.0 # (1.0 out of 1.0)
              end             else  # if same_day_duration_avg_diff > -104.80535507202148
               return 0.0 # (0.0 out of 1.0)
            end           end         else  # if removed_lines > 798.5
           return 1.0 # (1.0 out of 1.0)
        end       end     end   end )