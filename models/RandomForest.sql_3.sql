create or replace function RandomForest_3 (low_McCabe_max_before int64, LLOC_before int64, low_McCabe_sum_diff int64, modified_McCabe_max_diff int64, bugs_diff int64, McCabe_max_before int64, Single comments_before int64, prev_count_y int64, added_lines int64, LLOC_diff int64, N2_diff int64, added_functions int64, prev_count int64, too-many-boolean-expressions int64, SLOC_diff int64, mostly_delete int64, time_diff int64, calculated_length_diff int64, McCabe_max_after int64, Comments_diff int64, line-too-long int64, McCabe_sum_after int64, one_file_fix_rate_diff int64, h1_diff int64, high_McCabe_max_diff int64, too-many-branches int64, SLOC_before int64, cur_count_y int64, prev_count_x int64, McCabe_sum_before int64, Comments_after int64, wildcard-import int64, unnecessary-semicolon int64, same_day_duration_avg_diff int64, effort_diff int64, too-many-statements int64, broad-exception-caught int64, LOC_before int64, cur_count int64, Comments_before int64, using-constant-test int64, LOC_diff int64, high_McCabe_sum_diff int64, only_removal int64, superfluous-parens int64, try-except-raise int64, Blank_before int64, McCabe_max_diff int64, N1_diff int64, massive_change int64, refactor_mle_diff int64, pointless-statement int64, too-many-lines int64, simplifiable-if-statement int64, high_McCabe_sum_before int64, vocabulary_diff int64, removed_lines int64, difficulty_diff int64, Simplify-boolean-expression int64, avg_coupling_code_size_cut_diff int64, Single comments_after int64, low_ccp_group int64, Multi_diff int64, is_refactor int64, hunks_num int64, Single comments_diff int64, length_diff int64, unnecessary-pass int64, Blank_diff int64, h2_diff int64, changed_lines int64, cur_count_x int64, low_McCabe_max_diff int64, high_McCabe_max_before int64, high_ccp_group int64, too-many-nested-blocks int64, McCabe_sum_diff int64, volume_diff int64, comparison-of-constants int64, too-many-return-statements int64, simplifiable-condition int64, simplifiable-if-expression int64, low_McCabe_sum_before int64) as (
  case when Comments_before <= 3.5 then
    case when LLOC_before <= 26.5 then
       return 0.8235294117647058 # (0.8235294117647058 out of 1.0)
    else  # if LLOC_before > 26.5
       return 1.0 # (1.0 out of 1.0)
    end   else  # if Comments_before > 3.5
    case when Single comments_before <= 438.0 then
      case when low_ccp_group <= 0.5 then
        case when added_lines <= 89.5 then
          case when same_day_duration_avg_diff <= -124.79166412353516 then
             return 0.95 # (0.95 out of 1.0)
          else  # if same_day_duration_avg_diff > -124.79166412353516
            case when Single comments_diff <= -2.5 then
              case when McCabe_max_after <= 13.5 then
                 return 0.9545454545454546 # (0.9545454545454546 out of 1.0)
              else  # if McCabe_max_after > 13.5
                 return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
              end             else  # if Single comments_diff > -2.5
              case when added_functions <= 1.5 then
                case when avg_coupling_code_size_cut_diff <= 2.1666666865348816 then
                  case when modified_McCabe_max_diff <= -0.5 then
                    case when McCabe_max_after <= 20.0 then
                       return 0.3125 # (0.3125 out of 1.0)
                    else  # if McCabe_max_after > 20.0
                       return 1.0 # (1.0 out of 1.0)
                    end                   else  # if modified_McCabe_max_diff > -0.5
                    case when Comments_diff <= 3.0 then
                      case when prev_count_x <= 1.5 then
                        case when avg_coupling_code_size_cut_diff <= 0.2809523940086365 then
                          case when avg_coupling_code_size_cut_diff <= -0.0357142873108387 then
                            case when McCabe_sum_before <= 154.5 then
                               return 0.4444444444444444 # (0.4444444444444444 out of 1.0)
                            else  # if McCabe_sum_before > 154.5
                               return 0.2777777777777778 # (0.2777777777777778 out of 1.0)
                            end                           else  # if avg_coupling_code_size_cut_diff > -0.0357142873108387
                            case when McCabe_max_after <= 16.5 then
                               return 1.0 # (1.0 out of 1.0)
                            else  # if McCabe_max_after > 16.5
                               return 0.75 # (0.75 out of 1.0)
                            end                           end                         else  # if avg_coupling_code_size_cut_diff > 0.2809523940086365
                           return 0.23076923076923078 # (0.23076923076923078 out of 1.0)
                        end                       else  # if prev_count_x > 1.5
                         return 0.125 # (0.125 out of 1.0)
                      end                     else  # if Comments_diff > 3.0
                       return 0.0 # (0.0 out of 1.0)
                    end                   end                 else  # if avg_coupling_code_size_cut_diff > 2.1666666865348816
                   return 0.8666666666666667 # (0.8666666666666667 out of 1.0)
                end               else  # if added_functions > 1.5
                 return 0.8076923076923077 # (0.8076923076923077 out of 1.0)
              end             end           end         else  # if added_lines > 89.5
          case when LOC_diff <= -114.5 then
            case when same_day_duration_avg_diff <= -40.66520118713379 then
               return 0.11764705882352941 # (0.11764705882352941 out of 1.0)
            else  # if same_day_duration_avg_diff > -40.66520118713379
              case when Single comments_after <= 54.5 then
                 return 0.8518518518518519 # (0.8518518518518519 out of 1.0)
              else  # if Single comments_after > 54.5
                 return 0.45 # (0.45 out of 1.0)
              end             end           else  # if LOC_diff > -114.5
            case when changed_lines <= 130.5 then
               return 0.05 # (0.05 out of 1.0)
            else  # if changed_lines > 130.5
              case when Blank_before <= 128.5 then
                 return 0.15151515151515152 # (0.15151515151515152 out of 1.0)
              else  # if Blank_before > 128.5
                 return 0.5789473684210527 # (0.5789473684210527 out of 1.0)
              end             end           end         end       else  # if low_ccp_group > 0.5
        case when Blank_diff <= -12.5 then
           return 0.5833333333333334 # (0.5833333333333334 out of 1.0)
        else  # if Blank_diff > -12.5
          case when added_lines <= 12.5 then
            case when Blank_before <= 95.0 then
               return 0.1111111111111111 # (0.1111111111111111 out of 1.0)
            else  # if Blank_before > 95.0
               return 0.3888888888888889 # (0.3888888888888889 out of 1.0)
            end           else  # if added_lines > 12.5
            case when Blank_diff <= -1.5 then
               return 0.08333333333333333 # (0.08333333333333333 out of 1.0)
            else  # if Blank_diff > -1.5
               return 0.0 # (0.0 out of 1.0)
            end           end         end       end     else  # if Single comments_before > 438.0
       return 0.7931034482758621 # (0.7931034482758621 out of 1.0)
    end   end )