create or replace function RandomForest_8 (h1_diff int64, SLOC_before int64, avg_coupling_code_size_cut_diff int64, Multi_diff int64, using-constant-test int64, high_McCabe_sum_diff int64, difficulty_diff int64, LLOC_diff int64, length_diff int64, Comments_after int64, McCabe_max_before int64, low_McCabe_sum_before int64, cur_count int64, LOC_before int64, low_McCabe_max_before int64, massive_change int64, too-many-return-statements int64, Comments_diff int64, added_lines int64, broad-exception-caught int64, comparison-of-constants int64, Single comments_diff int64, refactor_mle_diff int64, prev_count_x int64, McCabe_sum_before int64, modified_McCabe_max_diff int64, Simplify-boolean-expression int64, Blank_diff int64, added_functions int64, LLOC_before int64, cur_count_x int64, high_McCabe_sum_before int64, volume_diff int64, low_McCabe_max_diff int64, LOC_diff int64, calculated_length_diff int64, changed_lines int64, N2_diff int64, h2_diff int64, too-many-lines int64, unnecessary-pass int64, simplifiable-if-statement int64, prev_count int64, too-many-nested-blocks int64, Comments_before int64, SLOC_diff int64, McCabe_sum_after int64, bugs_diff int64, cur_count_y int64, Single comments_after int64, McCabe_max_diff int64, N1_diff int64, wildcard-import int64, McCabe_sum_diff int64, prev_count_y int64, superfluous-parens int64, hunks_num int64, try-except-raise int64, simplifiable-if-expression int64, McCabe_max_after int64, high_McCabe_max_diff int64, too-many-statements int64, simplifiable-condition int64, only_removal int64, unnecessary-semicolon int64, effort_diff int64, is_refactor int64, same_day_duration_avg_diff int64, one_file_fix_rate_diff int64, high_McCabe_max_before int64, vocabulary_diff int64, too-many-branches int64, mostly_delete int64, high_ccp_group int64, low_ccp_group int64, removed_lines int64, Single comments_before int64, low_McCabe_sum_diff int64, time_diff int64, Blank_before int64, line-too-long int64, too-many-boolean-expressions int64, pointless-statement int64) as (
  case when LLOC_before <= 35.5 then
     return 1.0 # (1.0 out of 1.0)
  else  # if LLOC_before > 35.5
    case when Blank_before <= 29.0 then
      case when LOC_diff <= 0.5 then
         return 0.8947368421052632 # (0.8947368421052632 out of 1.0)
      else  # if LOC_diff > 0.5
         return 0.6 # (0.6 out of 1.0)
      end     else  # if Blank_before > 29.0
      case when changed_lines <= 137.0 then
        case when superfluous-parens <= 0.5 then
          case when changed_lines <= 111.5 then
            case when LLOC_before <= 1216.5 then
              case when low_McCabe_max_before <= 0.5 then
                case when refactor_mle_diff <= -0.1971895471215248 then
                   return 0.47368421052631576 # (0.47368421052631576 out of 1.0)
                else  # if refactor_mle_diff > -0.1971895471215248
                  case when Single comments_before <= 98.0 then
                    case when Single comments_after <= 55.5 then
                      case when McCabe_sum_before <= 137.0 then
                        case when LLOC_before <= 267.5 then
                           return 0.1724137931034483 # (0.1724137931034483 out of 1.0)
                        else  # if LLOC_before > 267.5
                           return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
                        end                       else  # if McCabe_sum_before > 137.0
                        case when McCabe_max_before <= 26.5 then
                           return 0.041666666666666664 # (0.041666666666666664 out of 1.0)
                        else  # if McCabe_max_before > 26.5
                           return 0.11764705882352941 # (0.11764705882352941 out of 1.0)
                        end                       end                     else  # if Single comments_after > 55.5
                      case when vocabulary_diff <= -2.5 then
                         return 0.4 # (0.4 out of 1.0)
                      else  # if vocabulary_diff > -2.5
                         return 0.6 # (0.6 out of 1.0)
                      end                     end                   else  # if Single comments_before > 98.0
                    case when added_lines <= 10.0 then
                       return 0.1 # (0.1 out of 1.0)
                    else  # if added_lines > 10.0
                       return 0.0 # (0.0 out of 1.0)
                    end                   end                 end               else  # if low_McCabe_max_before > 0.5
                case when LOC_before <= 528.5 then
                  case when refactor_mle_diff <= -0.15348463878035545 then
                     return 0.16666666666666666 # (0.16666666666666666 out of 1.0)
                  else  # if refactor_mle_diff > -0.15348463878035545
                     return 0.5333333333333333 # (0.5333333333333333 out of 1.0)
                  end                 else  # if LOC_before > 528.5
                   return 0.7272727272727273 # (0.7272727272727273 out of 1.0)
                end               end             else  # if LLOC_before > 1216.5
               return 0.6153846153846154 # (0.6153846153846154 out of 1.0)
            end           else  # if changed_lines > 111.5
            case when Blank_diff <= -5.5 then
               return 0.09090909090909091 # (0.09090909090909091 out of 1.0)
            else  # if Blank_diff > -5.5
               return 0.0 # (0.0 out of 1.0)
            end           end         else  # if superfluous-parens > 0.5
          case when SLOC_before <= 799.0 then
            case when Single comments_after <= 30.0 then
               return 0.7142857142857143 # (0.7142857142857143 out of 1.0)
            else  # if Single comments_after > 30.0
               return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
            end           else  # if SLOC_before > 799.0
             return 0.8888888888888888 # (0.8888888888888888 out of 1.0)
          end         end       else  # if changed_lines > 137.0
        case when Comments_after <= 77.5 then
          case when SLOC_before <= 268.0 then
             return 0.9629629629629629 # (0.9629629629629629 out of 1.0)
          else  # if SLOC_before > 268.0
            case when vocabulary_diff <= -11.0 then
              case when Single comments_after <= 26.5 then
                 return 0.55 # (0.55 out of 1.0)
              else  # if Single comments_after > 26.5
                 return 0.9565217391304348 # (0.9565217391304348 out of 1.0)
              end             else  # if vocabulary_diff > -11.0
              case when Blank_diff <= 5.5 then
                 return 0.2222222222222222 # (0.2222222222222222 out of 1.0)
              else  # if Blank_diff > 5.5
                 return 0.6428571428571429 # (0.6428571428571429 out of 1.0)
              end             end           end         else  # if Comments_after > 77.5
          case when Comments_after <= 108.0 then
             return 0.0 # (0.0 out of 1.0)
          else  # if Comments_after > 108.0
            case when McCabe_max_after <= 28.5 then
               return 0.6923076923076923 # (0.6923076923076923 out of 1.0)
            else  # if McCabe_max_after > 28.5
               return 0.19047619047619047 # (0.19047619047619047 out of 1.0)
            end           end         end       end     end   end )