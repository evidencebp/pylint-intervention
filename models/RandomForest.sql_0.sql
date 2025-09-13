create or replace function RandomForest_0 (McCabe_sum_before int64, changed_lines int64, prev_count_y int64, mostly_delete int64, h1_diff int64, too-many-lines int64, low_McCabe_sum_before int64, length_diff int64, LOC_before int64, simplifiable-if-expression int64, added_functions int64, broad-exception-caught int64, simplifiable-condition int64, prev_count_x int64, McCabe_max_diff int64, SLOC_before int64, LLOC_before int64, low_McCabe_max_diff int64, bugs_diff int64, same_day_duration_avg_diff int64, cur_count_x int64, only_removal int64, McCabe_max_after int64, Single comments_after int64, low_ccp_group int64, one_file_fix_rate_diff int64, effort_diff int64, difficulty_diff int64, removed_lines int64, Comments_diff int64, too-many-boolean-expressions int64, refactor_mle_diff int64, high_McCabe_max_before int64, hunks_num int64, LOC_diff int64, SLOC_diff int64, cur_count_y int64, vocabulary_diff int64, using-constant-test int64, Simplify-boolean-expression int64, low_McCabe_max_before int64, high_McCabe_sum_diff int64, high_McCabe_sum_before int64, McCabe_max_before int64, Comments_after int64, McCabe_sum_diff int64, unnecessary-pass int64, avg_coupling_code_size_cut_diff int64, simplifiable-if-statement int64, is_refactor int64, volume_diff int64, added_lines int64, high_McCabe_max_diff int64, superfluous-parens int64, cur_count int64, low_McCabe_sum_diff int64, calculated_length_diff int64, Multi_diff int64, N2_diff int64, h2_diff int64, Single comments_before int64, McCabe_sum_after int64, N1_diff int64, too-many-statements int64, comparison-of-constants int64, pointless-statement int64, time_diff int64, prev_count int64, Single comments_diff int64, massive_change int64, Blank_diff int64, too-many-nested-blocks int64, Comments_before int64, modified_McCabe_max_diff int64, LLOC_diff int64, Blank_before int64, try-except-raise int64, too-many-branches int64, too-many-return-statements int64, unnecessary-semicolon int64, wildcard-import int64, high_ccp_group int64, line-too-long int64) as (
  case when one_file_fix_rate_diff <= 0.06507936865091324 then
    case when vocabulary_diff <= -32.0 then
      case when McCabe_sum_before <= 244.5 then
        case when LLOC_diff <= -127.0 then
           return 0.8 # (0.8 out of 1.0)
        else  # if LLOC_diff > -127.0
           return 1.0 # (1.0 out of 1.0)
        end       else  # if McCabe_sum_before > 244.5
         return 0.12 # (0.12 out of 1.0)
      end     else  # if vocabulary_diff > -32.0
      case when low_McCabe_max_before <= 0.5 then
        case when h2_diff <= -24.5 then
           return 0.0 # (0.0 out of 1.0)
        else  # if h2_diff > -24.5
          case when McCabe_sum_after <= 195.0 then
            case when Single comments_before <= 9.5 then
               return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
            else  # if Single comments_before > 9.5
              case when SLOC_before <= 566.5 then
                case when N2_diff <= -11.0 then
                   return 0.625 # (0.625 out of 1.0)
                else  # if N2_diff > -11.0
                  case when hunks_num <= 7.5 then
                    case when avg_coupling_code_size_cut_diff <= 0.19769231230020523 then
                      case when Single comments_after <= 40.5 then
                         return 0.0 # (0.0 out of 1.0)
                      else  # if Single comments_after > 40.5
                         return 0.2631578947368421 # (0.2631578947368421 out of 1.0)
                      end                     else  # if avg_coupling_code_size_cut_diff > 0.19769231230020523
                       return 0.29411764705882354 # (0.29411764705882354 out of 1.0)
                    end                   else  # if hunks_num > 7.5
                     return 0.5416666666666666 # (0.5416666666666666 out of 1.0)
                  end                 end               else  # if SLOC_before > 566.5
                case when SLOC_before <= 757.5 then
                  case when changed_lines <= 73.0 then
                     return 0.06666666666666667 # (0.06666666666666667 out of 1.0)
                  else  # if changed_lines > 73.0
                     return 0.0 # (0.0 out of 1.0)
                  end                 else  # if SLOC_before > 757.5
                   return 0.2 # (0.2 out of 1.0)
                end               end             end           else  # if McCabe_sum_after > 195.0
            case when LOC_diff <= -27.5 then
               return 0.7222222222222222 # (0.7222222222222222 out of 1.0)
            else  # if LOC_diff > -27.5
              case when superfluous-parens <= 0.5 then
                case when length_diff <= 1.5 then
                  case when same_day_duration_avg_diff <= -6.6572465896606445 then
                     return 0.25 # (0.25 out of 1.0)
                  else  # if same_day_duration_avg_diff > -6.6572465896606445
                     return 0.09090909090909091 # (0.09090909090909091 out of 1.0)
                  end                 else  # if length_diff > 1.5
                   return 0.5294117647058824 # (0.5294117647058824 out of 1.0)
                end               else  # if superfluous-parens > 0.5
                 return 0.72 # (0.72 out of 1.0)
              end             end           end         end       else  # if low_McCabe_max_before > 0.5
        case when LOC_before <= 1109.5 then
          case when removed_lines <= 3.5 then
             return 0.0 # (0.0 out of 1.0)
          else  # if removed_lines > 3.5
            case when LOC_before <= 535.5 then
              case when McCabe_max_before <= 5.5 then
                 return 0.8333333333333334 # (0.8333333333333334 out of 1.0)
              else  # if McCabe_max_before > 5.5
                 return 0.631578947368421 # (0.631578947368421 out of 1.0)
              end             else  # if LOC_before > 535.5
               return 0.14285714285714285 # (0.14285714285714285 out of 1.0)
            end           end         else  # if LOC_before > 1109.5
           return 0.9411764705882353 # (0.9411764705882353 out of 1.0)
        end       end     end   else  # if one_file_fix_rate_diff > 0.06507936865091324
    case when same_day_duration_avg_diff <= 18.550000190734863 then
      case when changed_lines <= 122.5 then
        case when Comments_before <= 18.5 then
           return 0.30434782608695654 # (0.30434782608695654 out of 1.0)
        else  # if Comments_before > 18.5
          case when McCabe_sum_before <= 182.5 then
            case when added_lines <= 10.5 then
               return 0.8846153846153846 # (0.8846153846153846 out of 1.0)
            else  # if added_lines > 10.5
               return 0.631578947368421 # (0.631578947368421 out of 1.0)
            end           else  # if McCabe_sum_before > 182.5
             return 0.35714285714285715 # (0.35714285714285715 out of 1.0)
          end         end       else  # if changed_lines > 122.5
        case when SLOC_diff <= -15.5 then
           return 0.7692307692307693 # (0.7692307692307693 out of 1.0)
        else  # if SLOC_diff > -15.5
           return 0.9285714285714286 # (0.9285714285714286 out of 1.0)
        end       end     else  # if same_day_duration_avg_diff > 18.550000190734863
       return 0.3684210526315789 # (0.3684210526315789 out of 1.0)
    end   end )