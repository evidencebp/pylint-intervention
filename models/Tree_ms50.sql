create or replace function Tree_ms50 (McCabe_sum_before int64, changed_lines int64, prev_count_y int64, mostly_delete int64, h1_diff int64, too-many-lines int64, low_McCabe_sum_before int64, length_diff int64, LOC_before int64, simplifiable-if-expression int64, added_functions int64, broad-exception-caught int64, simplifiable-condition int64, prev_count_x int64, McCabe_max_diff int64, SLOC_before int64, LLOC_before int64, low_McCabe_max_diff int64, bugs_diff int64, same_day_duration_avg_diff int64, cur_count_x int64, only_removal int64, McCabe_max_after int64, Single comments_after int64, low_ccp_group int64, one_file_fix_rate_diff int64, effort_diff int64, difficulty_diff int64, removed_lines int64, Comments_diff int64, too-many-boolean-expressions int64, refactor_mle_diff int64, high_McCabe_max_before int64, hunks_num int64, LOC_diff int64, SLOC_diff int64, cur_count_y int64, vocabulary_diff int64, using-constant-test int64, Simplify-boolean-expression int64, low_McCabe_max_before int64, high_McCabe_sum_diff int64, high_McCabe_sum_before int64, McCabe_max_before int64, Comments_after int64, McCabe_sum_diff int64, unnecessary-pass int64, avg_coupling_code_size_cut_diff int64, simplifiable-if-statement int64, is_refactor int64, volume_diff int64, added_lines int64, high_McCabe_max_diff int64, superfluous-parens int64, cur_count int64, low_McCabe_sum_diff int64, calculated_length_diff int64, Multi_diff int64, N2_diff int64, h2_diff int64, Single comments_before int64, McCabe_sum_after int64, N1_diff int64, too-many-statements int64, comparison-of-constants int64, pointless-statement int64, time_diff int64, prev_count int64, Single comments_diff int64, massive_change int64, Blank_diff int64, too-many-nested-blocks int64, Comments_before int64, modified_McCabe_max_diff int64, LLOC_diff int64, Blank_before int64, try-except-raise int64, too-many-branches int64, too-many-return-statements int64, unnecessary-semicolon int64, wildcard-import int64, high_ccp_group int64, line-too-long int64) as (
  case when high_ccp_group <= 0.5 then
    case when Single comments_diff <= -18.5 then
      case when h1_diff <= -2.5 then
         return 1.0 # (1.0 out of 1.0)
      else  # if h1_diff > -2.5
         return 0.5333333333333333 # (0.5333333333333333 out of 1.0)
      end     else  # if Single comments_diff > -18.5
      case when low_ccp_group <= 0.5 then
        case when Comments_after <= 8.5 then
          case when McCabe_sum_after <= 16.5 then
             return 1.0 # (1.0 out of 1.0)
          else  # if McCabe_sum_after > 16.5
             return 0.6470588235294118 # (0.6470588235294118 out of 1.0)
          end         else  # if Comments_after > 8.5
          case when changed_lines <= 136.0 then
            case when same_day_duration_avg_diff <= -0.14351852238178253 then
              case when Comments_before <= 41.0 then
                case when Single comments_before <= 25.5 then
                  case when same_day_duration_avg_diff <= -28.0 then
                     return 0.3 # (0.3 out of 1.0)
                  else  # if same_day_duration_avg_diff > -28.0
                     return 0.5 # (0.5 out of 1.0)
                  end                 else  # if Single comments_before > 25.5
                  case when same_day_duration_avg_diff <= -68.5773811340332 then
                     return 0.6 # (0.6 out of 1.0)
                  else  # if same_day_duration_avg_diff > -68.5773811340332
                     return 1.0 # (1.0 out of 1.0)
                  end                 end               else  # if Comments_before > 41.0
                case when Single comments_before <= 126.5 then
                  case when hunks_num <= 2.5 then
                     return 0.3125 # (0.3125 out of 1.0)
                  else  # if hunks_num > 2.5
                     return 0.0 # (0.0 out of 1.0)
                  end                 else  # if Single comments_before > 126.5
                   return 0.6363636363636364 # (0.6363636363636364 out of 1.0)
                end               end             else  # if same_day_duration_avg_diff > -0.14351852238178253
              case when superfluous-parens <= 0.5 then
                case when Blank_before <= 104.5 then
                  case when removed_lines <= 4.0 then
                     return 0.1 # (0.1 out of 1.0)
                  else  # if removed_lines > 4.0
                     return 0.0 # (0.0 out of 1.0)
                  end                 else  # if Blank_before > 104.5
                  case when SLOC_before <= 1127.5 then
                    case when refactor_mle_diff <= -0.041382383555173874 then
                       return 0.7 # (0.7 out of 1.0)
                    else  # if refactor_mle_diff > -0.041382383555173874
                      case when Single comments_before <= 64.0 then
                         return 0.3 # (0.3 out of 1.0)
                      else  # if Single comments_before > 64.0
                         return 0.0 # (0.0 out of 1.0)
                      end                     end                   else  # if SLOC_before > 1127.5
                     return 0.0 # (0.0 out of 1.0)
                  end                 end               else  # if superfluous-parens > 0.5
                 return 0.5 # (0.5 out of 1.0)
              end             end           else  # if changed_lines > 136.0
            case when added_lines <= 250.5 then
              case when Single comments_diff <= 0.5 then
                case when one_file_fix_rate_diff <= -0.0714285746216774 then
                   return 0.7 # (0.7 out of 1.0)
                else  # if one_file_fix_rate_diff > -0.0714285746216774
                   return 1.0 # (1.0 out of 1.0)
                end               else  # if Single comments_diff > 0.5
                 return 0.4666666666666667 # (0.4666666666666667 out of 1.0)
              end             else  # if added_lines > 250.5
              case when added_functions <= 1.5 then
                 return 0.5 # (0.5 out of 1.0)
              else  # if added_functions > 1.5
                 return 0.0 # (0.0 out of 1.0)
              end             end           end         end       else  # if low_ccp_group > 0.5
        case when Comments_diff <= 20.5 then
          case when LOC_before <= 2947.5 then
            case when McCabe_sum_before <= 30.5 then
               return 0.3076923076923077 # (0.3076923076923077 out of 1.0)
            else  # if McCabe_sum_before > 30.5
              case when too-many-statements <= 0.5 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if too-many-statements > 0.5
                case when McCabe_max_diff <= -0.5 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if McCabe_max_diff > -0.5
                   return 0.4 # (0.4 out of 1.0)
                end               end             end           else  # if LOC_before > 2947.5
             return 0.6 # (0.6 out of 1.0)
          end         else  # if Comments_diff > 20.5
           return 0.9230769230769231 # (0.9230769230769231 out of 1.0)
        end       end     end   else  # if high_ccp_group > 0.5
    case when changed_lines <= 350.5 then
      case when Single comments_diff <= 4.5 then
        case when one_file_fix_rate_diff <= 0.36666667461395264 then
          case when avg_coupling_code_size_cut_diff <= -1.2380952835083008 then
             return 0.5333333333333333 # (0.5333333333333333 out of 1.0)
          else  # if avg_coupling_code_size_cut_diff > -1.2380952835083008
            case when length_diff <= -0.5 then
              case when changed_lines <= 46.5 then
                 return 0.4 # (0.4 out of 1.0)
              else  # if changed_lines > 46.5
                case when Comments_before <= 60.0 then
                   return 0.7272727272727273 # (0.7272727272727273 out of 1.0)
                else  # if Comments_before > 60.0
                   return 1.0 # (1.0 out of 1.0)
                end               end             else  # if length_diff > -0.5
              case when vocabulary_diff <= 3.5 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if vocabulary_diff > 3.5
                 return 0.9 # (0.9 out of 1.0)
              end             end           end         else  # if one_file_fix_rate_diff > 0.36666667461395264
           return 0.42857142857142855 # (0.42857142857142855 out of 1.0)
        end       else  # if Single comments_diff > 4.5
         return 0.1 # (0.1 out of 1.0)
      end     else  # if changed_lines > 350.5
      case when h1_diff <= -1.0 then
         return 0.3 # (0.3 out of 1.0)
      else  # if h1_diff > -1.0
         return 0.0 # (0.0 out of 1.0)
      end     end   end )