create or replace function RandomForest_7 (h1_diff int64, simplifiable-if-statement int64, McCabe_max_after int64, McCabe_sum_before int64, Single comments_before int64, low_McCabe_max_diff int64, high_ccp_group int64, pointless-statement int64, too-many-branches int64, high_McCabe_max_before int64, superfluous-parens int64, Multi_diff int64, wildcard-import int64, high_McCabe_sum_before int64, LLOC_before int64, cur_count int64, unnecessary-semicolon int64, Comments_after int64, mostly_delete int64, simplifiable-condition int64, avg_coupling_code_size_cut_diff int64, added_functions int64, McCabe_max_diff int64, McCabe_sum_diff int64, LLOC_diff int64, LOC_before int64, Comments_diff int64, prev_count_x int64, effort_diff int64, try-except-raise int64, difficulty_diff int64, line-too-long int64, Simplify-boolean-expression int64, SLOC_diff int64, McCabe_sum_after int64, refactor_mle_diff int64, one_file_fix_rate_diff int64, is_refactor int64, too-many-lines int64, too-many-boolean-expressions int64, Single comments_diff int64, low_McCabe_sum_diff int64, cur_count_y int64, comparison-of-constants int64, Comments_before int64, too-many-return-statements int64, vocabulary_diff int64, massive_change int64, hunks_num int64, modified_McCabe_max_diff int64, high_McCabe_sum_diff int64, N2_diff int64, broad-exception-caught int64, length_diff int64, unnecessary-pass int64, time_diff int64, changed_lines int64, Single comments_after int64, h2_diff int64, low_McCabe_sum_before int64, cur_count_x int64, McCabe_max_before int64, using-constant-test int64, added_lines int64, same_day_duration_avg_diff int64, prev_count_y int64, Blank_diff int64, LOC_diff int64, only_removal int64, low_McCabe_max_before int64, bugs_diff int64, too-many-statements int64, simplifiable-if-expression int64, calculated_length_diff int64, volume_diff int64, Blank_before int64, high_McCabe_max_diff int64, SLOC_before int64, too-many-nested-blocks int64, removed_lines int64, low_ccp_group int64, N1_diff int64, prev_count int64) as (
  case when Single comments_diff <= 21.0 then
    case when Comments_diff <= 1.5 then
      case when McCabe_max_after <= 29.5 then
        case when McCabe_sum_after <= 194.0 then
          case when McCabe_sum_diff <= -55.5 then
             return 0.92 # (0.92 out of 1.0)
          else  # if McCabe_sum_diff > -55.5
            case when McCabe_sum_before <= 76.5 then
              case when Blank_diff <= -6.5 then
                 return 0.20833333333333334 # (0.20833333333333334 out of 1.0)
              else  # if Blank_diff > -6.5
                case when McCabe_sum_before <= 38.5 then
                  case when refactor_mle_diff <= -0.15299566835165024 then
                     return 0.08333333333333333 # (0.08333333333333333 out of 1.0)
                  else  # if refactor_mle_diff > -0.15299566835165024
                    case when one_file_fix_rate_diff <= -0.10966810956597328 then
                       return 0.7333333333333333 # (0.7333333333333333 out of 1.0)
                    else  # if one_file_fix_rate_diff > -0.10966810956597328
                      case when Single comments_after <= 10.5 then
                         return 0.5 # (0.5 out of 1.0)
                      else  # if Single comments_after > 10.5
                         return 0.6470588235294118 # (0.6470588235294118 out of 1.0)
                      end                     end                   end                 else  # if McCabe_sum_before > 38.5
                  case when modified_McCabe_max_diff <= -0.5 then
                     return 0.8695652173913043 # (0.8695652173913043 out of 1.0)
                  else  # if modified_McCabe_max_diff > -0.5
                     return 0.64 # (0.64 out of 1.0)
                  end                 end               end             else  # if McCabe_sum_before > 76.5
              case when avg_coupling_code_size_cut_diff <= 0.23427128791809082 then
                case when N2_diff <= -1.0 then
                  case when avg_coupling_code_size_cut_diff <= -0.47708334028720856 then
                     return 0.6 # (0.6 out of 1.0)
                  else  # if avg_coupling_code_size_cut_diff > -0.47708334028720856
                     return 0.1111111111111111 # (0.1111111111111111 out of 1.0)
                  end                 else  # if N2_diff > -1.0
                  case when McCabe_max_after <= 14.5 then
                     return 0.21428571428571427 # (0.21428571428571427 out of 1.0)
                  else  # if McCabe_max_after > 14.5
                     return 0.058823529411764705 # (0.058823529411764705 out of 1.0)
                  end                 end               else  # if avg_coupling_code_size_cut_diff > 0.23427128791809082
                case when refactor_mle_diff <= 0.038500308990478516 then
                   return 0.6896551724137931 # (0.6896551724137931 out of 1.0)
                else  # if refactor_mle_diff > 0.038500308990478516
                   return 0.2916666666666667 # (0.2916666666666667 out of 1.0)
                end               end             end           end         else  # if McCabe_sum_after > 194.0
          case when avg_coupling_code_size_cut_diff <= 0.5691087245941162 then
            case when LOC_diff <= -29.5 then
               return 0.6875 # (0.6875 out of 1.0)
            else  # if LOC_diff > -29.5
              case when Blank_before <= 262.0 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if Blank_before > 262.0
                 return 0.8666666666666667 # (0.8666666666666667 out of 1.0)
              end             end           else  # if avg_coupling_code_size_cut_diff > 0.5691087245941162
             return 0.21428571428571427 # (0.21428571428571427 out of 1.0)
          end         end       else  # if McCabe_max_after > 29.5
        case when SLOC_before <= 945.0 then
          case when LOC_diff <= -17.5 then
             return 0.0 # (0.0 out of 1.0)
          else  # if LOC_diff > -17.5
             return 0.2564102564102564 # (0.2564102564102564 out of 1.0)
          end         else  # if SLOC_before > 945.0
          case when Comments_before <= 179.5 then
             return 0.4 # (0.4 out of 1.0)
          else  # if Comments_before > 179.5
             return 0.30434782608695654 # (0.30434782608695654 out of 1.0)
          end         end       end     else  # if Comments_diff > 1.5
      case when Single comments_before <= 19.5 then
         return 0.375 # (0.375 out of 1.0)
      else  # if Single comments_before > 19.5
        case when Comments_before <= 94.0 then
           return 0.0 # (0.0 out of 1.0)
        else  # if Comments_before > 94.0
          case when LLOC_before <= 607.5 then
             return 0.06666666666666667 # (0.06666666666666667 out of 1.0)
          else  # if LLOC_before > 607.5
             return 0.26666666666666666 # (0.26666666666666666 out of 1.0)
          end         end       end     end   else  # if Single comments_diff > 21.0
     return 0.8421052631578947 # (0.8421052631578947 out of 1.0)
  end )