create or replace function RandomForest_9 (h1_diff int64, simplifiable-if-statement int64, McCabe_max_after int64, McCabe_sum_before int64, Single comments_before int64, low_McCabe_max_diff int64, high_ccp_group int64, pointless-statement int64, too-many-branches int64, high_McCabe_max_before int64, superfluous-parens int64, Multi_diff int64, wildcard-import int64, high_McCabe_sum_before int64, LLOC_before int64, cur_count int64, unnecessary-semicolon int64, Comments_after int64, mostly_delete int64, simplifiable-condition int64, avg_coupling_code_size_cut_diff int64, added_functions int64, McCabe_max_diff int64, McCabe_sum_diff int64, LLOC_diff int64, LOC_before int64, Comments_diff int64, prev_count_x int64, effort_diff int64, try-except-raise int64, difficulty_diff int64, line-too-long int64, Simplify-boolean-expression int64, SLOC_diff int64, McCabe_sum_after int64, refactor_mle_diff int64, one_file_fix_rate_diff int64, is_refactor int64, too-many-lines int64, too-many-boolean-expressions int64, Single comments_diff int64, low_McCabe_sum_diff int64, cur_count_y int64, comparison-of-constants int64, Comments_before int64, too-many-return-statements int64, vocabulary_diff int64, massive_change int64, hunks_num int64, modified_McCabe_max_diff int64, high_McCabe_sum_diff int64, N2_diff int64, broad-exception-caught int64, length_diff int64, unnecessary-pass int64, time_diff int64, changed_lines int64, Single comments_after int64, h2_diff int64, low_McCabe_sum_before int64, cur_count_x int64, McCabe_max_before int64, using-constant-test int64, added_lines int64, same_day_duration_avg_diff int64, prev_count_y int64, Blank_diff int64, LOC_diff int64, only_removal int64, low_McCabe_max_before int64, bugs_diff int64, too-many-statements int64, simplifiable-if-expression int64, calculated_length_diff int64, volume_diff int64, Blank_before int64, high_McCabe_max_diff int64, SLOC_before int64, too-many-nested-blocks int64, removed_lines int64, low_ccp_group int64, N1_diff int64, prev_count int64) as (
  case when McCabe_max_before <= 15.5 then
    case when added_lines <= 1.5 then
      case when same_day_duration_avg_diff <= 9.435490608215332 then
         return 0.36363636363636365 # (0.36363636363636365 out of 1.0)
      else  # if same_day_duration_avg_diff > 9.435490608215332
         return 0.967741935483871 # (0.967741935483871 out of 1.0)
      end     else  # if added_lines > 1.5
      case when low_ccp_group <= 0.5 then
        case when same_day_duration_avg_diff <= -124.86651992797852 then
           return 0.9090909090909091 # (0.9090909090909091 out of 1.0)
        else  # if same_day_duration_avg_diff > -124.86651992797852
          case when Comments_before <= 51.5 then
            case when removed_lines <= 6.5 then
               return 0.30434782608695654 # (0.30434782608695654 out of 1.0)
            else  # if removed_lines > 6.5
              case when Comments_diff <= -0.5 then
                 return 0.9090909090909091 # (0.9090909090909091 out of 1.0)
              else  # if Comments_diff > -0.5
                 return 0.6285714285714286 # (0.6285714285714286 out of 1.0)
              end             end           else  # if Comments_before > 51.5
             return 0.19047619047619047 # (0.19047619047619047 out of 1.0)
          end         end       else  # if low_ccp_group > 0.5
        case when h1_diff <= -1.5 then
           return 0.631578947368421 # (0.631578947368421 out of 1.0)
        else  # if h1_diff > -1.5
          case when McCabe_max_after <= 8.0 then
             return 0.15384615384615385 # (0.15384615384615385 out of 1.0)
          else  # if McCabe_max_after > 8.0
             return 0.03333333333333333 # (0.03333333333333333 out of 1.0)
          end         end       end     end   else  # if McCabe_max_before > 15.5
    case when one_file_fix_rate_diff <= -0.049603176303207874 then
      case when McCabe_sum_after <= 142.5 then
        case when h1_diff <= -2.0 then
           return 0.55 # (0.55 out of 1.0)
        else  # if h1_diff > -2.0
          case when changed_lines <= 113.5 then
             return 0.0 # (0.0 out of 1.0)
          else  # if changed_lines > 113.5
             return 0.4090909090909091 # (0.4090909090909091 out of 1.0)
          end         end       else  # if McCabe_sum_after > 142.5
        case when N1_diff <= -0.5 then
          case when N2_diff <= -26.0 then
             return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
          else  # if N2_diff > -26.0
             return 0.35714285714285715 # (0.35714285714285715 out of 1.0)
          end         else  # if N1_diff > -0.5
          case when Comments_before <= 89.5 then
             return 0.9333333333333333 # (0.9333333333333333 out of 1.0)
          else  # if Comments_before > 89.5
             return 0.5333333333333333 # (0.5333333333333333 out of 1.0)
          end         end       end     else  # if one_file_fix_rate_diff > -0.049603176303207874
      case when McCabe_max_before <= 37.5 then
        case when refactor_mle_diff <= -0.3347773551940918 then
           return 0.625 # (0.625 out of 1.0)
        else  # if refactor_mle_diff > -0.3347773551940918
          case when Comments_diff <= -7.5 then
             return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
          else  # if Comments_diff > -7.5
            case when Comments_after <= 18.0 then
               return 0.043478260869565216 # (0.043478260869565216 out of 1.0)
            else  # if Comments_after > 18.0
              case when Blank_before <= 145.0 then
                case when length_diff <= -34.5 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if length_diff > -34.5
                   return 0.5172413793103449 # (0.5172413793103449 out of 1.0)
                end               else  # if Blank_before > 145.0
                case when low_ccp_group <= 0.5 then
                  case when N2_diff <= -4.5 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if N2_diff > -4.5
                     return 0.20833333333333334 # (0.20833333333333334 out of 1.0)
                  end                 else  # if low_ccp_group > 0.5
                   return 0.0 # (0.0 out of 1.0)
                end               end             end           end         end       else  # if McCabe_max_before > 37.5
        case when McCabe_sum_after <= 245.5 then
           return 0.6111111111111112 # (0.6111111111111112 out of 1.0)
        else  # if McCabe_sum_after > 245.5
           return 0.20689655172413793 # (0.20689655172413793 out of 1.0)
        end       end     end   end )