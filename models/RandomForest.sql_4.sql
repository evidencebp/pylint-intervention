create or replace function RandomForest_4 (LOC_diff int64, Comments_after int64, volume_diff int64, LOC_before int64, McCabe_max_diff int64, Blank_diff int64, unnecessary-pass int64, McCabe_max_before int64, prev_count_x int64, prev_count_y int64, N2_diff int64, LLOC_before int64, prev_count int64, too-many-branches int64, added_functions int64, length_diff int64, h2_diff int64, removed_lines int64, too-many-nested-blocks int64, comparison-of-constants int64, bugs_diff int64, N1_diff int64, Comments_diff int64, line-too-long int64, McCabe_sum_diff int64, superfluous-parens int64, Multi_diff int64, changed_lines int64, McCabe_sum_before int64, calculated_length_diff int64, Single comments_after int64, time_diff int64, Single comments_diff int64, Comments_before int64, added_lines int64, effort_diff int64, refactor_mle_diff int64, Blank_before int64, too-many-return-statements int64, pointless-statement int64, too-many-statements int64, cur_count_y int64, unnecessary-semicolon int64, cur_count_x int64, using-constant-test int64, McCabe_sum_after int64, McCabe_max_after int64, too-many-lines int64, LLOC_diff int64, difficulty_diff int64, simplifiable-if-statement int64, vocabulary_diff int64, SLOC_before int64, modified_McCabe_max_diff int64, wildcard-import int64, one_file_fix_rate_diff int64, simplifiable-condition int64, SLOC_diff int64, h1_diff int64, same_day_duration_avg_diff int64, Single comments_before int64, cur_count int64, try-except-raise int64, Simplify-boolean-expression int64, simplifiable-if-expression int64, broad-exception-caught int64, hunks_num int64, too-many-boolean-expressions int64, avg_coupling_code_size_cut_diff int64) as (
  case when changed_lines <= 919.0 then
    case when removed_lines <= 226.5 then
      case when SLOC_diff <= 36.5 then
        case when McCabe_max_after <= 51.5 then
          case when Single comments_diff <= -2.5 then
            case when McCabe_sum_after <= 56.5 then
              case when vocabulary_diff <= -10.5 then
                 return 1.0 # (22.0 out of 22.0)
              else  # if vocabulary_diff > -10.5
                 return 0.8947368421052632 # (17.0 out of 19.0)
              end             else  # if McCabe_sum_after > 56.5
              case when McCabe_sum_diff <= -9.5 then
                case when McCabe_sum_before <= 191.0 then
                   return 0.10526315789473684 # (2.0 out of 19.0)
                else  # if McCabe_sum_before > 191.0
                   return 0.38461538461538464 # (5.0 out of 13.0)
                end               else  # if McCabe_sum_diff > -9.5
                 return 0.75 # (18.0 out of 24.0)
              end             end           else  # if Single comments_diff > -2.5
            case when McCabe_max_before <= 15.5 then
              case when removed_lines <= 13.5 then
                case when Single comments_before <= 7.5 then
                  case when too-many-branches <= 0.5 then
                     return 0.4637281910009183 # (505.0 out of 1089.0)
                  else  # if too-many-branches > 0.5
                    case when same_day_duration_avg_diff <= 16.400961875915527 then
                      case when prev_count_x <= 0.5 then
                        case when same_day_duration_avg_diff <= -56.853261947631836 then
                           return 0.25 # (5.0 out of 20.0)
                        else  # if same_day_duration_avg_diff > -56.853261947631836
                           return 0.6 # (15.0 out of 25.0)
                        end                       else  # if prev_count_x > 0.5
                         return 0.4230769230769231 # (11.0 out of 26.0)
                      end                     else  # if same_day_duration_avg_diff > 16.400961875915527
                       return 0.09302325581395349 # (4.0 out of 43.0)
                    end                   end                 else  # if Single comments_before > 7.5
                  case when Single comments_before <= 20.5 then
                     return 0.05263157894736842 # (1.0 out of 19.0)
                  else  # if Single comments_before > 20.5
                    case when SLOC_before <= 614.5 then
                      case when McCabe_max_before <= 10.5 then
                         return 0.42857142857142855 # (6.0 out of 14.0)
                      else  # if McCabe_max_before > 10.5
                         return 0.11764705882352941 # (2.0 out of 17.0)
                      end                     else  # if SLOC_before > 614.5
                       return 0.5217391304347826 # (12.0 out of 23.0)
                    end                   end                 end               else  # if removed_lines > 13.5
                case when Comments_after <= 51.0 then
                  case when added_lines <= 42.0 then
                     return 0.9090909090909091 # (20.0 out of 22.0)
                  else  # if added_lines > 42.0
                     return 0.72 # (18.0 out of 25.0)
                  end                 else  # if Comments_after > 51.0
                   return 0.3333333333333333 # (5.0 out of 15.0)
                end               end             else  # if McCabe_max_before > 15.5
              case when McCabe_sum_before <= 196.5 then
                case when McCabe_max_before <= 45.5 then
                  case when McCabe_sum_diff <= -14.5 then
                     return 0.0 # (0.0 out of 27.0)
                  else  # if McCabe_sum_diff > -14.5
                    case when h2_diff <= -4.5 then
                       return 0.5384615384615384 # (7.0 out of 13.0)
                    else  # if h2_diff > -4.5
                      case when McCabe_sum_after <= 134.5 then
                        case when removed_lines <= 41.0 then
                           return 0.38461538461538464 # (10.0 out of 26.0)
                        else  # if removed_lines > 41.0
                           return 0.05555555555555555 # (1.0 out of 18.0)
                        end                       else  # if McCabe_sum_after > 134.5
                        case when McCabe_sum_after <= 149.0 then
                           return 0.0 # (0.0 out of 32.0)
                        else  # if McCabe_sum_after > 149.0
                           return 0.14285714285714285 # (3.0 out of 21.0)
                        end                       end                     end                   end                 else  # if McCabe_max_before > 45.5
                   return 0.4375 # (7.0 out of 16.0)
                end               else  # if McCabe_sum_before > 196.5
                case when LOC_before <= 3670.0 then
                  case when vocabulary_diff <= -6.5 then
                     return 0.043478260869565216 # (1.0 out of 23.0)
                  else  # if vocabulary_diff > -6.5
                    case when McCabe_sum_before <= 253.5 then
                       return 0.8636363636363636 # (19.0 out of 22.0)
                    else  # if McCabe_sum_before > 253.5
                      case when refactor_mle_diff <= 0.005040935706347227 then
                         return 0.13333333333333333 # (2.0 out of 15.0)
                      else  # if refactor_mle_diff > 0.005040935706347227
                         return 0.35714285714285715 # (5.0 out of 14.0)
                      end                     end                   end                 else  # if LOC_before > 3670.0
                   return 0.7333333333333333 # (11.0 out of 15.0)
                end               end             end           end         else  # if McCabe_max_after > 51.5
           return 0.8888888888888888 # (24.0 out of 27.0)
        end       else  # if SLOC_diff > 36.5
        case when LOC_before <= 949.0 then
           return 0.8947368421052632 # (17.0 out of 19.0)
        else  # if LOC_before > 949.0
           return 1.0 # (18.0 out of 18.0)
        end       end     else  # if removed_lines > 226.5
       return 0.0 # (0.0 out of 34.0)
    end   else  # if changed_lines > 919.0
    case when LLOC_before <= 1042.5 then
       return 1.0 # (28.0 out of 28.0)
    else  # if LLOC_before > 1042.5
       return 0.6470588235294118 # (11.0 out of 17.0)
    end   end )