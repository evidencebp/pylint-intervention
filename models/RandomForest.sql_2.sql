create or replace function RandomForest_2 (h1_diff int64, SLOC_before int64, avg_coupling_code_size_cut_diff int64, Multi_diff int64, using-constant-test int64, high_McCabe_sum_diff int64, difficulty_diff int64, LLOC_diff int64, length_diff int64, Comments_after int64, McCabe_max_before int64, low_McCabe_sum_before int64, cur_count int64, LOC_before int64, low_McCabe_max_before int64, massive_change int64, too-many-return-statements int64, Comments_diff int64, added_lines int64, broad-exception-caught int64, comparison-of-constants int64, Single comments_diff int64, refactor_mle_diff int64, prev_count_x int64, McCabe_sum_before int64, modified_McCabe_max_diff int64, Simplify-boolean-expression int64, Blank_diff int64, added_functions int64, LLOC_before int64, cur_count_x int64, high_McCabe_sum_before int64, volume_diff int64, low_McCabe_max_diff int64, LOC_diff int64, calculated_length_diff int64, changed_lines int64, N2_diff int64, h2_diff int64, too-many-lines int64, unnecessary-pass int64, simplifiable-if-statement int64, prev_count int64, too-many-nested-blocks int64, Comments_before int64, SLOC_diff int64, McCabe_sum_after int64, bugs_diff int64, cur_count_y int64, Single comments_after int64, McCabe_max_diff int64, N1_diff int64, wildcard-import int64, McCabe_sum_diff int64, prev_count_y int64, superfluous-parens int64, hunks_num int64, try-except-raise int64, simplifiable-if-expression int64, McCabe_max_after int64, high_McCabe_max_diff int64, too-many-statements int64, simplifiable-condition int64, only_removal int64, unnecessary-semicolon int64, effort_diff int64, is_refactor int64, same_day_duration_avg_diff int64, one_file_fix_rate_diff int64, high_McCabe_max_before int64, vocabulary_diff int64, too-many-branches int64, mostly_delete int64, high_ccp_group int64, low_ccp_group int64, removed_lines int64, Single comments_before int64, low_McCabe_sum_diff int64, time_diff int64, Blank_before int64, line-too-long int64, too-many-boolean-expressions int64, pointless-statement int64) as (
  case when hunks_num <= 11.5 then
    case when high_ccp_group <= 0.5 then
      case when LOC_diff <= -118.5 then
        case when N2_diff <= -73.5 then
          case when Comments_before <= 119.5 then
             return 1.0 # (1.0 out of 1.0)
          else  # if Comments_before > 119.5
             return 0.9285714285714286 # (0.9285714285714286 out of 1.0)
          end         else  # if N2_diff > -73.5
           return 0.68 # (0.68 out of 1.0)
        end       else  # if LOC_diff > -118.5
        case when Comments_before <= 246.5 then
          case when SLOC_before <= 117.5 then
             return 0.7647058823529411 # (0.7647058823529411 out of 1.0)
          else  # if SLOC_before > 117.5
            case when low_ccp_group <= 0.5 then
              case when McCabe_sum_after <= 56.5 then
                case when hunks_num <= 2.5 then
                   return 0.782608695652174 # (0.782608695652174 out of 1.0)
                else  # if hunks_num > 2.5
                  case when McCabe_max_after <= 3.5 then
                     return 0.13043478260869565 # (0.13043478260869565 out of 1.0)
                  else  # if McCabe_max_after > 3.5
                     return 0.75 # (0.75 out of 1.0)
                  end                 end               else  # if McCabe_sum_after > 56.5
                case when Blank_before <= 250.5 then
                  case when SLOC_diff <= -7.5 then
                    case when Comments_before <= 48.5 then
                       return 0.17647058823529413 # (0.17647058823529413 out of 1.0)
                    else  # if Comments_before > 48.5
                       return 0.05263157894736842 # (0.05263157894736842 out of 1.0)
                    end                   else  # if SLOC_diff > -7.5
                    case when Single comments_before <= 82.5 then
                      case when hunks_num <= 3.5 then
                        case when McCabe_max_after <= 14.5 then
                           return 0.3684210526315789 # (0.3684210526315789 out of 1.0)
                        else  # if McCabe_max_after > 14.5
                           return 0.6956521739130435 # (0.6956521739130435 out of 1.0)
                        end                       else  # if hunks_num > 3.5
                         return 0.15 # (0.15 out of 1.0)
                      end                     else  # if Single comments_before > 82.5
                       return 0.05263157894736842 # (0.05263157894736842 out of 1.0)
                    end                   end                 else  # if Blank_before > 250.5
                   return 0.8125 # (0.8125 out of 1.0)
                end               end             else  # if low_ccp_group > 0.5
              case when length_diff <= -1.0 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if length_diff > -1.0
                case when avg_coupling_code_size_cut_diff <= 0.1666666716337204 then
                   return 0.2692307692307692 # (0.2692307692307692 out of 1.0)
                else  # if avg_coupling_code_size_cut_diff > 0.1666666716337204
                   return 0.07142857142857142 # (0.07142857142857142 out of 1.0)
                end               end             end           end         else  # if Comments_before > 246.5
          case when McCabe_max_after <= 23.5 then
             return 0.7777777777777778 # (0.7777777777777778 out of 1.0)
          else  # if McCabe_max_after > 23.5
             return 0.5833333333333334 # (0.5833333333333334 out of 1.0)
          end         end       end     else  # if high_ccp_group > 0.5
      case when Single comments_before <= 71.0 then
        case when LLOC_diff <= -14.0 then
           return 1.0 # (1.0 out of 1.0)
        else  # if LLOC_diff > -14.0
           return 0.7906976744186046 # (0.7906976744186046 out of 1.0)
        end       else  # if Single comments_before > 71.0
        case when refactor_mle_diff <= -0.09296078234910965 then
           return 0.5263157894736842 # (0.5263157894736842 out of 1.0)
        else  # if refactor_mle_diff > -0.09296078234910965
           return 0.6842105263157895 # (0.6842105263157895 out of 1.0)
        end       end     end   else  # if hunks_num > 11.5
    case when Comments_before <= 204.0 then
      case when avg_coupling_code_size_cut_diff <= -1.1547619104385376 then
        case when avg_coupling_code_size_cut_diff <= -1.7916666865348816 then
           return 0.08333333333333333 # (0.08333333333333333 out of 1.0)
        else  # if avg_coupling_code_size_cut_diff > -1.7916666865348816
           return 0.0 # (0.0 out of 1.0)
        end       else  # if avg_coupling_code_size_cut_diff > -1.1547619104385376
        case when vocabulary_diff <= -22.0 then
           return 0.0 # (0.0 out of 1.0)
        else  # if vocabulary_diff > -22.0
          case when Blank_diff <= 5.5 then
            case when hunks_num <= 15.5 then
               return 0.42105263157894735 # (0.42105263157894735 out of 1.0)
            else  # if hunks_num > 15.5
               return 0.06666666666666667 # (0.06666666666666667 out of 1.0)
            end           else  # if Blank_diff > 5.5
             return 0.6470588235294118 # (0.6470588235294118 out of 1.0)
          end         end       end     else  # if Comments_before > 204.0
       return 0.6153846153846154 # (0.6153846153846154 out of 1.0)
    end   end )