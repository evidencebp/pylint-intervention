create or replace function Tree_ms50 (low_McCabe_sum_before int64, changed_lines int64, low_McCabe_max_diff int64, try-except-raise int64, Comments_before int64, high_McCabe_sum_diff int64, low_McCabe_max_before int64, Multi_diff int64, effort_diff int64, difficulty_diff int64, only_removal int64, length_diff int64, comparison-of-constants int64, LOC_diff int64, h2_diff int64, line-too-long int64, h1_diff int64, using-constant-test int64, broad-exception-caught int64, time_diff int64, calculated_length_diff int64, too-many-branches int64, SLOC_before int64, low_ccp_group int64, avg_coupling_code_size_cut_diff int64, new_function int64, wildcard-import int64, McCabe_max_before int64, superfluous-parens int64, low_McCabe_sum_diff int64, pointless-statement int64, one_file_fix_rate_diff int64, cur_count_x int64, same_day_duration_avg_diff int64, too-many-nested-blocks int64, simplifiable-condition int64, too-many-lines int64, SLOC_diff int64, cur_count_y int64, LLOC_before int64, Comments_after int64, high_ccp_group int64, bugs_diff int64, unnecessary-pass int64, prev_count_x int64, massive_change int64, McCabe_max_after int64, removed_lines int64, Comments_diff int64, Single comments_diff int64, too-many-statements int64, Simplify-boolean-expression int64, is_refactor int64, refactor_mle_diff int64, added_lines int64, mostly_delete int64, volume_diff int64, too-many-boolean-expressions int64, N2_diff int64, Blank_before int64, vocabulary_diff int64, McCabe_sum_before int64, high_McCabe_sum_before int64, N1_diff int64, LOC_before int64, LLOC_diff int64, high_McCabe_max_diff int64, simplifiable-if-statement int64, prev_count_y int64, hunks_num int64, Blank_diff int64, prev_count int64, Single comments_before int64, McCabe_max_diff int64, McCabe_sum_diff int64, modified_McCabe_max_diff int64, McCabe_sum_after int64, too-many-return-statements int64, Single comments_after int64, unnecessary-semicolon int64, added_functions int64, cur_count int64, simplifiable-if-expression int64, high_McCabe_max_before int64) as (
  case when low_ccp_group <= 0.5 then
    case when LLOC_before <= 190.5 then
      case when refactor_mle_diff <= -0.2524428591132164 then
         return 0.42857142857142855 # (0.42857142857142855 out of 1.0)
      else  # if refactor_mle_diff > -0.2524428591132164
        case when refactor_mle_diff <= 0.15853172540664673 then
          case when SLOC_diff <= -11.5 then
             return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
          else  # if SLOC_diff > -11.5
            case when Single comments_before <= 4.5 then
               return 0.8333333333333334 # (0.8333333333333334 out of 1.0)
            else  # if Single comments_before > 4.5
               return 1.0 # (1.0 out of 1.0)
            end           end         else  # if refactor_mle_diff > 0.15853172540664673
           return 0.5833333333333334 # (0.5833333333333334 out of 1.0)
        end       end     else  # if LLOC_before > 190.5
      case when changed_lines <= 136.5 then
        case when high_ccp_group <= 0.5 then
          case when SLOC_diff <= -17.5 then
            case when Blank_before <= 150.5 then
              case when h2_diff <= -7.5 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if h2_diff > -7.5
                 return 0.1 # (0.1 out of 1.0)
              end             else  # if Blank_before > 150.5
              case when changed_lines <= 88.5 then
                 return 0.45454545454545453 # (0.45454545454545453 out of 1.0)
              else  # if changed_lines > 88.5
                 return 0.09090909090909091 # (0.09090909090909091 out of 1.0)
              end             end           else  # if SLOC_diff > -17.5
            case when SLOC_before <= 1510.0 then
              case when SLOC_before <= 593.0 then
                case when one_file_fix_rate_diff <= 0.3282051384449005 then
                  case when Comments_before <= 37.0 then
                    case when McCabe_max_before <= 11.5 then
                       return 0.14285714285714285 # (0.14285714285714285 out of 1.0)
                    else  # if McCabe_max_before > 11.5
                       return 0.6153846153846154 # (0.6153846153846154 out of 1.0)
                    end                   else  # if Comments_before > 37.0
                     return 0.0 # (0.0 out of 1.0)
                  end                 else  # if one_file_fix_rate_diff > 0.3282051384449005
                   return 0.75 # (0.75 out of 1.0)
                end               else  # if SLOC_before > 593.0
                case when McCabe_max_before <= 31.0 then
                  case when avg_coupling_code_size_cut_diff <= -4.440892098500626e-16 then
                     return 0.75 # (0.75 out of 1.0)
                  else  # if avg_coupling_code_size_cut_diff > -4.440892098500626e-16
                     return 1.0 # (1.0 out of 1.0)
                  end                 else  # if McCabe_max_before > 31.0
                   return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
                end               end             else  # if SLOC_before > 1510.0
               return 0.058823529411764705 # (0.058823529411764705 out of 1.0)
            end           end         else  # if high_ccp_group > 0.5
          case when removed_lines <= 50.0 then
            case when refactor_mle_diff <= -0.12598980963230133 then
               return 0.4375 # (0.4375 out of 1.0)
            else  # if refactor_mle_diff > -0.12598980963230133
              case when Single comments_after <= 80.5 then
                case when Single comments_before <= 28.5 then
                   return 0.8 # (0.8 out of 1.0)
                else  # if Single comments_before > 28.5
                   return 1.0 # (1.0 out of 1.0)
                end               else  # if Single comments_after > 80.5
                 return 0.6153846153846154 # (0.6153846153846154 out of 1.0)
              end             end           else  # if removed_lines > 50.0
             return 0.2 # (0.2 out of 1.0)
          end         end       else  # if changed_lines > 136.5
        case when removed_lines <= 197.0 then
          case when N2_diff <= -40.5 then
            case when Single comments_diff <= -11.5 then
              case when Blank_before <= 182.5 then
                 return 0.9411764705882353 # (0.9411764705882353 out of 1.0)
              else  # if Blank_before > 182.5
                 return 0.4166666666666667 # (0.4166666666666667 out of 1.0)
              end             else  # if Single comments_diff > -11.5
               return 0.15384615384615385 # (0.15384615384615385 out of 1.0)
            end           else  # if N2_diff > -40.5
            case when McCabe_sum_before <= 162.0 then
              case when McCabe_max_before <= 16.5 then
                 return 0.9166666666666666 # (0.9166666666666666 out of 1.0)
              else  # if McCabe_max_before > 16.5
                 return 0.46153846153846156 # (0.46153846153846156 out of 1.0)
              end             else  # if McCabe_sum_before > 162.0
              case when McCabe_sum_before <= 225.5 then
                 return 0.9 # (0.9 out of 1.0)
              else  # if McCabe_sum_before > 225.5
                 return 1.0 # (1.0 out of 1.0)
              end             end           end         else  # if removed_lines > 197.0
          case when SLOC_diff <= 62.5 then
             return 0.05555555555555555 # (0.05555555555555555 out of 1.0)
          else  # if SLOC_diff > 62.5
             return 0.625 # (0.625 out of 1.0)
          end         end       end     end   else  # if low_ccp_group > 0.5
    case when Single comments_diff <= 21.0 then
      case when Comments_diff <= -20.5 then
         return 0.9230769230769231 # (0.9230769230769231 out of 1.0)
      else  # if Comments_diff > -20.5
        case when refactor_mle_diff <= -0.17002292722463608 then
          case when LOC_before <= 1010.5 then
            case when SLOC_diff <= -11.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if SLOC_diff > -11.5
               return 0.2 # (0.2 out of 1.0)
            end           else  # if LOC_before > 1010.5
             return 0.6363636363636364 # (0.6363636363636364 out of 1.0)
          end         else  # if refactor_mle_diff > -0.17002292722463608
          case when McCabe_sum_after <= 25.0 then
             return 0.2 # (0.2 out of 1.0)
          else  # if McCabe_sum_after > 25.0
            case when LLOC_diff <= 9.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if LLOC_diff > 9.5
               return 0.08333333333333333 # (0.08333333333333333 out of 1.0)
            end           end         end       end     else  # if Single comments_diff > 21.0
       return 0.9411764705882353 # (0.9411764705882353 out of 1.0)
    end   end )