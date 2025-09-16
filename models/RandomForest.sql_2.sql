create or replace function RandomForest_2 (low_McCabe_sum_before int64, changed_lines int64, low_McCabe_max_diff int64, try-except-raise int64, Comments_before int64, high_McCabe_sum_diff int64, low_McCabe_max_before int64, Multi_diff int64, effort_diff int64, difficulty_diff int64, only_removal int64, length_diff int64, comparison-of-constants int64, LOC_diff int64, h2_diff int64, line-too-long int64, h1_diff int64, using-constant-test int64, broad-exception-caught int64, time_diff int64, calculated_length_diff int64, too-many-branches int64, SLOC_before int64, low_ccp_group int64, avg_coupling_code_size_cut_diff int64, new_function int64, wildcard-import int64, McCabe_max_before int64, superfluous-parens int64, low_McCabe_sum_diff int64, pointless-statement int64, one_file_fix_rate_diff int64, cur_count_x int64, same_day_duration_avg_diff int64, too-many-nested-blocks int64, simplifiable-condition int64, too-many-lines int64, SLOC_diff int64, cur_count_y int64, LLOC_before int64, Comments_after int64, high_ccp_group int64, bugs_diff int64, unnecessary-pass int64, prev_count_x int64, massive_change int64, McCabe_max_after int64, removed_lines int64, Comments_diff int64, Single comments_diff int64, too-many-statements int64, Simplify-boolean-expression int64, is_refactor int64, refactor_mle_diff int64, added_lines int64, mostly_delete int64, volume_diff int64, too-many-boolean-expressions int64, N2_diff int64, Blank_before int64, vocabulary_diff int64, McCabe_sum_before int64, high_McCabe_sum_before int64, N1_diff int64, LOC_before int64, LLOC_diff int64, high_McCabe_max_diff int64, simplifiable-if-statement int64, prev_count_y int64, hunks_num int64, Blank_diff int64, prev_count int64, Single comments_before int64, McCabe_max_diff int64, McCabe_sum_diff int64, modified_McCabe_max_diff int64, McCabe_sum_after int64, too-many-return-statements int64, Single comments_after int64, unnecessary-semicolon int64, added_functions int64, cur_count int64, simplifiable-if-expression int64, high_McCabe_max_before int64) as (
  case when high_ccp_group <= 0.5 then
    case when length_diff <= -228.5 then
       return 0.875 # (0.875 out of 1.0)
    else  # if length_diff > -228.5
      case when SLOC_diff <= 38.0 then
        case when changed_lines <= 138.5 then
          case when refactor_mle_diff <= -0.048468658700585365 then
            case when removed_lines <= 1.5 then
              case when vocabulary_diff <= -1.5 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if vocabulary_diff > -1.5
                 return 0.2857142857142857 # (0.2857142857142857 out of 1.0)
              end             else  # if removed_lines > 1.5
              case when changed_lines <= 75.5 then
                case when Comments_diff <= -1.5 then
                   return 0.125 # (0.125 out of 1.0)
                else  # if Comments_diff > -1.5
                  case when length_diff <= -1.0 then
                     return 0.5652173913043478 # (0.5652173913043478 out of 1.0)
                  else  # if length_diff > -1.0
                    case when same_day_duration_avg_diff <= -7.983971118927002 then
                       return 0.9130434782608695 # (0.9130434782608695 out of 1.0)
                    else  # if same_day_duration_avg_diff > -7.983971118927002
                       return 0.5714285714285714 # (0.5714285714285714 out of 1.0)
                    end                   end                 end               else  # if changed_lines > 75.5
                 return 0.1111111111111111 # (0.1111111111111111 out of 1.0)
              end             end           else  # if refactor_mle_diff > -0.048468658700585365
            case when low_ccp_group <= 0.5 then
              case when Single comments_before <= 49.5 then
                case when LOC_diff <= 4.5 then
                   return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
                else  # if LOC_diff > 4.5
                   return 0.3125 # (0.3125 out of 1.0)
                end               else  # if Single comments_before > 49.5
                case when SLOC_before <= 816.0 then
                  case when Comments_before <= 68.0 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if Comments_before > 68.0
                     return 0.16666666666666666 # (0.16666666666666666 out of 1.0)
                  end                 else  # if SLOC_before > 816.0
                   return 0.25 # (0.25 out of 1.0)
                end               end             else  # if low_ccp_group > 0.5
              case when McCabe_sum_before <= 150.5 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if McCabe_sum_before > 150.5
                 return 0.13333333333333333 # (0.13333333333333333 out of 1.0)
              end             end           end         else  # if changed_lines > 138.5
          case when Comments_after <= 49.5 then
            case when Single comments_diff <= -0.5 then
               return 0.875 # (0.875 out of 1.0)
            else  # if Single comments_diff > -0.5
               return 0.28 # (0.28 out of 1.0)
            end           else  # if Comments_after > 49.5
            case when McCabe_sum_before <= 149.5 then
               return 0.05263157894736842 # (0.05263157894736842 out of 1.0)
            else  # if McCabe_sum_before > 149.5
               return 0.5384615384615384 # (0.5384615384615384 out of 1.0)
            end           end         end       else  # if SLOC_diff > 38.0
        case when Blank_diff <= 4.0 then
           return 0.9310344827586207 # (0.9310344827586207 out of 1.0)
        else  # if Blank_diff > 4.0
           return 0.4 # (0.4 out of 1.0)
        end       end     end   else  # if high_ccp_group > 0.5
    case when SLOC_before <= 541.0 then
      case when Comments_after <= 15.0 then
         return 0.8571428571428571 # (0.8571428571428571 out of 1.0)
      else  # if Comments_after > 15.0
        case when same_day_duration_avg_diff <= -49.957143783569336 then
           return 0.8333333333333334 # (0.8333333333333334 out of 1.0)
        else  # if same_day_duration_avg_diff > -49.957143783569336
           return 1.0 # (1.0 out of 1.0)
        end       end     else  # if SLOC_before > 541.0
      case when Blank_before <= 98.5 then
         return 0.0 # (0.0 out of 1.0)
      else  # if Blank_before > 98.5
        case when avg_coupling_code_size_cut_diff <= 0.540178582072258 then
          case when avg_coupling_code_size_cut_diff <= -0.7645929157733917 then
             return 0.6111111111111112 # (0.6111111111111112 out of 1.0)
          else  # if avg_coupling_code_size_cut_diff > -0.7645929157733917
            case when McCabe_sum_before <= 248.5 then
               return 0.9565217391304348 # (0.9565217391304348 out of 1.0)
            else  # if McCabe_sum_before > 248.5
               return 0.7692307692307693 # (0.7692307692307693 out of 1.0)
            end           end         else  # if avg_coupling_code_size_cut_diff > 0.540178582072258
           return 0.2857142857142857 # (0.2857142857142857 out of 1.0)
        end       end     end   end )