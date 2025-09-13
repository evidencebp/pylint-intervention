create or replace function RandomForest_4 (prev_count int64, simplifiable-if-expression int64, N1_diff int64, cur_count int64, wildcard-import int64, too-many-return-statements int64, low_McCabe_max_diff int64, length_diff int64, volume_diff int64, high_McCabe_sum_diff int64, high_McCabe_max_before int64, simplifiable-condition int64, Blank_before int64, high_ccp_group int64, McCabe_max_before int64, bugs_diff int64, too-many-nested-blocks int64, refactor_mle_diff int64, difficulty_diff int64, LLOC_diff int64, LOC_diff int64, simplifiable-if-statement int64, one_file_fix_rate_diff int64, SLOC_before int64, LOC_before int64, mostly_delete int64, changed_lines int64, Single comments_before int64, removed_lines int64, added_functions int64, h1_diff int64, effort_diff int64, hunks_num int64, Multi_diff int64, same_day_duration_avg_diff int64, N2_diff int64, cur_count_y int64, Comments_diff int64, modified_McCabe_max_diff int64, h2_diff int64, time_diff int64, LLOC_before int64, calculated_length_diff int64, Single comments_after int64, massive_change int64, McCabe_sum_before int64, too-many-boolean-expressions int64, Simplify-boolean-expression int64, line-too-long int64, superfluous-parens int64, low_ccp_group int64, McCabe_max_diff int64, comparison-of-constants int64, high_McCabe_sum_before int64, low_McCabe_sum_diff int64, avg_coupling_code_size_cut_diff int64, is_refactor int64, Single comments_diff int64, unnecessary-semicolon int64, added_lines int64, prev_count_y int64, try-except-raise int64, low_McCabe_sum_before int64, vocabulary_diff int64, too-many-branches int64, McCabe_sum_after int64, broad-exception-caught int64, prev_count_x int64, only_removal int64, McCabe_max_after int64, pointless-statement int64, low_McCabe_max_before int64, too-many-lines int64, McCabe_sum_diff int64, high_McCabe_max_diff int64, using-constant-test int64, SLOC_diff int64, Blank_diff int64, Comments_after int64, cur_count_x int64, unnecessary-pass int64, too-many-statements int64, Comments_before int64) as (
  case when Single comments_before <= 4.5 then
    case when Comments_before <= 3.5 then
       return 0.8484848484848485 # (0.8484848484848485 out of 1.0)
    else  # if Comments_before > 3.5
       return 0.5714285714285714 # (0.5714285714285714 out of 1.0)
    end   else  # if Single comments_before > 4.5
    case when added_functions <= 8.0 then
      case when too-many-return-statements <= 0.5 then
        case when refactor_mle_diff <= -0.1299530267715454 then
          case when removed_lines <= 8.0 then
            case when length_diff <= -4.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if length_diff > -4.5
              case when Single comments_after <= 38.5 then
                 return 0.4 # (0.4 out of 1.0)
              else  # if Single comments_after > 38.5
                 return 0.2 # (0.2 out of 1.0)
              end             end           else  # if removed_lines > 8.0
            case when Blank_before <= 229.0 then
              case when Comments_diff <= 1.5 then
                case when McCabe_sum_after <= 104.5 then
                  case when hunks_num <= 4.5 then
                     return 0.6875 # (0.6875 out of 1.0)
                  else  # if hunks_num > 4.5
                     return 0.17391304347826086 # (0.17391304347826086 out of 1.0)
                  end                 else  # if McCabe_sum_after > 104.5
                   return 0.6842105263157895 # (0.6842105263157895 out of 1.0)
                end               else  # if Comments_diff > 1.5
                 return 0.13333333333333333 # (0.13333333333333333 out of 1.0)
              end             else  # if Blank_before > 229.0
               return 0.8076923076923077 # (0.8076923076923077 out of 1.0)
            end           end         else  # if refactor_mle_diff > -0.1299530267715454
          case when SLOC_diff <= 35.0 then
            case when Single comments_after <= 50.5 then
              case when modified_McCabe_max_diff <= -7.5 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if modified_McCabe_max_diff > -7.5
                case when removed_lines <= 51.5 then
                  case when N1_diff <= -11.5 then
                     return 0.34782608695652173 # (0.34782608695652173 out of 1.0)
                  else  # if N1_diff > -11.5
                    case when McCabe_max_after <= 9.5 then
                       return 0.8387096774193549 # (0.8387096774193549 out of 1.0)
                    else  # if McCabe_max_after > 9.5
                      case when McCabe_max_after <= 18.5 then
                         return 0.21739130434782608 # (0.21739130434782608 out of 1.0)
                      else  # if McCabe_max_after > 18.5
                         return 0.7647058823529411 # (0.7647058823529411 out of 1.0)
                      end                     end                   end                 else  # if removed_lines > 51.5
                   return 0.34782608695652173 # (0.34782608695652173 out of 1.0)
                end               end             else  # if Single comments_after > 50.5
              case when LOC_diff <= 8.5 then
                case when SLOC_before <= 884.0 then
                  case when LOC_diff <= -25.5 then
                     return 0.47058823529411764 # (0.47058823529411764 out of 1.0)
                  else  # if LOC_diff > -25.5
                    case when refactor_mle_diff <= 0.14623214304447174 then
                       return 0.04 # (0.04 out of 1.0)
                    else  # if refactor_mle_diff > 0.14623214304447174
                       return 0.2413793103448276 # (0.2413793103448276 out of 1.0)
                    end                   end                 else  # if SLOC_before > 884.0
                  case when same_day_duration_avg_diff <= -9.363636255264282 then
                     return 0.84 # (0.84 out of 1.0)
                  else  # if same_day_duration_avg_diff > -9.363636255264282
                    case when Comments_after <= 203.5 then
                       return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
                    else  # if Comments_after > 203.5
                       return 0.3888888888888889 # (0.3888888888888889 out of 1.0)
                    end                   end                 end               else  # if LOC_diff > 8.5
                 return 0.047619047619047616 # (0.047619047619047616 out of 1.0)
              end             end           else  # if SLOC_diff > 35.0
            case when Comments_before <= 83.5 then
               return 0.8571428571428571 # (0.8571428571428571 out of 1.0)
            else  # if Comments_before > 83.5
               return 1.0 # (1.0 out of 1.0)
            end           end         end       else  # if too-many-return-statements > 0.5
         return 0.045454545454545456 # (0.045454545454545456 out of 1.0)
      end     else  # if added_functions > 8.0
       return 0.0 # (0.0 out of 1.0)
    end   end )