create or replace function RandomForest_5 (h1_diff int64, simplifiable-if-statement int64, McCabe_max_after int64, McCabe_sum_before int64, Single comments_before int64, low_McCabe_max_diff int64, high_ccp_group int64, pointless-statement int64, too-many-branches int64, high_McCabe_max_before int64, superfluous-parens int64, Multi_diff int64, wildcard-import int64, high_McCabe_sum_before int64, LLOC_before int64, cur_count int64, unnecessary-semicolon int64, Comments_after int64, mostly_delete int64, simplifiable-condition int64, avg_coupling_code_size_cut_diff int64, added_functions int64, McCabe_max_diff int64, McCabe_sum_diff int64, LLOC_diff int64, LOC_before int64, Comments_diff int64, prev_count_x int64, effort_diff int64, try-except-raise int64, difficulty_diff int64, line-too-long int64, Simplify-boolean-expression int64, SLOC_diff int64, McCabe_sum_after int64, refactor_mle_diff int64, one_file_fix_rate_diff int64, is_refactor int64, too-many-lines int64, too-many-boolean-expressions int64, Single comments_diff int64, low_McCabe_sum_diff int64, cur_count_y int64, comparison-of-constants int64, Comments_before int64, too-many-return-statements int64, vocabulary_diff int64, massive_change int64, hunks_num int64, modified_McCabe_max_diff int64, high_McCabe_sum_diff int64, N2_diff int64, broad-exception-caught int64, length_diff int64, unnecessary-pass int64, time_diff int64, changed_lines int64, Single comments_after int64, h2_diff int64, low_McCabe_sum_before int64, cur_count_x int64, McCabe_max_before int64, using-constant-test int64, added_lines int64, same_day_duration_avg_diff int64, prev_count_y int64, Blank_diff int64, LOC_diff int64, only_removal int64, low_McCabe_max_before int64, bugs_diff int64, too-many-statements int64, simplifiable-if-expression int64, calculated_length_diff int64, volume_diff int64, Blank_before int64, high_McCabe_max_diff int64, SLOC_before int64, too-many-nested-blocks int64, removed_lines int64, low_ccp_group int64, N1_diff int64, prev_count int64) as (
  case when high_ccp_group <= 0.5 then
    case when LLOC_before <= 327.5 then
      case when McCabe_sum_before <= 82.5 then
        case when SLOC_before <= 653.0 then
          case when high_McCabe_sum_diff <= 0.5 then
            case when low_ccp_group <= 0.5 then
              case when h2_diff <= -1.5 then
                 return 0.5909090909090909 # (0.5909090909090909 out of 1.0)
              else  # if h2_diff > -1.5
                case when McCabe_max_after <= 6.5 then
                   return 0.8275862068965517 # (0.8275862068965517 out of 1.0)
                else  # if McCabe_max_after > 6.5
                   return 1.0 # (1.0 out of 1.0)
                end               end             else  # if low_ccp_group > 0.5
              case when Single comments_after <= 14.5 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if Single comments_after > 14.5
                 return 0.2857142857142857 # (0.2857142857142857 out of 1.0)
              end             end           else  # if high_McCabe_sum_diff > 0.5
             return 0.13636363636363635 # (0.13636363636363635 out of 1.0)
          end         else  # if SLOC_before > 653.0
           return 1.0 # (1.0 out of 1.0)
        end       else  # if McCabe_sum_before > 82.5
        case when Comments_before <= 31.0 then
           return 0.6 # (0.6 out of 1.0)
        else  # if Comments_before > 31.0
           return 0.21052631578947367 # (0.21052631578947367 out of 1.0)
        end       end     else  # if LLOC_before > 327.5
      case when Blank_diff <= -52.0 then
         return 0.875 # (0.875 out of 1.0)
      else  # if Blank_diff > -52.0
        case when added_functions <= 0.5 then
          case when LLOC_before <= 1095.5 then
            case when McCabe_sum_before <= 133.5 then
               return 0.4230769230769231 # (0.4230769230769231 out of 1.0)
            else  # if McCabe_sum_before > 133.5
              case when Comments_after <= 52.0 then
                 return 0.25 # (0.25 out of 1.0)
              else  # if Comments_after > 52.0
                case when Comments_before <= 97.5 then
                   return 0.07692307692307693 # (0.07692307692307693 out of 1.0)
                else  # if Comments_before > 97.5
                  case when LOC_diff <= -13.0 then
                     return 0.07142857142857142 # (0.07142857142857142 out of 1.0)
                  else  # if LOC_diff > -13.0
                     return 0.0 # (0.0 out of 1.0)
                  end                 end               end             end           else  # if LLOC_before > 1095.5
             return 0.34285714285714286 # (0.34285714285714286 out of 1.0)
          end         else  # if added_functions > 0.5
          case when changed_lines <= 501.5 then
            case when refactor_mle_diff <= -0.003164685331285 then
              case when Blank_before <= 225.5 then
                 return 0.5 # (0.5 out of 1.0)
              else  # if Blank_before > 225.5
                 return 0.84 # (0.84 out of 1.0)
              end             else  # if refactor_mle_diff > -0.003164685331285
               return 0.32 # (0.32 out of 1.0)
            end           else  # if changed_lines > 501.5
             return 0.15384615384615385 # (0.15384615384615385 out of 1.0)
          end         end       end     end   else  # if high_ccp_group > 0.5
    case when hunks_num <= 23.0 then
      case when massive_change <= 0.5 then
        case when SLOC_before <= 358.0 then
          case when SLOC_diff <= -1.5 then
             return 0.875 # (0.875 out of 1.0)
          else  # if SLOC_diff > -1.5
             return 1.0 # (1.0 out of 1.0)
          end         else  # if SLOC_before > 358.0
          case when Single comments_after <= 21.0 then
             return 0.26666666666666666 # (0.26666666666666666 out of 1.0)
          else  # if Single comments_after > 21.0
            case when Comments_before <= 81.0 then
              case when McCabe_sum_after <= 118.5 then
                 return 0.9230769230769231 # (0.9230769230769231 out of 1.0)
              else  # if McCabe_sum_after > 118.5
                 return 1.0 # (1.0 out of 1.0)
              end             else  # if Comments_before > 81.0
               return 0.7368421052631579 # (0.7368421052631579 out of 1.0)
            end           end         end       else  # if massive_change > 0.5
         return 0.23076923076923078 # (0.23076923076923078 out of 1.0)
      end     else  # if hunks_num > 23.0
       return 0.25 # (0.25 out of 1.0)
    end   end )