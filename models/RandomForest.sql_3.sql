create or replace function RandomForest_3 (prev_count int64, prev_count_x int64, prev_count_y int64, using-constant-test int64, Comments_diff int64, massive_change int64, McCabe_max_after int64, Comments_before int64, too-many-statements int64, cur_count_x int64, h1_diff int64, McCabe_sum_diff int64, LLOC_before int64, McCabe_sum_before int64, high_McCabe_max_before int64, avg_coupling_code_size_cut_diff int64, is_refactor int64, N2_diff int64, too-many-branches int64, SLOC_before int64, too-many-nested-blocks int64, too-many-lines int64, bugs_diff int64, time_diff int64, Single comments_after int64, simplifiable-condition int64, Multi_diff int64, high_McCabe_sum_before int64, low_ccp_group int64, refactor_mle_diff int64, low_McCabe_max_diff int64, SLOC_diff int64, changed_lines int64, hunks_num int64, McCabe_sum_after int64, cur_count_y int64, one_file_fix_rate_diff int64, low_McCabe_sum_before int64, modified_McCabe_max_diff int64, superfluous-parens int64, mostly_delete int64, added_functions int64, Comments_after int64, N1_diff int64, McCabe_max_diff int64, simplifiable-if-statement int64, LOC_before int64, low_McCabe_max_before int64, McCabe_max_before int64, try-except-raise int64, line-too-long int64, unnecessary-semicolon int64, wildcard-import int64, difficulty_diff int64, Simplify-boolean-expression int64, cur_count int64, low_McCabe_sum_diff int64, pointless-statement int64, length_diff int64, broad-exception-caught int64, h2_diff int64, high_McCabe_sum_diff int64, only_removal int64, comparison-of-constants int64, Single comments_diff int64, too-many-boolean-expressions int64, Blank_before int64, calculated_length_diff int64, Single comments_before int64, removed_lines int64, simplifiable-if-expression int64, LOC_diff int64, volume_diff int64, high_McCabe_max_diff int64, high_ccp_group int64, same_day_duration_avg_diff int64, Blank_diff int64, effort_diff int64, too-many-return-statements int64, added_lines int64, unnecessary-pass int64, vocabulary_diff int64, LLOC_diff int64) as (
  case when Blank_before <= 28.5 then
    case when high_ccp_group <= 0.5 then
      case when same_day_duration_avg_diff <= 7.169132947921753 then
         return 0.6153846153846154 # (0.6153846153846154 out of 1.0)
      else  # if same_day_duration_avg_diff > 7.169132947921753
         return 1.0 # (1.0 out of 1.0)
      end     else  # if high_ccp_group > 0.5
       return 1.0 # (1.0 out of 1.0)
    end   else  # if Blank_before > 28.5
    case when Comments_after <= 37.5 then
      case when high_McCabe_max_before <= 0.5 then
        case when Comments_after <= 30.5 then
          case when removed_lines <= 23.0 then
            case when high_ccp_group <= 0.5 then
              case when changed_lines <= 25.0 then
                case when avg_coupling_code_size_cut_diff <= 0.25 then
                   return 0.42105263157894735 # (0.42105263157894735 out of 1.0)
                else  # if avg_coupling_code_size_cut_diff > 0.25
                   return 0.6875 # (0.6875 out of 1.0)
                end               else  # if changed_lines > 25.0
                case when LOC_diff <= -82.0 then
                   return 0.15384615384615385 # (0.15384615384615385 out of 1.0)
                else  # if LOC_diff > -82.0
                   return 0.0 # (0.0 out of 1.0)
                end               end             else  # if high_ccp_group > 0.5
               return 0.8125 # (0.8125 out of 1.0)
            end           else  # if removed_lines > 23.0
            case when McCabe_sum_diff <= -2.5 then
              case when low_McCabe_sum_before <= 0.5 then
                 return 0.7222222222222222 # (0.7222222222222222 out of 1.0)
              else  # if low_McCabe_sum_before > 0.5
                 return 1.0 # (1.0 out of 1.0)
              end             else  # if McCabe_sum_diff > -2.5
              case when LOC_before <= 440.0 then
                 return 0.625 # (0.625 out of 1.0)
              else  # if LOC_before > 440.0
                 return 0.38461538461538464 # (0.38461538461538464 out of 1.0)
              end             end           end         else  # if Comments_after > 30.5
          case when avg_coupling_code_size_cut_diff <= -1.0954545736312866 then
             return 1.0 # (1.0 out of 1.0)
          else  # if avg_coupling_code_size_cut_diff > -1.0954545736312866
             return 0.7058823529411765 # (0.7058823529411765 out of 1.0)
          end         end       else  # if high_McCabe_max_before > 0.5
        case when added_lines <= 73.0 then
           return 0.5652173913043478 # (0.5652173913043478 out of 1.0)
        else  # if added_lines > 73.0
           return 0.09523809523809523 # (0.09523809523809523 out of 1.0)
        end       end     else  # if Comments_after > 37.5
      case when refactor_mle_diff <= -0.022308796644210815 then
        case when Single comments_before <= 127.0 then
          case when Single comments_diff <= 1.5 then
            case when LLOC_before <= 571.0 then
              case when Comments_after <= 70.0 then
                 return 0.7272727272727273 # (0.7272727272727273 out of 1.0)
              else  # if Comments_after > 70.0
                 return 0.4666666666666667 # (0.4666666666666667 out of 1.0)
              end             else  # if LLOC_before > 571.0
              case when Single comments_before <= 102.5 then
                 return 0.5625 # (0.5625 out of 1.0)
              else  # if Single comments_before > 102.5
                 return 0.18181818181818182 # (0.18181818181818182 out of 1.0)
              end             end           else  # if Single comments_diff > 1.5
             return 0.0 # (0.0 out of 1.0)
          end         else  # if Single comments_before > 127.0
          case when changed_lines <= 71.5 then
             return 0.6086956521739131 # (0.6086956521739131 out of 1.0)
          else  # if changed_lines > 71.5
             return 0.9473684210526315 # (0.9473684210526315 out of 1.0)
          end         end       else  # if refactor_mle_diff > -0.022308796644210815
        case when N2_diff <= 5.5 then
          case when McCabe_sum_after <= 195.0 then
            case when low_McCabe_sum_diff <= 0.5 then
              case when McCabe_max_before <= 12.5 then
                 return 0.2631578947368421 # (0.2631578947368421 out of 1.0)
              else  # if McCabe_max_before > 12.5
                case when Single comments_after <= 97.0 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if Single comments_after > 97.0
                   return 0.08333333333333333 # (0.08333333333333333 out of 1.0)
                end               end             else  # if low_McCabe_sum_diff > 0.5
               return 0.4 # (0.4 out of 1.0)
            end           else  # if McCabe_sum_after > 195.0
            case when modified_McCabe_max_diff <= -0.5 then
              case when McCabe_sum_diff <= -3.5 then
                 return 0.23529411764705882 # (0.23529411764705882 out of 1.0)
              else  # if McCabe_sum_diff > -3.5
                 return 0.6190476190476191 # (0.6190476190476191 out of 1.0)
              end             else  # if modified_McCabe_max_diff > -0.5
              case when Comments_after <= 140.0 then
                 return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
              else  # if Comments_after > 140.0
                 return 0.09523809523809523 # (0.09523809523809523 out of 1.0)
              end             end           end         else  # if N2_diff > 5.5
           return 0.47619047619047616 # (0.47619047619047616 out of 1.0)
        end       end     end   end )