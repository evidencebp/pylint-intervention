create or replace function Tree_ms50 (h1_diff int64, SLOC_before int64, avg_coupling_code_size_cut_diff int64, Multi_diff int64, using-constant-test int64, high_McCabe_sum_diff int64, difficulty_diff int64, LLOC_diff int64, length_diff int64, Comments_after int64, McCabe_max_before int64, low_McCabe_sum_before int64, cur_count int64, LOC_before int64, low_McCabe_max_before int64, massive_change int64, too-many-return-statements int64, Comments_diff int64, added_lines int64, broad-exception-caught int64, comparison-of-constants int64, Single comments_diff int64, refactor_mle_diff int64, prev_count_x int64, McCabe_sum_before int64, modified_McCabe_max_diff int64, Simplify-boolean-expression int64, Blank_diff int64, added_functions int64, LLOC_before int64, cur_count_x int64, high_McCabe_sum_before int64, volume_diff int64, low_McCabe_max_diff int64, LOC_diff int64, calculated_length_diff int64, changed_lines int64, N2_diff int64, h2_diff int64, too-many-lines int64, unnecessary-pass int64, simplifiable-if-statement int64, prev_count int64, too-many-nested-blocks int64, Comments_before int64, SLOC_diff int64, McCabe_sum_after int64, bugs_diff int64, cur_count_y int64, Single comments_after int64, McCabe_max_diff int64, N1_diff int64, wildcard-import int64, McCabe_sum_diff int64, prev_count_y int64, superfluous-parens int64, hunks_num int64, try-except-raise int64, simplifiable-if-expression int64, McCabe_max_after int64, high_McCabe_max_diff int64, too-many-statements int64, simplifiable-condition int64, only_removal int64, unnecessary-semicolon int64, effort_diff int64, is_refactor int64, same_day_duration_avg_diff int64, one_file_fix_rate_diff int64, high_McCabe_max_before int64, vocabulary_diff int64, too-many-branches int64, mostly_delete int64, high_ccp_group int64, low_ccp_group int64, removed_lines int64, Single comments_before int64, low_McCabe_sum_diff int64, time_diff int64, Blank_before int64, line-too-long int64, too-many-boolean-expressions int64, pointless-statement int64) as (
  case when high_ccp_group <= 0.5 then
    case when Comments_diff <= -21.0 then
      case when h1_diff <= -2.5 then
         return 1.0 # (1.0 out of 1.0)
      else  # if h1_diff > -2.5
        case when LLOC_diff <= -212.5 then
           return 0.3 # (0.3 out of 1.0)
        else  # if LLOC_diff > -212.5
           return 0.8 # (0.8 out of 1.0)
        end       end     else  # if Comments_diff > -21.0
      case when SLOC_diff <= 38.0 then
        case when low_ccp_group <= 0.5 then
          case when Blank_before <= 40.5 then
            case when refactor_mle_diff <= -0.13993506506085396 then
               return 0.5 # (0.5 out of 1.0)
            else  # if refactor_mle_diff > -0.13993506506085396
               return 0.8888888888888888 # (0.8888888888888888 out of 1.0)
            end           else  # if Blank_before > 40.5
            case when Comments_after <= 8.5 then
               return 0.8181818181818182 # (0.8181818181818182 out of 1.0)
            else  # if Comments_after > 8.5
              case when N1_diff <= -34.5 then
                 return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
              else  # if N1_diff > -34.5
                case when N2_diff <= -18.0 then
                  case when avg_coupling_code_size_cut_diff <= -0.40625 then
                     return 0.2 # (0.2 out of 1.0)
                  else  # if avg_coupling_code_size_cut_diff > -0.40625
                     return 0.0 # (0.0 out of 1.0)
                  end                 else  # if N2_diff > -18.0
                  case when prev_count_y <= 2.5 then
                    case when LOC_before <= 589.0 then
                      case when LLOC_before <= 265.0 then
                        case when McCabe_max_after <= 17.5 then
                          case when LOC_diff <= -0.5 then
                             return 0.0 # (0.0 out of 1.0)
                          else  # if LOC_diff > -0.5
                             return 0.1 # (0.1 out of 1.0)
                          end                         else  # if McCabe_max_after > 17.5
                           return 0.3 # (0.3 out of 1.0)
                        end                       else  # if LLOC_before > 265.0
                         return 0.5 # (0.5 out of 1.0)
                      end                     else  # if LOC_before > 589.0
                      case when McCabe_sum_before <= 132.5 then
                        case when LLOC_diff <= 1.5 then
                           return 0.8823529411764706 # (0.8823529411764706 out of 1.0)
                        else  # if LLOC_diff > 1.5
                           return 0.4 # (0.4 out of 1.0)
                        end                       else  # if McCabe_sum_before > 132.5
                        case when LOC_before <= 1595.5 then
                          case when Comments_before <= 101.5 then
                            case when Comments_after <= 57.0 then
                              case when SLOC_before <= 609.5 then
                                 return 0.0 # (0.0 out of 1.0)
                              else  # if SLOC_before > 609.5
                                 return 0.45454545454545453 # (0.45454545454545453 out of 1.0)
                              end                             else  # if Comments_after > 57.0
                               return 0.6923076923076923 # (0.6923076923076923 out of 1.0)
                            end                           else  # if Comments_before > 101.5
                             return 0.0 # (0.0 out of 1.0)
                          end                         else  # if LOC_before > 1595.5
                          case when McCabe_sum_before <= 516.0 then
                             return 0.8823529411764706 # (0.8823529411764706 out of 1.0)
                          else  # if McCabe_sum_before > 516.0
                             return 0.21428571428571427 # (0.21428571428571427 out of 1.0)
                          end                         end                       end                     end                   else  # if prev_count_y > 2.5
                     return 0.0 # (0.0 out of 1.0)
                  end                 end               end             end           end         else  # if low_ccp_group > 0.5
          case when McCabe_sum_before <= 275.0 then
            case when McCabe_sum_after <= 19.0 then
               return 0.3076923076923077 # (0.3076923076923077 out of 1.0)
            else  # if McCabe_sum_after > 19.0
              case when vocabulary_diff <= -9.0 then
                 return 0.15384615384615385 # (0.15384615384615385 out of 1.0)
              else  # if vocabulary_diff > -9.0
                case when added_lines <= 5.5 then
                   return 0.1 # (0.1 out of 1.0)
                else  # if added_lines > 5.5
                   return 0.0 # (0.0 out of 1.0)
                end               end             end           else  # if McCabe_sum_before > 275.0
             return 0.4166666666666667 # (0.4166666666666667 out of 1.0)
          end         end       else  # if SLOC_diff > 38.0
        case when Blank_before <= 80.0 then
           return 1.0 # (1.0 out of 1.0)
        else  # if Blank_before > 80.0
          case when length_diff <= 22.5 then
             return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
          else  # if length_diff > 22.5
             return 0.2727272727272727 # (0.2727272727272727 out of 1.0)
          end         end       end     end   else  # if high_ccp_group > 0.5
    case when changed_lines <= 304.0 then
      case when LOC_before <= 794.0 then
        case when Comments_before <= 13.0 then
           return 0.7777777777777778 # (0.7777777777777778 out of 1.0)
        else  # if Comments_before > 13.0
           return 1.0 # (1.0 out of 1.0)
        end       else  # if LOC_before > 794.0
        case when Blank_before <= 118.0 then
           return 0.23529411764705882 # (0.23529411764705882 out of 1.0)
        else  # if Blank_before > 118.0
          case when avg_coupling_code_size_cut_diff <= -0.9416666626930237 then
             return 0.5384615384615384 # (0.5384615384615384 out of 1.0)
          else  # if avg_coupling_code_size_cut_diff > -0.9416666626930237
            case when added_lines <= 25.0 then
               return 1.0 # (1.0 out of 1.0)
            else  # if added_lines > 25.0
               return 0.8 # (0.8 out of 1.0)
            end           end         end       end     else  # if changed_lines > 304.0
      case when added_lines <= 201.0 then
         return 0.0 # (0.0 out of 1.0)
      else  # if added_lines > 201.0
        case when Comments_after <= 30.0 then
           return 0.25 # (0.25 out of 1.0)
        else  # if Comments_after > 30.0
           return 0.8181818181818182 # (0.8181818181818182 out of 1.0)
        end       end     end   end )