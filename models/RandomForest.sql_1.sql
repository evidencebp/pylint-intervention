create or replace function RandomForest_1 (low_McCabe_sum_before int64, changed_lines int64, low_McCabe_max_diff int64, try-except-raise int64, Comments_before int64, high_McCabe_sum_diff int64, low_McCabe_max_before int64, Multi_diff int64, effort_diff int64, difficulty_diff int64, only_removal int64, length_diff int64, comparison-of-constants int64, LOC_diff int64, h2_diff int64, line-too-long int64, h1_diff int64, using-constant-test int64, broad-exception-caught int64, time_diff int64, calculated_length_diff int64, too-many-branches int64, SLOC_before int64, low_ccp_group int64, avg_coupling_code_size_cut_diff int64, new_function int64, wildcard-import int64, McCabe_max_before int64, superfluous-parens int64, low_McCabe_sum_diff int64, pointless-statement int64, one_file_fix_rate_diff int64, cur_count_x int64, same_day_duration_avg_diff int64, too-many-nested-blocks int64, simplifiable-condition int64, too-many-lines int64, SLOC_diff int64, cur_count_y int64, LLOC_before int64, Comments_after int64, high_ccp_group int64, bugs_diff int64, unnecessary-pass int64, prev_count_x int64, massive_change int64, McCabe_max_after int64, removed_lines int64, Comments_diff int64, Single comments_diff int64, too-many-statements int64, Simplify-boolean-expression int64, is_refactor int64, refactor_mle_diff int64, added_lines int64, mostly_delete int64, volume_diff int64, too-many-boolean-expressions int64, N2_diff int64, Blank_before int64, vocabulary_diff int64, McCabe_sum_before int64, high_McCabe_sum_before int64, N1_diff int64, LOC_before int64, LLOC_diff int64, high_McCabe_max_diff int64, simplifiable-if-statement int64, prev_count_y int64, hunks_num int64, Blank_diff int64, prev_count int64, Single comments_before int64, McCabe_max_diff int64, McCabe_sum_diff int64, modified_McCabe_max_diff int64, McCabe_sum_after int64, too-many-return-statements int64, Single comments_after int64, unnecessary-semicolon int64, added_functions int64, cur_count int64, simplifiable-if-expression int64, high_McCabe_max_before int64) as (
  case when low_ccp_group <= 0.5 then
    case when Single comments_diff <= 2.5 then
      case when Single comments_after <= 47.5 then
        case when Single comments_after <= 3.5 then
          case when one_file_fix_rate_diff <= -0.00657894741743803 then
             return 1.0 # (1.0 out of 1.0)
          else  # if one_file_fix_rate_diff > -0.00657894741743803
             return 0.9090909090909091 # (0.9090909090909091 out of 1.0)
          end         else  # if Single comments_after > 3.5
          case when added_lines <= 31.5 then
            case when length_diff <= -1.5 then
               return 0.875 # (0.875 out of 1.0)
            else  # if length_diff > -1.5
              case when Comments_before <= 25.5 then
                case when changed_lines <= 5.5 then
                   return 0.5 # (0.5 out of 1.0)
                else  # if changed_lines > 5.5
                   return 0.6086956521739131 # (0.6086956521739131 out of 1.0)
                end               else  # if Comments_before > 25.5
                 return 0.2692307692307692 # (0.2692307692307692 out of 1.0)
              end             end           else  # if added_lines > 31.5
            case when SLOC_before <= 524.5 then
              case when Single comments_after <= 20.0 then
                 return 0.6956521739130435 # (0.6956521739130435 out of 1.0)
              else  # if Single comments_after > 20.0
                case when Comments_before <= 33.0 then
                   return 1.0 # (1.0 out of 1.0)
                else  # if Comments_before > 33.0
                   return 0.9375 # (0.9375 out of 1.0)
                end               end             else  # if SLOC_before > 524.5
              case when LOC_before <= 1083.5 then
                case when LOC_before <= 989.5 then
                   return 0.5 # (0.5 out of 1.0)
                else  # if LOC_before > 989.5
                   return 0.16666666666666666 # (0.16666666666666666 out of 1.0)
                end               else  # if LOC_before > 1083.5
                 return 0.8620689655172413 # (0.8620689655172413 out of 1.0)
              end             end           end         end       else  # if Single comments_after > 47.5
        case when Single comments_after <= 123.5 then
          case when Comments_before <= 124.0 then
            case when McCabe_sum_after <= 80.5 then
               return 0.6842105263157895 # (0.6842105263157895 out of 1.0)
            else  # if McCabe_sum_after > 80.5
              case when McCabe_sum_diff <= -3.5 then
                case when LLOC_before <= 647.5 then
                   return 0.043478260869565216 # (0.043478260869565216 out of 1.0)
                else  # if LLOC_before > 647.5
                   return 0.11764705882352941 # (0.11764705882352941 out of 1.0)
                end               else  # if McCabe_sum_diff > -3.5
                case when McCabe_max_after <= 18.0 then
                   return 0.5714285714285714 # (0.5714285714285714 out of 1.0)
                else  # if McCabe_max_after > 18.0
                   return 0.08695652173913043 # (0.08695652173913043 out of 1.0)
                end               end             end           else  # if Comments_before > 124.0
             return 0.6875 # (0.6875 out of 1.0)
          end         else  # if Single comments_after > 123.5
          case when high_ccp_group <= 0.5 then
            case when LLOC_before <= 1531.0 then
               return 0.8076923076923077 # (0.8076923076923077 out of 1.0)
            else  # if LLOC_before > 1531.0
               return 0.42857142857142855 # (0.42857142857142855 out of 1.0)
            end           else  # if high_ccp_group > 0.5
             return 0.8461538461538461 # (0.8461538461538461 out of 1.0)
          end         end       end     else  # if Single comments_diff > 2.5
      case when McCabe_sum_diff <= 1.0 then
         return 0.10714285714285714 # (0.10714285714285714 out of 1.0)
      else  # if McCabe_sum_diff > 1.0
         return 0.375 # (0.375 out of 1.0)
      end     end   else  # if low_ccp_group > 0.5
    case when Multi_diff <= -15.0 then
       return 0.7777777777777778 # (0.7777777777777778 out of 1.0)
    else  # if Multi_diff > -15.0
      case when h1_diff <= 0.5 then
        case when McCabe_sum_after <= 33.5 then
           return 0.3157894736842105 # (0.3157894736842105 out of 1.0)
        else  # if McCabe_sum_after > 33.5
          case when Single comments_after <= 182.5 then
            case when McCabe_sum_after <= 116.5 then
              case when LOC_before <= 454.0 then
                 return 0.06666666666666667 # (0.06666666666666667 out of 1.0)
              else  # if LOC_before > 454.0
                 return 0.0 # (0.0 out of 1.0)
              end             else  # if McCabe_sum_after > 116.5
               return 0.0 # (0.0 out of 1.0)
            end           else  # if Single comments_after > 182.5
             return 0.21052631578947367 # (0.21052631578947367 out of 1.0)
          end         end       else  # if h1_diff > 0.5
         return 0.8125 # (0.8125 out of 1.0)
      end     end   end )