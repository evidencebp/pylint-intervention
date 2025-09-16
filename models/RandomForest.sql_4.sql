create or replace function RandomForest_4 (low_McCabe_sum_before int64, changed_lines int64, low_McCabe_max_diff int64, try-except-raise int64, Comments_before int64, high_McCabe_sum_diff int64, low_McCabe_max_before int64, Multi_diff int64, effort_diff int64, difficulty_diff int64, only_removal int64, length_diff int64, comparison-of-constants int64, LOC_diff int64, h2_diff int64, line-too-long int64, h1_diff int64, using-constant-test int64, broad-exception-caught int64, time_diff int64, calculated_length_diff int64, too-many-branches int64, SLOC_before int64, low_ccp_group int64, avg_coupling_code_size_cut_diff int64, new_function int64, wildcard-import int64, McCabe_max_before int64, superfluous-parens int64, low_McCabe_sum_diff int64, pointless-statement int64, one_file_fix_rate_diff int64, cur_count_x int64, same_day_duration_avg_diff int64, too-many-nested-blocks int64, simplifiable-condition int64, too-many-lines int64, SLOC_diff int64, cur_count_y int64, LLOC_before int64, Comments_after int64, high_ccp_group int64, bugs_diff int64, unnecessary-pass int64, prev_count_x int64, massive_change int64, McCabe_max_after int64, removed_lines int64, Comments_diff int64, Single comments_diff int64, too-many-statements int64, Simplify-boolean-expression int64, is_refactor int64, refactor_mle_diff int64, added_lines int64, mostly_delete int64, volume_diff int64, too-many-boolean-expressions int64, N2_diff int64, Blank_before int64, vocabulary_diff int64, McCabe_sum_before int64, high_McCabe_sum_before int64, N1_diff int64, LOC_before int64, LLOC_diff int64, high_McCabe_max_diff int64, simplifiable-if-statement int64, prev_count_y int64, hunks_num int64, Blank_diff int64, prev_count int64, Single comments_before int64, McCabe_max_diff int64, McCabe_sum_diff int64, modified_McCabe_max_diff int64, McCabe_sum_after int64, too-many-return-statements int64, Single comments_after int64, unnecessary-semicolon int64, added_functions int64, cur_count int64, simplifiable-if-expression int64, high_McCabe_max_before int64) as (
  case when Comments_after <= 6.5 then
    case when LOC_diff <= -3.5 then
       return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
    else  # if LOC_diff > -3.5
      case when McCabe_max_after <= 4.0 then
         return 0.9473684210526315 # (0.9473684210526315 out of 1.0)
      else  # if McCabe_max_after > 4.0
         return 1.0 # (1.0 out of 1.0)
      end     end   else  # if Comments_after > 6.5
    case when avg_coupling_code_size_cut_diff <= 0.6020833551883698 then
      case when Comments_after <= 53.0 then
        case when changed_lines <= 134.0 then
          case when Single comments_after <= 21.5 then
            case when McCabe_max_after <= 10.5 then
               return 0.19444444444444445 # (0.19444444444444445 out of 1.0)
            else  # if McCabe_max_after > 10.5
               return 0.6153846153846154 # (0.6153846153846154 out of 1.0)
            end           else  # if Single comments_after > 21.5
            case when LLOC_diff <= 0.5 then
              case when Comments_after <= 37.5 then
                case when refactor_mle_diff <= -0.00530461547896266 then
                   return 0.8888888888888888 # (0.8888888888888888 out of 1.0)
                else  # if refactor_mle_diff > -0.00530461547896266
                   return 0.6111111111111112 # (0.6111111111111112 out of 1.0)
                end               else  # if Comments_after > 37.5
                 return 0.35714285714285715 # (0.35714285714285715 out of 1.0)
              end             else  # if LLOC_diff > 0.5
               return 0.35294117647058826 # (0.35294117647058826 out of 1.0)
            end           end         else  # if changed_lines > 134.0
          case when Comments_diff <= -9.5 then
            case when Single comments_before <= 60.0 then
               return 0.875 # (0.875 out of 1.0)
            else  # if Single comments_before > 60.0
               return 1.0 # (1.0 out of 1.0)
            end           else  # if Comments_diff > -9.5
            case when LLOC_diff <= -19.0 then
               return 0.23529411764705882 # (0.23529411764705882 out of 1.0)
            else  # if LLOC_diff > -19.0
              case when vocabulary_diff <= 0.5 then
                 return 0.6470588235294118 # (0.6470588235294118 out of 1.0)
              else  # if vocabulary_diff > 0.5
                 return 0.8571428571428571 # (0.8571428571428571 out of 1.0)
              end             end           end         end       else  # if Comments_after > 53.0
        case when McCabe_max_after <= 12.5 then
          case when h1_diff <= 0.5 then
             return 0.43333333333333335 # (0.43333333333333335 out of 1.0)
          else  # if h1_diff > 0.5
             return 1.0 # (1.0 out of 1.0)
          end         else  # if McCabe_max_after > 12.5
          case when LLOC_before <= 623.0 then
            case when SLOC_diff <= 4.5 then
              case when changed_lines <= 99.5 then
                case when length_diff <= -1.5 then
                   return 0.07142857142857142 # (0.07142857142857142 out of 1.0)
                else  # if length_diff > -1.5
                   return 0.36363636363636365 # (0.36363636363636365 out of 1.0)
                end               else  # if changed_lines > 99.5
                 return 0.4782608695652174 # (0.4782608695652174 out of 1.0)
              end             else  # if SLOC_diff > 4.5
              case when Single comments_after <= 121.0 then
                 return 0.0625 # (0.0625 out of 1.0)
              else  # if Single comments_after > 121.0
                 return 0.0 # (0.0 out of 1.0)
              end             end           else  # if LLOC_before > 623.0
            case when LLOC_before <= 1927.5 then
              case when LLOC_diff <= 1.0 then
                case when vocabulary_diff <= -6.0 then
                   return 0.8181818181818182 # (0.8181818181818182 out of 1.0)
                else  # if vocabulary_diff > -6.0
                   return 0.1875 # (0.1875 out of 1.0)
                end               else  # if LLOC_diff > 1.0
                 return 0.85 # (0.85 out of 1.0)
              end             else  # if LLOC_before > 1927.5
               return 0.26666666666666666 # (0.26666666666666666 out of 1.0)
            end           end         end       end     else  # if avg_coupling_code_size_cut_diff > 0.6020833551883698
      case when Blank_diff <= 4.5 then
        case when added_lines <= 105.0 then
          case when high_ccp_group <= 0.5 then
            case when added_lines <= 9.5 then
               return 0.21428571428571427 # (0.21428571428571427 out of 1.0)
            else  # if added_lines > 9.5
              case when Multi_diff <= -1.0 then
                 return 0.07142857142857142 # (0.07142857142857142 out of 1.0)
              else  # if Multi_diff > -1.0
                 return 0.0 # (0.0 out of 1.0)
              end             end           else  # if high_ccp_group > 0.5
             return 0.5294117647058824 # (0.5294117647058824 out of 1.0)
          end         else  # if added_lines > 105.0
          case when N2_diff <= -44.5 then
             return 0.25 # (0.25 out of 1.0)
          else  # if N2_diff > -44.5
             return 0.5333333333333333 # (0.5333333333333333 out of 1.0)
          end         end       else  # if Blank_diff > 4.5
         return 0.5714285714285714 # (0.5714285714285714 out of 1.0)
      end     end   end )