create or replace function RandomForest_7 (low_McCabe_sum_before int64, changed_lines int64, low_McCabe_max_diff int64, try-except-raise int64, Comments_before int64, high_McCabe_sum_diff int64, low_McCabe_max_before int64, Multi_diff int64, effort_diff int64, difficulty_diff int64, only_removal int64, length_diff int64, comparison-of-constants int64, LOC_diff int64, h2_diff int64, line-too-long int64, h1_diff int64, using-constant-test int64, broad-exception-caught int64, time_diff int64, calculated_length_diff int64, too-many-branches int64, SLOC_before int64, low_ccp_group int64, avg_coupling_code_size_cut_diff int64, new_function int64, wildcard-import int64, McCabe_max_before int64, superfluous-parens int64, low_McCabe_sum_diff int64, pointless-statement int64, one_file_fix_rate_diff int64, cur_count_x int64, same_day_duration_avg_diff int64, too-many-nested-blocks int64, simplifiable-condition int64, too-many-lines int64, SLOC_diff int64, cur_count_y int64, LLOC_before int64, Comments_after int64, high_ccp_group int64, bugs_diff int64, unnecessary-pass int64, prev_count_x int64, massive_change int64, McCabe_max_after int64, removed_lines int64, Comments_diff int64, Single comments_diff int64, too-many-statements int64, Simplify-boolean-expression int64, is_refactor int64, refactor_mle_diff int64, added_lines int64, mostly_delete int64, volume_diff int64, too-many-boolean-expressions int64, N2_diff int64, Blank_before int64, vocabulary_diff int64, McCabe_sum_before int64, high_McCabe_sum_before int64, N1_diff int64, LOC_before int64, LLOC_diff int64, high_McCabe_max_diff int64, simplifiable-if-statement int64, prev_count_y int64, hunks_num int64, Blank_diff int64, prev_count int64, Single comments_before int64, McCabe_max_diff int64, McCabe_sum_diff int64, modified_McCabe_max_diff int64, McCabe_sum_after int64, too-many-return-statements int64, Single comments_after int64, unnecessary-semicolon int64, added_functions int64, cur_count int64, simplifiable-if-expression int64, high_McCabe_max_before int64) as (
  case when LLOC_before <= 441.5 then
    case when McCabe_sum_before <= 81.0 then
      case when N1_diff <= 1.5 then
        case when LOC_before <= 1065.0 then
          case when added_lines <= 35.0 then
            case when LLOC_before <= 75.5 then
               return 0.7894736842105263 # (0.7894736842105263 out of 1.0)
            else  # if LLOC_before > 75.5
              case when LOC_before <= 310.5 then
                 return 0.6153846153846154 # (0.6153846153846154 out of 1.0)
              else  # if LOC_before > 310.5
                 return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
              end             end           else  # if added_lines > 35.0
            case when too-many-branches <= 0.5 then
              case when N2_diff <= -0.5 then
                 return 0.4166666666666667 # (0.4166666666666667 out of 1.0)
              else  # if N2_diff > -0.5
                 return 0.7391304347826086 # (0.7391304347826086 out of 1.0)
              end             else  # if too-many-branches > 0.5
               return 0.8695652173913043 # (0.8695652173913043 out of 1.0)
            end           end         else  # if LOC_before > 1065.0
           return 1.0 # (1.0 out of 1.0)
        end       else  # if N1_diff > 1.5
         return 0.2 # (0.2 out of 1.0)
      end     else  # if McCabe_sum_before > 81.0
      case when McCabe_max_before <= 17.0 then
        case when McCabe_sum_before <= 120.5 then
           return 0.48148148148148145 # (0.48148148148148145 out of 1.0)
        else  # if McCabe_sum_before > 120.5
           return 0.8076923076923077 # (0.8076923076923077 out of 1.0)
        end       else  # if McCabe_max_before > 17.0
        case when h2_diff <= -4.5 then
           return 0.6875 # (0.6875 out of 1.0)
        else  # if h2_diff > -4.5
          case when LOC_diff <= 14.5 then
            case when Blank_before <= 96.0 then
               return 0.05 # (0.05 out of 1.0)
            else  # if Blank_before > 96.0
               return 0.29411764705882354 # (0.29411764705882354 out of 1.0)
            end           else  # if LOC_diff > 14.5
             return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
          end         end       end     end   else  # if LLOC_before > 441.5
    case when Comments_diff <= -14.5 then
       return 0.7307692307692307 # (0.7307692307692307 out of 1.0)
    else  # if Comments_diff > -14.5
      case when high_ccp_group <= 0.5 then
        case when h2_diff <= -0.5 then
          case when Multi_diff <= -8.5 then
             return 0.38095238095238093 # (0.38095238095238093 out of 1.0)
          else  # if Multi_diff > -8.5
            case when LLOC_before <= 937.5 then
              case when SLOC_before <= 801.5 then
                 return 0.17857142857142858 # (0.17857142857142858 out of 1.0)
              else  # if SLOC_before > 801.5
                case when h2_diff <= -26.5 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if h2_diff > -26.5
                   return 0.047619047619047616 # (0.047619047619047616 out of 1.0)
                end               end             else  # if LLOC_before > 937.5
               return 0.28125 # (0.28125 out of 1.0)
            end           end         else  # if h2_diff > -0.5
          case when McCabe_max_before <= 19.5 then
             return 0.13333333333333333 # (0.13333333333333333 out of 1.0)
          else  # if McCabe_max_before > 19.5
            case when one_file_fix_rate_diff <= 0.15168998017907143 then
              case when McCabe_max_after <= 26.5 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if McCabe_max_after > 26.5
                 return 0.4074074074074074 # (0.4074074074074074 out of 1.0)
              end             else  # if one_file_fix_rate_diff > 0.15168998017907143
               return 0.1875 # (0.1875 out of 1.0)
            end           end         end       else  # if high_ccp_group > 0.5
        case when LLOC_before <= 524.0 then
           return 0.23809523809523808 # (0.23809523809523808 out of 1.0)
        else  # if LLOC_before > 524.0
          case when Single comments_after <= 102.5 then
             return 0.8333333333333334 # (0.8333333333333334 out of 1.0)
          else  # if Single comments_after > 102.5
             return 0.5789473684210527 # (0.5789473684210527 out of 1.0)
          end         end       end     end   end )