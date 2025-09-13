create or replace function RandomForest_3 (h1_diff int64, SLOC_before int64, avg_coupling_code_size_cut_diff int64, Multi_diff int64, using-constant-test int64, high_McCabe_sum_diff int64, difficulty_diff int64, LLOC_diff int64, length_diff int64, Comments_after int64, McCabe_max_before int64, low_McCabe_sum_before int64, cur_count int64, LOC_before int64, low_McCabe_max_before int64, massive_change int64, too-many-return-statements int64, Comments_diff int64, added_lines int64, broad-exception-caught int64, comparison-of-constants int64, Single comments_diff int64, refactor_mle_diff int64, prev_count_x int64, McCabe_sum_before int64, modified_McCabe_max_diff int64, Simplify-boolean-expression int64, Blank_diff int64, added_functions int64, LLOC_before int64, cur_count_x int64, high_McCabe_sum_before int64, volume_diff int64, low_McCabe_max_diff int64, LOC_diff int64, calculated_length_diff int64, changed_lines int64, N2_diff int64, h2_diff int64, too-many-lines int64, unnecessary-pass int64, simplifiable-if-statement int64, prev_count int64, too-many-nested-blocks int64, Comments_before int64, SLOC_diff int64, McCabe_sum_after int64, bugs_diff int64, cur_count_y int64, Single comments_after int64, McCabe_max_diff int64, N1_diff int64, wildcard-import int64, McCabe_sum_diff int64, prev_count_y int64, superfluous-parens int64, hunks_num int64, try-except-raise int64, simplifiable-if-expression int64, McCabe_max_after int64, high_McCabe_max_diff int64, too-many-statements int64, simplifiable-condition int64, only_removal int64, unnecessary-semicolon int64, effort_diff int64, is_refactor int64, same_day_duration_avg_diff int64, one_file_fix_rate_diff int64, high_McCabe_max_before int64, vocabulary_diff int64, too-many-branches int64, mostly_delete int64, high_ccp_group int64, low_ccp_group int64, removed_lines int64, Single comments_before int64, low_McCabe_sum_diff int64, time_diff int64, Blank_before int64, line-too-long int64, too-many-boolean-expressions int64, pointless-statement int64) as (
  case when McCabe_max_after <= 19.5 then
    case when low_ccp_group <= 0.5 then
      case when SLOC_before <= 866.0 then
        case when McCabe_max_before <= 5.5 then
           return 1.0 # (1.0 out of 1.0)
        else  # if McCabe_max_before > 5.5
          case when Multi_diff <= -2.5 then
            case when Single comments_before <= 40.0 then
               return 0.42857142857142855 # (0.42857142857142855 out of 1.0)
            else  # if Single comments_before > 40.0
               return 1.0 # (1.0 out of 1.0)
            end           else  # if Multi_diff > -2.5
            case when avg_coupling_code_size_cut_diff <= -0.29999999701976776 then
              case when modified_McCabe_max_diff <= -1.5 then
                 return 0.6818181818181818 # (0.6818181818181818 out of 1.0)
              else  # if modified_McCabe_max_diff > -1.5
                case when SLOC_before <= 388.5 then
                   return 0.1111111111111111 # (0.1111111111111111 out of 1.0)
                else  # if SLOC_before > 388.5
                   return 0.4 # (0.4 out of 1.0)
                end               end             else  # if avg_coupling_code_size_cut_diff > -0.29999999701976776
              case when McCabe_sum_diff <= -5.5 then
                 return 0.35 # (0.35 out of 1.0)
              else  # if McCabe_sum_diff > -5.5
                case when Blank_before <= 121.0 then
                  case when SLOC_diff <= -0.5 then
                     return 0.875 # (0.875 out of 1.0)
                  else  # if SLOC_diff > -0.5
                     return 0.6 # (0.6 out of 1.0)
                  end                 else  # if Blank_before > 121.0
                   return 0.95 # (0.95 out of 1.0)
                end               end             end           end         end       else  # if SLOC_before > 866.0
        case when SLOC_diff <= -14.5 then
           return 0.10344827586206896 # (0.10344827586206896 out of 1.0)
        else  # if SLOC_diff > -14.5
           return 0.5263157894736842 # (0.5263157894736842 out of 1.0)
        end       end     else  # if low_ccp_group > 0.5
      case when LOC_before <= 524.5 then
        case when added_lines <= 16.5 then
           return 0.14285714285714285 # (0.14285714285714285 out of 1.0)
        else  # if added_lines > 16.5
           return 0.0 # (0.0 out of 1.0)
        end       else  # if LOC_before > 524.5
        case when McCabe_sum_after <= 84.0 then
           return 0.8285714285714286 # (0.8285714285714286 out of 1.0)
        else  # if McCabe_sum_after > 84.0
           return 0.375 # (0.375 out of 1.0)
        end       end     end   else  # if McCabe_max_after > 19.5
    case when changed_lines <= 196.5 then
      case when Blank_diff <= 1.5 then
        case when one_file_fix_rate_diff <= -0.21458333730697632 then
           return 0.8125 # (0.8125 out of 1.0)
        else  # if one_file_fix_rate_diff > -0.21458333730697632
          case when high_ccp_group <= 0.5 then
            case when changed_lines <= 65.5 then
              case when McCabe_sum_before <= 270.0 then
                case when avg_coupling_code_size_cut_diff <= -0.16302521526813507 then
                   return 0.08 # (0.08 out of 1.0)
                else  # if avg_coupling_code_size_cut_diff > -0.16302521526813507
                   return 0.3888888888888889 # (0.3888888888888889 out of 1.0)
                end               else  # if McCabe_sum_before > 270.0
                 return 0.3888888888888889 # (0.3888888888888889 out of 1.0)
              end             else  # if changed_lines > 65.5
               return 0.04 # (0.04 out of 1.0)
            end           else  # if high_ccp_group > 0.5
             return 0.5384615384615384 # (0.5384615384615384 out of 1.0)
          end         end       else  # if Blank_diff > 1.5
        case when LOC_before <= 1909.0 then
           return 0.23809523809523808 # (0.23809523809523808 out of 1.0)
        else  # if LOC_before > 1909.0
           return 0.043478260869565216 # (0.043478260869565216 out of 1.0)
        end       end     else  # if changed_lines > 196.5
      case when LOC_before <= 1310.5 then
         return 0.35714285714285715 # (0.35714285714285715 out of 1.0)
      else  # if LOC_before > 1310.5
         return 0.7096774193548387 # (0.7096774193548387 out of 1.0)
      end     end   end )