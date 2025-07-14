create or replace function RandomForest_3 (SLOC_before int64, simplifiable-condition int64, bugs_diff int64, Blank_before int64, LLOC_diff int64, try-except-raise int64, LLOC_before int64, changed_lines int64, h2_diff int64, prev_count_x int64, too-many-lines int64, cur_count_y int64, Comments_before int64, McCabe_sum_after int64, cur_count_x int64, vocabulary_diff int64, Single comments_before int64, N2_diff int64, high_ccp_group int64, massive_change int64, added_lines int64, prev_count int64, refactor_mle_diff int64, superfluous-parens int64, avg_coupling_code_size_cut_diff int64, McCabe_sum_diff int64, LOC_before int64, too-many-return-statements int64, too-many-branches int64, too-many-nested-blocks int64, difficulty_diff int64, time_diff int64, Single comments_after int64, calculated_length_diff int64, Simplify-boolean-expression int64, unnecessary-semicolon int64, mostly_delete int64, effort_diff int64, Multi_diff int64, McCabe_max_diff int64, is_refactor int64, only_removal int64, LOC_diff int64, one_file_fix_rate_diff int64, Comments_after int64, comparison-of-constants int64, McCabe_max_after int64, length_diff int64, simplifiable-if-statement int64, removed_lines int64, unnecessary-pass int64, Comments_diff int64, cur_count int64, same_day_duration_avg_diff int64, hunks_num int64, N1_diff int64, line-too-long int64, volume_diff int64, using-constant-test int64, too-many-boolean-expressions int64, modified_McCabe_max_diff int64, h1_diff int64, added_functions int64, SLOC_diff int64, too-many-statements int64, pointless-statement int64, wildcard-import int64, McCabe_max_before int64, prev_count_y int64, broad-exception-caught int64, Blank_diff int64, McCabe_sum_before int64, simplifiable-if-expression int64, Single comments_diff int64) as (
  case when high_ccp_group <= 0.5 then
    case when refactor_mle_diff <= -0.363955557346344 then
      case when vocabulary_diff <= -12.0 then
         return 0.8666666666666667 # (13.0 out of 15.0)
      else  # if vocabulary_diff > -12.0
         return 0.6666666666666666 # (18.0 out of 27.0)
      end     else  # if refactor_mle_diff > -0.363955557346344
      case when Comments_diff <= -48.5 then
         return 0.8571428571428571 # (12.0 out of 14.0)
      else  # if Comments_diff > -48.5
        case when h2_diff <= -28.5 then
          case when LLOC_diff <= -151.0 then
             return 0.23809523809523808 # (5.0 out of 21.0)
          else  # if LLOC_diff > -151.0
             return 0.0 # (0.0 out of 31.0)
          end         else  # if h2_diff > -28.5
          case when SLOC_before <= 118.5 then
             return 0.7857142857142857 # (11.0 out of 14.0)
          else  # if SLOC_before > 118.5
            case when N1_diff <= -9.5 then
              case when added_functions <= 0.5 then
                 return 0.3125 # (5.0 out of 16.0)
              else  # if added_functions > 0.5
                 return 0.8125 # (13.0 out of 16.0)
              end             else  # if N1_diff > -9.5
              case when refactor_mle_diff <= -0.2043326273560524 then
                case when SLOC_before <= 569.5 then
                   return 0.045454545454545456 # (1.0 out of 22.0)
                else  # if SLOC_before > 569.5
                   return 0.07692307692307693 # (2.0 out of 26.0)
                end               else  # if refactor_mle_diff > -0.2043326273560524
                case when McCabe_sum_before <= 136.0 then
                  case when McCabe_sum_after <= 105.0 then
                    case when hunks_num <= 2.5 then
                      case when Comments_after <= 98.5 then
                         return 0.45161290322580644 # (14.0 out of 31.0)
                      else  # if Comments_after > 98.5
                         return 0.8461538461538461 # (11.0 out of 13.0)
                      end                     else  # if hunks_num > 2.5
                      case when h2_diff <= 1.0 then
                        case when McCabe_max_after <= 6.0 then
                           return 0.058823529411764705 # (1.0 out of 17.0)
                        else  # if McCabe_max_after > 6.0
                          case when McCabe_sum_before <= 66.5 then
                             return 0.5625 # (9.0 out of 16.0)
                          else  # if McCabe_sum_before > 66.5
                             return 0.15789473684210525 # (3.0 out of 19.0)
                          end                         end                       else  # if h2_diff > 1.0
                         return 0.21052631578947367 # (4.0 out of 19.0)
                      end                     end                   else  # if McCabe_sum_after > 105.0
                     return 0.9 # (18.0 out of 20.0)
                  end                 else  # if McCabe_sum_before > 136.0
                  case when changed_lines <= 160.0 then
                    case when N2_diff <= -1.5 then
                      case when added_lines <= 49.0 then
                         return 0.0 # (0.0 out of 23.0)
                      else  # if added_lines > 49.0
                         return 0.07142857142857142 # (1.0 out of 14.0)
                      end                     else  # if N2_diff > -1.5
                      case when SLOC_before <= 643.5 then
                         return 0.0 # (0.0 out of 27.0)
                      else  # if SLOC_before > 643.5
                        case when refactor_mle_diff <= -0.007893772795796394 then
                           return 0.2631578947368421 # (5.0 out of 19.0)
                        else  # if refactor_mle_diff > -0.007893772795796394
                           return 0.5 # (10.0 out of 20.0)
                        end                       end                     end                   else  # if changed_lines > 160.0
                     return 0.48 # (12.0 out of 25.0)
                  end                 end               end             end           end         end       end     end   else  # if high_ccp_group > 0.5
    case when Comments_diff <= 3.5 then
      case when Comments_before <= 101.0 then
        case when refactor_mle_diff <= -0.13844040036201477 then
           return 0.5833333333333334 # (14.0 out of 24.0)
        else  # if refactor_mle_diff > -0.13844040036201477
          case when McCabe_max_diff <= -1.5 then
             return 0.8571428571428571 # (18.0 out of 21.0)
          else  # if McCabe_max_diff > -1.5
             return 1.0 # (41.0 out of 41.0)
          end         end       else  # if Comments_before > 101.0
         return 0.47058823529411764 # (16.0 out of 34.0)
      end     else  # if Comments_diff > 3.5
       return 0.26666666666666666 # (4.0 out of 15.0)
    end   end )