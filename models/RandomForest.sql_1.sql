create or replace function RandomForest_1 (prev_count int64, prev_count_x int64, prev_count_y int64, using-constant-test int64, Comments_diff int64, massive_change int64, McCabe_max_after int64, Comments_before int64, too-many-statements int64, cur_count_x int64, h1_diff int64, McCabe_sum_diff int64, LLOC_before int64, McCabe_sum_before int64, high_McCabe_max_before int64, avg_coupling_code_size_cut_diff int64, is_refactor int64, N2_diff int64, too-many-branches int64, SLOC_before int64, too-many-nested-blocks int64, too-many-lines int64, bugs_diff int64, time_diff int64, Single comments_after int64, simplifiable-condition int64, Multi_diff int64, high_McCabe_sum_before int64, low_ccp_group int64, refactor_mle_diff int64, low_McCabe_max_diff int64, SLOC_diff int64, changed_lines int64, hunks_num int64, McCabe_sum_after int64, cur_count_y int64, one_file_fix_rate_diff int64, low_McCabe_sum_before int64, modified_McCabe_max_diff int64, superfluous-parens int64, mostly_delete int64, added_functions int64, Comments_after int64, N1_diff int64, McCabe_max_diff int64, simplifiable-if-statement int64, LOC_before int64, low_McCabe_max_before int64, McCabe_max_before int64, try-except-raise int64, line-too-long int64, unnecessary-semicolon int64, wildcard-import int64, difficulty_diff int64, Simplify-boolean-expression int64, cur_count int64, low_McCabe_sum_diff int64, pointless-statement int64, length_diff int64, broad-exception-caught int64, h2_diff int64, high_McCabe_sum_diff int64, only_removal int64, comparison-of-constants int64, Single comments_diff int64, too-many-boolean-expressions int64, Blank_before int64, calculated_length_diff int64, Single comments_before int64, removed_lines int64, simplifiable-if-expression int64, LOC_diff int64, volume_diff int64, high_McCabe_max_diff int64, high_ccp_group int64, same_day_duration_avg_diff int64, Blank_diff int64, effort_diff int64, too-many-return-statements int64, added_lines int64, unnecessary-pass int64, vocabulary_diff int64, LLOC_diff int64) as (
  case when McCabe_max_before <= 6.5 then
    case when SLOC_diff <= 2.0 then
      case when high_ccp_group <= 0.5 then
         return 0.7142857142857143 # (0.7142857142857143 out of 1.0)
      else  # if high_ccp_group > 0.5
         return 0.9259259259259259 # (0.9259259259259259 out of 1.0)
      end     else  # if SLOC_diff > 2.0
       return 0.5625 # (0.5625 out of 1.0)
    end   else  # if McCabe_max_before > 6.5
    case when h1_diff <= -2.5 then
      case when hunks_num <= 3.5 then
         return 0.4482758620689655 # (0.4482758620689655 out of 1.0)
      else  # if hunks_num > 3.5
         return 0.967741935483871 # (0.967741935483871 out of 1.0)
      end     else  # if h1_diff > -2.5
      case when N1_diff <= -21.0 then
        case when LLOC_diff <= -141.0 then
           return 0.35294117647058826 # (0.35294117647058826 out of 1.0)
        else  # if LLOC_diff > -141.0
           return 0.0 # (0.0 out of 1.0)
        end       else  # if N1_diff > -21.0
        case when removed_lines <= 176.0 then
          case when added_functions <= 0.5 then
            case when SLOC_diff <= 4.5 then
              case when Comments_after <= 112.5 then
                case when SLOC_before <= 936.5 then
                  case when high_ccp_group <= 0.5 then
                    case when low_ccp_group <= 0.5 then
                      case when McCabe_sum_diff <= -3.5 then
                         return 0.17857142857142858 # (0.17857142857142858 out of 1.0)
                      else  # if McCabe_sum_diff > -3.5
                        case when removed_lines <= 0.5 then
                           return 0.2857142857142857 # (0.2857142857142857 out of 1.0)
                        else  # if removed_lines > 0.5
                          case when Comments_after <= 47.0 then
                             return 0.6296296296296297 # (0.6296296296296297 out of 1.0)
                          else  # if Comments_after > 47.0
                             return 0.9047619047619048 # (0.9047619047619048 out of 1.0)
                          end                         end                       end                     else  # if low_ccp_group > 0.5
                      case when LOC_diff <= -0.5 then
                         return 0.0 # (0.0 out of 1.0)
                      else  # if LOC_diff > -0.5
                         return 0.2 # (0.2 out of 1.0)
                      end                     end                   else  # if high_ccp_group > 0.5
                    case when SLOC_diff <= -3.0 then
                       return 0.9 # (0.9 out of 1.0)
                    else  # if SLOC_diff > -3.0
                       return 0.5384615384615384 # (0.5384615384615384 out of 1.0)
                    end                   end                 else  # if SLOC_before > 936.5
                   return 0.9047619047619048 # (0.9047619047619048 out of 1.0)
                end               else  # if Comments_after > 112.5
                case when same_day_duration_avg_diff <= 6.533848762512207 then
                   return 0.03125 # (0.03125 out of 1.0)
                else  # if same_day_duration_avg_diff > 6.533848762512207
                   return 0.5625 # (0.5625 out of 1.0)
                end               end             else  # if SLOC_diff > 4.5
              case when Blank_before <= 100.0 then
                 return 0.5263157894736842 # (0.5263157894736842 out of 1.0)
              else  # if Blank_before > 100.0
                case when McCabe_max_after <= 25.0 then
                   return 0.047619047619047616 # (0.047619047619047616 out of 1.0)
                else  # if McCabe_max_after > 25.0
                   return 0.21428571428571427 # (0.21428571428571427 out of 1.0)
                end               end             end           else  # if added_functions > 0.5
            case when Comments_before <= 172.0 then
              case when high_ccp_group <= 0.5 then
                case when McCabe_max_before <= 24.5 then
                  case when LOC_diff <= 12.0 then
                    case when removed_lines <= 35.0 then
                       return 0.375 # (0.375 out of 1.0)
                    else  # if removed_lines > 35.0
                       return 0.7368421052631579 # (0.7368421052631579 out of 1.0)
                    end                   else  # if LOC_diff > 12.0
                     return 0.14285714285714285 # (0.14285714285714285 out of 1.0)
                  end                 else  # if McCabe_max_before > 24.5
                   return 0.7777777777777778 # (0.7777777777777778 out of 1.0)
                end               else  # if high_ccp_group > 0.5
                 return 0.9285714285714286 # (0.9285714285714286 out of 1.0)
              end             else  # if Comments_before > 172.0
               return 1.0 # (1.0 out of 1.0)
            end           end         else  # if removed_lines > 176.0
          case when refactor_mle_diff <= -0.08319350332021713 then
             return 0.0 # (0.0 out of 1.0)
          else  # if refactor_mle_diff > -0.08319350332021713
             return 0.4230769230769231 # (0.4230769230769231 out of 1.0)
          end         end       end     end   end )