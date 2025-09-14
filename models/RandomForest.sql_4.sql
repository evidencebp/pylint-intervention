create or replace function RandomForest_4 (low_McCabe_max_before int64, LLOC_before int64, low_McCabe_sum_diff int64, modified_McCabe_max_diff int64, bugs_diff int64, McCabe_max_before int64, Single comments_before int64, prev_count_y int64, added_lines int64, LLOC_diff int64, N2_diff int64, added_functions int64, prev_count int64, too-many-boolean-expressions int64, SLOC_diff int64, mostly_delete int64, time_diff int64, calculated_length_diff int64, McCabe_max_after int64, Comments_diff int64, line-too-long int64, McCabe_sum_after int64, one_file_fix_rate_diff int64, h1_diff int64, high_McCabe_max_diff int64, too-many-branches int64, SLOC_before int64, cur_count_y int64, prev_count_x int64, McCabe_sum_before int64, Comments_after int64, wildcard-import int64, unnecessary-semicolon int64, same_day_duration_avg_diff int64, effort_diff int64, too-many-statements int64, broad-exception-caught int64, LOC_before int64, cur_count int64, Comments_before int64, using-constant-test int64, LOC_diff int64, high_McCabe_sum_diff int64, only_removal int64, superfluous-parens int64, try-except-raise int64, Blank_before int64, McCabe_max_diff int64, N1_diff int64, massive_change int64, refactor_mle_diff int64, pointless-statement int64, too-many-lines int64, simplifiable-if-statement int64, high_McCabe_sum_before int64, vocabulary_diff int64, removed_lines int64, difficulty_diff int64, Simplify-boolean-expression int64, avg_coupling_code_size_cut_diff int64, Single comments_after int64, low_ccp_group int64, Multi_diff int64, is_refactor int64, hunks_num int64, Single comments_diff int64, length_diff int64, unnecessary-pass int64, Blank_diff int64, h2_diff int64, changed_lines int64, cur_count_x int64, low_McCabe_max_diff int64, high_McCabe_max_before int64, high_ccp_group int64, too-many-nested-blocks int64, McCabe_sum_diff int64, volume_diff int64, comparison-of-constants int64, too-many-return-statements int64, simplifiable-condition int64, simplifiable-if-expression int64, low_McCabe_sum_before int64) as (
  case when hunks_num <= 11.5 then
    case when mostly_delete <= 0.5 then
      case when Comments_before <= 405.0 then
        case when Comments_after <= 2.5 then
           return 0.875 # (0.875 out of 1.0)
        else  # if Comments_after > 2.5
          case when Blank_before <= 220.0 then
            case when one_file_fix_rate_diff <= 0.4833333343267441 then
              case when length_diff <= -105.0 then
                 return 0.6551724137931034 # (0.6551724137931034 out of 1.0)
              else  # if length_diff > -105.0
                case when N2_diff <= -34.5 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if N2_diff > -34.5
                  case when high_ccp_group <= 0.5 then
                    case when McCabe_sum_diff <= -0.5 then
                      case when added_lines <= 27.0 then
                         return 0.68 # (0.68 out of 1.0)
                      else  # if added_lines > 27.0
                        case when low_ccp_group <= 0.5 then
                          case when removed_lines <= 15.0 then
                             return 0.07142857142857142 # (0.07142857142857142 out of 1.0)
                          else  # if removed_lines > 15.0
                             return 0.75 # (0.75 out of 1.0)
                          end                         else  # if low_ccp_group > 0.5
                           return 0.07692307692307693 # (0.07692307692307693 out of 1.0)
                        end                       end                     else  # if McCabe_sum_diff > -0.5
                      case when McCabe_max_before <= 7.5 then
                         return 0.4444444444444444 # (0.4444444444444444 out of 1.0)
                      else  # if McCabe_max_before > 7.5
                        case when refactor_mle_diff <= -0.007477590348571539 then
                           return 0.21621621621621623 # (0.21621621621621623 out of 1.0)
                        else  # if refactor_mle_diff > -0.007477590348571539
                          case when avg_coupling_code_size_cut_diff <= 0.7100160121917725 then
                             return 0.034482758620689655 # (0.034482758620689655 out of 1.0)
                          else  # if avg_coupling_code_size_cut_diff > 0.7100160121917725
                             return 0.125 # (0.125 out of 1.0)
                          end                         end                       end                     end                   else  # if high_ccp_group > 0.5
                    case when removed_lines <= 11.5 then
                       return 0.6363636363636364 # (0.6363636363636364 out of 1.0)
                    else  # if removed_lines > 11.5
                       return 0.96 # (0.96 out of 1.0)
                    end                   end                 end               end             else  # if one_file_fix_rate_diff > 0.4833333343267441
               return 0.8125 # (0.8125 out of 1.0)
            end           else  # if Blank_before > 220.0
            case when avg_coupling_code_size_cut_diff <= -0.5371621549129486 then
              case when Blank_before <= 298.5 then
                 return 0.8235294117647058 # (0.8235294117647058 out of 1.0)
              else  # if Blank_before > 298.5
                 return 1.0 # (1.0 out of 1.0)
              end             else  # if avg_coupling_code_size_cut_diff > -0.5371621549129486
              case when Blank_before <= 272.0 then
                 return 0.9285714285714286 # (0.9285714285714286 out of 1.0)
              else  # if Blank_before > 272.0
                case when added_lines <= 22.5 then
                   return 0.4 # (0.4 out of 1.0)
                else  # if added_lines > 22.5
                   return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
                end               end             end           end         end       else  # if Comments_before > 405.0
         return 0.0 # (0.0 out of 1.0)
      end     else  # if mostly_delete > 0.5
      case when McCabe_sum_after <= 94.0 then
         return 0.8974358974358975 # (0.8974358974358975 out of 1.0)
      else  # if McCabe_sum_after > 94.0
         return 0.35714285714285715 # (0.35714285714285715 out of 1.0)
      end     end   else  # if hunks_num > 11.5
    case when McCabe_max_after <= 18.5 then
      case when Single comments_after <= 58.5 then
         return 0.7619047619047619 # (0.7619047619047619 out of 1.0)
      else  # if Single comments_after > 58.5
         return 0.16666666666666666 # (0.16666666666666666 out of 1.0)
      end     else  # if McCabe_max_after > 18.5
      case when Single comments_before <= 71.5 then
        case when N1_diff <= -2.0 then
           return 0.1875 # (0.1875 out of 1.0)
        else  # if N1_diff > -2.0
           return 0.42857142857142855 # (0.42857142857142855 out of 1.0)
        end       else  # if Single comments_before > 71.5
        case when Blank_before <= 265.0 then
           return 0.0 # (0.0 out of 1.0)
        else  # if Blank_before > 265.0
           return 0.25 # (0.25 out of 1.0)
        end       end     end   end )