create or replace function RandomForest_9 (low_McCabe_max_before int64, LLOC_before int64, low_McCabe_sum_diff int64, modified_McCabe_max_diff int64, bugs_diff int64, McCabe_max_before int64, Single comments_before int64, prev_count_y int64, added_lines int64, LLOC_diff int64, N2_diff int64, added_functions int64, prev_count int64, too-many-boolean-expressions int64, SLOC_diff int64, mostly_delete int64, time_diff int64, calculated_length_diff int64, McCabe_max_after int64, Comments_diff int64, line-too-long int64, McCabe_sum_after int64, one_file_fix_rate_diff int64, h1_diff int64, high_McCabe_max_diff int64, too-many-branches int64, SLOC_before int64, cur_count_y int64, prev_count_x int64, McCabe_sum_before int64, Comments_after int64, wildcard-import int64, unnecessary-semicolon int64, same_day_duration_avg_diff int64, effort_diff int64, too-many-statements int64, broad-exception-caught int64, LOC_before int64, cur_count int64, Comments_before int64, using-constant-test int64, LOC_diff int64, high_McCabe_sum_diff int64, only_removal int64, superfluous-parens int64, try-except-raise int64, Blank_before int64, McCabe_max_diff int64, N1_diff int64, massive_change int64, refactor_mle_diff int64, pointless-statement int64, too-many-lines int64, simplifiable-if-statement int64, high_McCabe_sum_before int64, vocabulary_diff int64, removed_lines int64, difficulty_diff int64, Simplify-boolean-expression int64, avg_coupling_code_size_cut_diff int64, Single comments_after int64, low_ccp_group int64, Multi_diff int64, is_refactor int64, hunks_num int64, Single comments_diff int64, length_diff int64, unnecessary-pass int64, Blank_diff int64, h2_diff int64, changed_lines int64, cur_count_x int64, low_McCabe_max_diff int64, high_McCabe_max_before int64, high_ccp_group int64, too-many-nested-blocks int64, McCabe_sum_diff int64, volume_diff int64, comparison-of-constants int64, too-many-return-statements int64, simplifiable-condition int64, simplifiable-if-expression int64, low_McCabe_sum_before int64) as (
  case when added_lines <= 1.5 then
    case when Blank_before <= 29.5 then
       return 1.0 # (1.0 out of 1.0)
    else  # if Blank_before > 29.5
      case when SLOC_before <= 547.0 then
         return 0.48 # (0.48 out of 1.0)
      else  # if SLOC_before > 547.0
         return 0.7391304347826086 # (0.7391304347826086 out of 1.0)
      end     end   else  # if added_lines > 1.5
    case when McCabe_sum_before <= 70.0 then
      case when Blank_diff <= -6.5 then
        case when Single comments_diff <= -2.5 then
           return 0.8666666666666667 # (0.8666666666666667 out of 1.0)
        else  # if Single comments_diff > -2.5
           return 0.125 # (0.125 out of 1.0)
        end       else  # if Blank_diff > -6.5
        case when too-many-branches <= 0.5 then
          case when avg_coupling_code_size_cut_diff <= 0.09890110045671463 then
            case when Comments_diff <= -2.5 then
               return 0.9285714285714286 # (0.9285714285714286 out of 1.0)
            else  # if Comments_diff > -2.5
              case when line-too-long <= 0.5 then
                 return 0.36 # (0.36 out of 1.0)
              else  # if line-too-long > 0.5
                 return 0.9565217391304348 # (0.9565217391304348 out of 1.0)
              end             end           else  # if avg_coupling_code_size_cut_diff > 0.09890110045671463
             return 0.375 # (0.375 out of 1.0)
          end         else  # if too-many-branches > 0.5
           return 0.9166666666666666 # (0.9166666666666666 out of 1.0)
        end       end     else  # if McCabe_sum_before > 70.0
      case when Multi_diff <= 0.5 then
        case when LOC_diff <= 42.5 then
          case when N1_diff <= 0.5 then
            case when hunks_num <= 11.5 then
              case when removed_lines <= 12.5 then
                case when LLOC_diff <= -23.5 then
                  case when avg_coupling_code_size_cut_diff <= 0.012987012974917889 then
                     return 0.3076923076923077 # (0.3076923076923077 out of 1.0)
                  else  # if avg_coupling_code_size_cut_diff > 0.012987012974917889
                    case when added_lines <= 137.5 then
                       return 0.0 # (0.0 out of 1.0)
                    else  # if added_lines > 137.5
                       return 0.15384615384615385 # (0.15384615384615385 out of 1.0)
                    end                   end                 else  # if LLOC_diff > -23.5
                  case when SLOC_diff <= -3.5 then
                    case when McCabe_sum_after <= 155.0 then
                       return 0.5454545454545454 # (0.5454545454545454 out of 1.0)
                    else  # if McCabe_sum_after > 155.0
                       return 0.8 # (0.8 out of 1.0)
                    end                   else  # if SLOC_diff > -3.5
                    case when Comments_after <= 98.0 then
                       return 0.4117647058823529 # (0.4117647058823529 out of 1.0)
                    else  # if Comments_after > 98.0
                       return 0.15 # (0.15 out of 1.0)
                    end                   end                 end               else  # if removed_lines > 12.5
                case when Multi_diff <= -3.5 then
                  case when LOC_diff <= -214.5 then
                     return 0.9333333333333333 # (0.9333333333333333 out of 1.0)
                  else  # if LOC_diff > -214.5
                     return 0.6923076923076923 # (0.6923076923076923 out of 1.0)
                  end                 else  # if Multi_diff > -3.5
                  case when same_day_duration_avg_diff <= 47.260942459106445 then
                     return 0.3684210526315789 # (0.3684210526315789 out of 1.0)
                  else  # if same_day_duration_avg_diff > 47.260942459106445
                     return 0.16666666666666666 # (0.16666666666666666 out of 1.0)
                  end                 end               end             else  # if hunks_num > 11.5
              case when McCabe_sum_diff <= -0.5 then
                case when Comments_diff <= -3.5 then
                   return 0.2631578947368421 # (0.2631578947368421 out of 1.0)
                else  # if Comments_diff > -3.5
                   return 0.0 # (0.0 out of 1.0)
                end               else  # if McCabe_sum_diff > -0.5
                 return 0.36363636363636365 # (0.36363636363636365 out of 1.0)
              end             end           else  # if N1_diff > 0.5
            case when Blank_before <= 109.0 then
               return 0.375 # (0.375 out of 1.0)
            else  # if Blank_before > 109.0
               return 0.8888888888888888 # (0.8888888888888888 out of 1.0)
            end           end         else  # if LOC_diff > 42.5
           return 0.6153846153846154 # (0.6153846153846154 out of 1.0)
        end       else  # if Multi_diff > 0.5
        case when one_file_fix_rate_diff <= -0.0062500000931322575 then
           return 0.8 # (0.8 out of 1.0)
        else  # if one_file_fix_rate_diff > -0.0062500000931322575
           return 0.4666666666666667 # (0.4666666666666667 out of 1.0)
        end       end     end   end )