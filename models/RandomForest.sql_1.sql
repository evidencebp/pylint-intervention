create or replace function RandomForest_1 (h1_diff int64, simplifiable-if-statement int64, McCabe_max_after int64, McCabe_sum_before int64, Single comments_before int64, low_McCabe_max_diff int64, high_ccp_group int64, pointless-statement int64, too-many-branches int64, high_McCabe_max_before int64, superfluous-parens int64, Multi_diff int64, wildcard-import int64, high_McCabe_sum_before int64, LLOC_before int64, cur_count int64, unnecessary-semicolon int64, Comments_after int64, mostly_delete int64, simplifiable-condition int64, avg_coupling_code_size_cut_diff int64, added_functions int64, McCabe_max_diff int64, McCabe_sum_diff int64, LLOC_diff int64, LOC_before int64, Comments_diff int64, prev_count_x int64, effort_diff int64, try-except-raise int64, difficulty_diff int64, line-too-long int64, Simplify-boolean-expression int64, SLOC_diff int64, McCabe_sum_after int64, refactor_mle_diff int64, one_file_fix_rate_diff int64, is_refactor int64, too-many-lines int64, too-many-boolean-expressions int64, Single comments_diff int64, low_McCabe_sum_diff int64, cur_count_y int64, comparison-of-constants int64, Comments_before int64, too-many-return-statements int64, vocabulary_diff int64, massive_change int64, hunks_num int64, modified_McCabe_max_diff int64, high_McCabe_sum_diff int64, N2_diff int64, broad-exception-caught int64, length_diff int64, unnecessary-pass int64, time_diff int64, changed_lines int64, Single comments_after int64, h2_diff int64, low_McCabe_sum_before int64, cur_count_x int64, McCabe_max_before int64, using-constant-test int64, added_lines int64, same_day_duration_avg_diff int64, prev_count_y int64, Blank_diff int64, LOC_diff int64, only_removal int64, low_McCabe_max_before int64, bugs_diff int64, too-many-statements int64, simplifiable-if-expression int64, calculated_length_diff int64, volume_diff int64, Blank_before int64, high_McCabe_max_diff int64, SLOC_before int64, too-many-nested-blocks int64, removed_lines int64, low_ccp_group int64, N1_diff int64, prev_count int64) as (
  case when LLOC_before <= 347.0 then
    case when LLOC_diff <= -40.5 then
       return 0.8823529411764706 # (0.8823529411764706 out of 1.0)
    else  # if LLOC_diff > -40.5
      case when McCabe_sum_before <= 28.0 then
        case when Blank_diff <= 0.5 then
          case when added_lines <= 6.5 then
             return 0.9375 # (0.9375 out of 1.0)
          else  # if added_lines > 6.5
             return 0.7 # (0.7 out of 1.0)
          end         else  # if Blank_diff > 0.5
           return 0.7 # (0.7 out of 1.0)
        end       else  # if McCabe_sum_before > 28.0
        case when SLOC_before <= 653.0 then
          case when McCabe_sum_before <= 97.0 then
            case when LLOC_diff <= 7.0 then
              case when changed_lines <= 27.5 then
                case when LOC_before <= 462.5 then
                   return 0.038461538461538464 # (0.038461538461538464 out of 1.0)
                else  # if LOC_before > 462.5
                   return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
                end               else  # if changed_lines > 27.5
                case when N1_diff <= -1.5 then
                   return 0.6 # (0.6 out of 1.0)
                else  # if N1_diff > -1.5
                  case when Single comments_before <= 12.5 then
                     return 0.125 # (0.125 out of 1.0)
                  else  # if Single comments_before > 12.5
                     return 0.6296296296296297 # (0.6296296296296297 out of 1.0)
                  end                 end               end             else  # if LLOC_diff > 7.0
               return 0.13043478260869565 # (0.13043478260869565 out of 1.0)
            end           else  # if McCabe_sum_before > 97.0
             return 0.7692307692307693 # (0.7692307692307693 out of 1.0)
          end         else  # if SLOC_before > 653.0
           return 1.0 # (1.0 out of 1.0)
        end       end     end   else  # if LLOC_before > 347.0
    case when McCabe_max_before <= 25.5 then
      case when high_ccp_group <= 0.5 then
        case when LLOC_before <= 473.5 then
          case when Comments_before <= 57.0 then
            case when Single comments_before <= 23.5 then
               return 0.15384615384615385 # (0.15384615384615385 out of 1.0)
            else  # if Single comments_before > 23.5
               return 0.0 # (0.0 out of 1.0)
            end           else  # if Comments_before > 57.0
             return 0.2962962962962963 # (0.2962962962962963 out of 1.0)
          end         else  # if LLOC_before > 473.5
          case when one_file_fix_rate_diff <= -0.19722222536802292 then
             return 0.7368421052631579 # (0.7368421052631579 out of 1.0)
          else  # if one_file_fix_rate_diff > -0.19722222536802292
            case when added_lines <= 166.0 then
              case when vocabulary_diff <= -0.5 then
                 return 0.12903225806451613 # (0.12903225806451613 out of 1.0)
              else  # if vocabulary_diff > -0.5
                 return 0.3076923076923077 # (0.3076923076923077 out of 1.0)
              end             else  # if added_lines > 166.0
               return 0.75 # (0.75 out of 1.0)
            end           end         end       else  # if high_ccp_group > 0.5
        case when McCabe_sum_before <= 178.0 then
           return 0.3888888888888889 # (0.3888888888888889 out of 1.0)
        else  # if McCabe_sum_before > 178.0
           return 0.9473684210526315 # (0.9473684210526315 out of 1.0)
        end       end     else  # if McCabe_max_before > 25.5
      case when Blank_before <= 540.0 then
        case when Single comments_after <= 49.5 then
          case when Single comments_before <= 40.5 then
             return 0.42105263157894735 # (0.42105263157894735 out of 1.0)
          else  # if Single comments_before > 40.5
             return 0.6 # (0.6 out of 1.0)
          end         else  # if Single comments_after > 49.5
          case when McCabe_sum_before <= 201.0 then
            case when McCabe_max_diff <= -0.5 then
               return 0.08333333333333333 # (0.08333333333333333 out of 1.0)
            else  # if McCabe_max_diff > -0.5
               return 0.0 # (0.0 out of 1.0)
            end           else  # if McCabe_sum_before > 201.0
            case when McCabe_max_before <= 47.5 then
              case when vocabulary_diff <= -0.5 then
                 return 0.4 # (0.4 out of 1.0)
              else  # if vocabulary_diff > -0.5
                 return 0.043478260869565216 # (0.043478260869565216 out of 1.0)
              end             else  # if McCabe_max_before > 47.5
               return 0.5294117647058824 # (0.5294117647058824 out of 1.0)
            end           end         end       else  # if Blank_before > 540.0
         return 0.0 # (0.0 out of 1.0)
      end     end   end )