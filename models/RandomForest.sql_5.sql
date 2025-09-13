create or replace function RandomForest_5 (h1_diff int64, SLOC_before int64, avg_coupling_code_size_cut_diff int64, Multi_diff int64, using-constant-test int64, high_McCabe_sum_diff int64, difficulty_diff int64, LLOC_diff int64, length_diff int64, Comments_after int64, McCabe_max_before int64, low_McCabe_sum_before int64, cur_count int64, LOC_before int64, low_McCabe_max_before int64, massive_change int64, too-many-return-statements int64, Comments_diff int64, added_lines int64, broad-exception-caught int64, comparison-of-constants int64, Single comments_diff int64, refactor_mle_diff int64, prev_count_x int64, McCabe_sum_before int64, modified_McCabe_max_diff int64, Simplify-boolean-expression int64, Blank_diff int64, added_functions int64, LLOC_before int64, cur_count_x int64, high_McCabe_sum_before int64, volume_diff int64, low_McCabe_max_diff int64, LOC_diff int64, calculated_length_diff int64, changed_lines int64, N2_diff int64, h2_diff int64, too-many-lines int64, unnecessary-pass int64, simplifiable-if-statement int64, prev_count int64, too-many-nested-blocks int64, Comments_before int64, SLOC_diff int64, McCabe_sum_after int64, bugs_diff int64, cur_count_y int64, Single comments_after int64, McCabe_max_diff int64, N1_diff int64, wildcard-import int64, McCabe_sum_diff int64, prev_count_y int64, superfluous-parens int64, hunks_num int64, try-except-raise int64, simplifiable-if-expression int64, McCabe_max_after int64, high_McCabe_max_diff int64, too-many-statements int64, simplifiable-condition int64, only_removal int64, unnecessary-semicolon int64, effort_diff int64, is_refactor int64, same_day_duration_avg_diff int64, one_file_fix_rate_diff int64, high_McCabe_max_before int64, vocabulary_diff int64, too-many-branches int64, mostly_delete int64, high_ccp_group int64, low_ccp_group int64, removed_lines int64, Single comments_before int64, low_McCabe_sum_diff int64, time_diff int64, Blank_before int64, line-too-long int64, too-many-boolean-expressions int64, pointless-statement int64) as (
  case when Single comments_after <= 2.5 then
     return 0.8888888888888888 # (0.8888888888888888 out of 1.0)
  else  # if Single comments_after > 2.5
    case when N1_diff <= -40.0 then
      case when avg_coupling_code_size_cut_diff <= 0.5214285850524902 then
        case when vocabulary_diff <= -81.5 then
           return 0.7142857142857143 # (0.7142857142857143 out of 1.0)
        else  # if vocabulary_diff > -81.5
           return 0.875 # (0.875 out of 1.0)
        end       else  # if avg_coupling_code_size_cut_diff > 0.5214285850524902
         return 0.35294117647058826 # (0.35294117647058826 out of 1.0)
      end     else  # if N1_diff > -40.0
      case when Multi_diff <= -33.5 then
         return 0.9 # (0.9 out of 1.0)
      else  # if Multi_diff > -33.5
        case when high_ccp_group <= 0.5 then
          case when N2_diff <= -19.5 then
            case when Blank_before <= 203.5 then
              case when McCabe_max_diff <= -6.5 then
                 return 0.058823529411764705 # (0.058823529411764705 out of 1.0)
              else  # if McCabe_max_diff > -6.5
                 return 0.0 # (0.0 out of 1.0)
              end             else  # if Blank_before > 203.5
               return 0.42857142857142855 # (0.42857142857142855 out of 1.0)
            end           else  # if N2_diff > -19.5
            case when length_diff <= -8.5 then
              case when SLOC_diff <= -13.5 then
                 return 0.5 # (0.5 out of 1.0)
              else  # if SLOC_diff > -13.5
                 return 0.7142857142857143 # (0.7142857142857143 out of 1.0)
              end             else  # if length_diff > -8.5
              case when Comments_before <= 246.5 then
                case when low_ccp_group <= 0.5 then
                  case when same_day_duration_avg_diff <= -113.59166717529297 then
                     return 0.7 # (0.7 out of 1.0)
                  else  # if same_day_duration_avg_diff > -113.59166717529297
                    case when LLOC_diff <= -6.5 then
                       return 0.6153846153846154 # (0.6153846153846154 out of 1.0)
                    else  # if LLOC_diff > -6.5
                      case when removed_lines <= 78.0 then
                        case when LLOC_diff <= 1.5 then
                          case when Comments_after <= 24.5 then
                             return 0.4782608695652174 # (0.4782608695652174 out of 1.0)
                          else  # if Comments_after > 24.5
                            case when same_day_duration_avg_diff <= -10.207798957824707 then
                               return 0.1111111111111111 # (0.1111111111111111 out of 1.0)
                            else  # if same_day_duration_avg_diff > -10.207798957824707
                              case when removed_lines <= 2.5 then
                                 return 0.10526315789473684 # (0.10526315789473684 out of 1.0)
                              else  # if removed_lines > 2.5
                                 return 0.5 # (0.5 out of 1.0)
                              end                             end                           end                         else  # if LLOC_diff > 1.5
                           return 0.0 # (0.0 out of 1.0)
                        end                       else  # if removed_lines > 78.0
                         return 0.5714285714285714 # (0.5714285714285714 out of 1.0)
                      end                     end                   end                 else  # if low_ccp_group > 0.5
                  case when SLOC_before <= 648.5 then
                    case when changed_lines <= 21.5 then
                       return 0.16666666666666666 # (0.16666666666666666 out of 1.0)
                    else  # if changed_lines > 21.5
                       return 0.0 # (0.0 out of 1.0)
                    end                   else  # if SLOC_before > 648.5
                     return 0.4117647058823529 # (0.4117647058823529 out of 1.0)
                  end                 end               else  # if Comments_before > 246.5
                case when added_functions <= 0.5 then
                   return 0.4782608695652174 # (0.4782608695652174 out of 1.0)
                else  # if added_functions > 0.5
                   return 0.875 # (0.875 out of 1.0)
                end               end             end           end         else  # if high_ccp_group > 0.5
          case when LLOC_before <= 356.0 then
            case when LOC_before <= 254.5 then
               return 0.8 # (0.8 out of 1.0)
            else  # if LOC_before > 254.5
               return 1.0 # (1.0 out of 1.0)
            end           else  # if LLOC_before > 356.0
            case when Single comments_diff <= -0.5 then
               return 0.7307692307692307 # (0.7307692307692307 out of 1.0)
            else  # if Single comments_diff > -0.5
              case when LLOC_before <= 525.0 then
                 return 0.14814814814814814 # (0.14814814814814814 out of 1.0)
              else  # if LLOC_before > 525.0
                 return 0.8 # (0.8 out of 1.0)
              end             end           end         end       end     end   end )