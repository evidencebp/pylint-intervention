create or replace function RandomForest_8 (using-constant-test int64, simplifiable-if-statement int64, Comments_after int64, same_day_duration_avg_diff int64, Single comments_before int64, one_file_fix_rate_diff int64, too-many-boolean-expressions int64, Single comments_diff int64, high_McCabe_sum_before int64, pointless-statement int64, bugs_diff int64, McCabe_max_before int64, length_diff int64, LOC_diff int64, N2_diff int64, superfluous-parens int64, too-many-nested-blocks int64, effort_diff int64, cur_count_x int64, high_McCabe_max_before int64, comparison-of-constants int64, SLOC_diff int64, hunks_num int64, high_McCabe_max_diff int64, prev_count int64, McCabe_sum_after int64, cur_count_y int64, refactor_mle_diff int64, too-many-return-statements int64, too-many-statements int64, too-many-lines int64, only_removal int64, removed_lines int64, cur_count int64, volume_diff int64, is_refactor int64, prev_count_y int64, calculated_length_diff int64, Simplify-boolean-expression int64, h1_diff int64, McCabe_max_diff int64, wildcard-import int64, McCabe_sum_before int64, line-too-long int64, N1_diff int64, too-many-branches int64, h2_diff int64, McCabe_max_after int64, unnecessary-pass int64, avg_coupling_code_size_cut_diff int64, high_ccp_group int64, vocabulary_diff int64, try-except-raise int64, broad-exception-caught int64, simplifiable-condition int64, LLOC_before int64, added_functions int64, LLOC_diff int64, difficulty_diff int64, McCabe_sum_diff int64, Multi_diff int64, massive_change int64, mostly_delete int64, Comments_before int64, changed_lines int64, Comments_diff int64, time_diff int64, Blank_before int64, high_McCabe_sum_diff int64, added_lines int64, prev_count_x int64, unnecessary-semicolon int64, Blank_diff int64, modified_McCabe_max_diff int64, Single comments_after int64, LOC_before int64, simplifiable-if-expression int64, SLOC_before int64) as (
  case when N1_diff <= 9.5 then
    case when SLOC_diff <= 29.5 then
      case when SLOC_diff <= 9.5 then
        case when Comments_diff <= 1.5 then
          case when N1_diff <= -58.0 then
             return 0.9523809523809523 # (20.0 out of 21.0)
          else  # if N1_diff > -58.0
            case when McCabe_sum_before <= 395.0 then
              case when McCabe_sum_diff <= -7.5 then
                case when Blank_diff <= -12.5 then
                  case when Single comments_before <= 55.5 then
                     return 0.6363636363636364 # (14.0 out of 22.0)
                  else  # if Single comments_before > 55.5
                     return 0.21052631578947367 # (4.0 out of 19.0)
                  end                 else  # if Blank_diff > -12.5
                  case when McCabe_sum_diff <= -14.5 then
                    case when McCabe_max_after <= 14.5 then
                       return 0.0 # (0.0 out of 24.0)
                    else  # if McCabe_max_after > 14.5
                       return 0.09090909090909091 # (1.0 out of 11.0)
                    end                   else  # if McCabe_sum_diff > -14.5
                     return 0.20689655172413793 # (6.0 out of 29.0)
                  end                 end               else  # if McCabe_sum_diff > -7.5
                case when one_file_fix_rate_diff <= 0.4833333343267441 then
                  case when Single comments_before <= 4.5 then
                     return 0.8888888888888888 # (24.0 out of 27.0)
                  else  # if Single comments_before > 4.5
                    case when added_lines <= 0.5 then
                       return 0.13043478260869565 # (3.0 out of 23.0)
                    else  # if added_lines > 0.5
                      case when Blank_before <= 109.0 then
                        case when Comments_before <= 52.5 then
                          case when Comments_before <= 13.0 then
                             return 0.1875 # (3.0 out of 16.0)
                          else  # if Comments_before > 13.0
                            case when SLOC_diff <= -1.5 then
                               return 0.8125 # (26.0 out of 32.0)
                            else  # if SLOC_diff > -1.5
                               return 0.5625 # (9.0 out of 16.0)
                            end                           end                         else  # if Comments_before > 52.5
                           return 0.16666666666666666 # (5.0 out of 30.0)
                        end                       else  # if Blank_before > 109.0
                        case when SLOC_before <= 934.5 then
                          case when Comments_after <= 63.5 then
                             return 0.92 # (23.0 out of 25.0)
                          else  # if Comments_after > 63.5
                             return 0.6666666666666666 # (14.0 out of 21.0)
                          end                         else  # if SLOC_before > 934.5
                          case when hunks_num <= 3.5 then
                             return 0.6875 # (11.0 out of 16.0)
                          else  # if hunks_num > 3.5
                             return 0.47368421052631576 # (9.0 out of 19.0)
                          end                         end                       end                     end                   end                 else  # if one_file_fix_rate_diff > 0.4833333343267441
                   return 0.95 # (19.0 out of 20.0)
                end               end             else  # if McCabe_sum_before > 395.0
              case when McCabe_max_after <= 39.0 then
                 return 0.8095238095238095 # (17.0 out of 21.0)
              else  # if McCabe_max_after > 39.0
                 return 0.7894736842105263 # (15.0 out of 19.0)
              end             end           end         else  # if Comments_diff > 1.5
          case when high_McCabe_max_before <= 0.5 then
            case when removed_lines <= 46.5 then
               return 0.0 # (0.0 out of 21.0)
            else  # if removed_lines > 46.5
               return 0.17647058823529413 # (3.0 out of 17.0)
            end           else  # if high_McCabe_max_before > 0.5
             return 0.29411764705882354 # (5.0 out of 17.0)
          end         end       else  # if SLOC_diff > 9.5
        case when N2_diff <= -0.5 then
           return 0.05 # (1.0 out of 20.0)
        else  # if N2_diff > -0.5
           return 0.2 # (6.0 out of 30.0)
        end       end     else  # if SLOC_diff > 29.5
      case when LOC_before <= 1221.0 then
        case when Blank_before <= 51.5 then
           return 1.0 # (22.0 out of 22.0)
        else  # if Blank_before > 51.5
           return 0.7333333333333333 # (11.0 out of 15.0)
        end       else  # if LOC_before > 1221.0
         return 0.5384615384615384 # (7.0 out of 13.0)
      end     end   else  # if N1_diff > 9.5
    case when changed_lines <= 351.0 then
       return 0.25 # (4.0 out of 16.0)
    else  # if changed_lines > 351.0
       return 0.05555555555555555 # (1.0 out of 18.0)
    end   end )