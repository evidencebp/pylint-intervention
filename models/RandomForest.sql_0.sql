create or replace function RandomForest_0 (low_McCabe_sum_before int64, changed_lines int64, low_McCabe_max_diff int64, try-except-raise int64, Comments_before int64, high_McCabe_sum_diff int64, low_McCabe_max_before int64, Multi_diff int64, effort_diff int64, difficulty_diff int64, only_removal int64, length_diff int64, comparison-of-constants int64, LOC_diff int64, h2_diff int64, line-too-long int64, h1_diff int64, using-constant-test int64, broad-exception-caught int64, time_diff int64, calculated_length_diff int64, too-many-branches int64, SLOC_before int64, low_ccp_group int64, avg_coupling_code_size_cut_diff int64, new_function int64, wildcard-import int64, McCabe_max_before int64, superfluous-parens int64, low_McCabe_sum_diff int64, pointless-statement int64, one_file_fix_rate_diff int64, cur_count_x int64, same_day_duration_avg_diff int64, too-many-nested-blocks int64, simplifiable-condition int64, too-many-lines int64, SLOC_diff int64, cur_count_y int64, LLOC_before int64, Comments_after int64, high_ccp_group int64, bugs_diff int64, unnecessary-pass int64, prev_count_x int64, massive_change int64, McCabe_max_after int64, removed_lines int64, Comments_diff int64, Single comments_diff int64, too-many-statements int64, Simplify-boolean-expression int64, is_refactor int64, refactor_mle_diff int64, added_lines int64, mostly_delete int64, volume_diff int64, too-many-boolean-expressions int64, N2_diff int64, Blank_before int64, vocabulary_diff int64, McCabe_sum_before int64, high_McCabe_sum_before int64, N1_diff int64, LOC_before int64, LLOC_diff int64, high_McCabe_max_diff int64, simplifiable-if-statement int64, prev_count_y int64, hunks_num int64, Blank_diff int64, prev_count int64, Single comments_before int64, McCabe_max_diff int64, McCabe_sum_diff int64, modified_McCabe_max_diff int64, McCabe_sum_after int64, too-many-return-statements int64, Single comments_after int64, unnecessary-semicolon int64, added_functions int64, cur_count int64, simplifiable-if-expression int64, high_McCabe_max_before int64) as (
  case when McCabe_sum_after <= 59.5 then
    case when Comments_after <= 74.5 then
      case when refactor_mle_diff <= 0.272966668009758 then
        case when N2_diff <= -0.5 then
          case when avg_coupling_code_size_cut_diff <= -0.4996212273836136 then
             return 0.7916666666666666 # (0.7916666666666666 out of 1.0)
          else  # if avg_coupling_code_size_cut_diff > -0.4996212273836136
            case when SLOC_diff <= -17.5 then
               return 0.5 # (0.5 out of 1.0)
            else  # if SLOC_diff > -17.5
               return 0.3076923076923077 # (0.3076923076923077 out of 1.0)
            end           end         else  # if N2_diff > -0.5
          case when Single comments_diff <= -1.0 then
             return 0.9411764705882353 # (0.9411764705882353 out of 1.0)
          else  # if Single comments_diff > -1.0
            case when McCabe_sum_after <= 21.0 then
              case when changed_lines <= 5.5 then
                 return 0.8095238095238095 # (0.8095238095238095 out of 1.0)
              else  # if changed_lines > 5.5
                 return 0.8125 # (0.8125 out of 1.0)
              end             else  # if McCabe_sum_after > 21.0
               return 0.4482758620689655 # (0.4482758620689655 out of 1.0)
            end           end         end       else  # if refactor_mle_diff > 0.272966668009758
         return 0.95 # (0.95 out of 1.0)
      end     else  # if Comments_after > 74.5
       return 0.11538461538461539 # (0.11538461538461539 out of 1.0)
    end   else  # if McCabe_sum_after > 59.5
    case when Single comments_after <= 186.5 then
      case when LOC_before <= 410.0 then
         return 0.7142857142857143 # (0.7142857142857143 out of 1.0)
      else  # if LOC_before > 410.0
        case when modified_McCabe_max_diff <= -0.5 then
          case when Single comments_after <= 59.0 then
            case when McCabe_max_diff <= -5.5 then
               return 0.4 # (0.4 out of 1.0)
            else  # if McCabe_max_diff > -5.5
              case when Comments_diff <= -7.5 then
                 return 0.8823529411764706 # (0.8823529411764706 out of 1.0)
              else  # if Comments_diff > -7.5
                case when Comments_after <= 38.0 then
                   return 0.5 # (0.5 out of 1.0)
                else  # if Comments_after > 38.0
                   return 0.7333333333333333 # (0.7333333333333333 out of 1.0)
                end               end             end           else  # if Single comments_after > 59.0
            case when SLOC_diff <= -9.0 then
               return 0.034482758620689655 # (0.034482758620689655 out of 1.0)
            else  # if SLOC_diff > -9.0
              case when h2_diff <= -0.5 then
                 return 0.17391304347826086 # (0.17391304347826086 out of 1.0)
              else  # if h2_diff > -0.5
                 return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
              end             end           end         else  # if modified_McCabe_max_diff > -0.5
          case when LOC_diff <= -91.5 then
             return 0.6428571428571429 # (0.6428571428571429 out of 1.0)
          else  # if LOC_diff > -91.5
            case when Comments_before <= 25.0 then
              case when same_day_duration_avg_diff <= -10.94916582107544 then
                 return 0.6 # (0.6 out of 1.0)
              else  # if same_day_duration_avg_diff > -10.94916582107544
                 return 0.23529411764705882 # (0.23529411764705882 out of 1.0)
              end             else  # if Comments_before > 25.0
              case when hunks_num <= 3.5 then
                case when Comments_after <= 66.5 then
                   return 0.32142857142857145 # (0.32142857142857145 out of 1.0)
                else  # if Comments_after > 66.5
                   return 0.125 # (0.125 out of 1.0)
                end               else  # if hunks_num > 3.5
                case when low_ccp_group <= 0.5 then
                  case when one_file_fix_rate_diff <= -0.1785714328289032 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if one_file_fix_rate_diff > -0.1785714328289032
                    case when McCabe_sum_before <= 182.5 then
                       return 0.2916666666666667 # (0.2916666666666667 out of 1.0)
                    else  # if McCabe_sum_before > 182.5
                       return 0.0 # (0.0 out of 1.0)
                    end                   end                 else  # if low_ccp_group > 0.5
                   return 0.0 # (0.0 out of 1.0)
                end               end             end           end         end       end     else  # if Single comments_after > 186.5
      case when avg_coupling_code_size_cut_diff <= -0.4300193041563034 then
         return 0.9333333333333333 # (0.9333333333333333 out of 1.0)
      else  # if avg_coupling_code_size_cut_diff > -0.4300193041563034
        case when hunks_num <= 2.5 then
           return 0.9411764705882353 # (0.9411764705882353 out of 1.0)
        else  # if hunks_num > 2.5
           return 0.4482758620689655 # (0.4482758620689655 out of 1.0)
        end       end     end   end )