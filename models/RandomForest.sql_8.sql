create or replace function RandomForest_8 (McCabe_sum_before int64, changed_lines int64, prev_count_y int64, mostly_delete int64, h1_diff int64, too-many-lines int64, low_McCabe_sum_before int64, length_diff int64, LOC_before int64, simplifiable-if-expression int64, added_functions int64, broad-exception-caught int64, simplifiable-condition int64, prev_count_x int64, McCabe_max_diff int64, SLOC_before int64, LLOC_before int64, low_McCabe_max_diff int64, bugs_diff int64, same_day_duration_avg_diff int64, cur_count_x int64, only_removal int64, McCabe_max_after int64, Single comments_after int64, low_ccp_group int64, one_file_fix_rate_diff int64, effort_diff int64, difficulty_diff int64, removed_lines int64, Comments_diff int64, too-many-boolean-expressions int64, refactor_mle_diff int64, high_McCabe_max_before int64, hunks_num int64, LOC_diff int64, SLOC_diff int64, cur_count_y int64, vocabulary_diff int64, using-constant-test int64, Simplify-boolean-expression int64, low_McCabe_max_before int64, high_McCabe_sum_diff int64, high_McCabe_sum_before int64, McCabe_max_before int64, Comments_after int64, McCabe_sum_diff int64, unnecessary-pass int64, avg_coupling_code_size_cut_diff int64, simplifiable-if-statement int64, is_refactor int64, volume_diff int64, added_lines int64, high_McCabe_max_diff int64, superfluous-parens int64, cur_count int64, low_McCabe_sum_diff int64, calculated_length_diff int64, Multi_diff int64, N2_diff int64, h2_diff int64, Single comments_before int64, McCabe_sum_after int64, N1_diff int64, too-many-statements int64, comparison-of-constants int64, pointless-statement int64, time_diff int64, prev_count int64, Single comments_diff int64, massive_change int64, Blank_diff int64, too-many-nested-blocks int64, Comments_before int64, modified_McCabe_max_diff int64, LLOC_diff int64, Blank_before int64, try-except-raise int64, too-many-branches int64, too-many-return-statements int64, unnecessary-semicolon int64, wildcard-import int64, high_ccp_group int64, line-too-long int64) as (
  case when h2_diff <= -193.0 then
     return 0.8695652173913043 # (0.8695652173913043 out of 1.0)
  else  # if h2_diff > -193.0
    case when removed_lines <= 184.5 then
      case when low_ccp_group <= 0.5 then
        case when changed_lines <= 136.5 then
          case when low_McCabe_sum_diff <= 0.5 then
            case when Single comments_after <= 3.5 then
               return 0.8571428571428571 # (0.8571428571428571 out of 1.0)
            else  # if Single comments_after > 3.5
              case when McCabe_sum_before <= 192.5 then
                case when high_ccp_group <= 0.5 then
                  case when SLOC_before <= 246.0 then
                     return 0.5185185185185185 # (0.5185185185185185 out of 1.0)
                  else  # if SLOC_before > 246.0
                    case when refactor_mle_diff <= 0.037602392956614494 then
                      case when McCabe_sum_after <= 165.5 then
                        case when changed_lines <= 41.0 then
                           return 0.5555555555555556 # (0.5555555555555556 out of 1.0)
                        else  # if changed_lines > 41.0
                           return 0.21428571428571427 # (0.21428571428571427 out of 1.0)
                        end                       else  # if McCabe_sum_after > 165.5
                         return 0.15384615384615385 # (0.15384615384615385 out of 1.0)
                      end                     else  # if refactor_mle_diff > 0.037602392956614494
                      case when Single comments_before <= 61.0 then
                         return 0.2222222222222222 # (0.2222222222222222 out of 1.0)
                      else  # if Single comments_before > 61.0
                         return 0.038461538461538464 # (0.038461538461538464 out of 1.0)
                      end                     end                   end                 else  # if high_ccp_group > 0.5
                  case when Single comments_before <= 26.5 then
                     return 0.375 # (0.375 out of 1.0)
                  else  # if Single comments_before > 26.5
                     return 0.7619047619047619 # (0.7619047619047619 out of 1.0)
                  end                 end               else  # if McCabe_sum_before > 192.5
                case when McCabe_sum_before <= 222.0 then
                   return 0.9411764705882353 # (0.9411764705882353 out of 1.0)
                else  # if McCabe_sum_before > 222.0
                  case when McCabe_max_after <= 39.0 then
                     return 0.22580645161290322 # (0.22580645161290322 out of 1.0)
                  else  # if McCabe_max_after > 39.0
                    case when LOC_diff <= 4.5 then
                       return 0.7894736842105263 # (0.7894736842105263 out of 1.0)
                    else  # if LOC_diff > 4.5
                       return 0.42857142857142855 # (0.42857142857142855 out of 1.0)
                    end                   end                 end               end             end           else  # if low_McCabe_sum_diff > 0.5
             return 0.0625 # (0.0625 out of 1.0)
          end         else  # if changed_lines > 136.5
          case when h2_diff <= -56.0 then
             return 0.13636363636363635 # (0.13636363636363635 out of 1.0)
          else  # if h2_diff > -56.0
            case when Blank_before <= 190.5 then
              case when added_lines <= 149.5 then
                case when Blank_before <= 59.5 then
                   return 0.6153846153846154 # (0.6153846153846154 out of 1.0)
                else  # if Blank_before > 59.5
                   return 0.8823529411764706 # (0.8823529411764706 out of 1.0)
                end               else  # if added_lines > 149.5
                 return 0.25 # (0.25 out of 1.0)
              end             else  # if Blank_before > 190.5
              case when Single comments_after <= 66.0 then
                 return 0.9411764705882353 # (0.9411764705882353 out of 1.0)
              else  # if Single comments_after > 66.0
                 return 1.0 # (1.0 out of 1.0)
              end             end           end         end       else  # if low_ccp_group > 0.5
        case when N1_diff <= -12.5 then
           return 0.6153846153846154 # (0.6153846153846154 out of 1.0)
        else  # if N1_diff > -12.5
          case when h1_diff <= 0.5 then
            case when added_lines <= 12.5 then
              case when SLOC_diff <= 2.5 then
                 return 0.07142857142857142 # (0.07142857142857142 out of 1.0)
              else  # if SLOC_diff > 2.5
                 return 0.4444444444444444 # (0.4444444444444444 out of 1.0)
              end             else  # if added_lines > 12.5
              case when vocabulary_diff <= -7.5 then
                 return 0.21428571428571427 # (0.21428571428571427 out of 1.0)
              else  # if vocabulary_diff > -7.5
                case when McCabe_max_before <= 14.0 then
                   return 0.1 # (0.1 out of 1.0)
                else  # if McCabe_max_before > 14.0
                   return 0.0 # (0.0 out of 1.0)
                end               end             end           else  # if h1_diff > 0.5
             return 0.75 # (0.75 out of 1.0)
          end         end       end     else  # if removed_lines > 184.5
      case when added_functions <= 0.5 then
         return 0.14285714285714285 # (0.14285714285714285 out of 1.0)
      else  # if added_functions > 0.5
         return 0.0 # (0.0 out of 1.0)
      end     end   end )