create or replace function RandomForest_5 (effort_diff int64, too-many-nested-blocks int64, Single comments_diff int64, N1_diff int64, avg_coupling_code_size_cut_diff int64, Simplify-boolean-expression int64, try-except-raise int64, h1_diff int64, added_functions int64, too-many-boolean-expressions int64, LLOC_diff int64, cur_count_x int64, wildcard-import int64, mostly_delete int64, LOC_diff int64, difficulty_diff int64, Comments_before int64, prev_count_y int64, time_diff int64, pointless-statement int64, vocabulary_diff int64, modified_McCabe_max_diff int64, prev_count int64, McCabe_sum_before int64, McCabe_max_after int64, Blank_diff int64, using-constant-test int64, McCabe_max_before int64, is_refactor int64, Comments_after int64, SLOC_before int64, superfluous-parens int64, too-many-branches int64, massive_change int64, comparison-of-constants int64, broad-exception-caught int64, Blank_before int64, N2_diff int64, McCabe_sum_after int64, too-many-statements int64, refactor_mle_diff int64, LOC_before int64, simplifiable-if-statement int64, only_removal int64, h2_diff int64, unnecessary-semicolon int64, too-many-lines int64, LLOC_before int64, volume_diff int64, too-many-return-statements int64, high_ccp_group int64, Single comments_before int64, simplifiable-if-expression int64, changed_lines int64, Multi_diff int64, one_file_fix_rate_diff int64, prev_count_x int64, simplifiable-condition int64, cur_count_y int64, calculated_length_diff int64, SLOC_diff int64, line-too-long int64, McCabe_max_diff int64, Comments_diff int64, cur_count int64, Single comments_after int64, removed_lines int64, added_lines int64, length_diff int64, unnecessary-pass int64, hunks_num int64, bugs_diff int64, same_day_duration_avg_diff int64, McCabe_sum_diff int64) as (
  case when LOC_diff <= 57.5 then
    case when McCabe_max_after <= 7.5 then
      case when LLOC_before <= 595.5 then
        case when SLOC_diff <= -25.5 then
          case when Single comments_diff <= -6.0 then
             return 1.0 # (25.0 out of 25.0)
          else  # if Single comments_diff > -6.0
             return 0.625 # (10.0 out of 16.0)
          end         else  # if SLOC_diff > -25.5
          case when SLOC_before <= 189.5 then
            case when McCabe_sum_before <= 6.5 then
               return 0.6111111111111112 # (11.0 out of 18.0)
            else  # if McCabe_sum_before > 6.5
               return 0.696969696969697 # (23.0 out of 33.0)
            end           else  # if SLOC_before > 189.5
             return 0.3548387096774194 # (11.0 out of 31.0)
          end         end       else  # if LLOC_before > 595.5
         return 0.16666666666666666 # (2.0 out of 12.0)
      end     else  # if McCabe_max_after > 7.5
      case when McCabe_max_after <= 27.5 then
        case when LLOC_diff <= -168.5 then
           return 0.631578947368421 # (12.0 out of 19.0)
        else  # if LLOC_diff > -168.5
          case when same_day_duration_avg_diff <= -125.12247085571289 then
             return 0.75 # (15.0 out of 20.0)
          else  # if same_day_duration_avg_diff > -125.12247085571289
            case when McCabe_sum_after <= 59.5 then
              case when hunks_num <= 4.5 then
                 return 0.7058823529411765 # (12.0 out of 17.0)
              else  # if hunks_num > 4.5
                 return 0.1111111111111111 # (2.0 out of 18.0)
              end             else  # if McCabe_sum_after > 59.5
              case when LOC_diff <= 0.5 then
                case when length_diff <= -20.0 then
                  case when McCabe_sum_after <= 120.0 then
                     return 0.4666666666666667 # (7.0 out of 15.0)
                  else  # if McCabe_sum_after > 120.0
                     return 0.17391304347826086 # (4.0 out of 23.0)
                  end                 else  # if length_diff > -20.0
                  case when superfluous-parens <= 0.5 then
                    case when LLOC_before <= 361.5 then
                       return 0.3684210526315789 # (7.0 out of 19.0)
                    else  # if LLOC_before > 361.5
                      case when one_file_fix_rate_diff <= 0.10000000149011612 then
                         return 0.0 # (0.0 out of 42.0)
                      else  # if one_file_fix_rate_diff > 0.10000000149011612
                         return 0.10526315789473684 # (2.0 out of 19.0)
                      end                     end                   else  # if superfluous-parens > 0.5
                     return 0.38461538461538464 # (5.0 out of 13.0)
                  end                 end               else  # if LOC_diff > 0.5
                case when LOC_diff <= 4.5 then
                   return 0.6153846153846154 # (8.0 out of 13.0)
                else  # if LOC_diff > 4.5
                  case when McCabe_sum_after <= 167.5 then
                    case when hunks_num <= 10.5 then
                      case when SLOC_before <= 360.0 then
                         return 0.058823529411764705 # (1.0 out of 17.0)
                      else  # if SLOC_before > 360.0
                         return 0.038461538461538464 # (1.0 out of 26.0)
                      end                     else  # if hunks_num > 10.5
                       return 0.23809523809523808 # (5.0 out of 21.0)
                    end                   else  # if McCabe_sum_after > 167.5
                     return 0.48148148148148145 # (13.0 out of 27.0)
                  end                 end               end             end           end         end       else  # if McCabe_max_after > 27.5
        case when LLOC_diff <= -12.5 then
          case when added_lines <= 212.5 then
             return 0.13043478260869565 # (3.0 out of 23.0)
          else  # if added_lines > 212.5
             return 0.4666666666666667 # (7.0 out of 15.0)
          end         else  # if LLOC_diff > -12.5
          case when SLOC_before <= 715.5 then
             return 0.8571428571428571 # (18.0 out of 21.0)
          else  # if SLOC_before > 715.5
            case when McCabe_max_before <= 46.5 then
               return 0.6111111111111112 # (11.0 out of 18.0)
            else  # if McCabe_max_before > 46.5
               return 0.34615384615384615 # (9.0 out of 26.0)
            end           end         end       end     end   else  # if LOC_diff > 57.5
    case when LOC_diff <= 93.5 then
       return 0.9047619047619048 # (19.0 out of 21.0)
    else  # if LOC_diff > 93.5
      case when McCabe_max_after <= 18.5 then
         return 0.47058823529411764 # (8.0 out of 17.0)
      else  # if McCabe_max_after > 18.5
         return 0.8 # (12.0 out of 15.0)
      end     end   end )