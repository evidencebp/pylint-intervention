create or replace function RandomForest_1 (using-constant-test int64, simplifiable-if-statement int64, Comments_after int64, same_day_duration_avg_diff int64, Single comments_before int64, one_file_fix_rate_diff int64, too-many-boolean-expressions int64, Single comments_diff int64, high_McCabe_sum_before int64, pointless-statement int64, bugs_diff int64, McCabe_max_before int64, length_diff int64, LOC_diff int64, N2_diff int64, superfluous-parens int64, too-many-nested-blocks int64, effort_diff int64, cur_count_x int64, high_McCabe_max_before int64, comparison-of-constants int64, SLOC_diff int64, hunks_num int64, high_McCabe_max_diff int64, prev_count int64, McCabe_sum_after int64, cur_count_y int64, refactor_mle_diff int64, too-many-return-statements int64, too-many-statements int64, too-many-lines int64, only_removal int64, removed_lines int64, cur_count int64, volume_diff int64, is_refactor int64, prev_count_y int64, calculated_length_diff int64, Simplify-boolean-expression int64, h1_diff int64, McCabe_max_diff int64, wildcard-import int64, McCabe_sum_before int64, line-too-long int64, N1_diff int64, too-many-branches int64, h2_diff int64, McCabe_max_after int64, unnecessary-pass int64, avg_coupling_code_size_cut_diff int64, high_ccp_group int64, vocabulary_diff int64, try-except-raise int64, broad-exception-caught int64, simplifiable-condition int64, LLOC_before int64, added_functions int64, LLOC_diff int64, difficulty_diff int64, McCabe_sum_diff int64, Multi_diff int64, massive_change int64, mostly_delete int64, Comments_before int64, changed_lines int64, Comments_diff int64, time_diff int64, Blank_before int64, high_McCabe_sum_diff int64, added_lines int64, prev_count_x int64, unnecessary-semicolon int64, Blank_diff int64, modified_McCabe_max_diff int64, Single comments_after int64, LOC_before int64, simplifiable-if-expression int64, SLOC_before int64) as (
  case when N1_diff <= -47.0 then
    case when McCabe_max_diff <= -8.5 then
       return 1.0 # (22.0 out of 22.0)
    else  # if McCabe_max_diff > -8.5
       return 0.6 # (12.0 out of 20.0)
    end   else  # if N1_diff > -47.0
    case when Multi_diff <= -33.5 then
       return 0.8947368421052632 # (17.0 out of 19.0)
    else  # if Multi_diff > -33.5
      case when SLOC_diff <= 38.0 then
        case when McCabe_sum_before <= 349.5 then
          case when line-too-long <= 0.5 then
            case when high_ccp_group <= 0.5 then
              case when Single comments_before <= 59.0 then
                case when LOC_before <= 1052.5 then
                  case when added_lines <= 98.5 then
                    case when McCabe_sum_diff <= -3.5 then
                      case when same_day_duration_avg_diff <= -24.54264736175537 then
                         return 0.6 # (12.0 out of 20.0)
                      else  # if same_day_duration_avg_diff > -24.54264736175537
                         return 0.35 # (7.0 out of 20.0)
                      end                     else  # if McCabe_sum_diff > -3.5
                      case when SLOC_before <= 458.5 then
                        case when McCabe_max_before <= 15.5 then
                          case when McCabe_max_after <= 11.5 then
                             return 0.20689655172413793 # (6.0 out of 29.0)
                          else  # if McCabe_max_after > 11.5
                             return 0.875 # (14.0 out of 16.0)
                          end                         else  # if McCabe_max_before > 15.5
                           return 0.1 # (2.0 out of 20.0)
                        end                       else  # if SLOC_before > 458.5
                         return 0.125 # (3.0 out of 24.0)
                      end                     end                   else  # if added_lines > 98.5
                     return 0.05 # (1.0 out of 20.0)
                  end                 else  # if LOC_before > 1052.5
                   return 0.5454545454545454 # (12.0 out of 22.0)
                end               else  # if Single comments_before > 59.0
                case when Comments_diff <= 1.0 then
                  case when McCabe_sum_after <= 146.0 then
                    case when same_day_duration_avg_diff <= -22.78708839416504 then
                       return 0.125 # (2.0 out of 16.0)
                    else  # if same_day_duration_avg_diff > -22.78708839416504
                       return 0.0 # (0.0 out of 22.0)
                    end                   else  # if McCabe_sum_after > 146.0
                    case when LOC_before <= 1213.0 then
                       return 0.36363636363636365 # (4.0 out of 11.0)
                    else  # if LOC_before > 1213.0
                       return 0.16666666666666666 # (3.0 out of 18.0)
                    end                   end                 else  # if Comments_diff > 1.0
                   return 0.0 # (0.0 out of 29.0)
                end               end             else  # if high_ccp_group > 0.5
              case when refactor_mle_diff <= -0.1276846081018448 then
                 return 0.32 # (8.0 out of 25.0)
              else  # if refactor_mle_diff > -0.1276846081018448
                case when avg_coupling_code_size_cut_diff <= -0.959090918302536 then
                   return 0.3 # (6.0 out of 20.0)
                else  # if avg_coupling_code_size_cut_diff > -0.959090918302536
                  case when changed_lines <= 37.5 then
                     return 1.0 # (24.0 out of 24.0)
                  else  # if changed_lines > 37.5
                     return 0.75 # (18.0 out of 24.0)
                  end                 end               end             end           else  # if line-too-long > 0.5
            case when SLOC_before <= 170.5 then
               return 0.7894736842105263 # (15.0 out of 19.0)
            else  # if SLOC_before > 170.5
              case when McCabe_sum_after <= 63.0 then
                 return 0.5882352941176471 # (10.0 out of 17.0)
              else  # if McCabe_sum_after > 63.0
                 return 0.48 # (12.0 out of 25.0)
              end             end           end         else  # if McCabe_sum_before > 349.5
          case when Comments_diff <= -0.5 then
             return 0.38461538461538464 # (10.0 out of 26.0)
          else  # if Comments_diff > -0.5
            case when added_lines <= 8.5 then
               return 0.75 # (12.0 out of 16.0)
            else  # if added_lines > 8.5
               return 0.9411764705882353 # (16.0 out of 17.0)
            end           end         end       else  # if SLOC_diff > 38.0
        case when changed_lines <= 301.5 then
          case when Comments_before <= 98.5 then
             return 0.7777777777777778 # (14.0 out of 18.0)
          else  # if Comments_before > 98.5
             return 1.0 # (21.0 out of 21.0)
          end         else  # if changed_lines > 301.5
           return 0.45 # (9.0 out of 20.0)
        end       end     end   end )