create or replace function RandomForest_3 (McCabe_sum_before int64, changed_lines int64, prev_count_y int64, mostly_delete int64, h1_diff int64, too-many-lines int64, low_McCabe_sum_before int64, length_diff int64, LOC_before int64, simplifiable-if-expression int64, added_functions int64, broad-exception-caught int64, simplifiable-condition int64, prev_count_x int64, McCabe_max_diff int64, SLOC_before int64, LLOC_before int64, low_McCabe_max_diff int64, bugs_diff int64, same_day_duration_avg_diff int64, cur_count_x int64, only_removal int64, McCabe_max_after int64, Single comments_after int64, low_ccp_group int64, one_file_fix_rate_diff int64, effort_diff int64, difficulty_diff int64, removed_lines int64, Comments_diff int64, too-many-boolean-expressions int64, refactor_mle_diff int64, high_McCabe_max_before int64, hunks_num int64, LOC_diff int64, SLOC_diff int64, cur_count_y int64, vocabulary_diff int64, using-constant-test int64, Simplify-boolean-expression int64, low_McCabe_max_before int64, high_McCabe_sum_diff int64, high_McCabe_sum_before int64, McCabe_max_before int64, Comments_after int64, McCabe_sum_diff int64, unnecessary-pass int64, avg_coupling_code_size_cut_diff int64, simplifiable-if-statement int64, is_refactor int64, volume_diff int64, added_lines int64, high_McCabe_max_diff int64, superfluous-parens int64, cur_count int64, low_McCabe_sum_diff int64, calculated_length_diff int64, Multi_diff int64, N2_diff int64, h2_diff int64, Single comments_before int64, McCabe_sum_after int64, N1_diff int64, too-many-statements int64, comparison-of-constants int64, pointless-statement int64, time_diff int64, prev_count int64, Single comments_diff int64, massive_change int64, Blank_diff int64, too-many-nested-blocks int64, Comments_before int64, modified_McCabe_max_diff int64, LLOC_diff int64, Blank_before int64, try-except-raise int64, too-many-branches int64, too-many-return-statements int64, unnecessary-semicolon int64, wildcard-import int64, high_ccp_group int64, line-too-long int64) as (
  case when Comments_before <= 3.5 then
     return 1.0 # (1.0 out of 1.0)
  else  # if Comments_before > 3.5
    case when McCabe_max_after <= 7.5 then
      case when SLOC_before <= 265.0 then
        case when low_McCabe_max_before <= 0.5 then
           return 0.9428571428571428 # (0.9428571428571428 out of 1.0)
        else  # if low_McCabe_max_before > 0.5
          case when LOC_before <= 248.0 then
             return 0.36363636363636365 # (0.36363636363636365 out of 1.0)
          else  # if LOC_before > 248.0
             return 0.7647058823529411 # (0.7647058823529411 out of 1.0)
          end         end       else  # if SLOC_before > 265.0
        case when LOC_before <= 1196.0 then
           return 0.5263157894736842 # (0.5263157894736842 out of 1.0)
        else  # if LOC_before > 1196.0
           return 0.06666666666666667 # (0.06666666666666667 out of 1.0)
        end       end     else  # if McCabe_max_after > 7.5
      case when Single comments_after <= 162.5 then
        case when same_day_duration_avg_diff <= -125.36413955688477 then
          case when avg_coupling_code_size_cut_diff <= -0.0833333358168602 then
             return 0.75 # (0.75 out of 1.0)
          else  # if avg_coupling_code_size_cut_diff > -0.0833333358168602
             return 0.631578947368421 # (0.631578947368421 out of 1.0)
          end         else  # if same_day_duration_avg_diff > -125.36413955688477
          case when SLOC_diff <= -112.0 then
             return 0.5357142857142857 # (0.5357142857142857 out of 1.0)
          else  # if SLOC_diff > -112.0
            case when Single comments_after <= 90.5 then
              case when Comments_diff <= 1.5 then
                case when low_ccp_group <= 0.5 then
                  case when high_ccp_group <= 0.5 then
                    case when refactor_mle_diff <= 0.20730680972337723 then
                      case when added_lines <= 59.5 then
                        case when McCabe_max_after <= 16.5 then
                           return 0.16666666666666666 # (0.16666666666666666 out of 1.0)
                        else  # if McCabe_max_after > 16.5
                           return 0.4583333333333333 # (0.4583333333333333 out of 1.0)
                        end                       else  # if added_lines > 59.5
                        case when McCabe_max_before <= 18.5 then
                           return 0.875 # (0.875 out of 1.0)
                        else  # if McCabe_max_before > 18.5
                           return 0.3 # (0.3 out of 1.0)
                        end                       end                     else  # if refactor_mle_diff > 0.20730680972337723
                       return 0.045454545454545456 # (0.045454545454545456 out of 1.0)
                    end                   else  # if high_ccp_group > 0.5
                    case when modified_McCabe_max_diff <= -1.5 then
                       return 0.782608695652174 # (0.782608695652174 out of 1.0)
                    else  # if modified_McCabe_max_diff > -1.5
                       return 0.5238095238095238 # (0.5238095238095238 out of 1.0)
                    end                   end                 else  # if low_ccp_group > 0.5
                  case when McCabe_max_before <= 14.5 then
                     return 0.13636363636363635 # (0.13636363636363635 out of 1.0)
                  else  # if McCabe_max_before > 14.5
                     return 0.03571428571428571 # (0.03571428571428571 out of 1.0)
                  end                 end               else  # if Comments_diff > 1.5
                case when N1_diff <= 1.5 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if N1_diff > 1.5
                   return 0.14285714285714285 # (0.14285714285714285 out of 1.0)
                end               end             else  # if Single comments_after > 90.5
              case when SLOC_before <= 695.0 then
                case when refactor_mle_diff <= 0.044172514230012894 then
                   return 0.09090909090909091 # (0.09090909090909091 out of 1.0)
                else  # if refactor_mle_diff > 0.044172514230012894
                   return 0.0 # (0.0 out of 1.0)
                end               else  # if SLOC_before > 695.0
                 return 0.21739130434782608 # (0.21739130434782608 out of 1.0)
              end             end           end         end       else  # if Single comments_after > 162.5
        case when Comments_after <= 202.0 then
           return 0.8695652173913043 # (0.8695652173913043 out of 1.0)
        else  # if Comments_after > 202.0
          case when N1_diff <= 0.5 then
            case when hunks_num <= 6.5 then
              case when Comments_before <= 372.5 then
                 return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
              else  # if Comments_before > 372.5
                 return 0.14285714285714285 # (0.14285714285714285 out of 1.0)
              end             else  # if hunks_num > 6.5
               return 0.25 # (0.25 out of 1.0)
            end           else  # if N1_diff > 0.5
             return 0.6774193548387096 # (0.6774193548387096 out of 1.0)
          end         end       end     end   end )