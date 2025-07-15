create or replace function Tree_ms50 (using-constant-test int64, simplifiable-if-statement int64, Comments_after int64, same_day_duration_avg_diff int64, Single comments_before int64, one_file_fix_rate_diff int64, too-many-boolean-expressions int64, Single comments_diff int64, high_McCabe_sum_before int64, pointless-statement int64, bugs_diff int64, McCabe_max_before int64, length_diff int64, LOC_diff int64, N2_diff int64, superfluous-parens int64, too-many-nested-blocks int64, effort_diff int64, cur_count_x int64, high_McCabe_max_before int64, comparison-of-constants int64, SLOC_diff int64, hunks_num int64, high_McCabe_max_diff int64, prev_count int64, McCabe_sum_after int64, cur_count_y int64, refactor_mle_diff int64, too-many-return-statements int64, too-many-statements int64, too-many-lines int64, only_removal int64, removed_lines int64, cur_count int64, volume_diff int64, is_refactor int64, prev_count_y int64, calculated_length_diff int64, Simplify-boolean-expression int64, h1_diff int64, McCabe_max_diff int64, wildcard-import int64, McCabe_sum_before int64, line-too-long int64, N1_diff int64, too-many-branches int64, h2_diff int64, McCabe_max_after int64, unnecessary-pass int64, avg_coupling_code_size_cut_diff int64, high_ccp_group int64, vocabulary_diff int64, try-except-raise int64, broad-exception-caught int64, simplifiable-condition int64, LLOC_before int64, added_functions int64, LLOC_diff int64, difficulty_diff int64, McCabe_sum_diff int64, Multi_diff int64, massive_change int64, mostly_delete int64, Comments_before int64, changed_lines int64, Comments_diff int64, time_diff int64, Blank_before int64, high_McCabe_sum_diff int64, added_lines int64, prev_count_x int64, unnecessary-semicolon int64, Blank_diff int64, modified_McCabe_max_diff int64, Single comments_after int64, LOC_before int64, simplifiable-if-expression int64, SLOC_before int64) as (
  case when high_ccp_group <= 0.5 then
    case when Comments_diff <= -21.0 then
      case when McCabe_max_diff <= -2.0 then
        case when Multi_diff <= -16.5 then
           return 1.0 # (14.0 out of 14.0)
        else  # if Multi_diff > -16.5
           return 0.9 # (9.0 out of 10.0)
        end       else  # if McCabe_max_diff > -2.0
         return 0.6 # (6.0 out of 10.0)
      end     else  # if Comments_diff > -21.0
      case when SLOC_diff <= 38.0 then
        case when Comments_after <= 6.5 then
          case when one_file_fix_rate_diff <= -0.0555555559694767 then
             return 1.0 # (10.0 out of 10.0)
          else  # if one_file_fix_rate_diff > -0.0555555559694767
            case when LOC_before <= 234.5 then
               return 0.3 # (3.0 out of 10.0)
            else  # if LOC_before > 234.5
               return 0.6 # (6.0 out of 10.0)
            end           end         else  # if Comments_after > 6.5
          case when one_file_fix_rate_diff <= 0.4833333343267441 then
            case when McCabe_sum_after <= 370.0 then
              case when McCabe_max_diff <= -0.5 then
                case when avg_coupling_code_size_cut_diff <= 0.18065998703241348 then
                  case when refactor_mle_diff <= 0.05333428084850311 then
                    case when Single comments_diff <= -5.0 then
                       return 0.1 # (1.0 out of 10.0)
                    else  # if Single comments_diff > -5.0
                       return 0.0 # (0.0 out of 40.0)
                    end                   else  # if refactor_mle_diff > 0.05333428084850311
                    case when McCabe_max_after <= 16.5 then
                       return 0.0 # (0.0 out of 12.0)
                    else  # if McCabe_max_after > 16.5
                       return 0.3076923076923077 # (4.0 out of 13.0)
                    end                   end                 else  # if avg_coupling_code_size_cut_diff > 0.18065998703241348
                   return 0.3333333333333333 # (6.0 out of 18.0)
                end               else  # if McCabe_max_diff > -0.5
                case when modified_McCabe_max_diff <= -0.5 then
                  case when one_file_fix_rate_diff <= -0.02463235380128026 then
                     return 0.2 # (2.0 out of 10.0)
                  else  # if one_file_fix_rate_diff > -0.02463235380128026
                    case when Comments_after <= 33.5 then
                       return 0.9090909090909091 # (10.0 out of 11.0)
                    else  # if Comments_after > 33.5
                       return 0.5 # (8.0 out of 16.0)
                    end                   end                 else  # if modified_McCabe_max_diff > -0.5
                  case when McCabe_sum_before <= 175.5 then
                    case when added_lines <= 91.5 then
                      case when LLOC_before <= 391.0 then
                        case when McCabe_sum_before <= 48.0 then
                           return 0.47368421052631576 # (9.0 out of 19.0)
                        else  # if McCabe_sum_before > 48.0
                          case when LOC_diff <= 0.5 then
                            case when SLOC_diff <= -2.5 then
                               return 0.0 # (0.0 out of 10.0)
                            else  # if SLOC_diff > -2.5
                               return 0.3333333333333333 # (4.0 out of 12.0)
                            end                           else  # if LOC_diff > 0.5
                             return 0.0 # (0.0 out of 26.0)
                          end                         end                       else  # if LLOC_before > 391.0
                        case when McCabe_max_before <= 12.5 then
                           return 0.2 # (2.0 out of 10.0)
                        else  # if McCabe_max_before > 12.5
                           return 0.7692307692307693 # (10.0 out of 13.0)
                        end                       end                     else  # if added_lines > 91.5
                       return 0.8 # (8.0 out of 10.0)
                    end                   else  # if McCabe_sum_before > 175.5
                    case when removed_lines <= 11.5 then
                      case when removed_lines <= 0.5 then
                         return 0.0 # (0.0 out of 15.0)
                      else  # if removed_lines > 0.5
                         return 0.4 # (4.0 out of 10.0)
                      end                     else  # if removed_lines > 11.5
                       return 0.0 # (0.0 out of 29.0)
                    end                   end                 end               end             else  # if McCabe_sum_after > 370.0
              case when avg_coupling_code_size_cut_diff <= -0.04989034961909056 then
                 return 0.8333333333333334 # (10.0 out of 12.0)
              else  # if avg_coupling_code_size_cut_diff > -0.04989034961909056
                case when McCabe_max_before <= 41.0 then
                   return 0.1875 # (3.0 out of 16.0)
                else  # if McCabe_max_before > 41.0
                   return 0.6 # (6.0 out of 10.0)
                end               end             end           else  # if one_file_fix_rate_diff > 0.4833333343267441
            case when LOC_before <= 905.5 then
               return 0.9230769230769231 # (12.0 out of 13.0)
            else  # if LOC_before > 905.5
               return 0.18181818181818182 # (2.0 out of 11.0)
            end           end         end       else  # if SLOC_diff > 38.0
        case when Blank_before <= 80.0 then
           return 1.0 # (19.0 out of 19.0)
        else  # if Blank_before > 80.0
          case when LLOC_diff <= 41.5 then
            case when same_day_duration_avg_diff <= -24.034839630126953 then
               return 0.8333333333333334 # (10.0 out of 12.0)
            else  # if same_day_duration_avg_diff > -24.034839630126953
               return 0.3 # (3.0 out of 10.0)
            end           else  # if LLOC_diff > 41.5
             return 0.16666666666666666 # (2.0 out of 12.0)
          end         end       end     end   else  # if high_ccp_group > 0.5
    case when changed_lines <= 312.5 then
      case when refactor_mle_diff <= -0.0790850818157196 then
        case when added_lines <= 59.5 then
          case when hunks_num <= 3.5 then
            case when changed_lines <= 3.0 then
               return 0.5 # (5.0 out of 10.0)
            else  # if changed_lines > 3.0
               return 0.8181818181818182 # (9.0 out of 11.0)
            end           else  # if hunks_num > 3.5
             return 0.1 # (1.0 out of 10.0)
          end         else  # if added_lines > 59.5
           return 1.0 # (12.0 out of 12.0)
        end       else  # if refactor_mle_diff > -0.0790850818157196
        case when avg_coupling_code_size_cut_diff <= -0.9416666626930237 then
           return 0.6 # (9.0 out of 15.0)
        else  # if avg_coupling_code_size_cut_diff > -0.9416666626930237
          case when one_file_fix_rate_diff <= 0.04841846041381359 then
             return 1.0 # (42.0 out of 42.0)
          else  # if one_file_fix_rate_diff > 0.04841846041381359
             return 0.75 # (12.0 out of 16.0)
          end         end       end     else  # if changed_lines > 312.5
      case when one_file_fix_rate_diff <= -0.2500000037252903 then
         return 0.0 # (0.0 out of 10.0)
      else  # if one_file_fix_rate_diff > -0.2500000037252903
         return 0.6363636363636364 # (7.0 out of 11.0)
      end     end   end )