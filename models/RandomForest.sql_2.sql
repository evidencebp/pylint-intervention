create or replace function RandomForest_2 (too-many-nested-blocks int64, unnecessary-semicolon int64, broad-exception-caught int64, Blank_diff int64, high_McCabe_sum_before int64, h1_diff int64, volume_diff int64, comparison-of-constants int64, McCabe_max_after int64, too-many-lines int64, LLOC_diff int64, cur_count int64, LOC_before int64, line-too-long int64, too-many-boolean-expressions int64, Multi_diff int64, Comments_after int64, McCabe_max_before int64, only_removal int64, high_McCabe_max_diff int64, removed_lines int64, Single comments_diff int64, modified_McCabe_max_diff int64, low_McCabe_max_diff int64, LOC_diff int64, prev_count_y int64, high_McCabe_max_before int64, high_McCabe_sum_diff int64, Simplify-boolean-expression int64, low_ccp_group int64, McCabe_max_diff int64, same_day_duration_avg_diff int64, is_refactor int64, mostly_delete int64, hunks_num int64, McCabe_sum_diff int64, prev_count int64, SLOC_diff int64, low_McCabe_max_before int64, try-except-raise int64, bugs_diff int64, low_McCabe_sum_before int64, avg_coupling_code_size_cut_diff int64, calculated_length_diff int64, SLOC_before int64, added_lines int64, unnecessary-pass int64, N1_diff int64, h2_diff int64, prev_count_x int64, LLOC_before int64, added_functions int64, McCabe_sum_before int64, simplifiable-if-expression int64, simplifiable-condition int64, refactor_mle_diff int64, pointless-statement int64, N2_diff int64, Blank_before int64, Comments_diff int64, cur_count_y int64, time_diff int64, length_diff int64, effort_diff int64, one_file_fix_rate_diff int64, superfluous-parens int64, high_ccp_group int64, too-many-return-statements int64, Comments_before int64, too-many-statements int64, simplifiable-if-statement int64, too-many-branches int64, cur_count_x int64, Single comments_after int64, low_McCabe_sum_diff int64, using-constant-test int64, changed_lines int64, massive_change int64, McCabe_sum_after int64, difficulty_diff int64, vocabulary_diff int64, Single comments_before int64, wildcard-import int64) as (
  case when SLOC_before <= 106.5 then
    case when added_lines <= 10.0 then
       return 0.875 # (0.875 out of 1.0)
    else  # if added_lines > 10.0
       return 0.7647058823529411 # (0.7647058823529411 out of 1.0)
    end   else  # if SLOC_before > 106.5
    case when SLOC_before <= 3137.5 then
      case when Blank_before <= 28.5 then
         return 0.8648648648648649 # (0.8648648648648649 out of 1.0)
      else  # if Blank_before > 28.5
        case when Multi_diff <= -60.5 then
           return 0.9444444444444444 # (0.9444444444444444 out of 1.0)
        else  # if Multi_diff > -60.5
          case when McCabe_max_after <= 7.5 then
            case when low_McCabe_max_diff <= 0.5 then
              case when changed_lines <= 10.0 then
                 return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
              else  # if changed_lines > 10.0
                case when SLOC_diff <= -1.0 then
                   return 0.6153846153846154 # (0.6153846153846154 out of 1.0)
                else  # if SLOC_diff > -1.0
                   return 0.1111111111111111 # (0.1111111111111111 out of 1.0)
                end               end             else  # if low_McCabe_max_diff > 0.5
               return 0.8518518518518519 # (0.8518518518518519 out of 1.0)
            end           else  # if McCabe_max_after > 7.5
            case when low_ccp_group <= 0.5 then
              case when McCabe_max_before <= 49.5 then
                case when Multi_diff <= -4.5 then
                   return 0.05714285714285714 # (0.05714285714285714 out of 1.0)
                else  # if Multi_diff > -4.5
                  case when hunks_num <= 12.5 then
                    case when Comments_diff <= -0.5 then
                      case when high_ccp_group <= 0.5 then
                        case when length_diff <= -49.0 then
                           return 0.21052631578947367 # (0.21052631578947367 out of 1.0)
                        else  # if length_diff > -49.0
                           return 0.6896551724137931 # (0.6896551724137931 out of 1.0)
                        end                       else  # if high_ccp_group > 0.5
                         return 1.0 # (1.0 out of 1.0)
                      end                     else  # if Comments_diff > -0.5
                      case when Blank_diff <= -0.5 then
                         return 0.5862068965517241 # (0.5862068965517241 out of 1.0)
                      else  # if Blank_diff > -0.5
                        case when refactor_mle_diff <= -0.1276846081018448 then
                           return 0.1875 # (0.1875 out of 1.0)
                        else  # if refactor_mle_diff > -0.1276846081018448
                          case when McCabe_max_after <= 22.5 then
                            case when Comments_after <= 29.0 then
                               return 0.47368421052631576 # (0.47368421052631576 out of 1.0)
                            else  # if Comments_after > 29.0
                               return 0.7692307692307693 # (0.7692307692307693 out of 1.0)
                            end                           else  # if McCabe_max_after > 22.5
                             return 0.25 # (0.25 out of 1.0)
                          end                         end                       end                     end                   else  # if hunks_num > 12.5
                    case when superfluous-parens <= 0.5 then
                      case when Comments_after <= 52.5 then
                         return 0.23809523809523808 # (0.23809523809523808 out of 1.0)
                      else  # if Comments_after > 52.5
                         return 0.047619047619047616 # (0.047619047619047616 out of 1.0)
                      end                     else  # if superfluous-parens > 0.5
                       return 0.47368421052631576 # (0.47368421052631576 out of 1.0)
                    end                   end                 end               else  # if McCabe_max_before > 49.5
                 return 0.7241379310344828 # (0.7241379310344828 out of 1.0)
              end             else  # if low_ccp_group > 0.5
              case when SLOC_diff <= -41.0 then
                 return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
              else  # if SLOC_diff > -41.0
                case when Single comments_before <= 182.0 then
                  case when Comments_before <= 21.5 then
                     return 0.08333333333333333 # (0.08333333333333333 out of 1.0)
                  else  # if Comments_before > 21.5
                     return 0.0 # (0.0 out of 1.0)
                  end                 else  # if Single comments_before > 182.0
                   return 0.16666666666666666 # (0.16666666666666666 out of 1.0)
                end               end             end           end         end       end     else  # if SLOC_before > 3137.5
       return 0.0 # (0.0 out of 1.0)
    end   end )