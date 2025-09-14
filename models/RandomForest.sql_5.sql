create or replace function RandomForest_5 (prev_count int64, prev_count_x int64, prev_count_y int64, using-constant-test int64, Comments_diff int64, massive_change int64, McCabe_max_after int64, Comments_before int64, too-many-statements int64, cur_count_x int64, h1_diff int64, McCabe_sum_diff int64, LLOC_before int64, McCabe_sum_before int64, high_McCabe_max_before int64, avg_coupling_code_size_cut_diff int64, is_refactor int64, N2_diff int64, too-many-branches int64, SLOC_before int64, too-many-nested-blocks int64, too-many-lines int64, bugs_diff int64, time_diff int64, Single comments_after int64, simplifiable-condition int64, Multi_diff int64, high_McCabe_sum_before int64, low_ccp_group int64, refactor_mle_diff int64, low_McCabe_max_diff int64, SLOC_diff int64, changed_lines int64, hunks_num int64, McCabe_sum_after int64, cur_count_y int64, one_file_fix_rate_diff int64, low_McCabe_sum_before int64, modified_McCabe_max_diff int64, superfluous-parens int64, mostly_delete int64, added_functions int64, Comments_after int64, N1_diff int64, McCabe_max_diff int64, simplifiable-if-statement int64, LOC_before int64, low_McCabe_max_before int64, McCabe_max_before int64, try-except-raise int64, line-too-long int64, unnecessary-semicolon int64, wildcard-import int64, difficulty_diff int64, Simplify-boolean-expression int64, cur_count int64, low_McCabe_sum_diff int64, pointless-statement int64, length_diff int64, broad-exception-caught int64, h2_diff int64, high_McCabe_sum_diff int64, only_removal int64, comparison-of-constants int64, Single comments_diff int64, too-many-boolean-expressions int64, Blank_before int64, calculated_length_diff int64, Single comments_before int64, removed_lines int64, simplifiable-if-expression int64, LOC_diff int64, volume_diff int64, high_McCabe_max_diff int64, high_ccp_group int64, same_day_duration_avg_diff int64, Blank_diff int64, effort_diff int64, too-many-return-statements int64, added_lines int64, unnecessary-pass int64, vocabulary_diff int64, LLOC_diff int64) as (
  case when avg_coupling_code_size_cut_diff <= -1.1597222089767456 then
    case when McCabe_max_before <= 13.5 then
       return 0.6363636363636364 # (0.6363636363636364 out of 1.0)
    else  # if McCabe_max_before > 13.5
      case when McCabe_sum_before <= 217.0 then
        case when Comments_diff <= -1.5 then
           return 0.5714285714285714 # (0.5714285714285714 out of 1.0)
        else  # if Comments_diff > -1.5
          case when LLOC_before <= 424.5 then
             return 0.07142857142857142 # (0.07142857142857142 out of 1.0)
          else  # if LLOC_before > 424.5
             return 0.0 # (0.0 out of 1.0)
          end         end       else  # if McCabe_sum_before > 217.0
         return 0.5 # (0.5 out of 1.0)
      end     end   else  # if avg_coupling_code_size_cut_diff > -1.1597222089767456
    case when LLOC_before <= 347.5 then
      case when added_lines <= 4.5 then
        case when McCabe_sum_before <= 34.5 then
           return 1.0 # (1.0 out of 1.0)
        else  # if McCabe_sum_before > 34.5
           return 0.7931034482758621 # (0.7931034482758621 out of 1.0)
        end       else  # if added_lines > 4.5
        case when low_ccp_group <= 0.5 then
          case when Blank_before <= 79.5 then
            case when added_lines <= 38.5 then
               return 0.64 # (0.64 out of 1.0)
            else  # if added_lines > 38.5
              case when Comments_before <= 13.5 then
                 return 0.8333333333333334 # (0.8333333333333334 out of 1.0)
              else  # if Comments_before > 13.5
                 return 1.0 # (1.0 out of 1.0)
              end             end           else  # if Blank_before > 79.5
             return 0.5 # (0.5 out of 1.0)
          end         else  # if low_ccp_group > 0.5
          case when vocabulary_diff <= -6.5 then
             return 0.7333333333333333 # (0.7333333333333333 out of 1.0)
          else  # if vocabulary_diff > -6.5
            case when length_diff <= -1.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if length_diff > -1.5
               return 0.21428571428571427 # (0.21428571428571427 out of 1.0)
            end           end         end       end     else  # if LLOC_before > 347.5
      case when superfluous-parens <= 0.5 then
        case when Single comments_after <= 39.5 then
          case when McCabe_max_after <= 14.0 then
            case when Single comments_diff <= -7.5 then
               return 0.625 # (0.625 out of 1.0)
            else  # if Single comments_diff > -7.5
               return 0.07142857142857142 # (0.07142857142857142 out of 1.0)
            end           else  # if McCabe_max_after > 14.0
             return 0.8484848484848485 # (0.8484848484848485 out of 1.0)
          end         else  # if Single comments_after > 39.5
          case when Single comments_before <= 53.5 then
            case when changed_lines <= 117.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if changed_lines > 117.5
               return 0.35714285714285715 # (0.35714285714285715 out of 1.0)
            end           else  # if Single comments_before > 53.5
            case when SLOC_diff <= 1.5 then
              case when McCabe_sum_before <= 195.5 then
                case when McCabe_max_before <= 20.5 then
                  case when Comments_before <= 97.5 then
                     return 0.35714285714285715 # (0.35714285714285715 out of 1.0)
                  else  # if Comments_before > 97.5
                     return 0.15789473684210525 # (0.15789473684210525 out of 1.0)
                  end                 else  # if McCabe_max_before > 20.5
                   return 0.047619047619047616 # (0.047619047619047616 out of 1.0)
                end               else  # if McCabe_sum_before > 195.5
                case when LLOC_before <= 678.0 then
                   return 0.75 # (0.75 out of 1.0)
                else  # if LLOC_before > 678.0
                   return 0.2692307692307692 # (0.2692307692307692 out of 1.0)
                end               end             else  # if SLOC_diff > 1.5
              case when vocabulary_diff <= 2.5 then
                 return 0.6785714285714286 # (0.6785714285714286 out of 1.0)
              else  # if vocabulary_diff > 2.5
                 return 0.5 # (0.5 out of 1.0)
              end             end           end         end       else  # if superfluous-parens > 0.5
        case when changed_lines <= 29.5 then
           return 0.6521739130434783 # (0.6521739130434783 out of 1.0)
        else  # if changed_lines > 29.5
           return 0.7916666666666666 # (0.7916666666666666 out of 1.0)
        end       end     end   end )