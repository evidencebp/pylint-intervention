create or replace function RandomForest_0 (low_McCabe_max_before int64, LLOC_before int64, low_McCabe_sum_diff int64, modified_McCabe_max_diff int64, bugs_diff int64, McCabe_max_before int64, Single comments_before int64, prev_count_y int64, added_lines int64, LLOC_diff int64, N2_diff int64, added_functions int64, prev_count int64, too-many-boolean-expressions int64, SLOC_diff int64, mostly_delete int64, time_diff int64, calculated_length_diff int64, McCabe_max_after int64, Comments_diff int64, line-too-long int64, McCabe_sum_after int64, one_file_fix_rate_diff int64, h1_diff int64, high_McCabe_max_diff int64, too-many-branches int64, SLOC_before int64, cur_count_y int64, prev_count_x int64, McCabe_sum_before int64, Comments_after int64, wildcard-import int64, unnecessary-semicolon int64, same_day_duration_avg_diff int64, effort_diff int64, too-many-statements int64, broad-exception-caught int64, LOC_before int64, cur_count int64, Comments_before int64, using-constant-test int64, LOC_diff int64, high_McCabe_sum_diff int64, only_removal int64, superfluous-parens int64, try-except-raise int64, Blank_before int64, McCabe_max_diff int64, N1_diff int64, massive_change int64, refactor_mle_diff int64, pointless-statement int64, too-many-lines int64, simplifiable-if-statement int64, high_McCabe_sum_before int64, vocabulary_diff int64, removed_lines int64, difficulty_diff int64, Simplify-boolean-expression int64, avg_coupling_code_size_cut_diff int64, Single comments_after int64, low_ccp_group int64, Multi_diff int64, is_refactor int64, hunks_num int64, Single comments_diff int64, length_diff int64, unnecessary-pass int64, Blank_diff int64, h2_diff int64, changed_lines int64, cur_count_x int64, low_McCabe_max_diff int64, high_McCabe_max_before int64, high_ccp_group int64, too-many-nested-blocks int64, McCabe_sum_diff int64, volume_diff int64, comparison-of-constants int64, too-many-return-statements int64, simplifiable-condition int64, simplifiable-if-expression int64, low_McCabe_sum_before int64) as (
  case when too-many-return-statements <= 0.5 then
    case when length_diff <= -9.5 then
      case when removed_lines <= 23.0 then
        case when Blank_before <= 119.5 then
          case when vocabulary_diff <= -25.0 then
             return 0.047619047619047616 # (0.047619047619047616 out of 1.0)
          else  # if vocabulary_diff > -25.0
             return 0.17647058823529413 # (0.17647058823529413 out of 1.0)
          end         else  # if Blank_before > 119.5
          case when LOC_diff <= -366.5 then
             return 0.1875 # (0.1875 out of 1.0)
          else  # if LOC_diff > -366.5
            case when added_lines <= 68.0 then
               return 0.3 # (0.3 out of 1.0)
            else  # if added_lines > 68.0
               return 0.6875 # (0.6875 out of 1.0)
            end           end         end       else  # if removed_lines > 23.0
        case when McCabe_sum_after <= 64.5 then
           return 0.8823529411764706 # (0.8823529411764706 out of 1.0)
        else  # if McCabe_sum_after > 64.5
          case when McCabe_max_before <= 18.5 then
             return 0.8095238095238095 # (0.8095238095238095 out of 1.0)
          else  # if McCabe_max_before > 18.5
            case when Comments_diff <= -3.5 then
               return 0.5555555555555556 # (0.5555555555555556 out of 1.0)
            else  # if Comments_diff > -3.5
               return 0.043478260869565216 # (0.043478260869565216 out of 1.0)
            end           end         end       end     else  # if length_diff > -9.5
      case when low_ccp_group <= 0.5 then
        case when avg_coupling_code_size_cut_diff <= 0.5691087245941162 then
          case when N1_diff <= 6.5 then
            case when one_file_fix_rate_diff <= 0.45000000298023224 then
              case when high_McCabe_sum_before <= 0.5 then
                case when Comments_diff <= -2.5 then
                   return 0.85 # (0.85 out of 1.0)
                else  # if Comments_diff > -2.5
                  case when avg_coupling_code_size_cut_diff <= -0.42499999701976776 then
                    case when Comments_after <= 35.5 then
                       return 0.6538461538461539 # (0.6538461538461539 out of 1.0)
                    else  # if Comments_after > 35.5
                       return 0.2631578947368421 # (0.2631578947368421 out of 1.0)
                    end                   else  # if avg_coupling_code_size_cut_diff > -0.42499999701976776
                    case when hunks_num <= 9.0 then
                      case when N1_diff <= -0.5 then
                         return 0.8235294117647058 # (0.8235294117647058 out of 1.0)
                      else  # if N1_diff > -0.5
                        case when Single comments_before <= 37.5 then
                          case when Single comments_after <= 3.5 then
                             return 0.6923076923076923 # (0.6923076923076923 out of 1.0)
                          else  # if Single comments_after > 3.5
                             return 0.47368421052631576 # (0.47368421052631576 out of 1.0)
                          end                         else  # if Single comments_before > 37.5
                           return 0.8 # (0.8 out of 1.0)
                        end                       end                     else  # if hunks_num > 9.0
                       return 0.9130434782608695 # (0.9130434782608695 out of 1.0)
                    end                   end                 end               else  # if high_McCabe_sum_before > 0.5
                case when McCabe_sum_after <= 360.5 then
                   return 0.7 # (0.7 out of 1.0)
                else  # if McCabe_sum_after > 360.5
                   return 0.9629629629629629 # (0.9629629629629629 out of 1.0)
                end               end             else  # if one_file_fix_rate_diff > 0.45000000298023224
               return 1.0 # (1.0 out of 1.0)
            end           else  # if N1_diff > 6.5
             return 0.26666666666666666 # (0.26666666666666666 out of 1.0)
          end         else  # if avg_coupling_code_size_cut_diff > 0.5691087245941162
          case when changed_lines <= 48.5 then
            case when removed_lines <= 2.5 then
               return 0.5517241379310345 # (0.5517241379310345 out of 1.0)
            else  # if removed_lines > 2.5
               return 0.23529411764705882 # (0.23529411764705882 out of 1.0)
            end           else  # if changed_lines > 48.5
             return 0.7586206896551724 # (0.7586206896551724 out of 1.0)
          end         end       else  # if low_ccp_group > 0.5
        case when Comments_before <= 246.0 then
          case when changed_lines <= 22.5 then
             return 0.2222222222222222 # (0.2222222222222222 out of 1.0)
          else  # if changed_lines > 22.5
            case when LOC_diff <= 10.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if LOC_diff > 10.5
               return 0.06666666666666667 # (0.06666666666666667 out of 1.0)
            end           end         else  # if Comments_before > 246.0
           return 0.8461538461538461 # (0.8461538461538461 out of 1.0)
        end       end     end   else  # if too-many-return-statements > 0.5
    case when changed_lines <= 87.0 then
       return 0.2857142857142857 # (0.2857142857142857 out of 1.0)
    else  # if changed_lines > 87.0
       return 0.05555555555555555 # (0.05555555555555555 out of 1.0)
    end   end )