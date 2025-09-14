create or replace function RandomForest_6 (prev_count int64, prev_count_x int64, prev_count_y int64, using-constant-test int64, Comments_diff int64, massive_change int64, McCabe_max_after int64, Comments_before int64, too-many-statements int64, cur_count_x int64, h1_diff int64, McCabe_sum_diff int64, LLOC_before int64, McCabe_sum_before int64, high_McCabe_max_before int64, avg_coupling_code_size_cut_diff int64, is_refactor int64, N2_diff int64, too-many-branches int64, SLOC_before int64, too-many-nested-blocks int64, too-many-lines int64, bugs_diff int64, time_diff int64, Single comments_after int64, simplifiable-condition int64, Multi_diff int64, high_McCabe_sum_before int64, low_ccp_group int64, refactor_mle_diff int64, low_McCabe_max_diff int64, SLOC_diff int64, changed_lines int64, hunks_num int64, McCabe_sum_after int64, cur_count_y int64, one_file_fix_rate_diff int64, low_McCabe_sum_before int64, modified_McCabe_max_diff int64, superfluous-parens int64, mostly_delete int64, added_functions int64, Comments_after int64, N1_diff int64, McCabe_max_diff int64, simplifiable-if-statement int64, LOC_before int64, low_McCabe_max_before int64, McCabe_max_before int64, try-except-raise int64, line-too-long int64, unnecessary-semicolon int64, wildcard-import int64, difficulty_diff int64, Simplify-boolean-expression int64, cur_count int64, low_McCabe_sum_diff int64, pointless-statement int64, length_diff int64, broad-exception-caught int64, h2_diff int64, high_McCabe_sum_diff int64, only_removal int64, comparison-of-constants int64, Single comments_diff int64, too-many-boolean-expressions int64, Blank_before int64, calculated_length_diff int64, Single comments_before int64, removed_lines int64, simplifiable-if-expression int64, LOC_diff int64, volume_diff int64, high_McCabe_max_diff int64, high_ccp_group int64, same_day_duration_avg_diff int64, Blank_diff int64, effort_diff int64, too-many-return-statements int64, added_lines int64, unnecessary-pass int64, vocabulary_diff int64, LLOC_diff int64) as (
  case when LOC_before <= 186.0 then
    case when high_ccp_group <= 0.5 then
       return 0.7083333333333334 # (0.7083333333333334 out of 1.0)
    else  # if high_ccp_group > 0.5
       return 1.0 # (1.0 out of 1.0)
    end   else  # if LOC_before > 186.0
    case when low_ccp_group <= 0.5 then
      case when SLOC_diff <= -236.5 then
        case when removed_lines <= 18.0 then
           return 0.17647058823529413 # (0.17647058823529413 out of 1.0)
        else  # if removed_lines > 18.0
           return 0.1111111111111111 # (0.1111111111111111 out of 1.0)
        end       else  # if SLOC_diff > -236.5
        case when avg_coupling_code_size_cut_diff <= -2.6875 then
           return 0.8214285714285714 # (0.8214285714285714 out of 1.0)
        else  # if avg_coupling_code_size_cut_diff > -2.6875
          case when Single comments_after <= 96.5 then
            case when removed_lines <= 67.0 then
              case when high_McCabe_max_before <= 0.5 then
                case when removed_lines <= 0.5 then
                   return 0.3076923076923077 # (0.3076923076923077 out of 1.0)
                else  # if removed_lines > 0.5
                  case when Comments_before <= 62.0 then
                    case when McCabe_max_after <= 7.5 then
                       return 0.8095238095238095 # (0.8095238095238095 out of 1.0)
                    else  # if McCabe_max_after > 7.5
                      case when Blank_diff <= 0.5 then
                        case when McCabe_sum_after <= 65.5 then
                           return 0.7333333333333333 # (0.7333333333333333 out of 1.0)
                        else  # if McCabe_sum_after > 65.5
                          case when refactor_mle_diff <= 0.024753378704190254 then
                             return 0.7037037037037037 # (0.7037037037037037 out of 1.0)
                          else  # if refactor_mle_diff > 0.024753378704190254
                             return 0.19230769230769232 # (0.19230769230769232 out of 1.0)
                          end                         end                       else  # if Blank_diff > 0.5
                         return 0.2727272727272727 # (0.2727272727272727 out of 1.0)
                      end                     end                   else  # if Comments_before > 62.0
                     return 0.875 # (0.875 out of 1.0)
                  end                 end               else  # if high_McCabe_max_before > 0.5
                case when LOC_before <= 967.5 then
                   return 0.6428571428571429 # (0.6428571428571429 out of 1.0)
                else  # if LOC_before > 967.5
                   return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
                end               end             else  # if removed_lines > 67.0
              case when McCabe_sum_before <= 93.0 then
                 return 0.9333333333333333 # (0.9333333333333333 out of 1.0)
              else  # if McCabe_sum_before > 93.0
                case when SLOC_before <= 538.5 then
                   return 0.8421052631578947 # (0.8421052631578947 out of 1.0)
                else  # if SLOC_before > 538.5
                   return 0.65 # (0.65 out of 1.0)
                end               end             end           else  # if Single comments_after > 96.5
            case when removed_lines <= 12.5 then
              case when removed_lines <= 4.5 then
                 return 0.2916666666666667 # (0.2916666666666667 out of 1.0)
              else  # if removed_lines > 4.5
                 return 0.1111111111111111 # (0.1111111111111111 out of 1.0)
              end             else  # if removed_lines > 12.5
              case when high_McCabe_max_before <= 0.5 then
                 return 0.11538461538461539 # (0.11538461538461539 out of 1.0)
              else  # if high_McCabe_max_before > 0.5
                 return 0.625 # (0.625 out of 1.0)
              end             end           end         end       end     else  # if low_ccp_group > 0.5
      case when Single comments_before <= 201.0 then
        case when LLOC_diff <= -42.0 then
           return 0.48148148148148145 # (0.48148148148148145 out of 1.0)
        else  # if LLOC_diff > -42.0
          case when added_lines <= 6.0 then
             return 0.13333333333333333 # (0.13333333333333333 out of 1.0)
          else  # if added_lines > 6.0
            case when same_day_duration_avg_diff <= 114.3605728149414 then
               return 0.0 # (0.0 out of 1.0)
            else  # if same_day_duration_avg_diff > 114.3605728149414
               return 0.11764705882352941 # (0.11764705882352941 out of 1.0)
            end           end         end       else  # if Single comments_before > 201.0
         return 0.6857142857142857 # (0.6857142857142857 out of 1.0)
      end     end   end )