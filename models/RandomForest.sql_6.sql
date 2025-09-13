create or replace function RandomForest_6 (McCabe_sum_before int64, changed_lines int64, prev_count_y int64, mostly_delete int64, h1_diff int64, too-many-lines int64, low_McCabe_sum_before int64, length_diff int64, LOC_before int64, simplifiable-if-expression int64, added_functions int64, broad-exception-caught int64, simplifiable-condition int64, prev_count_x int64, McCabe_max_diff int64, SLOC_before int64, LLOC_before int64, low_McCabe_max_diff int64, bugs_diff int64, same_day_duration_avg_diff int64, cur_count_x int64, only_removal int64, McCabe_max_after int64, Single comments_after int64, low_ccp_group int64, one_file_fix_rate_diff int64, effort_diff int64, difficulty_diff int64, removed_lines int64, Comments_diff int64, too-many-boolean-expressions int64, refactor_mle_diff int64, high_McCabe_max_before int64, hunks_num int64, LOC_diff int64, SLOC_diff int64, cur_count_y int64, vocabulary_diff int64, using-constant-test int64, Simplify-boolean-expression int64, low_McCabe_max_before int64, high_McCabe_sum_diff int64, high_McCabe_sum_before int64, McCabe_max_before int64, Comments_after int64, McCabe_sum_diff int64, unnecessary-pass int64, avg_coupling_code_size_cut_diff int64, simplifiable-if-statement int64, is_refactor int64, volume_diff int64, added_lines int64, high_McCabe_max_diff int64, superfluous-parens int64, cur_count int64, low_McCabe_sum_diff int64, calculated_length_diff int64, Multi_diff int64, N2_diff int64, h2_diff int64, Single comments_before int64, McCabe_sum_after int64, N1_diff int64, too-many-statements int64, comparison-of-constants int64, pointless-statement int64, time_diff int64, prev_count int64, Single comments_diff int64, massive_change int64, Blank_diff int64, too-many-nested-blocks int64, Comments_before int64, modified_McCabe_max_diff int64, LLOC_diff int64, Blank_before int64, try-except-raise int64, too-many-branches int64, too-many-return-statements int64, unnecessary-semicolon int64, wildcard-import int64, high_ccp_group int64, line-too-long int64) as (
  case when Single comments_diff <= -4.5 then
    case when N1_diff <= -126.0 then
       return 0.9375 # (0.9375 out of 1.0)
    else  # if N1_diff > -126.0
      case when LLOC_diff <= -179.5 then
         return 0.29411764705882354 # (0.29411764705882354 out of 1.0)
      else  # if LLOC_diff > -179.5
        case when LLOC_diff <= -47.5 then
           return 0.8518518518518519 # (0.8518518518518519 out of 1.0)
        else  # if LLOC_diff > -47.5
          case when McCabe_sum_before <= 61.0 then
             return 0.7777777777777778 # (0.7777777777777778 out of 1.0)
          else  # if McCabe_sum_before > 61.0
             return 0.4090909090909091 # (0.4090909090909091 out of 1.0)
          end         end       end     end   else  # if Single comments_diff > -4.5
    case when LOC_before <= 231.5 then
      case when Comments_before <= 21.5 then
        case when McCabe_sum_after <= 22.5 then
           return 0.8260869565217391 # (0.8260869565217391 out of 1.0)
        else  # if McCabe_sum_after > 22.5
           return 0.07692307692307693 # (0.07692307692307693 out of 1.0)
        end       else  # if Comments_before > 21.5
         return 1.0 # (1.0 out of 1.0)
      end     else  # if LOC_before > 231.5
      case when h2_diff <= -24.5 then
         return 0.0 # (0.0 out of 1.0)
      else  # if h2_diff > -24.5
        case when avg_coupling_code_size_cut_diff <= 1.9375 then
          case when LOC_diff <= 62.5 then
            case when McCabe_sum_after <= 449.0 then
              case when one_file_fix_rate_diff <= 0.01666666753590107 then
                case when Comments_diff <= -3.5 then
                   return 0.46153846153846156 # (0.46153846153846156 out of 1.0)
                else  # if Comments_diff > -3.5
                  case when Single comments_after <= 45.5 then
                    case when LLOC_before <= 432.0 then
                      case when Blank_before <= 71.5 then
                        case when McCabe_sum_before <= 41.5 then
                           return 0.5555555555555556 # (0.5555555555555556 out of 1.0)
                        else  # if McCabe_sum_before > 41.5
                           return 0.35714285714285715 # (0.35714285714285715 out of 1.0)
                        end                       else  # if Blank_before > 71.5
                         return 0.05555555555555555 # (0.05555555555555555 out of 1.0)
                      end                     else  # if LLOC_before > 432.0
                       return 0.625 # (0.625 out of 1.0)
                    end                   else  # if Single comments_after > 45.5
                    case when Multi_diff <= -3.0 then
                       return 0.0 # (0.0 out of 1.0)
                    else  # if Multi_diff > -3.0
                      case when h2_diff <= 1.5 then
                        case when LOC_before <= 1609.0 then
                          case when low_ccp_group <= 0.5 then
                            case when hunks_num <= 5.5 then
                               return 0.34782608695652173 # (0.34782608695652173 out of 1.0)
                            else  # if hunks_num > 5.5
                               return 0.0 # (0.0 out of 1.0)
                            end                           else  # if low_ccp_group > 0.5
                             return 0.08333333333333333 # (0.08333333333333333 out of 1.0)
                          end                         else  # if LOC_before > 1609.0
                           return 0.35714285714285715 # (0.35714285714285715 out of 1.0)
                        end                       else  # if h2_diff > 1.5
                         return 0.041666666666666664 # (0.041666666666666664 out of 1.0)
                      end                     end                   end                 end               else  # if one_file_fix_rate_diff > 0.01666666753590107
                case when McCabe_max_before <= 12.5 then
                   return 0.75 # (0.75 out of 1.0)
                else  # if McCabe_max_before > 12.5
                  case when high_McCabe_sum_diff <= 0.5 then
                    case when Single comments_after <= 100.5 then
                      case when Comments_after <= 40.5 then
                         return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
                      else  # if Comments_after > 40.5
                         return 0.5294117647058824 # (0.5294117647058824 out of 1.0)
                      end                     else  # if Single comments_after > 100.5
                       return 0.16666666666666666 # (0.16666666666666666 out of 1.0)
                    end                   else  # if high_McCabe_sum_diff > 0.5
                     return 0.11764705882352941 # (0.11764705882352941 out of 1.0)
                  end                 end               end             else  # if McCabe_sum_after > 449.0
              case when LLOC_before <= 1623.0 then
                 return 0.8823529411764706 # (0.8823529411764706 out of 1.0)
              else  # if LLOC_before > 1623.0
                 return 0.47368421052631576 # (0.47368421052631576 out of 1.0)
              end             end           else  # if LOC_diff > 62.5
            case when changed_lines <= 152.5 then
               return 0.8333333333333334 # (0.8333333333333334 out of 1.0)
            else  # if changed_lines > 152.5
               return 0.4166666666666667 # (0.4166666666666667 out of 1.0)
            end           end         else  # if avg_coupling_code_size_cut_diff > 1.9375
          case when Single comments_after <= 58.5 then
             return 0.9375 # (0.9375 out of 1.0)
          else  # if Single comments_after > 58.5
             return 0.47058823529411764 # (0.47058823529411764 out of 1.0)
          end         end       end     end   end )