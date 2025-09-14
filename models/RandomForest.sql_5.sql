create or replace function RandomForest_5 (low_McCabe_max_before int64, LLOC_before int64, low_McCabe_sum_diff int64, modified_McCabe_max_diff int64, bugs_diff int64, McCabe_max_before int64, Single comments_before int64, prev_count_y int64, added_lines int64, LLOC_diff int64, N2_diff int64, added_functions int64, prev_count int64, too-many-boolean-expressions int64, SLOC_diff int64, mostly_delete int64, time_diff int64, calculated_length_diff int64, McCabe_max_after int64, Comments_diff int64, line-too-long int64, McCabe_sum_after int64, one_file_fix_rate_diff int64, h1_diff int64, high_McCabe_max_diff int64, too-many-branches int64, SLOC_before int64, cur_count_y int64, prev_count_x int64, McCabe_sum_before int64, Comments_after int64, wildcard-import int64, unnecessary-semicolon int64, same_day_duration_avg_diff int64, effort_diff int64, too-many-statements int64, broad-exception-caught int64, LOC_before int64, cur_count int64, Comments_before int64, using-constant-test int64, LOC_diff int64, high_McCabe_sum_diff int64, only_removal int64, superfluous-parens int64, try-except-raise int64, Blank_before int64, McCabe_max_diff int64, N1_diff int64, massive_change int64, refactor_mle_diff int64, pointless-statement int64, too-many-lines int64, simplifiable-if-statement int64, high_McCabe_sum_before int64, vocabulary_diff int64, removed_lines int64, difficulty_diff int64, Simplify-boolean-expression int64, avg_coupling_code_size_cut_diff int64, Single comments_after int64, low_ccp_group int64, Multi_diff int64, is_refactor int64, hunks_num int64, Single comments_diff int64, length_diff int64, unnecessary-pass int64, Blank_diff int64, h2_diff int64, changed_lines int64, cur_count_x int64, low_McCabe_max_diff int64, high_McCabe_max_before int64, high_ccp_group int64, too-many-nested-blocks int64, McCabe_sum_diff int64, volume_diff int64, comparison-of-constants int64, too-many-return-statements int64, simplifiable-condition int64, simplifiable-if-expression int64, low_McCabe_sum_before int64) as (
  case when low_ccp_group <= 0.5 then
    case when LLOC_diff <= -23.5 then
      case when Comments_after <= 30.0 then
        case when removed_lines <= 24.0 then
          case when Blank_diff <= -16.0 then
             return 0.14285714285714285 # (0.14285714285714285 out of 1.0)
          else  # if Blank_diff > -16.0
             return 0.0 # (0.0 out of 1.0)
          end         else  # if removed_lines > 24.0
           return 0.46153846153846156 # (0.46153846153846156 out of 1.0)
        end       else  # if Comments_after > 30.0
        case when McCabe_max_after <= 15.5 then
           return 0.7741935483870968 # (0.7741935483870968 out of 1.0)
        else  # if McCabe_max_after > 15.5
          case when Blank_diff <= -27.0 then
             return 0.2631578947368421 # (0.2631578947368421 out of 1.0)
          else  # if Blank_diff > -27.0
            case when Multi_diff <= -2.5 then
               return 0.6153846153846154 # (0.6153846153846154 out of 1.0)
            else  # if Multi_diff > -2.5
               return 0.23076923076923078 # (0.23076923076923078 out of 1.0)
            end           end         end       end     else  # if LLOC_diff > -23.5
      case when same_day_duration_avg_diff <= -123.48900985717773 then
         return 0.9714285714285714 # (0.9714285714285714 out of 1.0)
      else  # if same_day_duration_avg_diff > -123.48900985717773
        case when Blank_before <= 47.5 then
          case when Blank_diff <= 1.5 then
            case when avg_coupling_code_size_cut_diff <= -0.2083333283662796 then
               return 0.8571428571428571 # (0.8571428571428571 out of 1.0)
            else  # if avg_coupling_code_size_cut_diff > -0.2083333283662796
               return 0.6086956521739131 # (0.6086956521739131 out of 1.0)
            end           else  # if Blank_diff > 1.5
             return 1.0 # (1.0 out of 1.0)
          end         else  # if Blank_before > 47.5
          case when N1_diff <= 6.0 then
            case when Comments_diff <= 2.5 then
              case when N2_diff <= 3.0 then
                case when LLOC_diff <= -11.5 then
                   return 0.8636363636363636 # (0.8636363636363636 out of 1.0)
                else  # if LLOC_diff > -11.5
                  case when avg_coupling_code_size_cut_diff <= -0.42499999701976776 then
                    case when same_day_duration_avg_diff <= 16.55951452255249 then
                       return 0.44 # (0.44 out of 1.0)
                    else  # if same_day_duration_avg_diff > 16.55951452255249
                       return 0.15 # (0.15 out of 1.0)
                    end                   else  # if avg_coupling_code_size_cut_diff > -0.42499999701976776
                    case when LLOC_before <= 763.0 then
                      case when Comments_before <= 95.5 then
                        case when McCabe_sum_before <= 77.5 then
                           return 0.8421052631578947 # (0.8421052631578947 out of 1.0)
                        else  # if McCabe_sum_before > 77.5
                          case when SLOC_before <= 472.0 then
                             return 0.2222222222222222 # (0.2222222222222222 out of 1.0)
                          else  # if SLOC_before > 472.0
                             return 0.7222222222222222 # (0.7222222222222222 out of 1.0)
                          end                         end                       else  # if Comments_before > 95.5
                         return 0.8823529411764706 # (0.8823529411764706 out of 1.0)
                      end                     else  # if LLOC_before > 763.0
                       return 0.37037037037037035 # (0.37037037037037035 out of 1.0)
                    end                   end                 end               else  # if N2_diff > 3.0
                 return 0.9375 # (0.9375 out of 1.0)
              end             else  # if Comments_diff > 2.5
               return 0.07692307692307693 # (0.07692307692307693 out of 1.0)
            end           else  # if N1_diff > 6.0
             return 0.2 # (0.2 out of 1.0)
          end         end       end     end   else  # if low_ccp_group > 0.5
    case when Comments_after <= 500.0 then
      case when vocabulary_diff <= -47.5 then
         return 0.7333333333333333 # (0.7333333333333333 out of 1.0)
      else  # if vocabulary_diff > -47.5
        case when changed_lines <= 19.0 then
           return 0.24 # (0.24 out of 1.0)
        else  # if changed_lines > 19.0
          case when LLOC_before <= 617.0 then
            case when LLOC_diff <= -13.5 then
               return 0.08333333333333333 # (0.08333333333333333 out of 1.0)
            else  # if LLOC_diff > -13.5
               return 0.0 # (0.0 out of 1.0)
            end           else  # if LLOC_before > 617.0
             return 0.16666666666666666 # (0.16666666666666666 out of 1.0)
          end         end       end     else  # if Comments_after > 500.0
       return 0.8888888888888888 # (0.8888888888888888 out of 1.0)
    end   end )