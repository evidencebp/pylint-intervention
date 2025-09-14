create or replace function RandomForest_1 (low_McCabe_max_before int64, LLOC_before int64, low_McCabe_sum_diff int64, modified_McCabe_max_diff int64, bugs_diff int64, McCabe_max_before int64, Single comments_before int64, prev_count_y int64, added_lines int64, LLOC_diff int64, N2_diff int64, added_functions int64, prev_count int64, too-many-boolean-expressions int64, SLOC_diff int64, mostly_delete int64, time_diff int64, calculated_length_diff int64, McCabe_max_after int64, Comments_diff int64, line-too-long int64, McCabe_sum_after int64, one_file_fix_rate_diff int64, h1_diff int64, high_McCabe_max_diff int64, too-many-branches int64, SLOC_before int64, cur_count_y int64, prev_count_x int64, McCabe_sum_before int64, Comments_after int64, wildcard-import int64, unnecessary-semicolon int64, same_day_duration_avg_diff int64, effort_diff int64, too-many-statements int64, broad-exception-caught int64, LOC_before int64, cur_count int64, Comments_before int64, using-constant-test int64, LOC_diff int64, high_McCabe_sum_diff int64, only_removal int64, superfluous-parens int64, try-except-raise int64, Blank_before int64, McCabe_max_diff int64, N1_diff int64, massive_change int64, refactor_mle_diff int64, pointless-statement int64, too-many-lines int64, simplifiable-if-statement int64, high_McCabe_sum_before int64, vocabulary_diff int64, removed_lines int64, difficulty_diff int64, Simplify-boolean-expression int64, avg_coupling_code_size_cut_diff int64, Single comments_after int64, low_ccp_group int64, Multi_diff int64, is_refactor int64, hunks_num int64, Single comments_diff int64, length_diff int64, unnecessary-pass int64, Blank_diff int64, h2_diff int64, changed_lines int64, cur_count_x int64, low_McCabe_max_diff int64, high_McCabe_max_before int64, high_ccp_group int64, too-many-nested-blocks int64, McCabe_sum_diff int64, volume_diff int64, comparison-of-constants int64, too-many-return-statements int64, simplifiable-condition int64, simplifiable-if-expression int64, low_McCabe_sum_before int64) as (
  case when LOC_before <= 145.5 then
     return 0.9230769230769231 # (0.9230769230769231 out of 1.0)
  else  # if LOC_before > 145.5
    case when changed_lines <= 123.5 then
      case when Comments_before <= 285.5 then
        case when McCabe_sum_diff <= -14.5 then
           return 0.0 # (0.0 out of 1.0)
        else  # if McCabe_sum_diff > -14.5
          case when Comments_before <= 196.5 then
            case when SLOC_before <= 1034.5 then
              case when SLOC_diff <= 0.5 then
                case when SLOC_before <= 748.0 then
                  case when McCabe_max_after <= 6.5 then
                     return 0.6923076923076923 # (0.6923076923076923 out of 1.0)
                  else  # if McCabe_max_after > 6.5
                    case when changed_lines <= 73.5 then
                      case when N2_diff <= -2.5 then
                         return 0.6875 # (0.6875 out of 1.0)
                      else  # if N2_diff > -2.5
                        case when SLOC_before <= 580.5 then
                          case when Blank_before <= 57.0 then
                             return 0.6428571428571429 # (0.6428571428571429 out of 1.0)
                          else  # if Blank_before > 57.0
                             return 0.12 # (0.12 out of 1.0)
                          end                         else  # if SLOC_before > 580.5
                           return 0.8235294117647058 # (0.8235294117647058 out of 1.0)
                        end                       end                     else  # if changed_lines > 73.5
                       return 0.2692307692307692 # (0.2692307692307692 out of 1.0)
                    end                   end                 else  # if SLOC_before > 748.0
                  case when avg_coupling_code_size_cut_diff <= -4.440892098500626e-16 then
                     return 0.06666666666666667 # (0.06666666666666667 out of 1.0)
                  else  # if avg_coupling_code_size_cut_diff > -4.440892098500626e-16
                     return 0.4 # (0.4 out of 1.0)
                  end                 end               else  # if SLOC_diff > 0.5
                case when modified_McCabe_max_diff <= -0.5 then
                   return 0.5 # (0.5 out of 1.0)
                else  # if modified_McCabe_max_diff > -0.5
                  case when changed_lines <= 17.0 then
                     return 0.07407407407407407 # (0.07407407407407407 out of 1.0)
                  else  # if changed_lines > 17.0
                    case when Single comments_after <= 45.5 then
                       return 0.5185185185185185 # (0.5185185185185185 out of 1.0)
                    else  # if Single comments_after > 45.5
                       return 0.0 # (0.0 out of 1.0)
                    end                   end                 end               end             else  # if SLOC_before > 1034.5
               return 0.7916666666666666 # (0.7916666666666666 out of 1.0)
            end           else  # if Comments_before > 196.5
             return 0.14285714285714285 # (0.14285714285714285 out of 1.0)
          end         end       else  # if Comments_before > 285.5
        case when removed_lines <= 61.0 then
           return 0.5263157894736842 # (0.5263157894736842 out of 1.0)
        else  # if removed_lines > 61.0
           return 0.9 # (0.9 out of 1.0)
        end       end     else  # if changed_lines > 123.5
      case when N2_diff <= 12.5 then
        case when low_McCabe_sum_before <= 0.5 then
          case when LOC_before <= 1037.5 then
            case when Single comments_after <= 77.0 then
              case when Multi_diff <= -2.5 then
                 return 0.6923076923076923 # (0.6923076923076923 out of 1.0)
              else  # if Multi_diff > -2.5
                case when N2_diff <= -19.5 then
                   return 0.2222222222222222 # (0.2222222222222222 out of 1.0)
                else  # if N2_diff > -19.5
                   return 0.5714285714285714 # (0.5714285714285714 out of 1.0)
                end               end             else  # if Single comments_after > 77.0
               return 0.0 # (0.0 out of 1.0)
            end           else  # if LOC_before > 1037.5
            case when LLOC_before <= 1657.0 then
              case when LLOC_diff <= -99.5 then
                case when Blank_diff <= -55.5 then
                   return 0.9411764705882353 # (0.9411764705882353 out of 1.0)
                else  # if Blank_diff > -55.5
                   return 0.8125 # (0.8125 out of 1.0)
                end               else  # if LLOC_diff > -99.5
                case when LLOC_diff <= -18.0 then
                   return 0.42857142857142855 # (0.42857142857142855 out of 1.0)
                else  # if LLOC_diff > -18.0
                   return 0.7647058823529411 # (0.7647058823529411 out of 1.0)
                end               end             else  # if LLOC_before > 1657.0
               return 0.26666666666666666 # (0.26666666666666666 out of 1.0)
            end           end         else  # if low_McCabe_sum_before > 0.5
          case when McCabe_max_before <= 10.5 then
             return 0.625 # (0.625 out of 1.0)
          else  # if McCabe_max_before > 10.5
             return 1.0 # (1.0 out of 1.0)
          end         end       else  # if N2_diff > 12.5
         return 0.16666666666666666 # (0.16666666666666666 out of 1.0)
      end     end   end )