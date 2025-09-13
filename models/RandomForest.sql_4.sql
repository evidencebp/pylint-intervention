create or replace function RandomForest_4 (h1_diff int64, SLOC_before int64, avg_coupling_code_size_cut_diff int64, Multi_diff int64, using-constant-test int64, high_McCabe_sum_diff int64, difficulty_diff int64, LLOC_diff int64, length_diff int64, Comments_after int64, McCabe_max_before int64, low_McCabe_sum_before int64, cur_count int64, LOC_before int64, low_McCabe_max_before int64, massive_change int64, too-many-return-statements int64, Comments_diff int64, added_lines int64, broad-exception-caught int64, comparison-of-constants int64, Single comments_diff int64, refactor_mle_diff int64, prev_count_x int64, McCabe_sum_before int64, modified_McCabe_max_diff int64, Simplify-boolean-expression int64, Blank_diff int64, added_functions int64, LLOC_before int64, cur_count_x int64, high_McCabe_sum_before int64, volume_diff int64, low_McCabe_max_diff int64, LOC_diff int64, calculated_length_diff int64, changed_lines int64, N2_diff int64, h2_diff int64, too-many-lines int64, unnecessary-pass int64, simplifiable-if-statement int64, prev_count int64, too-many-nested-blocks int64, Comments_before int64, SLOC_diff int64, McCabe_sum_after int64, bugs_diff int64, cur_count_y int64, Single comments_after int64, McCabe_max_diff int64, N1_diff int64, wildcard-import int64, McCabe_sum_diff int64, prev_count_y int64, superfluous-parens int64, hunks_num int64, try-except-raise int64, simplifiable-if-expression int64, McCabe_max_after int64, high_McCabe_max_diff int64, too-many-statements int64, simplifiable-condition int64, only_removal int64, unnecessary-semicolon int64, effort_diff int64, is_refactor int64, same_day_duration_avg_diff int64, one_file_fix_rate_diff int64, high_McCabe_max_before int64, vocabulary_diff int64, too-many-branches int64, mostly_delete int64, high_ccp_group int64, low_ccp_group int64, removed_lines int64, Single comments_before int64, low_McCabe_sum_diff int64, time_diff int64, Blank_before int64, line-too-long int64, too-many-boolean-expressions int64, pointless-statement int64) as (
  case when LOC_before <= 1032.5 then
    case when McCabe_sum_diff <= -14.5 then
      case when h1_diff <= -1.5 then
         return 0.5 # (0.5 out of 1.0)
      else  # if h1_diff > -1.5
        case when SLOC_diff <= -57.0 then
           return 0.0625 # (0.0625 out of 1.0)
        else  # if SLOC_diff > -57.0
           return 0.0 # (0.0 out of 1.0)
        end       end     else  # if McCabe_sum_diff > -14.5
      case when refactor_mle_diff <= -0.5393025577068329 then
         return 1.0 # (1.0 out of 1.0)
      else  # if refactor_mle_diff > -0.5393025577068329
        case when Comments_before <= 48.5 then
          case when Blank_before <= 16.0 then
             return 0.9411764705882353 # (0.9411764705882353 out of 1.0)
          else  # if Blank_before > 16.0
            case when Single comments_after <= 12.5 then
              case when same_day_duration_avg_diff <= 3.0089285373687744 then
                 return 0.631578947368421 # (0.631578947368421 out of 1.0)
              else  # if same_day_duration_avg_diff > 3.0089285373687744
                 return 0.18518518518518517 # (0.18518518518518517 out of 1.0)
              end             else  # if Single comments_after > 12.5
              case when removed_lines <= 34.0 then
                case when one_file_fix_rate_diff <= 0.0714285746216774 then
                  case when McCabe_sum_after <= 40.5 then
                     return 0.3076923076923077 # (0.3076923076923077 out of 1.0)
                  else  # if McCabe_sum_after > 40.5
                    case when Comments_before <= 34.0 then
                       return 0.5 # (0.5 out of 1.0)
                    else  # if Comments_before > 34.0
                       return 0.7894736842105263 # (0.7894736842105263 out of 1.0)
                    end                   end                 else  # if one_file_fix_rate_diff > 0.0714285746216774
                   return 0.7916666666666666 # (0.7916666666666666 out of 1.0)
                end               else  # if removed_lines > 34.0
                case when vocabulary_diff <= 1.0 then
                  case when SLOC_diff <= 6.5 then
                     return 0.1875 # (0.1875 out of 1.0)
                  else  # if SLOC_diff > 6.5
                     return 0.4117647058823529 # (0.4117647058823529 out of 1.0)
                  end                 else  # if vocabulary_diff > 1.0
                   return 0.6428571428571429 # (0.6428571428571429 out of 1.0)
                end               end             end           end         else  # if Comments_before > 48.5
          case when McCabe_max_after <= 27.0 then
            case when McCabe_sum_before <= 145.5 then
               return 0.047619047619047616 # (0.047619047619047616 out of 1.0)
            else  # if McCabe_sum_before > 145.5
               return 0.5 # (0.5 out of 1.0)
            end           else  # if McCabe_max_after > 27.0
             return 0.5 # (0.5 out of 1.0)
          end         end       end     end   else  # if LOC_before > 1032.5
    case when refactor_mle_diff <= -0.22133412212133408 then
      case when McCabe_sum_before <= 383.0 then
         return 1.0 # (1.0 out of 1.0)
      else  # if McCabe_sum_before > 383.0
         return 0.75 # (0.75 out of 1.0)
      end     else  # if refactor_mle_diff > -0.22133412212133408
      case when one_file_fix_rate_diff <= 0.06969697028398514 then
        case when Blank_before <= 143.0 then
           return 0.8611111111111112 # (0.8611111111111112 out of 1.0)
        else  # if Blank_before > 143.0
          case when avg_coupling_code_size_cut_diff <= 0.6157604455947876 then
            case when changed_lines <= 351.0 then
              case when hunks_num <= 6.5 then
                case when changed_lines <= 25.0 then
                   return 0.8125 # (0.8125 out of 1.0)
                else  # if changed_lines > 25.0
                   return 0.8461538461538461 # (0.8461538461538461 out of 1.0)
                end               else  # if hunks_num > 6.5
                case when SLOC_before <= 689.5 then
                   return 0.06666666666666667 # (0.06666666666666667 out of 1.0)
                else  # if SLOC_before > 689.5
                   return 0.25 # (0.25 out of 1.0)
                end               end             else  # if changed_lines > 351.0
               return 0.8888888888888888 # (0.8888888888888888 out of 1.0)
            end           else  # if avg_coupling_code_size_cut_diff > 0.6157604455947876
            case when Single comments_diff <= -0.5 then
               return 0.07692307692307693 # (0.07692307692307693 out of 1.0)
            else  # if Single comments_diff > -0.5
               return 0.4583333333333333 # (0.4583333333333333 out of 1.0)
            end           end         end       else  # if one_file_fix_rate_diff > 0.06969697028398514
        case when N2_diff <= -5.0 then
           return 0.09090909090909091 # (0.09090909090909091 out of 1.0)
        else  # if N2_diff > -5.0
          case when removed_lines <= 8.0 then
             return 0.5714285714285714 # (0.5714285714285714 out of 1.0)
          else  # if removed_lines > 8.0
             return 0.3548387096774194 # (0.3548387096774194 out of 1.0)
          end         end       end     end   end )