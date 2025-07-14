create or replace function Tree_ms50 (SLOC_before int64, simplifiable-condition int64, bugs_diff int64, Blank_before int64, LLOC_diff int64, try-except-raise int64, LLOC_before int64, changed_lines int64, h2_diff int64, prev_count_x int64, too-many-lines int64, cur_count_y int64, Comments_before int64, McCabe_sum_after int64, cur_count_x int64, vocabulary_diff int64, Single comments_before int64, N2_diff int64, high_ccp_group int64, massive_change int64, added_lines int64, prev_count int64, refactor_mle_diff int64, superfluous-parens int64, avg_coupling_code_size_cut_diff int64, McCabe_sum_diff int64, LOC_before int64, too-many-return-statements int64, too-many-branches int64, too-many-nested-blocks int64, difficulty_diff int64, time_diff int64, Single comments_after int64, calculated_length_diff int64, Simplify-boolean-expression int64, unnecessary-semicolon int64, mostly_delete int64, effort_diff int64, Multi_diff int64, McCabe_max_diff int64, is_refactor int64, only_removal int64, LOC_diff int64, one_file_fix_rate_diff int64, Comments_after int64, comparison-of-constants int64, McCabe_max_after int64, length_diff int64, simplifiable-if-statement int64, removed_lines int64, unnecessary-pass int64, Comments_diff int64, cur_count int64, same_day_duration_avg_diff int64, hunks_num int64, N1_diff int64, line-too-long int64, volume_diff int64, using-constant-test int64, too-many-boolean-expressions int64, modified_McCabe_max_diff int64, h1_diff int64, added_functions int64, SLOC_diff int64, too-many-statements int64, pointless-statement int64, wildcard-import int64, McCabe_max_before int64, prev_count_y int64, broad-exception-caught int64, Blank_diff int64, McCabe_sum_before int64, simplifiable-if-expression int64, Single comments_diff int64) as (
  case when Comments_after <= 5.5 then
    case when Comments_after <= 1.5 then
       return 1.0 # (23.0 out of 23.0)
    else  # if Comments_after > 1.5
      case when LOC_diff <= -2.0 then
         return 0.34782608695652173 # (8.0 out of 23.0)
      else  # if LOC_diff > -2.0
         return 0.8 # (12.0 out of 15.0)
      end     end   else  # if Comments_after > 5.5
    case when high_ccp_group <= 0.5 then
      case when Comments_diff <= -21.0 then
        case when McCabe_max_after <= 10.5 then
           return 1.0 # (17.0 out of 17.0)
        else  # if McCabe_max_after > 10.5
           return 0.2702702702702703 # (10.0 out of 37.0)
        end       else  # if Comments_diff > -21.0
        case when Single comments_diff <= 22.5 then
          case when changed_lines <= 137.0 then
            case when changed_lines <= 32.0 then
              case when avg_coupling_code_size_cut_diff <= 1.4633458256721497 then
                case when added_lines <= 11.5 then
                  case when hunks_num <= 2.5 then
                    case when changed_lines <= 4.5 then
                      case when refactor_mle_diff <= -0.026706756092607975 then
                         return 0.0425531914893617 # (2.0 out of 47.0)
                      else  # if refactor_mle_diff > -0.026706756092607975
                        case when same_day_duration_avg_diff <= 16.188889503479004 then
                           return 0.2222222222222222 # (6.0 out of 27.0)
                        else  # if same_day_duration_avg_diff > 16.188889503479004
                           return 0.07692307692307693 # (2.0 out of 26.0)
                        end                       end                     else  # if changed_lines > 4.5
                       return 0.2702702702702703 # (10.0 out of 37.0)
                    end                   else  # if hunks_num > 2.5
                    case when SLOC_diff <= 3.5 then
                       return 0.0 # (0.0 out of 54.0)
                    else  # if SLOC_diff > 3.5
                       return 0.07692307692307693 # (2.0 out of 26.0)
                    end                   end                 else  # if added_lines > 11.5
                   return 0.36363636363636365 # (12.0 out of 33.0)
                end               else  # if avg_coupling_code_size_cut_diff > 1.4633458256721497
                 return 0.4 # (10.0 out of 25.0)
              end             else  # if changed_lines > 32.0
              case when McCabe_sum_after <= 59.0 then
                case when McCabe_sum_after <= 28.0 then
                  case when LOC_diff <= -24.0 then
                     return 0.0 # (0.0 out of 30.0)
                  else  # if LOC_diff > -24.0
                     return 0.07692307692307693 # (2.0 out of 26.0)
                  end                 else  # if McCabe_sum_after > 28.0
                   return 0.4782608695652174 # (11.0 out of 23.0)
                end               else  # if McCabe_sum_after > 59.0
                case when SLOC_before <= 966.0 then
                  case when McCabe_sum_before <= 136.0 then
                    case when LOC_before <= 738.5 then
                       return 0.0 # (0.0 out of 63.0)
                    else  # if LOC_before > 738.5
                       return 0.1724137931034483 # (5.0 out of 29.0)
                    end                   else  # if McCabe_sum_before > 136.0
                    case when McCabe_sum_diff <= -0.5 then
                       return 0.0 # (0.0 out of 147.0)
                    else  # if McCabe_sum_diff > -0.5
                       return 0.03571428571428571 # (1.0 out of 28.0)
                    end                   end                 else  # if SLOC_before > 966.0
                   return 0.14285714285714285 # (6.0 out of 42.0)
                end               end             end           else  # if changed_lines > 137.0
            case when LOC_before <= 391.0 then
               return 0.7857142857142857 # (11.0 out of 14.0)
            else  # if LOC_before > 391.0
              case when added_functions <= 7.5 then
                case when McCabe_max_diff <= -6.5 then
                   return 0.6 # (9.0 out of 15.0)
                else  # if McCabe_max_diff > -6.5
                  case when SLOC_diff <= 86.5 then
                    case when added_lines <= 78.5 then
                       return 0.4 # (8.0 out of 20.0)
                    else  # if added_lines > 78.5
                      case when modified_McCabe_max_diff <= -0.5 then
                        case when LLOC_before <= 591.5 then
                           return 0.07692307692307693 # (2.0 out of 26.0)
                        else  # if LLOC_before > 591.5
                           return 0.5714285714285714 # (8.0 out of 14.0)
                        end                       else  # if modified_McCabe_max_diff > -0.5
                        case when added_lines <= 175.0 then
                           return 0.0 # (0.0 out of 39.0)
                        else  # if added_lines > 175.0
                           return 0.12903225806451613 # (4.0 out of 31.0)
                        end                       end                     end                   else  # if SLOC_diff > 86.5
                     return 0.6 # (9.0 out of 15.0)
                  end                 end               else  # if added_functions > 7.5
                 return 0.019230769230769232 # (1.0 out of 52.0)
              end             end           end         else  # if Single comments_diff > 22.5
           return 0.6842105263157895 # (13.0 out of 19.0)
        end       end     else  # if high_ccp_group > 0.5
      case when LOC_before <= 729.0 then
        case when hunks_num <= 2.5 then
           return 0.42857142857142855 # (9.0 out of 21.0)
        else  # if hunks_num > 2.5
           return 1.0 # (31.0 out of 31.0)
        end       else  # if LOC_before > 729.0
        case when McCabe_sum_after <= 196.0 then
          case when LOC_diff <= 5.5 then
            case when Comments_after <= 30.0 then
               return 0.1 # (4.0 out of 40.0)
            else  # if Comments_after > 30.0
               return 0.6666666666666666 # (12.0 out of 18.0)
            end           else  # if LOC_diff > 5.5
             return 0.0 # (0.0 out of 48.0)
          end         else  # if McCabe_sum_after > 196.0
          case when avg_coupling_code_size_cut_diff <= 0.019999999552965164 then
            case when Comments_after <= 97.0 then
               return 0.25 # (5.0 out of 20.0)
            else  # if Comments_after > 97.0
               return 0.6 # (9.0 out of 15.0)
            end           else  # if avg_coupling_code_size_cut_diff > 0.019999999552965164
             return 1.0 # (12.0 out of 12.0)
          end         end       end     end   end )