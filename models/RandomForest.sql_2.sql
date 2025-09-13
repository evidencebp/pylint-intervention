create or replace function RandomForest_2 (McCabe_sum_before int64, changed_lines int64, prev_count_y int64, mostly_delete int64, h1_diff int64, too-many-lines int64, low_McCabe_sum_before int64, length_diff int64, LOC_before int64, simplifiable-if-expression int64, added_functions int64, broad-exception-caught int64, simplifiable-condition int64, prev_count_x int64, McCabe_max_diff int64, SLOC_before int64, LLOC_before int64, low_McCabe_max_diff int64, bugs_diff int64, same_day_duration_avg_diff int64, cur_count_x int64, only_removal int64, McCabe_max_after int64, Single comments_after int64, low_ccp_group int64, one_file_fix_rate_diff int64, effort_diff int64, difficulty_diff int64, removed_lines int64, Comments_diff int64, too-many-boolean-expressions int64, refactor_mle_diff int64, high_McCabe_max_before int64, hunks_num int64, LOC_diff int64, SLOC_diff int64, cur_count_y int64, vocabulary_diff int64, using-constant-test int64, Simplify-boolean-expression int64, low_McCabe_max_before int64, high_McCabe_sum_diff int64, high_McCabe_sum_before int64, McCabe_max_before int64, Comments_after int64, McCabe_sum_diff int64, unnecessary-pass int64, avg_coupling_code_size_cut_diff int64, simplifiable-if-statement int64, is_refactor int64, volume_diff int64, added_lines int64, high_McCabe_max_diff int64, superfluous-parens int64, cur_count int64, low_McCabe_sum_diff int64, calculated_length_diff int64, Multi_diff int64, N2_diff int64, h2_diff int64, Single comments_before int64, McCabe_sum_after int64, N1_diff int64, too-many-statements int64, comparison-of-constants int64, pointless-statement int64, time_diff int64, prev_count int64, Single comments_diff int64, massive_change int64, Blank_diff int64, too-many-nested-blocks int64, Comments_before int64, modified_McCabe_max_diff int64, LLOC_diff int64, Blank_before int64, try-except-raise int64, too-many-branches int64, too-many-return-statements int64, unnecessary-semicolon int64, wildcard-import int64, high_ccp_group int64, line-too-long int64) as (
  case when LLOC_before <= 39.5 then
     return 1.0 # (1.0 out of 1.0)
  else  # if LLOC_before > 39.5
    case when McCabe_sum_diff <= -36.0 then
      case when Multi_diff <= -3.5 then
         return 0.8275862068965517 # (0.8275862068965517 out of 1.0)
      else  # if Multi_diff > -3.5
         return 0.375 # (0.375 out of 1.0)
      end     else  # if McCabe_sum_diff > -36.0
      case when high_ccp_group <= 0.5 then
        case when Multi_diff <= -25.5 then
           return 0.6521739130434783 # (0.6521739130434783 out of 1.0)
        else  # if Multi_diff > -25.5
          case when changed_lines <= 138.5 then
            case when length_diff <= -2.5 then
              case when same_day_duration_avg_diff <= 5.4001624584198 then
                case when McCabe_max_after <= 23.5 then
                  case when refactor_mle_diff <= -0.181977778673172 then
                     return 0.2777777777777778 # (0.2777777777777778 out of 1.0)
                  else  # if refactor_mle_diff > -0.181977778673172
                     return 0.0 # (0.0 out of 1.0)
                  end                 else  # if McCabe_max_after > 23.5
                   return 0.4117647058823529 # (0.4117647058823529 out of 1.0)
                end               else  # if same_day_duration_avg_diff > 5.4001624584198
                case when Single comments_before <= 66.5 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if Single comments_before > 66.5
                   return 0.15789473684210525 # (0.15789473684210525 out of 1.0)
                end               end             else  # if length_diff > -2.5
              case when Single comments_before <= 438.0 then
                case when Blank_diff <= -0.5 then
                   return 0.5142857142857142 # (0.5142857142857142 out of 1.0)
                else  # if Blank_diff > -0.5
                  case when changed_lines <= 32.0 then
                    case when Comments_after <= 23.0 then
                       return 0.48 # (0.48 out of 1.0)
                    else  # if Comments_after > 23.0
                      case when same_day_duration_avg_diff <= -34.166666984558105 then
                         return 0.10526315789473684 # (0.10526315789473684 out of 1.0)
                      else  # if same_day_duration_avg_diff > -34.166666984558105
                        case when same_day_duration_avg_diff <= 14.382739067077637 then
                           return 0.47368421052631576 # (0.47368421052631576 out of 1.0)
                        else  # if same_day_duration_avg_diff > 14.382739067077637
                           return 0.23076923076923078 # (0.23076923076923078 out of 1.0)
                        end                       end                     end                   else  # if changed_lines > 32.0
                    case when LOC_diff <= 24.5 then
                      case when McCabe_max_before <= 27.5 then
                         return 0.0 # (0.0 out of 1.0)
                      else  # if McCabe_max_before > 27.5
                         return 0.06666666666666667 # (0.06666666666666667 out of 1.0)
                      end                     else  # if LOC_diff > 24.5
                       return 0.17647058823529413 # (0.17647058823529413 out of 1.0)
                    end                   end                 end               else  # if Single comments_before > 438.0
                 return 0.75 # (0.75 out of 1.0)
              end             end           else  # if changed_lines > 138.5
            case when h2_diff <= 2.5 then
              case when N1_diff <= -1.5 then
                 return 0.47619047619047616 # (0.47619047619047616 out of 1.0)
              else  # if N1_diff > -1.5
                 return 0.8421052631578947 # (0.8421052631578947 out of 1.0)
              end             else  # if h2_diff > 2.5
               return 0.17647058823529413 # (0.17647058823529413 out of 1.0)
            end           end         end       else  # if high_ccp_group > 0.5
        case when Blank_diff <= -5.0 then
           return 0.2777777777777778 # (0.2777777777777778 out of 1.0)
        else  # if Blank_diff > -5.0
          case when modified_McCabe_max_diff <= -0.5 then
            case when added_lines <= 40.0 then
               return 0.7647058823529411 # (0.7647058823529411 out of 1.0)
            else  # if added_lines > 40.0
               return 0.9545454545454546 # (0.9545454545454546 out of 1.0)
            end           else  # if modified_McCabe_max_diff > -0.5
            case when one_file_fix_rate_diff <= 0.36666667461395264 then
              case when LOC_before <= 952.0 then
                 return 0.42857142857142855 # (0.42857142857142855 out of 1.0)
              else  # if LOC_before > 952.0
                 return 0.9130434782608695 # (0.9130434782608695 out of 1.0)
              end             else  # if one_file_fix_rate_diff > 0.36666667461395264
               return 0.25 # (0.25 out of 1.0)
            end           end         end       end     end   end )