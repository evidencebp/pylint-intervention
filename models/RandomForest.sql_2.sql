create or replace function RandomForest_2 (effort_diff int64, too-many-nested-blocks int64, Single comments_diff int64, N1_diff int64, avg_coupling_code_size_cut_diff int64, Simplify-boolean-expression int64, try-except-raise int64, h1_diff int64, added_functions int64, too-many-boolean-expressions int64, LLOC_diff int64, cur_count_x int64, wildcard-import int64, mostly_delete int64, LOC_diff int64, difficulty_diff int64, Comments_before int64, prev_count_y int64, time_diff int64, pointless-statement int64, vocabulary_diff int64, modified_McCabe_max_diff int64, prev_count int64, McCabe_sum_before int64, McCabe_max_after int64, Blank_diff int64, using-constant-test int64, McCabe_max_before int64, is_refactor int64, Comments_after int64, SLOC_before int64, superfluous-parens int64, too-many-branches int64, massive_change int64, comparison-of-constants int64, broad-exception-caught int64, Blank_before int64, N2_diff int64, McCabe_sum_after int64, too-many-statements int64, refactor_mle_diff int64, LOC_before int64, simplifiable-if-statement int64, only_removal int64, h2_diff int64, unnecessary-semicolon int64, too-many-lines int64, LLOC_before int64, volume_diff int64, too-many-return-statements int64, high_ccp_group int64, Single comments_before int64, simplifiable-if-expression int64, changed_lines int64, Multi_diff int64, one_file_fix_rate_diff int64, prev_count_x int64, simplifiable-condition int64, cur_count_y int64, calculated_length_diff int64, SLOC_diff int64, line-too-long int64, McCabe_max_diff int64, Comments_diff int64, cur_count int64, Single comments_after int64, removed_lines int64, added_lines int64, length_diff int64, unnecessary-pass int64, hunks_num int64, bugs_diff int64, same_day_duration_avg_diff int64, McCabe_sum_diff int64) as (
  case when high_ccp_group <= 0.5 then
    case when SLOC_diff <= 38.0 then
      case when Comments_after <= 6.5 then
         return 0.6785714285714286 # (19.0 out of 28.0)
      else  # if Comments_after > 6.5
        case when SLOC_before <= 153.0 then
          case when Comments_before <= 12.5 then
             return 0.0 # (0.0 out of 18.0)
          else  # if Comments_before > 12.5
             return 0.16666666666666666 # (3.0 out of 18.0)
          end         else  # if SLOC_before > 153.0
          case when N2_diff <= -71.5 then
            case when h1_diff <= -2.5 then
               return 0.9130434782608695 # (21.0 out of 23.0)
            else  # if h1_diff > -2.5
               return 0.3125 # (5.0 out of 16.0)
            end           else  # if N2_diff > -71.5
            case when LLOC_before <= 190.0 then
               return 0.65 # (13.0 out of 20.0)
            else  # if LLOC_before > 190.0
              case when changed_lines <= 146.0 then
                case when added_lines <= 16.0 then
                  case when SLOC_before <= 1549.5 then
                    case when McCabe_sum_diff <= 1.5 then
                      case when Single comments_after <= 75.0 then
                        case when same_day_duration_avg_diff <= -0.10606062412261963 then
                           return 0.5294117647058824 # (9.0 out of 17.0)
                        else  # if same_day_duration_avg_diff > -0.10606062412261963
                           return 0.17647058823529413 # (3.0 out of 17.0)
                        end                       else  # if Single comments_after > 75.0
                         return 0.6666666666666666 # (18.0 out of 27.0)
                      end                     else  # if McCabe_sum_diff > 1.5
                       return 0.24 # (6.0 out of 25.0)
                    end                   else  # if SLOC_before > 1549.5
                     return 0.125 # (2.0 out of 16.0)
                  end                 else  # if added_lines > 16.0
                  case when same_day_duration_avg_diff <= -12.407936573028564 then
                    case when Comments_after <= 167.0 then
                       return 0.0 # (0.0 out of 40.0)
                    else  # if Comments_after > 167.0
                       return 0.1111111111111111 # (2.0 out of 18.0)
                    end                   else  # if same_day_duration_avg_diff > -12.407936573028564
                    case when Comments_before <= 35.5 then
                       return 0.0 # (0.0 out of 18.0)
                    else  # if Comments_before > 35.5
                      case when vocabulary_diff <= -4.5 then
                         return 0.16666666666666666 # (3.0 out of 18.0)
                      else  # if vocabulary_diff > -4.5
                         return 0.4166666666666667 # (10.0 out of 24.0)
                      end                     end                   end                 end               else  # if changed_lines > 146.0
                case when Multi_diff <= -1.0 then
                   return 0.7307692307692307 # (19.0 out of 26.0)
                else  # if Multi_diff > -1.0
                  case when McCabe_max_diff <= -1.0 then
                     return 0.19230769230769232 # (5.0 out of 26.0)
                  else  # if McCabe_max_diff > -1.0
                     return 0.38095238095238093 # (8.0 out of 21.0)
                  end                 end               end             end           end         end       end     else  # if SLOC_diff > 38.0
      case when Blank_diff <= 4.0 then
         return 0.9615384615384616 # (25.0 out of 26.0)
      else  # if Blank_diff > 4.0
        case when added_lines <= 90.0 then
           return 0.6 # (6.0 out of 10.0)
        else  # if added_lines > 90.0
           return 0.30434782608695654 # (7.0 out of 23.0)
        end       end     end   else  # if high_ccp_group > 0.5
    case when massive_change <= 0.5 then
      case when LLOC_diff <= 0.5 then
        case when N1_diff <= -1.5 then
           return 0.5833333333333334 # (7.0 out of 12.0)
        else  # if N1_diff > -1.5
          case when hunks_num <= 1.5 then
             return 0.875 # (21.0 out of 24.0)
          else  # if hunks_num > 1.5
             return 0.9565217391304348 # (22.0 out of 23.0)
          end         end       else  # if LLOC_diff > 0.5
        case when same_day_duration_avg_diff <= -16.36477279663086 then
           return 0.3125 # (5.0 out of 16.0)
        else  # if same_day_duration_avg_diff > -16.36477279663086
           return 0.7333333333333333 # (11.0 out of 15.0)
        end       end     else  # if massive_change > 0.5
      case when changed_lines <= 380.5 then
         return 0.6 # (9.0 out of 15.0)
      else  # if changed_lines > 380.5
         return 0.35 # (7.0 out of 20.0)
      end     end   end )