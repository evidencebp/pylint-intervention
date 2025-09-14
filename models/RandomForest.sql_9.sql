create or replace function RandomForest_9 (prev_count int64, prev_count_x int64, prev_count_y int64, using-constant-test int64, Comments_diff int64, massive_change int64, McCabe_max_after int64, Comments_before int64, too-many-statements int64, cur_count_x int64, h1_diff int64, McCabe_sum_diff int64, LLOC_before int64, McCabe_sum_before int64, high_McCabe_max_before int64, avg_coupling_code_size_cut_diff int64, is_refactor int64, N2_diff int64, too-many-branches int64, SLOC_before int64, too-many-nested-blocks int64, too-many-lines int64, bugs_diff int64, time_diff int64, Single comments_after int64, simplifiable-condition int64, Multi_diff int64, high_McCabe_sum_before int64, low_ccp_group int64, refactor_mle_diff int64, low_McCabe_max_diff int64, SLOC_diff int64, changed_lines int64, hunks_num int64, McCabe_sum_after int64, cur_count_y int64, one_file_fix_rate_diff int64, low_McCabe_sum_before int64, modified_McCabe_max_diff int64, superfluous-parens int64, mostly_delete int64, added_functions int64, Comments_after int64, N1_diff int64, McCabe_max_diff int64, simplifiable-if-statement int64, LOC_before int64, low_McCabe_max_before int64, McCabe_max_before int64, try-except-raise int64, line-too-long int64, unnecessary-semicolon int64, wildcard-import int64, difficulty_diff int64, Simplify-boolean-expression int64, cur_count int64, low_McCabe_sum_diff int64, pointless-statement int64, length_diff int64, broad-exception-caught int64, h2_diff int64, high_McCabe_sum_diff int64, only_removal int64, comparison-of-constants int64, Single comments_diff int64, too-many-boolean-expressions int64, Blank_before int64, calculated_length_diff int64, Single comments_before int64, removed_lines int64, simplifiable-if-expression int64, LOC_diff int64, volume_diff int64, high_McCabe_max_diff int64, high_ccp_group int64, same_day_duration_avg_diff int64, Blank_diff int64, effort_diff int64, too-many-return-statements int64, added_lines int64, unnecessary-pass int64, vocabulary_diff int64, LLOC_diff int64) as (
  case when high_ccp_group <= 0.5 then
    case when h2_diff <= -51.5 then
      case when Single comments_after <= 42.0 then
         return 0.65 # (0.65 out of 1.0)
      else  # if Single comments_after > 42.0
         return 0.7777777777777778 # (0.7777777777777778 out of 1.0)
      end     else  # if h2_diff > -51.5
      case when Comments_diff <= 19.0 then
        case when hunks_num <= 26.0 then
          case when Blank_diff <= -19.5 then
             return 0.625 # (0.625 out of 1.0)
          else  # if Blank_diff > -19.5
            case when h2_diff <= -1.5 then
              case when McCabe_sum_diff <= -9.5 then
                case when Single comments_after <= 86.5 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if Single comments_after > 86.5
                   return 0.18181818181818182 # (0.18181818181818182 out of 1.0)
                end               else  # if McCabe_sum_diff > -9.5
                case when LOC_before <= 757.5 then
                   return 0.03571428571428571 # (0.03571428571428571 out of 1.0)
                else  # if LOC_before > 757.5
                  case when Comments_diff <= -0.5 then
                     return 0.3888888888888889 # (0.3888888888888889 out of 1.0)
                  else  # if Comments_diff > -0.5
                     return 0.2727272727272727 # (0.2727272727272727 out of 1.0)
                  end                 end               end             else  # if h2_diff > -1.5
              case when Multi_diff <= -4.5 then
                 return 0.05263157894736842 # (0.05263157894736842 out of 1.0)
              else  # if Multi_diff > -4.5
                case when McCabe_sum_after <= 77.0 then
                  case when Blank_before <= 153.5 then
                    case when hunks_num <= 2.5 then
                      case when avg_coupling_code_size_cut_diff <= -0.24047619849443436 then
                         return 0.5294117647058824 # (0.5294117647058824 out of 1.0)
                      else  # if avg_coupling_code_size_cut_diff > -0.24047619849443436
                         return 0.8947368421052632 # (0.8947368421052632 out of 1.0)
                      end                     else  # if hunks_num > 2.5
                      case when LOC_before <= 214.5 then
                         return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
                      else  # if LOC_before > 214.5
                         return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
                      end                     end                   else  # if Blank_before > 153.5
                     return 0.11764705882352941 # (0.11764705882352941 out of 1.0)
                  end                 else  # if McCabe_sum_after > 77.0
                  case when avg_coupling_code_size_cut_diff <= -0.8125 then
                    case when LOC_before <= 783.0 then
                       return 0.0 # (0.0 out of 1.0)
                    else  # if LOC_before > 783.0
                       return 0.14285714285714285 # (0.14285714285714285 out of 1.0)
                    end                   else  # if avg_coupling_code_size_cut_diff > -0.8125
                    case when McCabe_max_after <= 13.5 then
                       return 0.05555555555555555 # (0.05555555555555555 out of 1.0)
                    else  # if McCabe_max_after > 13.5
                      case when low_ccp_group <= 0.5 then
                        case when removed_lines <= 4.0 then
                           return 0.29411764705882354 # (0.29411764705882354 out of 1.0)
                        else  # if removed_lines > 4.0
                          case when McCabe_sum_after <= 152.5 then
                             return 0.7692307692307693 # (0.7692307692307693 out of 1.0)
                          else  # if McCabe_sum_after > 152.5
                             return 0.6470588235294118 # (0.6470588235294118 out of 1.0)
                          end                         end                       else  # if low_ccp_group > 0.5
                         return 0.2727272727272727 # (0.2727272727272727 out of 1.0)
                      end                     end                   end                 end               end             end           end         else  # if hunks_num > 26.0
           return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
        end       else  # if Comments_diff > 19.0
         return 0.875 # (0.875 out of 1.0)
      end     end   else  # if high_ccp_group > 0.5
    case when changed_lines <= 350.5 then
      case when LLOC_before <= 351.0 then
        case when Blank_before <= 42.5 then
           return 1.0 # (1.0 out of 1.0)
        else  # if Blank_before > 42.5
           return 0.8888888888888888 # (0.8888888888888888 out of 1.0)
        end       else  # if LLOC_before > 351.0
        case when LLOC_before <= 525.0 then
           return 0.4642857142857143 # (0.4642857142857143 out of 1.0)
        else  # if LLOC_before > 525.0
          case when hunks_num <= 3.5 then
             return 1.0 # (1.0 out of 1.0)
          else  # if hunks_num > 3.5
             return 0.7272727272727273 # (0.7272727272727273 out of 1.0)
          end         end       end     else  # if changed_lines > 350.5
       return 0.4090909090909091 # (0.4090909090909091 out of 1.0)
    end   end )