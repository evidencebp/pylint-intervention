create or replace function RandomForest_2 (SLOC_before int64, simplifiable-condition int64, bugs_diff int64, Blank_before int64, LLOC_diff int64, try-except-raise int64, LLOC_before int64, changed_lines int64, h2_diff int64, prev_count_x int64, too-many-lines int64, cur_count_y int64, Comments_before int64, McCabe_sum_after int64, cur_count_x int64, vocabulary_diff int64, Single comments_before int64, N2_diff int64, high_ccp_group int64, massive_change int64, added_lines int64, prev_count int64, refactor_mle_diff int64, superfluous-parens int64, avg_coupling_code_size_cut_diff int64, McCabe_sum_diff int64, LOC_before int64, too-many-return-statements int64, too-many-branches int64, too-many-nested-blocks int64, difficulty_diff int64, time_diff int64, Single comments_after int64, calculated_length_diff int64, Simplify-boolean-expression int64, unnecessary-semicolon int64, mostly_delete int64, effort_diff int64, Multi_diff int64, McCabe_max_diff int64, is_refactor int64, only_removal int64, LOC_diff int64, one_file_fix_rate_diff int64, Comments_after int64, comparison-of-constants int64, McCabe_max_after int64, length_diff int64, simplifiable-if-statement int64, removed_lines int64, unnecessary-pass int64, Comments_diff int64, cur_count int64, same_day_duration_avg_diff int64, hunks_num int64, N1_diff int64, line-too-long int64, volume_diff int64, using-constant-test int64, too-many-boolean-expressions int64, modified_McCabe_max_diff int64, h1_diff int64, added_functions int64, SLOC_diff int64, too-many-statements int64, pointless-statement int64, wildcard-import int64, McCabe_max_before int64, prev_count_y int64, broad-exception-caught int64, Blank_diff int64, McCabe_sum_before int64, simplifiable-if-expression int64, Single comments_diff int64) as (
  case when too-many-return-statements <= 0.5 then
    case when Single comments_after <= 2.5 then
      case when McCabe_sum_after <= 12.5 then
         return 1.0 # (16.0 out of 16.0)
      else  # if McCabe_sum_after > 12.5
         return 0.9166666666666666 # (11.0 out of 12.0)
      end     else  # if Single comments_after > 2.5
      case when McCabe_sum_before <= 303.0 then
        case when McCabe_max_before <= 0.5 then
           return 0.125 # (2.0 out of 16.0)
        else  # if McCabe_max_before > 0.5
          case when Comments_diff <= -4.5 then
            case when McCabe_max_after <= 6.5 then
               return 1.0 # (25.0 out of 25.0)
            else  # if McCabe_max_after > 6.5
              case when vocabulary_diff <= -15.0 then
                case when McCabe_max_before <= 21.5 then
                   return 0.3333333333333333 # (6.0 out of 18.0)
                else  # if McCabe_max_before > 21.5
                   return 0.6190476190476191 # (13.0 out of 21.0)
                end               else  # if vocabulary_diff > -15.0
                 return 0.9655172413793104 # (28.0 out of 29.0)
              end             end           else  # if Comments_diff > -4.5
            case when Single comments_before <= 187.5 then
              case when length_diff <= -50.0 then
                 return 0.0 # (0.0 out of 24.0)
              else  # if length_diff > -50.0
                case when added_lines <= 62.0 then
                  case when high_ccp_group <= 0.5 then
                    case when Comments_diff <= -0.5 then
                       return 0.0 # (0.0 out of 29.0)
                    else  # if Comments_diff > -0.5
                      case when Comments_before <= 82.0 then
                        case when SLOC_before <= 579.0 then
                          case when refactor_mle_diff <= -0.07434321194887161 then
                            case when same_day_duration_avg_diff <= -23.62018394470215 then
                               return 0.8125 # (13.0 out of 16.0)
                            else  # if same_day_duration_avg_diff > -23.62018394470215
                               return 0.47619047619047616 # (10.0 out of 21.0)
                            end                           else  # if refactor_mle_diff > -0.07434321194887161
                            case when McCabe_sum_after <= 67.0 then
                               return 0.5714285714285714 # (12.0 out of 21.0)
                            else  # if McCabe_sum_after > 67.0
                               return 0.07142857142857142 # (2.0 out of 28.0)
                            end                           end                         else  # if SLOC_before > 579.0
                           return 0.7 # (14.0 out of 20.0)
                        end                       else  # if Comments_before > 82.0
                        case when SLOC_before <= 688.0 then
                           return 0.0 # (0.0 out of 31.0)
                        else  # if SLOC_before > 688.0
                           return 0.4117647058823529 # (7.0 out of 17.0)
                        end                       end                     end                   else  # if high_ccp_group > 0.5
                    case when added_lines <= 42.5 then
                      case when changed_lines <= 16.5 then
                         return 0.5833333333333334 # (14.0 out of 24.0)
                      else  # if changed_lines > 16.5
                         return 1.0 # (14.0 out of 14.0)
                      end                     else  # if added_lines > 42.5
                       return 0.25 # (4.0 out of 16.0)
                    end                   end                 else  # if added_lines > 62.0
                  case when changed_lines <= 134.0 then
                     return 0.3 # (6.0 out of 20.0)
                  else  # if changed_lines > 134.0
                    case when Single comments_after <= 24.0 then
                       return 0.9259259259259259 # (25.0 out of 27.0)
                    else  # if Single comments_after > 24.0
                      case when Single comments_after <= 67.5 then
                         return 0.5416666666666666 # (13.0 out of 24.0)
                      else  # if Single comments_after > 67.5
                         return 0.8235294117647058 # (14.0 out of 17.0)
                      end                     end                   end                 end               end             else  # if Single comments_before > 187.5
               return 0.875 # (21.0 out of 24.0)
            end           end         end       else  # if McCabe_sum_before > 303.0
        case when Blank_before <= 472.5 then
          case when one_file_fix_rate_diff <= 0.03333333507180214 then
             return 0.037037037037037035 # (1.0 out of 27.0)
          else  # if one_file_fix_rate_diff > 0.03333333507180214
             return 0.25 # (5.0 out of 20.0)
          end         else  # if Blank_before > 472.5
          case when McCabe_sum_before <= 590.5 then
             return 0.8181818181818182 # (9.0 out of 11.0)
          else  # if McCabe_sum_before > 590.5
             return 0.25 # (4.0 out of 16.0)
          end         end       end     end   else  # if too-many-return-statements > 0.5
     return 0.0625 # (1.0 out of 16.0)
  end )