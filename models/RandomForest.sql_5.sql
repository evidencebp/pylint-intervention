create or replace function RandomForest_5 (McCabe_sum_before int64, changed_lines int64, prev_count_y int64, mostly_delete int64, h1_diff int64, too-many-lines int64, low_McCabe_sum_before int64, length_diff int64, LOC_before int64, simplifiable-if-expression int64, added_functions int64, broad-exception-caught int64, simplifiable-condition int64, prev_count_x int64, McCabe_max_diff int64, SLOC_before int64, LLOC_before int64, low_McCabe_max_diff int64, bugs_diff int64, same_day_duration_avg_diff int64, cur_count_x int64, only_removal int64, McCabe_max_after int64, Single comments_after int64, low_ccp_group int64, one_file_fix_rate_diff int64, effort_diff int64, difficulty_diff int64, removed_lines int64, Comments_diff int64, too-many-boolean-expressions int64, refactor_mle_diff int64, high_McCabe_max_before int64, hunks_num int64, LOC_diff int64, SLOC_diff int64, cur_count_y int64, vocabulary_diff int64, using-constant-test int64, Simplify-boolean-expression int64, low_McCabe_max_before int64, high_McCabe_sum_diff int64, high_McCabe_sum_before int64, McCabe_max_before int64, Comments_after int64, McCabe_sum_diff int64, unnecessary-pass int64, avg_coupling_code_size_cut_diff int64, simplifiable-if-statement int64, is_refactor int64, volume_diff int64, added_lines int64, high_McCabe_max_diff int64, superfluous-parens int64, cur_count int64, low_McCabe_sum_diff int64, calculated_length_diff int64, Multi_diff int64, N2_diff int64, h2_diff int64, Single comments_before int64, McCabe_sum_after int64, N1_diff int64, too-many-statements int64, comparison-of-constants int64, pointless-statement int64, time_diff int64, prev_count int64, Single comments_diff int64, massive_change int64, Blank_diff int64, too-many-nested-blocks int64, Comments_before int64, modified_McCabe_max_diff int64, LLOC_diff int64, Blank_before int64, try-except-raise int64, too-many-branches int64, too-many-return-statements int64, unnecessary-semicolon int64, wildcard-import int64, high_ccp_group int64, line-too-long int64) as (
  case when Single comments_after <= 4.5 then
    case when removed_lines <= 17.5 then
       return 0.8666666666666667 # (0.8666666666666667 out of 1.0)
    else  # if removed_lines > 17.5
       return 0.75 # (0.75 out of 1.0)
    end   else  # if Single comments_after > 4.5
    case when high_ccp_group <= 0.5 then
      case when h2_diff <= -51.5 then
        case when McCabe_sum_after <= 60.5 then
           return 1.0 # (1.0 out of 1.0)
        else  # if McCabe_sum_after > 60.5
           return 0.5217391304347826 # (0.5217391304347826 out of 1.0)
        end       else  # if h2_diff > -51.5
        case when added_functions <= 0.5 then
          case when superfluous-parens <= 0.5 then
            case when Single comments_after <= 51.5 then
              case when Comments_diff <= 0.5 then
                case when McCabe_max_diff <= -0.5 then
                   return 0.08 # (0.08 out of 1.0)
                else  # if McCabe_max_diff > -0.5
                  case when same_day_duration_avg_diff <= -27.686281204223633 then
                     return 0.14814814814814814 # (0.14814814814814814 out of 1.0)
                  else  # if same_day_duration_avg_diff > -27.686281204223633
                    case when changed_lines <= 48.5 then
                       return 0.3 # (0.3 out of 1.0)
                    else  # if changed_lines > 48.5
                       return 0.7142857142857143 # (0.7142857142857143 out of 1.0)
                    end                   end                 end               else  # if Comments_diff > 0.5
                 return 0.5 # (0.5 out of 1.0)
              end             else  # if Single comments_after > 51.5
              case when Single comments_before <= 197.0 then
                case when N1_diff <= 0.5 then
                  case when length_diff <= -15.5 then
                     return 0.20689655172413793 # (0.20689655172413793 out of 1.0)
                  else  # if length_diff > -15.5
                    case when LLOC_diff <= -0.5 then
                       return 0.0 # (0.0 out of 1.0)
                    else  # if LLOC_diff > -0.5
                       return 0.19230769230769232 # (0.19230769230769232 out of 1.0)
                    end                   end                 else  # if N1_diff > 0.5
                   return 0.46153846153846156 # (0.46153846153846156 out of 1.0)
                end               else  # if Single comments_before > 197.0
                 return 0.0 # (0.0 out of 1.0)
              end             end           else  # if superfluous-parens > 0.5
            case when Comments_before <= 78.5 then
               return 0.5833333333333334 # (0.5833333333333334 out of 1.0)
            else  # if Comments_before > 78.5
               return 0.375 # (0.375 out of 1.0)
            end           end         else  # if added_functions > 0.5
          case when SLOC_before <= 447.5 then
            case when vocabulary_diff <= 2.5 then
               return 0.40540540540540543 # (0.40540540540540543 out of 1.0)
            else  # if vocabulary_diff > 2.5
               return 0.08 # (0.08 out of 1.0)
            end           else  # if SLOC_before > 447.5
            case when McCabe_sum_diff <= 0.5 then
              case when LLOC_diff <= -13.0 then
                 return 0.5 # (0.5 out of 1.0)
              else  # if LLOC_diff > -13.0
                 return 0.2727272727272727 # (0.2727272727272727 out of 1.0)
              end             else  # if McCabe_sum_diff > 0.5
              case when changed_lines <= 116.0 then
                 return 0.9166666666666666 # (0.9166666666666666 out of 1.0)
              else  # if changed_lines > 116.0
                 return 0.6875 # (0.6875 out of 1.0)
              end             end           end         end       end     else  # if high_ccp_group > 0.5
      case when length_diff <= -38.0 then
         return 0.0 # (0.0 out of 1.0)
      else  # if length_diff > -38.0
        case when LLOC_diff <= -3.5 then
          case when LOC_diff <= -36.0 then
             return 1.0 # (1.0 out of 1.0)
          else  # if LOC_diff > -36.0
             return 0.6470588235294118 # (0.6470588235294118 out of 1.0)
          end         else  # if LLOC_diff > -3.5
          case when Comments_after <= 56.5 then
            case when removed_lines <= 6.0 then
               return 0.5333333333333333 # (0.5333333333333333 out of 1.0)
            else  # if removed_lines > 6.0
               return 1.0 # (1.0 out of 1.0)
            end           else  # if Comments_after > 56.5
            case when Blank_before <= 114.5 then
               return 0.0625 # (0.0625 out of 1.0)
            else  # if Blank_before > 114.5
               return 0.5789473684210527 # (0.5789473684210527 out of 1.0)
            end           end         end       end     end   end )