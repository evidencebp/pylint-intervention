create or replace function RandomForest_9 (effort_diff int64, too-many-nested-blocks int64, Single comments_diff int64, N1_diff int64, avg_coupling_code_size_cut_diff int64, Simplify-boolean-expression int64, try-except-raise int64, h1_diff int64, added_functions int64, too-many-boolean-expressions int64, LLOC_diff int64, cur_count_x int64, wildcard-import int64, mostly_delete int64, LOC_diff int64, difficulty_diff int64, Comments_before int64, prev_count_y int64, time_diff int64, pointless-statement int64, vocabulary_diff int64, modified_McCabe_max_diff int64, prev_count int64, McCabe_sum_before int64, McCabe_max_after int64, Blank_diff int64, using-constant-test int64, McCabe_max_before int64, is_refactor int64, Comments_after int64, SLOC_before int64, superfluous-parens int64, too-many-branches int64, massive_change int64, comparison-of-constants int64, broad-exception-caught int64, Blank_before int64, N2_diff int64, McCabe_sum_after int64, too-many-statements int64, refactor_mle_diff int64, LOC_before int64, simplifiable-if-statement int64, only_removal int64, h2_diff int64, unnecessary-semicolon int64, too-many-lines int64, LLOC_before int64, volume_diff int64, too-many-return-statements int64, high_ccp_group int64, Single comments_before int64, simplifiable-if-expression int64, changed_lines int64, Multi_diff int64, one_file_fix_rate_diff int64, prev_count_x int64, simplifiable-condition int64, cur_count_y int64, calculated_length_diff int64, SLOC_diff int64, line-too-long int64, McCabe_max_diff int64, Comments_diff int64, cur_count int64, Single comments_after int64, removed_lines int64, added_lines int64, length_diff int64, unnecessary-pass int64, hunks_num int64, bugs_diff int64, same_day_duration_avg_diff int64, McCabe_sum_diff int64) as (
  case when Single comments_after <= 58.5 then
    case when changed_lines <= 126.5 then
      case when refactor_mle_diff <= -0.10556042939424515 then
        case when SLOC_diff <= -36.0 then
           return 0.0 # (0.0 out of 19.0)
        else  # if SLOC_diff > -36.0
          case when hunks_num <= 3.5 then
            case when changed_lines <= 22.0 then
               return 0.2916666666666667 # (7.0 out of 24.0)
            else  # if changed_lines > 22.0
               return 0.75 # (12.0 out of 16.0)
            end           else  # if hunks_num > 3.5
             return 0.19230769230769232 # (5.0 out of 26.0)
          end         end       else  # if refactor_mle_diff > -0.10556042939424515
        case when only_removal <= 0.5 then
          case when McCabe_max_after <= 24.0 then
            case when Blank_diff <= -4.5 then
               return 0.8181818181818182 # (18.0 out of 22.0)
            else  # if Blank_diff > -4.5
              case when removed_lines <= 17.5 then
                case when LLOC_diff <= -2.0 then
                   return 0.1875 # (3.0 out of 16.0)
                else  # if LLOC_diff > -2.0
                   return 0.8148148148148148 # (22.0 out of 27.0)
                end               else  # if removed_lines > 17.5
                 return 0.38461538461538464 # (10.0 out of 26.0)
              end             end           else  # if McCabe_max_after > 24.0
             return 0.23076923076923078 # (3.0 out of 13.0)
          end         else  # if only_removal > 0.5
           return 0.7391304347826086 # (17.0 out of 23.0)
        end       end     else  # if changed_lines > 126.5
      case when Single comments_before <= 111.5 then
        case when removed_lines <= 154.5 then
          case when same_day_duration_avg_diff <= -30.263736724853516 then
            case when McCabe_max_diff <= -5.0 then
               return 0.9285714285714286 # (13.0 out of 14.0)
            else  # if McCabe_max_diff > -5.0
               return 0.47619047619047616 # (10.0 out of 21.0)
            end           else  # if same_day_duration_avg_diff > -30.263736724853516
            case when N2_diff <= -4.0 then
              case when SLOC_diff <= -58.0 then
                 return 1.0 # (19.0 out of 19.0)
              else  # if SLOC_diff > -58.0
                 return 0.9285714285714286 # (13.0 out of 14.0)
              end             else  # if N2_diff > -4.0
               return 0.65 # (13.0 out of 20.0)
            end           end         else  # if removed_lines > 154.5
           return 0.36 # (9.0 out of 25.0)
        end       else  # if Single comments_before > 111.5
         return 0.38461538461538464 # (5.0 out of 13.0)
      end     end   else  # if Single comments_after > 58.5
    case when hunks_num <= 3.5 then
      case when h1_diff <= 0.5 then
        case when Single comments_after <= 101.0 then
          case when added_lines <= 18.0 then
             return 0.78125 # (25.0 out of 32.0)
          else  # if added_lines > 18.0
             return 0.4 # (6.0 out of 15.0)
          end         else  # if Single comments_after > 101.0
          case when Blank_before <= 205.0 then
             return 0.0625 # (1.0 out of 16.0)
          else  # if Blank_before > 205.0
             return 0.6071428571428571 # (17.0 out of 28.0)
          end         end       else  # if h1_diff > 0.5
         return 1.0 # (15.0 out of 15.0)
      end     else  # if hunks_num > 3.5
      case when superfluous-parens <= 0.5 then
        case when McCabe_sum_diff <= -28.5 then
           return 0.42857142857142855 # (6.0 out of 14.0)
        else  # if McCabe_sum_diff > -28.5
          case when refactor_mle_diff <= -0.15066488832235336 then
             return 0.3888888888888889 # (7.0 out of 18.0)
          else  # if refactor_mle_diff > -0.15066488832235336
            case when added_lines <= 33.5 then
              case when SLOC_diff <= 4.5 then
                 return 0.25 # (3.0 out of 12.0)
              else  # if SLOC_diff > 4.5
                 return 0.043478260869565216 # (1.0 out of 23.0)
              end             else  # if added_lines > 33.5
              case when McCabe_sum_after <= 166.0 then
                 return 0.0 # (0.0 out of 31.0)
              else  # if McCabe_sum_after > 166.0
                 return 0.1111111111111111 # (2.0 out of 18.0)
              end             end           end         end       else  # if superfluous-parens > 0.5
        case when LOC_before <= 2569.0 then
           return 0.13636363636363635 # (3.0 out of 22.0)
        else  # if LOC_before > 2569.0
           return 0.7222222222222222 # (13.0 out of 18.0)
        end       end     end   end )