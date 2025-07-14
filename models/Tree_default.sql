create or replace function Tree_default (effort_diff int64, too-many-nested-blocks int64, Single comments_diff int64, N1_diff int64, avg_coupling_code_size_cut_diff int64, Simplify-boolean-expression int64, try-except-raise int64, h1_diff int64, added_functions int64, too-many-boolean-expressions int64, LLOC_diff int64, cur_count_x int64, wildcard-import int64, mostly_delete int64, LOC_diff int64, difficulty_diff int64, Comments_before int64, prev_count_y int64, time_diff int64, pointless-statement int64, vocabulary_diff int64, modified_McCabe_max_diff int64, prev_count int64, McCabe_sum_before int64, McCabe_max_after int64, Blank_diff int64, using-constant-test int64, McCabe_max_before int64, is_refactor int64, Comments_after int64, SLOC_before int64, superfluous-parens int64, too-many-branches int64, massive_change int64, comparison-of-constants int64, broad-exception-caught int64, Blank_before int64, N2_diff int64, McCabe_sum_after int64, too-many-statements int64, refactor_mle_diff int64, LOC_before int64, simplifiable-if-statement int64, only_removal int64, h2_diff int64, unnecessary-semicolon int64, too-many-lines int64, LLOC_before int64, volume_diff int64, too-many-return-statements int64, high_ccp_group int64, Single comments_before int64, simplifiable-if-expression int64, changed_lines int64, Multi_diff int64, one_file_fix_rate_diff int64, prev_count_x int64, simplifiable-condition int64, cur_count_y int64, calculated_length_diff int64, SLOC_diff int64, line-too-long int64, McCabe_max_diff int64, Comments_diff int64, cur_count int64, Single comments_after int64, removed_lines int64, added_lines int64, length_diff int64, unnecessary-pass int64, hunks_num int64, bugs_diff int64, same_day_duration_avg_diff int64, McCabe_sum_diff int64) as (
  case when high_ccp_group <= 0.5 then
    case when changed_lines <= 138.5 then
      case when LOC_diff <= 38.5 then
        case when changed_lines <= 32.0 then
          case when Multi_diff <= 0.5 then
            case when Comments_before <= 196.5 then
              case when one_file_fix_rate_diff <= 0.3095238208770752 then
                case when SLOC_before <= 593.0 then
                  case when Single comments_after <= 18.0 then
                    case when Blank_diff <= 1.0 then
                      case when McCabe_sum_after <= 6.5 then
                        case when LLOC_before <= 298.5 then
                           return 0.0 # (0.0 out of 2.0)
                        else  # if LLOC_before > 298.5
                           return 1.0 # (1.0 out of 1.0)
                        end                       else  # if McCabe_sum_after > 6.5
                        case when McCabe_sum_after <= 139.0 then
                           return 1.0 # (9.0 out of 9.0)
                        else  # if McCabe_sum_after > 139.0
                           return 0.0 # (0.0 out of 1.0)
                        end                       end                     else  # if Blank_diff > 1.0
                       return 0.0 # (0.0 out of 3.0)
                    end                   else  # if Single comments_after > 18.0
                    case when McCabe_max_after <= 30.0 then
                      case when Comments_before <= 170.5 then
                        case when one_file_fix_rate_diff <= -0.6904762089252472 then
                          case when McCabe_max_before <= 14.0 then
                             return 0.0 # (0.0 out of 2.0)
                          else  # if McCabe_max_before > 14.0
                             return 1.0 # (1.0 out of 1.0)
                          end                         else  # if one_file_fix_rate_diff > -0.6904762089252472
                           return 0.0 # (0.0 out of 37.0)
                        end                       else  # if Comments_before > 170.5
                         return 1.0 # (1.0 out of 1.0)
                      end                     else  # if McCabe_max_after > 30.0
                       return 1.0 # (3.0 out of 3.0)
                    end                   end                 else  # if SLOC_before > 593.0
                  case when McCabe_sum_after <= 227.0 then
                    case when McCabe_max_after <= 31.0 then
                      case when unnecessary-semicolon <= 0.5 then
                         return 1.0 # (16.0 out of 16.0)
                      else  # if unnecessary-semicolon > 0.5
                         return 0.0 # (0.0 out of 1.0)
                      end                     else  # if McCabe_max_after > 31.0
                       return 0.0 # (0.0 out of 2.0)
                    end                   else  # if McCabe_sum_after > 227.0
                    case when LLOC_before <= 1200.0 then
                       return 0.0 # (0.0 out of 10.0)
                    else  # if LLOC_before > 1200.0
                       return 1.0 # (3.0 out of 3.0)
                    end                   end                 end               else  # if one_file_fix_rate_diff > 0.3095238208770752
                 return 1.0 # (8.0 out of 8.0)
              end             else  # if Comments_before > 196.5
              case when one_file_fix_rate_diff <= -0.24657286703586578 then
                case when McCabe_sum_before <= 407.0 then
                   return 1.0 # (1.0 out of 1.0)
                else  # if McCabe_sum_before > 407.0
                   return 0.0 # (0.0 out of 2.0)
                end               else  # if one_file_fix_rate_diff > -0.24657286703586578
                 return 0.0 # (0.0 out of 16.0)
              end             end           else  # if Multi_diff > 0.5
             return 1.0 # (7.0 out of 7.0)
          end         else  # if changed_lines > 32.0
          case when Blank_before <= 13.5 then
             return 1.0 # (2.0 out of 2.0)
          else  # if Blank_before > 13.5
            case when modified_McCabe_max_diff <= -1.5 then
              case when Single comments_after <= 20.5 then
                 return 0.0 # (0.0 out of 16.0)
              else  # if Single comments_after > 20.5
                case when Single comments_after <= 33.0 then
                  case when same_day_duration_avg_diff <= 100.95833015441895 then
                     return 1.0 # (9.0 out of 9.0)
                  else  # if same_day_duration_avg_diff > 100.95833015441895
                     return 0.0 # (0.0 out of 1.0)
                  end                 else  # if Single comments_after > 33.0
                  case when is_refactor <= 0.5 then
                    case when removed_lines <= 14.5 then
                       return 0.0 # (0.0 out of 8.0)
                    else  # if removed_lines > 14.5
                      case when LOC_before <= 2171.0 then
                        case when same_day_duration_avg_diff <= 54.54828071594238 then
                           return 1.0 # (5.0 out of 5.0)
                        else  # if same_day_duration_avg_diff > 54.54828071594238
                          case when McCabe_sum_diff <= 0.5 then
                             return 0.0 # (0.0 out of 2.0)
                          else  # if McCabe_sum_diff > 0.5
                             return 1.0 # (1.0 out of 1.0)
                          end                         end                       else  # if LOC_before > 2171.0
                         return 0.0 # (0.0 out of 2.0)
                      end                     end                   else  # if is_refactor > 0.5
                     return 0.0 # (0.0 out of 11.0)
                  end                 end               end             else  # if modified_McCabe_max_diff > -1.5
              case when Blank_diff <= 4.5 then
                case when Single comments_diff <= -13.5 then
                   return 1.0 # (1.0 out of 1.0)
                else  # if Single comments_diff > -13.5
                  case when LOC_before <= 136.5 then
                     return 1.0 # (1.0 out of 1.0)
                  else  # if LOC_before > 136.5
                    case when Blank_diff <= -5.5 then
                      case when SLOC_before <= 757.5 then
                        case when changed_lines <= 56.0 then
                           return 1.0 # (1.0 out of 1.0)
                        else  # if changed_lines > 56.0
                           return 0.0 # (0.0 out of 11.0)
                        end                       else  # if SLOC_before > 757.5
                         return 1.0 # (3.0 out of 3.0)
                      end                     else  # if Blank_diff > -5.5
                      case when Blank_before <= 405.0 then
                         return 0.0 # (0.0 out of 70.0)
                      else  # if Blank_before > 405.0
                        case when refactor_mle_diff <= -0.3819451183080673 then
                           return 1.0 # (1.0 out of 1.0)
                        else  # if refactor_mle_diff > -0.3819451183080673
                           return 0.0 # (0.0 out of 3.0)
                        end                       end                     end                   end                 end               else  # if Blank_diff > 4.5
                case when modified_McCabe_max_diff <= 2.0 then
                   return 1.0 # (3.0 out of 3.0)
                else  # if modified_McCabe_max_diff > 2.0
                   return 0.0 # (0.0 out of 2.0)
                end               end             end           end         end       else  # if LOC_diff > 38.5
        case when LLOC_diff <= 31.5 then
           return 1.0 # (16.0 out of 16.0)
        else  # if LLOC_diff > 31.5
           return 0.0 # (0.0 out of 3.0)
        end       end     else  # if changed_lines > 138.5
      case when McCabe_max_after <= 7.5 then
        case when same_day_duration_avg_diff <= -63.91071319580078 then
          case when SLOC_before <= 125.5 then
             return 1.0 # (1.0 out of 1.0)
          else  # if SLOC_before > 125.5
             return 0.0 # (0.0 out of 4.0)
          end         else  # if same_day_duration_avg_diff > -63.91071319580078
          case when McCabe_max_before <= 2.5 then
            case when LOC_before <= 328.5 then
               return 1.0 # (1.0 out of 1.0)
            else  # if LOC_before > 328.5
               return 0.0 # (0.0 out of 3.0)
            end           else  # if McCabe_max_before > 2.5
            case when SLOC_diff <= 68.5 then
               return 1.0 # (37.0 out of 37.0)
            else  # if SLOC_diff > 68.5
               return 0.0 # (0.0 out of 1.0)
            end           end         end       else  # if McCabe_max_after > 7.5
        case when h2_diff <= -193.0 then
           return 1.0 # (9.0 out of 9.0)
        else  # if h2_diff > -193.0
          case when McCabe_sum_after <= 105.5 then
            case when SLOC_before <= 268.5 then
              case when too-many-statements <= 0.5 then
                 return 1.0 # (4.0 out of 4.0)
              else  # if too-many-statements > 0.5
                 return 0.0 # (0.0 out of 1.0)
              end             else  # if SLOC_before > 268.5
              case when Single comments_diff <= 22.5 then
                case when McCabe_sum_diff <= -41.5 then
                  case when Single comments_diff <= -27.5 then
                     return 1.0 # (1.0 out of 1.0)
                  else  # if Single comments_diff > -27.5
                     return 0.0 # (0.0 out of 1.0)
                  end                 else  # if McCabe_sum_diff > -41.5
                   return 0.0 # (0.0 out of 26.0)
                end               else  # if Single comments_diff > 22.5
                 return 1.0 # (1.0 out of 1.0)
              end             end           else  # if McCabe_sum_after > 105.5
            case when LLOC_diff <= -235.0 then
               return 0.0 # (0.0 out of 7.0)
            else  # if LLOC_diff > -235.0
              case when McCabe_max_diff <= -6.5 then
                 return 1.0 # (10.0 out of 10.0)
              else  # if McCabe_max_diff > -6.5
                case when McCabe_max_diff <= -0.5 then
                  case when LOC_before <= 4313.5 then
                     return 0.0 # (0.0 out of 6.0)
                  else  # if LOC_before > 4313.5
                    case when refactor_mle_diff <= 0.3678737282752991 then
                       return 1.0 # (1.0 out of 1.0)
                    else  # if refactor_mle_diff > 0.3678737282752991
                       return 0.0 # (0.0 out of 1.0)
                    end                   end                 else  # if McCabe_max_diff > -0.5
                  case when Single comments_after <= 76.5 then
                    case when avg_coupling_code_size_cut_diff <= -3.0863094329833984 then
                       return 0.0 # (0.0 out of 2.0)
                    else  # if avg_coupling_code_size_cut_diff > -3.0863094329833984
                      case when Single comments_diff <= 1.0 then
                         return 1.0 # (16.0 out of 16.0)
                      else  # if Single comments_diff > 1.0
                        case when one_file_fix_rate_diff <= -0.15927128260955215 then
                           return 1.0 # (3.0 out of 3.0)
                        else  # if one_file_fix_rate_diff > -0.15927128260955215
                           return 0.0 # (0.0 out of 3.0)
                        end                       end                     end                   else  # if Single comments_after > 76.5
                    case when LOC_before <= 2595.0 then
                      case when LLOC_diff <= -122.5 then
                         return 1.0 # (1.0 out of 1.0)
                      else  # if LLOC_diff > -122.5
                         return 0.0 # (0.0 out of 12.0)
                      end                     else  # if LOC_before > 2595.0
                      case when refactor_mle_diff <= -0.2951292097568512 then
                         return 0.0 # (0.0 out of 2.0)
                      else  # if refactor_mle_diff > -0.2951292097568512
                        case when Single comments_after <= 566.0 then
                           return 1.0 # (8.0 out of 8.0)
                        else  # if Single comments_after > 566.0
                           return 0.0 # (0.0 out of 1.0)
                        end                       end                     end                   end                 end               end             end           end         end       end     end   else  # if high_ccp_group > 0.5
    case when LOC_before <= 718.0 then
      case when same_day_duration_avg_diff <= 40.03510284423828 then
        case when avg_coupling_code_size_cut_diff <= -2.375 then
           return 0.0 # (0.0 out of 1.0)
        else  # if avg_coupling_code_size_cut_diff > -2.375
           return 1.0 # (35.0 out of 35.0)
        end       else  # if same_day_duration_avg_diff > 40.03510284423828
        case when line-too-long <= 0.5 then
          case when refactor_mle_diff <= -0.20951388776302338 then
             return 0.0 # (0.0 out of 2.0)
          else  # if refactor_mle_diff > -0.20951388776302338
             return 1.0 # (13.0 out of 13.0)
          end         else  # if line-too-long > 0.5
          case when massive_change <= 0.5 then
             return 0.0 # (0.0 out of 4.0)
          else  # if massive_change > 0.5
             return 1.0 # (1.0 out of 1.0)
          end         end       end     else  # if LOC_before > 718.0
      case when McCabe_sum_after <= 195.5 then
        case when one_file_fix_rate_diff <= -0.10128205269575119 then
          case when LLOC_before <= 399.5 then
            case when removed_lines <= 7.0 then
               return 0.0 # (0.0 out of 1.0)
            else  # if removed_lines > 7.0
               return 1.0 # (2.0 out of 2.0)
            end           else  # if LLOC_before > 399.5
             return 0.0 # (0.0 out of 20.0)
          end         else  # if one_file_fix_rate_diff > -0.10128205269575119
          case when LOC_before <= 810.5 then
             return 0.0 # (0.0 out of 7.0)
          else  # if LOC_before > 810.5
            case when avg_coupling_code_size_cut_diff <= 0.3735119178891182 then
              case when Multi_diff <= 11.0 then
                 return 1.0 # (11.0 out of 11.0)
              else  # if Multi_diff > 11.0
                 return 0.0 # (0.0 out of 1.0)
              end             else  # if avg_coupling_code_size_cut_diff > 0.3735119178891182
              case when Comments_before <= 28.5 then
                 return 0.0 # (0.0 out of 4.0)
              else  # if Comments_before > 28.5
                case when McCabe_max_after <= 8.0 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if McCabe_max_after > 8.0
                   return 1.0 # (4.0 out of 4.0)
                end               end             end           end         end       else  # if McCabe_sum_after > 195.5
        case when Blank_before <= 267.5 then
          case when avg_coupling_code_size_cut_diff <= 4.711538553237915 then
             return 1.0 # (22.0 out of 22.0)
          else  # if avg_coupling_code_size_cut_diff > 4.711538553237915
             return 0.0 # (0.0 out of 1.0)
          end         else  # if Blank_before > 267.5
          case when LOC_before <= 2994.5 then
            case when broad-exception-caught <= 0.5 then
               return 0.0 # (0.0 out of 4.0)
            else  # if broad-exception-caught > 0.5
               return 1.0 # (1.0 out of 1.0)
            end           else  # if LOC_before > 2994.5
             return 1.0 # (4.0 out of 4.0)
          end         end       end     end   end )