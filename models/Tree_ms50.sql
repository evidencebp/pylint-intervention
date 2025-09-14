create or replace function Tree_ms50 (h1_diff int64, simplifiable-if-statement int64, McCabe_max_after int64, McCabe_sum_before int64, Single comments_before int64, low_McCabe_max_diff int64, high_ccp_group int64, pointless-statement int64, too-many-branches int64, high_McCabe_max_before int64, superfluous-parens int64, Multi_diff int64, wildcard-import int64, high_McCabe_sum_before int64, LLOC_before int64, cur_count int64, unnecessary-semicolon int64, Comments_after int64, mostly_delete int64, simplifiable-condition int64, avg_coupling_code_size_cut_diff int64, added_functions int64, McCabe_max_diff int64, McCabe_sum_diff int64, LLOC_diff int64, LOC_before int64, Comments_diff int64, prev_count_x int64, effort_diff int64, try-except-raise int64, difficulty_diff int64, line-too-long int64, Simplify-boolean-expression int64, SLOC_diff int64, McCabe_sum_after int64, refactor_mle_diff int64, one_file_fix_rate_diff int64, is_refactor int64, too-many-lines int64, too-many-boolean-expressions int64, Single comments_diff int64, low_McCabe_sum_diff int64, cur_count_y int64, comparison-of-constants int64, Comments_before int64, too-many-return-statements int64, vocabulary_diff int64, massive_change int64, hunks_num int64, modified_McCabe_max_diff int64, high_McCabe_sum_diff int64, N2_diff int64, broad-exception-caught int64, length_diff int64, unnecessary-pass int64, time_diff int64, changed_lines int64, Single comments_after int64, h2_diff int64, low_McCabe_sum_before int64, cur_count_x int64, McCabe_max_before int64, using-constant-test int64, added_lines int64, same_day_duration_avg_diff int64, prev_count_y int64, Blank_diff int64, LOC_diff int64, only_removal int64, low_McCabe_max_before int64, bugs_diff int64, too-many-statements int64, simplifiable-if-expression int64, calculated_length_diff int64, volume_diff int64, Blank_before int64, high_McCabe_max_diff int64, SLOC_before int64, too-many-nested-blocks int64, removed_lines int64, low_ccp_group int64, N1_diff int64, prev_count int64) as (
  case when high_ccp_group <= 0.5 then
    case when Single comments_diff <= -18.5 then
      case when Comments_after <= 45.0 then
         return 1.0 # (1.0 out of 1.0)
      else  # if Comments_after > 45.0
         return 0.5333333333333333 # (0.5333333333333333 out of 1.0)
      end     else  # if Single comments_diff > -18.5
      case when low_ccp_group <= 0.5 then
        case when low_McCabe_sum_before <= 0.5 then
          case when SLOC_diff <= 36.5 then
            case when same_day_duration_avg_diff <= -128.49257278442383 then
               return 0.6470588235294118 # (0.6470588235294118 out of 1.0)
            else  # if same_day_duration_avg_diff > -128.49257278442383
              case when superfluous-parens <= 0.5 then
                case when Comments_after <= 23.5 then
                   return 0.5263157894736842 # (0.5263157894736842 out of 1.0)
                else  # if Comments_after > 23.5
                  case when Blank_before <= 107.5 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if Blank_before > 107.5
                    case when McCabe_max_before <= 31.5 then
                      case when Comments_after <= 56.5 then
                        case when LLOC_before <= 502.0 then
                           return 0.0 # (0.0 out of 1.0)
                        else  # if LLOC_before > 502.0
                           return 0.2 # (0.2 out of 1.0)
                        end                       else  # if Comments_after > 56.5
                        case when LOC_before <= 1207.5 then
                           return 0.7692307692307693 # (0.7692307692307693 out of 1.0)
                        else  # if LOC_before > 1207.5
                          case when refactor_mle_diff <= -0.1440657377243042 then
                             return 0.08333333333333333 # (0.08333333333333333 out of 1.0)
                          else  # if refactor_mle_diff > -0.1440657377243042
                             return 0.4444444444444444 # (0.4444444444444444 out of 1.0)
                          end                         end                       end                     else  # if McCabe_max_before > 31.5
                       return 0.058823529411764705 # (0.058823529411764705 out of 1.0)
                    end                   end                 end               else  # if superfluous-parens > 0.5
                case when McCabe_sum_before <= 201.5 then
                   return 0.2 # (0.2 out of 1.0)
                else  # if McCabe_sum_before > 201.5
                   return 0.7058823529411765 # (0.7058823529411765 out of 1.0)
                end               end             end           else  # if SLOC_diff > 36.5
            case when Single comments_diff <= 2.0 then
               return 0.9166666666666666 # (0.9166666666666666 out of 1.0)
            else  # if Single comments_diff > 2.0
               return 0.5 # (0.5 out of 1.0)
            end           end         else  # if low_McCabe_sum_before > 0.5
          case when Single comments_before <= 39.5 then
            case when refactor_mle_diff <= -0.11903809756040573 then
              case when McCabe_sum_diff <= -0.5 then
                 return 0.7692307692307693 # (0.7692307692307693 out of 1.0)
              else  # if McCabe_sum_diff > -0.5
                 return 0.1 # (0.1 out of 1.0)
              end             else  # if refactor_mle_diff > -0.11903809756040573
              case when same_day_duration_avg_diff <= -7.148529529571533 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if same_day_duration_avg_diff > -7.148529529571533
                case when removed_lines <= 11.0 then
                   return 0.5 # (0.5 out of 1.0)
                else  # if removed_lines > 11.0
                   return 0.9 # (0.9 out of 1.0)
                end               end             end           else  # if Single comments_before > 39.5
             return 0.23076923076923078 # (0.23076923076923078 out of 1.0)
          end         end       else  # if low_ccp_group > 0.5
        case when Single comments_diff <= 21.0 then
          case when refactor_mle_diff <= -0.10518452152609825 then
            case when added_lines <= 12.5 then
               return 0.46153846153846156 # (0.46153846153846156 out of 1.0)
            else  # if added_lines > 12.5
              case when Comments_after <= 73.0 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if Comments_after > 73.0
                 return 0.3 # (0.3 out of 1.0)
              end             end           else  # if refactor_mle_diff > -0.10518452152609825
            case when added_lines <= 4.5 then
               return 0.1 # (0.1 out of 1.0)
            else  # if added_lines > 4.5
               return 0.0 # (0.0 out of 1.0)
            end           end         else  # if Single comments_diff > 21.0
           return 0.9411764705882353 # (0.9411764705882353 out of 1.0)
        end       end     end   else  # if high_ccp_group > 0.5
    case when Comments_diff <= 10.5 then
      case when added_lines <= 390.5 then
        case when high_McCabe_max_diff <= 0.5 then
          case when refactor_mle_diff <= -0.15069085359573364 then
            case when Single comments_after <= 14.5 then
               return 0.2 # (0.2 out of 1.0)
            else  # if Single comments_after > 14.5
               return 0.8823529411764706 # (0.8823529411764706 out of 1.0)
            end           else  # if refactor_mle_diff > -0.15069085359573364
            case when avg_coupling_code_size_cut_diff <= -1.0954545736312866 then
               return 0.7142857142857143 # (0.7142857142857143 out of 1.0)
            else  # if avg_coupling_code_size_cut_diff > -1.0954545736312866
              case when hunks_num <= 7.0 then
                case when Single comments_diff <= -3.0 then
                   return 0.9 # (0.9 out of 1.0)
                else  # if Single comments_diff > -3.0
                   return 1.0 # (1.0 out of 1.0)
                end               else  # if hunks_num > 7.0
                 return 0.75 # (0.75 out of 1.0)
              end             end           end         else  # if high_McCabe_max_diff > 0.5
           return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
        end       else  # if added_lines > 390.5
         return 0.16666666666666666 # (0.16666666666666666 out of 1.0)
      end     else  # if Comments_diff > 10.5
       return 0.09090909090909091 # (0.09090909090909091 out of 1.0)
    end   end )