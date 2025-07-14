create or replace function RandomForest_6 (effort_diff int64, too-many-nested-blocks int64, Single comments_diff int64, N1_diff int64, avg_coupling_code_size_cut_diff int64, Simplify-boolean-expression int64, try-except-raise int64, h1_diff int64, added_functions int64, too-many-boolean-expressions int64, LLOC_diff int64, cur_count_x int64, wildcard-import int64, mostly_delete int64, LOC_diff int64, difficulty_diff int64, Comments_before int64, prev_count_y int64, time_diff int64, pointless-statement int64, vocabulary_diff int64, modified_McCabe_max_diff int64, prev_count int64, McCabe_sum_before int64, McCabe_max_after int64, Blank_diff int64, using-constant-test int64, McCabe_max_before int64, is_refactor int64, Comments_after int64, SLOC_before int64, superfluous-parens int64, too-many-branches int64, massive_change int64, comparison-of-constants int64, broad-exception-caught int64, Blank_before int64, N2_diff int64, McCabe_sum_after int64, too-many-statements int64, refactor_mle_diff int64, LOC_before int64, simplifiable-if-statement int64, only_removal int64, h2_diff int64, unnecessary-semicolon int64, too-many-lines int64, LLOC_before int64, volume_diff int64, too-many-return-statements int64, high_ccp_group int64, Single comments_before int64, simplifiable-if-expression int64, changed_lines int64, Multi_diff int64, one_file_fix_rate_diff int64, prev_count_x int64, simplifiable-condition int64, cur_count_y int64, calculated_length_diff int64, SLOC_diff int64, line-too-long int64, McCabe_max_diff int64, Comments_diff int64, cur_count int64, Single comments_after int64, removed_lines int64, added_lines int64, length_diff int64, unnecessary-pass int64, hunks_num int64, bugs_diff int64, same_day_duration_avg_diff int64, McCabe_sum_diff int64) as (
  case when avg_coupling_code_size_cut_diff <= 0.6696820259094238 then
    case when high_ccp_group <= 0.5 then
      case when Multi_diff <= -25.5 then
         return 0.8 # (20.0 out of 25.0)
      else  # if Multi_diff > -25.5
        case when Comments_after <= 45.5 then
          case when SLOC_diff <= 21.5 then
            case when LLOC_diff <= -4.0 then
              case when length_diff <= -25.0 then
                 return 0.5769230769230769 # (15.0 out of 26.0)
              else  # if length_diff > -25.0
                case when Single comments_after <= 26.0 then
                   return 0.4166666666666667 # (5.0 out of 12.0)
                else  # if Single comments_after > 26.0
                   return 0.9375 # (15.0 out of 16.0)
                end               end             else  # if LLOC_diff > -4.0
              case when added_lines <= 15.0 then
                case when SLOC_before <= 247.0 then
                   return 0.75 # (12.0 out of 16.0)
                else  # if SLOC_before > 247.0
                   return 0.4230769230769231 # (11.0 out of 26.0)
                end               else  # if added_lines > 15.0
                 return 0.2222222222222222 # (6.0 out of 27.0)
              end             end           else  # if SLOC_diff > 21.5
             return 0.8214285714285714 # (23.0 out of 28.0)
          end         else  # if Comments_after > 45.5
          case when Comments_after <= 500.0 then
            case when Blank_diff <= -0.5 then
              case when LOC_before <= 1474.5 then
                case when Multi_diff <= -1.5 then
                   return 0.18181818181818182 # (4.0 out of 22.0)
                else  # if Multi_diff > -1.5
                   return 0.02702702702702703 # (1.0 out of 37.0)
                end               else  # if LOC_before > 1474.5
                 return 0.3333333333333333 # (4.0 out of 12.0)
              end             else  # if Blank_diff > -0.5
              case when refactor_mle_diff <= -0.040783628821372986 then
                case when McCabe_max_after <= 18.5 then
                   return 0.6666666666666666 # (10.0 out of 15.0)
                else  # if McCabe_max_after > 18.5
                   return 0.4482758620689655 # (13.0 out of 29.0)
                end               else  # if refactor_mle_diff > -0.040783628821372986
                case when changed_lines <= 212.5 then
                  case when LLOC_before <= 527.0 then
                     return 0.2222222222222222 # (4.0 out of 18.0)
                  else  # if LLOC_before > 527.0
                     return 0.0 # (0.0 out of 18.0)
                  end                 else  # if changed_lines > 212.5
                   return 0.5 # (8.0 out of 16.0)
                end               end             end           else  # if Comments_after > 500.0
             return 0.8260869565217391 # (19.0 out of 23.0)
          end         end       end     else  # if high_ccp_group > 0.5
      case when Single comments_after <= 58.5 then
        case when McCabe_sum_diff <= -6.5 then
           return 0.84 # (21.0 out of 25.0)
        else  # if McCabe_sum_diff > -6.5
          case when SLOC_diff <= 2.5 then
             return 1.0 # (35.0 out of 35.0)
          else  # if SLOC_diff > 2.5
             return 0.9230769230769231 # (12.0 out of 13.0)
          end         end       else  # if Single comments_after > 58.5
        case when refactor_mle_diff <= -0.07897983118891716 then
           return 0.47058823529411764 # (8.0 out of 17.0)
        else  # if refactor_mle_diff > -0.07897983118891716
           return 0.7647058823529411 # (13.0 out of 17.0)
        end       end     end   else  # if avg_coupling_code_size_cut_diff > 0.6696820259094238
    case when refactor_mle_diff <= -0.21621163189411163 then
       return 0.0 # (0.0 out of 18.0)
    else  # if refactor_mle_diff > -0.21621163189411163
      case when Blank_before <= 318.0 then
        case when McCabe_max_before <= 41.5 then
          case when modified_McCabe_max_diff <= -2.5 then
             return 0.6666666666666666 # (8.0 out of 12.0)
          else  # if modified_McCabe_max_diff > -2.5
            case when changed_lines <= 10.5 then
               return 0.6666666666666666 # (8.0 out of 12.0)
            else  # if changed_lines > 10.5
              case when McCabe_sum_after <= 137.5 then
                 return 0.2857142857142857 # (4.0 out of 14.0)
              else  # if McCabe_sum_after > 137.5
                 return 0.041666666666666664 # (1.0 out of 24.0)
              end             end           end         else  # if McCabe_max_before > 41.5
           return 0.75 # (21.0 out of 28.0)
        end       else  # if Blank_before > 318.0
         return 0.10526315789473684 # (2.0 out of 19.0)
      end     end   end )