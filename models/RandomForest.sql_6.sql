create or replace function RandomForest_6 (low_McCabe_sum_before int64, changed_lines int64, low_McCabe_max_diff int64, try-except-raise int64, Comments_before int64, high_McCabe_sum_diff int64, low_McCabe_max_before int64, Multi_diff int64, effort_diff int64, difficulty_diff int64, only_removal int64, length_diff int64, comparison-of-constants int64, LOC_diff int64, h2_diff int64, line-too-long int64, h1_diff int64, using-constant-test int64, broad-exception-caught int64, time_diff int64, calculated_length_diff int64, too-many-branches int64, SLOC_before int64, low_ccp_group int64, avg_coupling_code_size_cut_diff int64, new_function int64, wildcard-import int64, McCabe_max_before int64, superfluous-parens int64, low_McCabe_sum_diff int64, pointless-statement int64, one_file_fix_rate_diff int64, cur_count_x int64, same_day_duration_avg_diff int64, too-many-nested-blocks int64, simplifiable-condition int64, too-many-lines int64, SLOC_diff int64, cur_count_y int64, LLOC_before int64, Comments_after int64, high_ccp_group int64, bugs_diff int64, unnecessary-pass int64, prev_count_x int64, massive_change int64, McCabe_max_after int64, removed_lines int64, Comments_diff int64, Single comments_diff int64, too-many-statements int64, Simplify-boolean-expression int64, is_refactor int64, refactor_mle_diff int64, added_lines int64, mostly_delete int64, volume_diff int64, too-many-boolean-expressions int64, N2_diff int64, Blank_before int64, vocabulary_diff int64, McCabe_sum_before int64, high_McCabe_sum_before int64, N1_diff int64, LOC_before int64, LLOC_diff int64, high_McCabe_max_diff int64, simplifiable-if-statement int64, prev_count_y int64, hunks_num int64, Blank_diff int64, prev_count int64, Single comments_before int64, McCabe_max_diff int64, McCabe_sum_diff int64, modified_McCabe_max_diff int64, McCabe_sum_after int64, too-many-return-statements int64, Single comments_after int64, unnecessary-semicolon int64, added_functions int64, cur_count int64, simplifiable-if-expression int64, high_McCabe_max_before int64) as (
  case when LLOC_before <= 400.0 then
    case when Single comments_diff <= -4.5 then
      case when modified_McCabe_max_diff <= -0.5 then
         return 0.9615384615384616 # (0.9615384615384616 out of 1.0)
      else  # if modified_McCabe_max_diff > -0.5
         return 0.6956521739130435 # (0.6956521739130435 out of 1.0)
      end     else  # if Single comments_diff > -4.5
      case when removed_lines <= 62.0 then
        case when added_lines <= 0.5 then
           return 0.8181818181818182 # (0.8181818181818182 out of 1.0)
        else  # if added_lines > 0.5
          case when McCabe_sum_diff <= 0.5 then
            case when Single comments_before <= 6.5 then
               return 0.6818181818181818 # (0.6818181818181818 out of 1.0)
            else  # if Single comments_before > 6.5
              case when same_day_duration_avg_diff <= -67.23214340209961 then
                 return 0.6428571428571429 # (0.6428571428571429 out of 1.0)
              else  # if same_day_duration_avg_diff > -67.23214340209961
                case when McCabe_max_diff <= -2.5 then
                   return 0.26666666666666666 # (0.26666666666666666 out of 1.0)
                else  # if McCabe_max_diff > -2.5
                  case when refactor_mle_diff <= 0.015917614102363586 then
                     return 0.2631578947368421 # (0.2631578947368421 out of 1.0)
                  else  # if refactor_mle_diff > 0.015917614102363586
                     return 0.08333333333333333 # (0.08333333333333333 out of 1.0)
                  end                 end               end             end           else  # if McCabe_sum_diff > 0.5
             return 0.15 # (0.15 out of 1.0)
          end         end       else  # if removed_lines > 62.0
        case when added_lines <= 79.5 then
          case when added_functions <= 1.5 then
             return 1.0 # (1.0 out of 1.0)
          else  # if added_functions > 1.5
             return 0.8823529411764706 # (0.8823529411764706 out of 1.0)
          end         else  # if added_lines > 79.5
           return 0.4375 # (0.4375 out of 1.0)
        end       end     end   else  # if LLOC_before > 400.0
    case when N1_diff <= 7.5 then
      case when McCabe_max_after <= 20.5 then
        case when low_ccp_group <= 0.5 then
          case when SLOC_before <= 913.5 then
            case when added_lines <= 16.5 then
               return 0.46153846153846156 # (0.46153846153846156 out of 1.0)
            else  # if added_lines > 16.5
              case when N2_diff <= -56.0 then
                 return 0.5833333333333334 # (0.5833333333333334 out of 1.0)
              else  # if N2_diff > -56.0
                case when N2_diff <= -14.5 then
                   return 1.0 # (1.0 out of 1.0)
                else  # if N2_diff > -14.5
                   return 0.8125 # (0.8125 out of 1.0)
                end               end             end           else  # if SLOC_before > 913.5
            case when refactor_mle_diff <= 0.03664580173790455 then
               return 0.5652173913043478 # (0.5652173913043478 out of 1.0)
            else  # if refactor_mle_diff > 0.03664580173790455
               return 0.06666666666666667 # (0.06666666666666667 out of 1.0)
            end           end         else  # if low_ccp_group > 0.5
           return 0.14285714285714285 # (0.14285714285714285 out of 1.0)
        end       else  # if McCabe_max_after > 20.5
        case when SLOC_before <= 907.0 then
          case when superfluous-parens <= 0.5 then
            case when McCabe_sum_diff <= -4.5 then
              case when Blank_diff <= -5.5 then
                 return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
              else  # if Blank_diff > -5.5
                 return 0.0 # (0.0 out of 1.0)
              end             else  # if McCabe_sum_diff > -4.5
               return 0.0 # (0.0 out of 1.0)
            end           else  # if superfluous-parens > 0.5
             return 0.45454545454545453 # (0.45454545454545453 out of 1.0)
          end         else  # if SLOC_before > 907.0
          case when removed_lines <= 1.5 then
             return 0.1111111111111111 # (0.1111111111111111 out of 1.0)
          else  # if removed_lines > 1.5
            case when Single comments_diff <= -0.5 then
               return 0.23809523809523808 # (0.23809523809523808 out of 1.0)
            else  # if Single comments_diff > -0.5
              case when McCabe_max_before <= 47.5 then
                 return 0.43333333333333335 # (0.43333333333333335 out of 1.0)
              else  # if McCabe_max_before > 47.5
                 return 0.85 # (0.85 out of 1.0)
              end             end           end         end       end     else  # if N1_diff > 7.5
       return 0.07142857142857142 # (0.07142857142857142 out of 1.0)
    end   end )