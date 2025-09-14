create or replace function RandomForest_2 (prev_count int64, prev_count_x int64, prev_count_y int64, using-constant-test int64, Comments_diff int64, massive_change int64, McCabe_max_after int64, Comments_before int64, too-many-statements int64, cur_count_x int64, h1_diff int64, McCabe_sum_diff int64, LLOC_before int64, McCabe_sum_before int64, high_McCabe_max_before int64, avg_coupling_code_size_cut_diff int64, is_refactor int64, N2_diff int64, too-many-branches int64, SLOC_before int64, too-many-nested-blocks int64, too-many-lines int64, bugs_diff int64, time_diff int64, Single comments_after int64, simplifiable-condition int64, Multi_diff int64, high_McCabe_sum_before int64, low_ccp_group int64, refactor_mle_diff int64, low_McCabe_max_diff int64, SLOC_diff int64, changed_lines int64, hunks_num int64, McCabe_sum_after int64, cur_count_y int64, one_file_fix_rate_diff int64, low_McCabe_sum_before int64, modified_McCabe_max_diff int64, superfluous-parens int64, mostly_delete int64, added_functions int64, Comments_after int64, N1_diff int64, McCabe_max_diff int64, simplifiable-if-statement int64, LOC_before int64, low_McCabe_max_before int64, McCabe_max_before int64, try-except-raise int64, line-too-long int64, unnecessary-semicolon int64, wildcard-import int64, difficulty_diff int64, Simplify-boolean-expression int64, cur_count int64, low_McCabe_sum_diff int64, pointless-statement int64, length_diff int64, broad-exception-caught int64, h2_diff int64, high_McCabe_sum_diff int64, only_removal int64, comparison-of-constants int64, Single comments_diff int64, too-many-boolean-expressions int64, Blank_before int64, calculated_length_diff int64, Single comments_before int64, removed_lines int64, simplifiable-if-expression int64, LOC_diff int64, volume_diff int64, high_McCabe_max_diff int64, high_ccp_group int64, same_day_duration_avg_diff int64, Blank_diff int64, effort_diff int64, too-many-return-statements int64, added_lines int64, unnecessary-pass int64, vocabulary_diff int64, LLOC_diff int64) as (
  case when McCabe_max_before <= 5.5 then
    case when Comments_before <= 88.5 then
      case when LOC_before <= 130.5 then
         return 1.0 # (1.0 out of 1.0)
      else  # if LOC_before > 130.5
        case when changed_lines <= 61.5 then
           return 0.8636363636363636 # (0.8636363636363636 out of 1.0)
        else  # if changed_lines > 61.5
           return 0.4666666666666667 # (0.4666666666666667 out of 1.0)
        end       end     else  # if Comments_before > 88.5
       return 0.3076923076923077 # (0.3076923076923077 out of 1.0)
    end   else  # if McCabe_max_before > 5.5
    case when h2_diff <= -51.0 then
      case when LLOC_before <= 680.0 then
         return 0.92 # (0.92 out of 1.0)
      else  # if LLOC_before > 680.0
         return 0.5217391304347826 # (0.5217391304347826 out of 1.0)
      end     else  # if h2_diff > -51.0
      case when same_day_duration_avg_diff <= 272.75 then
        case when low_ccp_group <= 0.5 then
          case when McCabe_max_after <= 39.0 then
            case when Comments_after <= 35.5 then
              case when changed_lines <= 161.0 then
                case when McCabe_sum_diff <= -0.5 then
                  case when McCabe_max_after <= 10.5 then
                     return 0.6470588235294118 # (0.6470588235294118 out of 1.0)
                  else  # if McCabe_max_after > 10.5
                     return 0.9285714285714286 # (0.9285714285714286 out of 1.0)
                  end                 else  # if McCabe_sum_diff > -0.5
                  case when same_day_duration_avg_diff <= 5.288182020187378 then
                    case when added_lines <= 11.0 then
                       return 0.8461538461538461 # (0.8461538461538461 out of 1.0)
                    else  # if added_lines > 11.0
                       return 0.631578947368421 # (0.631578947368421 out of 1.0)
                    end                   else  # if same_day_duration_avg_diff > 5.288182020187378
                     return 0.2 # (0.2 out of 1.0)
                  end                 end               else  # if changed_lines > 161.0
                 return 0.8421052631578947 # (0.8421052631578947 out of 1.0)
              end             else  # if Comments_after > 35.5
              case when McCabe_sum_after <= 159.5 then
                case when avg_coupling_code_size_cut_diff <= -0.0357142873108387 then
                  case when changed_lines <= 47.0 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if changed_lines > 47.0
                     return 0.0625 # (0.0625 out of 1.0)
                  end                 else  # if avg_coupling_code_size_cut_diff > -0.0357142873108387
                  case when modified_McCabe_max_diff <= -0.5 then
                     return 0.4 # (0.4 out of 1.0)
                  else  # if modified_McCabe_max_diff > -0.5
                     return 0.2222222222222222 # (0.2222222222222222 out of 1.0)
                  end                 end               else  # if McCabe_sum_after > 159.5
                case when McCabe_sum_diff <= -2.0 then
                  case when Single comments_diff <= -0.5 then
                     return 0.5 # (0.5 out of 1.0)
                  else  # if Single comments_diff > -0.5
                     return 0.13636363636363635 # (0.13636363636363635 out of 1.0)
                  end                 else  # if McCabe_sum_diff > -2.0
                  case when Comments_after <= 85.5 then
                     return 0.875 # (0.875 out of 1.0)
                  else  # if Comments_after > 85.5
                     return 0.625 # (0.625 out of 1.0)
                  end                 end               end             end           else  # if McCabe_max_after > 39.0
            case when refactor_mle_diff <= 0.06791515089571476 then
              case when LLOC_before <= 1162.5 then
                 return 0.5333333333333333 # (0.5333333333333333 out of 1.0)
              else  # if LLOC_before > 1162.5
                 return 0.9230769230769231 # (0.9230769230769231 out of 1.0)
              end             else  # if refactor_mle_diff > 0.06791515089571476
               return 1.0 # (1.0 out of 1.0)
            end           end         else  # if low_ccp_group > 0.5
          case when McCabe_sum_diff <= 0.5 then
            case when N1_diff <= -0.5 then
              case when refactor_mle_diff <= -0.09301017224788666 then
                 return 0.06666666666666667 # (0.06666666666666667 out of 1.0)
              else  # if refactor_mle_diff > -0.09301017224788666
                 return 0.0 # (0.0 out of 1.0)
              end             else  # if N1_diff > -0.5
              case when Comments_after <= 63.0 then
                 return 0.2857142857142857 # (0.2857142857142857 out of 1.0)
              else  # if Comments_after > 63.0
                 return 0.09523809523809523 # (0.09523809523809523 out of 1.0)
              end             end           else  # if McCabe_sum_diff > 0.5
            case when Comments_after <= 231.0 then
               return 0.0 # (0.0 out of 1.0)
            else  # if Comments_after > 231.0
               return 0.8181818181818182 # (0.8181818181818182 out of 1.0)
            end           end         end       else  # if same_day_duration_avg_diff > 272.75
         return 0.0 # (0.0 out of 1.0)
      end     end   end )