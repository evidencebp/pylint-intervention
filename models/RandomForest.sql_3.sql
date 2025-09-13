create or replace function RandomForest_3 (prev_count int64, simplifiable-if-expression int64, N1_diff int64, cur_count int64, wildcard-import int64, too-many-return-statements int64, low_McCabe_max_diff int64, length_diff int64, volume_diff int64, high_McCabe_sum_diff int64, high_McCabe_max_before int64, simplifiable-condition int64, Blank_before int64, high_ccp_group int64, McCabe_max_before int64, bugs_diff int64, too-many-nested-blocks int64, refactor_mle_diff int64, difficulty_diff int64, LLOC_diff int64, LOC_diff int64, simplifiable-if-statement int64, one_file_fix_rate_diff int64, SLOC_before int64, LOC_before int64, mostly_delete int64, changed_lines int64, Single comments_before int64, removed_lines int64, added_functions int64, h1_diff int64, effort_diff int64, hunks_num int64, Multi_diff int64, same_day_duration_avg_diff int64, N2_diff int64, cur_count_y int64, Comments_diff int64, modified_McCabe_max_diff int64, h2_diff int64, time_diff int64, LLOC_before int64, calculated_length_diff int64, Single comments_after int64, massive_change int64, McCabe_sum_before int64, too-many-boolean-expressions int64, Simplify-boolean-expression int64, line-too-long int64, superfluous-parens int64, low_ccp_group int64, McCabe_max_diff int64, comparison-of-constants int64, high_McCabe_sum_before int64, low_McCabe_sum_diff int64, avg_coupling_code_size_cut_diff int64, is_refactor int64, Single comments_diff int64, unnecessary-semicolon int64, added_lines int64, prev_count_y int64, try-except-raise int64, low_McCabe_sum_before int64, vocabulary_diff int64, too-many-branches int64, McCabe_sum_after int64, broad-exception-caught int64, prev_count_x int64, only_removal int64, McCabe_max_after int64, pointless-statement int64, low_McCabe_max_before int64, too-many-lines int64, McCabe_sum_diff int64, high_McCabe_max_diff int64, using-constant-test int64, SLOC_diff int64, Blank_diff int64, Comments_after int64, cur_count_x int64, unnecessary-pass int64, too-many-statements int64, Comments_before int64) as (
  case when low_ccp_group <= 0.5 then
    case when low_McCabe_sum_before <= 0.5 then
      case when modified_McCabe_max_diff <= -14.5 then
         return 0.9444444444444444 # (0.9444444444444444 out of 1.0)
      else  # if modified_McCabe_max_diff > -14.5
        case when McCabe_max_before <= 51.5 then
          case when superfluous-parens <= 0.5 then
            case when hunks_num <= 11.5 then
              case when hunks_num <= 7.5 then
                case when low_McCabe_max_diff <= 0.5 then
                  case when high_ccp_group <= 0.5 then
                    case when Single comments_after <= 104.5 then
                      case when McCabe_sum_before <= 185.5 then
                        case when Single comments_after <= 26.5 then
                           return 0.8235294117647058 # (0.8235294117647058 out of 1.0)
                        else  # if Single comments_after > 26.5
                           return 0.4 # (0.4 out of 1.0)
                        end                       else  # if McCabe_sum_before > 185.5
                         return 0.3181818181818182 # (0.3181818181818182 out of 1.0)
                      end                     else  # if Single comments_after > 104.5
                       return 0.12 # (0.12 out of 1.0)
                    end                   else  # if high_ccp_group > 0.5
                    case when removed_lines <= 4.5 then
                       return 0.88 # (0.88 out of 1.0)
                    else  # if removed_lines > 4.5
                       return 0.3888888888888889 # (0.3888888888888889 out of 1.0)
                    end                   end                 else  # if low_McCabe_max_diff > 0.5
                  case when hunks_num <= 4.5 then
                     return 0.16666666666666666 # (0.16666666666666666 out of 1.0)
                  else  # if hunks_num > 4.5
                     return 0.2857142857142857 # (0.2857142857142857 out of 1.0)
                  end                 end               else  # if hunks_num > 7.5
                 return 0.8125 # (0.8125 out of 1.0)
              end             else  # if hunks_num > 11.5
              case when McCabe_sum_diff <= -5.5 then
                 return 0.13043478260869565 # (0.13043478260869565 out of 1.0)
              else  # if McCabe_sum_diff > -5.5
                 return 0.36666666666666664 # (0.36666666666666664 out of 1.0)
              end             end           else  # if superfluous-parens > 0.5
            case when McCabe_sum_after <= 214.0 then
              case when same_day_duration_avg_diff <= 4.222706854343414 then
                 return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
              else  # if same_day_duration_avg_diff > 4.222706854343414
                 return 0.4117647058823529 # (0.4117647058823529 out of 1.0)
              end             else  # if McCabe_sum_after > 214.0
               return 0.9285714285714286 # (0.9285714285714286 out of 1.0)
            end           end         else  # if McCabe_max_before > 51.5
           return 0.85 # (0.85 out of 1.0)
        end       end     else  # if low_McCabe_sum_before > 0.5
      case when Comments_before <= 32.5 then
        case when LOC_diff <= -7.0 then
           return 0.5454545454545454 # (0.5454545454545454 out of 1.0)
        else  # if LOC_diff > -7.0
          case when LOC_diff <= 3.5 then
            case when same_day_duration_avg_diff <= 0.6089285612106323 then
               return 0.85 # (0.85 out of 1.0)
            else  # if same_day_duration_avg_diff > 0.6089285612106323
               return 0.7058823529411765 # (0.7058823529411765 out of 1.0)
            end           else  # if LOC_diff > 3.5
             return 0.9655172413793104 # (0.9655172413793104 out of 1.0)
          end         end       else  # if Comments_before > 32.5
        case when McCabe_sum_diff <= 0.5 then
           return 0.7368421052631579 # (0.7368421052631579 out of 1.0)
        else  # if McCabe_sum_diff > 0.5
           return 0.14285714285714285 # (0.14285714285714285 out of 1.0)
        end       end     end   else  # if low_ccp_group > 0.5
    case when Single comments_diff <= 18.5 then
      case when Comments_before <= 34.5 then
        case when length_diff <= -1.0 then
           return 0.0 # (0.0 out of 1.0)
        else  # if length_diff > -1.0
           return 0.08333333333333333 # (0.08333333333333333 out of 1.0)
        end       else  # if Comments_before > 34.5
        case when Blank_diff <= -5.5 then
           return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
        else  # if Blank_diff > -5.5
          case when Comments_after <= 75.0 then
             return 0.3 # (0.3 out of 1.0)
          else  # if Comments_after > 75.0
            case when same_day_duration_avg_diff <= 33.235469818115234 then
               return 0.0 # (0.0 out of 1.0)
            else  # if same_day_duration_avg_diff > 33.235469818115234
               return 0.06666666666666667 # (0.06666666666666667 out of 1.0)
            end           end         end       end     else  # if Single comments_diff > 18.5
       return 0.8 # (0.8 out of 1.0)
    end   end )