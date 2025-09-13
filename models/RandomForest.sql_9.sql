create or replace function RandomForest_9 (prev_count int64, simplifiable-if-expression int64, N1_diff int64, cur_count int64, wildcard-import int64, too-many-return-statements int64, low_McCabe_max_diff int64, length_diff int64, volume_diff int64, high_McCabe_sum_diff int64, high_McCabe_max_before int64, simplifiable-condition int64, Blank_before int64, high_ccp_group int64, McCabe_max_before int64, bugs_diff int64, too-many-nested-blocks int64, refactor_mle_diff int64, difficulty_diff int64, LLOC_diff int64, LOC_diff int64, simplifiable-if-statement int64, one_file_fix_rate_diff int64, SLOC_before int64, LOC_before int64, mostly_delete int64, changed_lines int64, Single comments_before int64, removed_lines int64, added_functions int64, h1_diff int64, effort_diff int64, hunks_num int64, Multi_diff int64, same_day_duration_avg_diff int64, N2_diff int64, cur_count_y int64, Comments_diff int64, modified_McCabe_max_diff int64, h2_diff int64, time_diff int64, LLOC_before int64, calculated_length_diff int64, Single comments_after int64, massive_change int64, McCabe_sum_before int64, too-many-boolean-expressions int64, Simplify-boolean-expression int64, line-too-long int64, superfluous-parens int64, low_ccp_group int64, McCabe_max_diff int64, comparison-of-constants int64, high_McCabe_sum_before int64, low_McCabe_sum_diff int64, avg_coupling_code_size_cut_diff int64, is_refactor int64, Single comments_diff int64, unnecessary-semicolon int64, added_lines int64, prev_count_y int64, try-except-raise int64, low_McCabe_sum_before int64, vocabulary_diff int64, too-many-branches int64, McCabe_sum_after int64, broad-exception-caught int64, prev_count_x int64, only_removal int64, McCabe_max_after int64, pointless-statement int64, low_McCabe_max_before int64, too-many-lines int64, McCabe_sum_diff int64, high_McCabe_max_diff int64, using-constant-test int64, SLOC_diff int64, Blank_diff int64, Comments_after int64, cur_count_x int64, unnecessary-pass int64, too-many-statements int64, Comments_before int64) as (
  case when McCabe_sum_before <= 129.5 then
    case when h2_diff <= 3.5 then
      case when removed_lines <= 9.5 then
        case when SLOC_before <= 234.0 then
          case when LOC_diff <= -3.5 then
             return 0.13333333333333333 # (0.13333333333333333 out of 1.0)
          else  # if LOC_diff > -3.5
             return 0.5 # (0.5 out of 1.0)
          end         else  # if SLOC_before > 234.0
          case when LOC_before <= 1002.0 then
            case when Single comments_after <= 22.5 then
               return 1.0 # (1.0 out of 1.0)
            else  # if Single comments_after > 22.5
               return 0.5666666666666667 # (0.5666666666666667 out of 1.0)
            end           else  # if LOC_before > 1002.0
             return 0.125 # (0.125 out of 1.0)
          end         end       else  # if removed_lines > 9.5
        case when N2_diff <= -19.5 then
          case when N1_diff <= -19.0 then
             return 0.5 # (0.5 out of 1.0)
          else  # if N1_diff > -19.0
             return 0.5 # (0.5 out of 1.0)
          end         else  # if N2_diff > -19.5
          case when LOC_before <= 970.5 then
            case when low_ccp_group <= 0.5 then
              case when LLOC_diff <= 0.5 then
                case when Blank_before <= 29.0 then
                   return 0.6875 # (0.6875 out of 1.0)
                else  # if Blank_before > 29.0
                  case when McCabe_max_before <= 19.0 then
                    case when changed_lines <= 83.0 then
                       return 0.8 # (0.8 out of 1.0)
                    else  # if changed_lines > 83.0
                       return 0.9565217391304348 # (0.9565217391304348 out of 1.0)
                    end                   else  # if McCabe_max_before > 19.0
                     return 1.0 # (1.0 out of 1.0)
                  end                 end               else  # if LLOC_diff > 0.5
                 return 0.4117647058823529 # (0.4117647058823529 out of 1.0)
              end             else  # if low_ccp_group > 0.5
               return 0.09090909090909091 # (0.09090909090909091 out of 1.0)
            end           else  # if LOC_before > 970.5
            case when Single comments_after <= 253.0 then
               return 1.0 # (1.0 out of 1.0)
            else  # if Single comments_after > 253.0
               return 0.9375 # (0.9375 out of 1.0)
            end           end         end       end     else  # if h2_diff > 3.5
       return 0.14814814814814814 # (0.14814814814814814 out of 1.0)
    end   else  # if McCabe_sum_before > 129.5
    case when high_ccp_group <= 0.5 then
      case when length_diff <= -199.0 then
         return 0.8333333333333334 # (0.8333333333333334 out of 1.0)
      else  # if length_diff > -199.0
        case when vocabulary_diff <= 4.5 then
          case when Multi_diff <= 1.5 then
            case when McCabe_sum_after <= 150.0 then
              case when avg_coupling_code_size_cut_diff <= -0.9642857015132904 then
                 return 0.25 # (0.25 out of 1.0)
              else  # if avg_coupling_code_size_cut_diff > -0.9642857015132904
                 return 0.0 # (0.0 out of 1.0)
              end             else  # if McCabe_sum_after > 150.0
              case when Comments_after <= 30.0 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if Comments_after > 30.0
                case when LOC_before <= 2026.5 then
                  case when McCabe_sum_before <= 175.5 then
                     return 0.7333333333333333 # (0.7333333333333333 out of 1.0)
                  else  # if McCabe_sum_before > 175.5
                    case when Blank_before <= 211.0 then
                      case when added_lines <= 49.5 then
                         return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
                      else  # if added_lines > 49.5
                         return 0.0 # (0.0 out of 1.0)
                      end                     else  # if Blank_before > 211.0
                       return 0.45454545454545453 # (0.45454545454545453 out of 1.0)
                    end                   end                 else  # if LOC_before > 2026.5
                   return 0.10526315789473684 # (0.10526315789473684 out of 1.0)
                end               end             end           else  # if Multi_diff > 1.5
             return 0.6923076923076923 # (0.6923076923076923 out of 1.0)
          end         else  # if vocabulary_diff > 4.5
           return 0.5384615384615384 # (0.5384615384615384 out of 1.0)
        end       end     else  # if high_ccp_group > 0.5
      case when length_diff <= -53.5 then
         return 0.23529411764705882 # (0.23529411764705882 out of 1.0)
      else  # if length_diff > -53.5
        case when hunks_num <= 13.0 then
          case when McCabe_max_after <= 23.0 then
             return 1.0 # (1.0 out of 1.0)
          else  # if McCabe_max_after > 23.0
             return 0.7 # (0.7 out of 1.0)
          end         else  # if hunks_num > 13.0
           return 0.25 # (0.25 out of 1.0)
        end       end     end   end )