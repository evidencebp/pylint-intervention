create or replace function Tree_default (McCabe_sum_before int64, changed_lines int64, prev_count_y int64, mostly_delete int64, h1_diff int64, too-many-lines int64, low_McCabe_sum_before int64, length_diff int64, LOC_before int64, simplifiable-if-expression int64, added_functions int64, broad-exception-caught int64, simplifiable-condition int64, prev_count_x int64, McCabe_max_diff int64, SLOC_before int64, LLOC_before int64, low_McCabe_max_diff int64, bugs_diff int64, same_day_duration_avg_diff int64, cur_count_x int64, only_removal int64, McCabe_max_after int64, Single comments_after int64, low_ccp_group int64, one_file_fix_rate_diff int64, effort_diff int64, difficulty_diff int64, removed_lines int64, Comments_diff int64, too-many-boolean-expressions int64, refactor_mle_diff int64, high_McCabe_max_before int64, hunks_num int64, LOC_diff int64, SLOC_diff int64, cur_count_y int64, vocabulary_diff int64, using-constant-test int64, Simplify-boolean-expression int64, low_McCabe_max_before int64, high_McCabe_sum_diff int64, high_McCabe_sum_before int64, McCabe_max_before int64, Comments_after int64, McCabe_sum_diff int64, unnecessary-pass int64, avg_coupling_code_size_cut_diff int64, simplifiable-if-statement int64, is_refactor int64, volume_diff int64, added_lines int64, high_McCabe_max_diff int64, superfluous-parens int64, cur_count int64, low_McCabe_sum_diff int64, calculated_length_diff int64, Multi_diff int64, N2_diff int64, h2_diff int64, Single comments_before int64, McCabe_sum_after int64, N1_diff int64, too-many-statements int64, comparison-of-constants int64, pointless-statement int64, time_diff int64, prev_count int64, Single comments_diff int64, massive_change int64, Blank_diff int64, too-many-nested-blocks int64, Comments_before int64, modified_McCabe_max_diff int64, LLOC_diff int64, Blank_before int64, try-except-raise int64, too-many-branches int64, too-many-return-statements int64, unnecessary-semicolon int64, wildcard-import int64, high_ccp_group int64, line-too-long int64) as (
  case when high_ccp_group <= 0.5 then
    case when Single comments_diff <= -18.5 then
      case when hunks_num <= 12.5 then
        case when h1_diff <= -0.5 then
           return 1.0 # (1.0 out of 1.0)
        else  # if h1_diff > -0.5
          case when Comments_diff <= -23.5 then
             return 0.0 # (0.0 out of 1.0)
          else  # if Comments_diff > -23.5
             return 1.0 # (1.0 out of 1.0)
          end         end       else  # if hunks_num > 12.5
         return 0.0 # (0.0 out of 1.0)
      end     else  # if Single comments_diff > -18.5
      case when low_ccp_group <= 0.5 then
        case when Comments_after <= 8.5 then
          case when SLOC_diff <= -9.5 then
            case when LOC_before <= 317.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if LOC_before > 317.5
               return 1.0 # (1.0 out of 1.0)
            end           else  # if SLOC_diff > -9.5
            case when broad-exception-caught <= 0.5 then
              case when too-many-nested-blocks <= 0.5 then
                case when McCabe_max_before <= 4.5 then
                  case when refactor_mle_diff <= -0.05866388976573944 then
                     return 1.0 # (1.0 out of 1.0)
                  else  # if refactor_mle_diff > -0.05866388976573944
                     return 0.0 # (0.0 out of 1.0)
                  end                 else  # if McCabe_max_before > 4.5
                   return 1.0 # (1.0 out of 1.0)
                end               else  # if too-many-nested-blocks > 0.5
                case when hunks_num <= 0.5 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if hunks_num > 0.5
                   return 1.0 # (1.0 out of 1.0)
                end               end             else  # if broad-exception-caught > 0.5
               return 0.0 # (0.0 out of 1.0)
            end           end         else  # if Comments_after > 8.5
          case when changed_lines <= 136.0 then
            case when same_day_duration_avg_diff <= -0.14351852238178253 then
              case when Comments_before <= 41.0 then
                case when Single comments_before <= 25.5 then
                  case when Single comments_after <= 22.5 then
                    case when Comments_after <= 18.5 then
                      case when Multi_diff <= 0.5 then
                         return 0.0 # (0.0 out of 1.0)
                      else  # if Multi_diff > 0.5
                         return 1.0 # (1.0 out of 1.0)
                      end                     else  # if Comments_after > 18.5
                       return 1.0 # (1.0 out of 1.0)
                    end                   else  # if Single comments_after > 22.5
                     return 0.0 # (0.0 out of 1.0)
                  end                 else  # if Single comments_before > 25.5
                  case when same_day_duration_avg_diff <= -68.5773811340332 then
                    case when Blank_before <= 67.5 then
                       return 1.0 # (1.0 out of 1.0)
                    else  # if Blank_before > 67.5
                      case when LOC_diff <= 4.5 then
                         return 0.0 # (0.0 out of 1.0)
                      else  # if LOC_diff > 4.5
                         return 1.0 # (1.0 out of 1.0)
                      end                     end                   else  # if same_day_duration_avg_diff > -68.5773811340332
                     return 1.0 # (1.0 out of 1.0)
                  end                 end               else  # if Comments_before > 41.0
                case when Single comments_after <= 126.5 then
                  case when refactor_mle_diff <= -0.20208058506250381 then
                    case when added_lines <= 9.5 then
                       return 1.0 # (1.0 out of 1.0)
                    else  # if added_lines > 9.5
                      case when one_file_fix_rate_diff <= 0.1964285746216774 then
                         return 0.0 # (0.0 out of 1.0)
                      else  # if one_file_fix_rate_diff > 0.1964285746216774
                         return 1.0 # (1.0 out of 1.0)
                      end                     end                   else  # if refactor_mle_diff > -0.20208058506250381
                    case when simplifiable-if-expression <= 0.5 then
                       return 0.0 # (0.0 out of 1.0)
                    else  # if simplifiable-if-expression > 0.5
                       return 1.0 # (1.0 out of 1.0)
                    end                   end                 else  # if Single comments_after > 126.5
                  case when LLOC_before <= 1604.0 then
                     return 1.0 # (1.0 out of 1.0)
                  else  # if LLOC_before > 1604.0
                     return 0.0 # (0.0 out of 1.0)
                  end                 end               end             else  # if same_day_duration_avg_diff > -0.14351852238178253
              case when superfluous-parens <= 0.5 then
                case when one_file_fix_rate_diff <= 0.440476194024086 then
                  case when Comments_diff <= -15.0 then
                     return 1.0 # (1.0 out of 1.0)
                  else  # if Comments_diff > -15.0
                    case when Multi_diff <= -29.0 then
                       return 1.0 # (1.0 out of 1.0)
                    else  # if Multi_diff > -29.0
                      case when refactor_mle_diff <= 0.8250571489334106 then
                        case when unnecessary-semicolon <= 0.5 then
                          case when too-many-boolean-expressions <= 0.5 then
                            case when McCabe_max_before <= 20.5 then
                              case when McCabe_sum_diff <= -1.5 then
                                case when Comments_diff <= -0.5 then
                                   return 0.0 # (0.0 out of 1.0)
                                else  # if Comments_diff > -0.5
                                   return 1.0 # (1.0 out of 1.0)
                                end                               else  # if McCabe_sum_diff > -1.5
                                case when avg_coupling_code_size_cut_diff <= 1.9235294461250305 then
                                   return 0.0 # (0.0 out of 1.0)
                                else  # if avg_coupling_code_size_cut_diff > 1.9235294461250305
                                   return 1.0 # (1.0 out of 1.0)
                                end                               end                             else  # if McCabe_max_before > 20.5
                               return 0.0 # (0.0 out of 1.0)
                            end                           else  # if too-many-boolean-expressions > 0.5
                            case when Single comments_diff <= 1.0 then
                               return 1.0 # (1.0 out of 1.0)
                            else  # if Single comments_diff > 1.0
                               return 0.0 # (0.0 out of 1.0)
                            end                           end                         else  # if unnecessary-semicolon > 0.5
                          case when refactor_mle_diff <= 0.08619999885559082 then
                             return 0.0 # (0.0 out of 1.0)
                          else  # if refactor_mle_diff > 0.08619999885559082
                             return 1.0 # (1.0 out of 1.0)
                          end                         end                       else  # if refactor_mle_diff > 0.8250571489334106
                         return 1.0 # (1.0 out of 1.0)
                      end                     end                   end                 else  # if one_file_fix_rate_diff > 0.440476194024086
                  case when McCabe_max_after <= 17.5 then
                     return 1.0 # (1.0 out of 1.0)
                  else  # if McCabe_max_after > 17.5
                     return 0.0 # (0.0 out of 1.0)
                  end                 end               else  # if superfluous-parens > 0.5
                case when prev_count <= 4.0 then
                  case when removed_lines <= 1.5 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if removed_lines > 1.5
                    case when N1_diff <= 2.5 then
                       return 1.0 # (1.0 out of 1.0)
                    else  # if N1_diff > 2.5
                      case when LLOC_diff <= 16.0 then
                         return 0.0 # (0.0 out of 1.0)
                      else  # if LLOC_diff > 16.0
                         return 1.0 # (1.0 out of 1.0)
                      end                     end                   end                 else  # if prev_count > 4.0
                   return 0.0 # (0.0 out of 1.0)
                end               end             end           else  # if changed_lines > 136.0
            case when added_lines <= 250.5 then
              case when Single comments_diff <= 0.5 then
                case when one_file_fix_rate_diff <= -0.3166666775941849 then
                  case when SLOC_before <= 622.0 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if SLOC_before > 622.0
                     return 1.0 # (1.0 out of 1.0)
                  end                 else  # if one_file_fix_rate_diff > -0.3166666775941849
                   return 1.0 # (1.0 out of 1.0)
                end               else  # if Single comments_diff > 0.5
                case when refactor_mle_diff <= -0.12184464931488037 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if refactor_mle_diff > -0.12184464931488037
                  case when modified_McCabe_max_diff <= -2.0 then
                    case when changed_lines <= 151.5 then
                      case when avg_coupling_code_size_cut_diff <= 0.3333333134651184 then
                         return 1.0 # (1.0 out of 1.0)
                      else  # if avg_coupling_code_size_cut_diff > 0.3333333134651184
                         return 0.0 # (0.0 out of 1.0)
                      end                     else  # if changed_lines > 151.5
                       return 0.0 # (0.0 out of 1.0)
                    end                   else  # if modified_McCabe_max_diff > -2.0
                     return 1.0 # (1.0 out of 1.0)
                  end                 end               end             else  # if added_lines > 250.5
              case when added_functions <= 1.5 then
                case when same_day_duration_avg_diff <= -27.68233013153076 then
                  case when McCabe_sum_after <= 87.0 then
                    case when h2_diff <= -156.0 then
                       return 1.0 # (1.0 out of 1.0)
                    else  # if h2_diff > -156.0
                       return 0.0 # (0.0 out of 1.0)
                    end                   else  # if McCabe_sum_after > 87.0
                     return 1.0 # (1.0 out of 1.0)
                  end                 else  # if same_day_duration_avg_diff > -27.68233013153076
                   return 0.0 # (0.0 out of 1.0)
                end               else  # if added_functions > 1.5
                 return 0.0 # (0.0 out of 1.0)
              end             end           end         end       else  # if low_ccp_group > 0.5
        case when Single comments_diff <= 21.0 then
          case when Blank_before <= 562.0 then
            case when Single comments_after <= 0.5 then
               return 1.0 # (1.0 out of 1.0)
            else  # if Single comments_after > 0.5
              case when same_day_duration_avg_diff <= 658.5833282470703 then
                case when unnecessary-semicolon <= 0.5 then
                  case when one_file_fix_rate_diff <= 0.2916666716337204 then
                    case when refactor_mle_diff <= 0.4816414415836334 then
                      case when Single comments_before <= 5.5 then
                        case when too-many-lines <= 0.5 then
                           return 0.0 # (0.0 out of 1.0)
                        else  # if too-many-lines > 0.5
                           return 1.0 # (1.0 out of 1.0)
                        end                       else  # if Single comments_before > 5.5
                         return 0.0 # (0.0 out of 1.0)
                      end                     else  # if refactor_mle_diff > 0.4816414415836334
                      case when McCabe_max_after <= 22.0 then
                         return 0.0 # (0.0 out of 1.0)
                      else  # if McCabe_max_after > 22.0
                         return 1.0 # (1.0 out of 1.0)
                      end                     end                   else  # if one_file_fix_rate_diff > 0.2916666716337204
                    case when LOC_diff <= 2.5 then
                      case when modified_McCabe_max_diff <= 0.5 then
                         return 0.0 # (0.0 out of 1.0)
                      else  # if modified_McCabe_max_diff > 0.5
                         return 1.0 # (1.0 out of 1.0)
                      end                     else  # if LOC_diff > 2.5
                       return 1.0 # (1.0 out of 1.0)
                    end                   end                 else  # if unnecessary-semicolon > 0.5
                  case when McCabe_max_before <= 8.0 then
                     return 1.0 # (1.0 out of 1.0)
                  else  # if McCabe_max_before > 8.0
                     return 0.0 # (0.0 out of 1.0)
                  end                 end               else  # if same_day_duration_avg_diff > 658.5833282470703
                 return 1.0 # (1.0 out of 1.0)
              end             end           else  # if Blank_before > 562.0
            case when Comments_before <= 486.0 then
               return 1.0 # (1.0 out of 1.0)
            else  # if Comments_before > 486.0
               return 0.0 # (0.0 out of 1.0)
            end           end         else  # if Single comments_diff > 21.0
          case when McCabe_max_after <= 9.0 then
             return 0.0 # (0.0 out of 1.0)
          else  # if McCabe_max_after > 9.0
             return 1.0 # (1.0 out of 1.0)
          end         end       end     end   else  # if high_ccp_group > 0.5
    case when changed_lines <= 350.5 then
      case when Comments_diff <= 7.0 then
        case when one_file_fix_rate_diff <= 0.36666667461395264 then
          case when avg_coupling_code_size_cut_diff <= -1.2380952835083008 then
            case when refactor_mle_diff <= 0.0420738086104393 then
              case when SLOC_before <= 149.5 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if SLOC_before > 149.5
                case when one_file_fix_rate_diff <= -0.4416666626930237 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if one_file_fix_rate_diff > -0.4416666626930237
                   return 1.0 # (1.0 out of 1.0)
                end               end             else  # if refactor_mle_diff > 0.0420738086104393
               return 0.0 # (0.0 out of 1.0)
            end           else  # if avg_coupling_code_size_cut_diff > -1.2380952835083008
            case when vocabulary_diff <= -0.5 then
              case when same_day_duration_avg_diff <= 28.825932025909424 then
                case when LOC_diff <= -3.0 then
                  case when N2_diff <= -64.5 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if N2_diff > -64.5
                     return 1.0 # (1.0 out of 1.0)
                  end                 else  # if LOC_diff > -3.0
                  case when removed_lines <= 66.0 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if removed_lines > 66.0
                     return 1.0 # (1.0 out of 1.0)
                  end                 end               else  # if same_day_duration_avg_diff > 28.825932025909424
                case when removed_lines <= 13.0 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if removed_lines > 13.0
                   return 1.0 # (1.0 out of 1.0)
                end               end             else  # if vocabulary_diff > -0.5
              case when simplifiable-condition <= 0.5 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if simplifiable-condition > 0.5
                 return 0.0 # (0.0 out of 1.0)
              end             end           end         else  # if one_file_fix_rate_diff > 0.36666667461395264
          case when refactor_mle_diff <= -0.1139286682009697 then
            case when is_refactor <= 0.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if is_refactor > 0.5
               return 1.0 # (1.0 out of 1.0)
            end           else  # if refactor_mle_diff > -0.1139286682009697
            case when McCabe_sum_after <= 404.0 then
               return 1.0 # (1.0 out of 1.0)
            else  # if McCabe_sum_after > 404.0
               return 0.0 # (0.0 out of 1.0)
            end           end         end       else  # if Comments_diff > 7.0
        case when low_McCabe_max_diff <= 0.5 then
           return 0.0 # (0.0 out of 1.0)
        else  # if low_McCabe_max_diff > 0.5
           return 1.0 # (1.0 out of 1.0)
        end       end     else  # if changed_lines > 350.5
      case when refactor_mle_diff <= 0.09177327528595924 then
         return 0.0 # (0.0 out of 1.0)
      else  # if refactor_mle_diff > 0.09177327528595924
        case when N1_diff <= -16.0 then
           return 1.0 # (1.0 out of 1.0)
        else  # if N1_diff > -16.0
           return 0.0 # (0.0 out of 1.0)
        end       end     end   end )