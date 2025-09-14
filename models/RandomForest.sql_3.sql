create or replace function RandomForest_3 (h1_diff int64, simplifiable-if-statement int64, McCabe_max_after int64, McCabe_sum_before int64, Single comments_before int64, low_McCabe_max_diff int64, high_ccp_group int64, pointless-statement int64, too-many-branches int64, high_McCabe_max_before int64, superfluous-parens int64, Multi_diff int64, wildcard-import int64, high_McCabe_sum_before int64, LLOC_before int64, cur_count int64, unnecessary-semicolon int64, Comments_after int64, mostly_delete int64, simplifiable-condition int64, avg_coupling_code_size_cut_diff int64, added_functions int64, McCabe_max_diff int64, McCabe_sum_diff int64, LLOC_diff int64, LOC_before int64, Comments_diff int64, prev_count_x int64, effort_diff int64, try-except-raise int64, difficulty_diff int64, line-too-long int64, Simplify-boolean-expression int64, SLOC_diff int64, McCabe_sum_after int64, refactor_mle_diff int64, one_file_fix_rate_diff int64, is_refactor int64, too-many-lines int64, too-many-boolean-expressions int64, Single comments_diff int64, low_McCabe_sum_diff int64, cur_count_y int64, comparison-of-constants int64, Comments_before int64, too-many-return-statements int64, vocabulary_diff int64, massive_change int64, hunks_num int64, modified_McCabe_max_diff int64, high_McCabe_sum_diff int64, N2_diff int64, broad-exception-caught int64, length_diff int64, unnecessary-pass int64, time_diff int64, changed_lines int64, Single comments_after int64, h2_diff int64, low_McCabe_sum_before int64, cur_count_x int64, McCabe_max_before int64, using-constant-test int64, added_lines int64, same_day_duration_avg_diff int64, prev_count_y int64, Blank_diff int64, LOC_diff int64, only_removal int64, low_McCabe_max_before int64, bugs_diff int64, too-many-statements int64, simplifiable-if-expression int64, calculated_length_diff int64, volume_diff int64, Blank_before int64, high_McCabe_max_diff int64, SLOC_before int64, too-many-nested-blocks int64, removed_lines int64, low_ccp_group int64, N1_diff int64, prev_count int64) as (
  case when Comments_diff <= 16.5 then
    case when Single comments_before <= 99.0 then
      case when McCabe_max_before <= 5.5 then
        case when hunks_num <= 2.5 then
           return 0.92 # (0.92 out of 1.0)
        else  # if hunks_num > 2.5
           return 0.48148148148148145 # (0.48148148148148145 out of 1.0)
        end       else  # if McCabe_max_before > 5.5
        case when added_lines <= 211.0 then
          case when added_functions <= 1.5 then
            case when low_ccp_group <= 0.5 then
              case when McCabe_max_diff <= -7.0 then
                 return 0.125 # (0.125 out of 1.0)
              else  # if McCabe_max_diff > -7.0
                case when refactor_mle_diff <= -0.2116723656654358 then
                  case when Comments_after <= 30.0 then
                     return 0.6111111111111112 # (0.6111111111111112 out of 1.0)
                  else  # if Comments_after > 30.0
                     return 0.12 # (0.12 out of 1.0)
                  end                 else  # if refactor_mle_diff > -0.2116723656654358
                  case when hunks_num <= 12.5 then
                    case when Blank_diff <= -2.5 then
                      case when McCabe_sum_before <= 117.0 then
                         return 0.8 # (0.8 out of 1.0)
                      else  # if McCabe_sum_before > 117.0
                         return 0.8 # (0.8 out of 1.0)
                      end                     else  # if Blank_diff > -2.5
                      case when removed_lines <= 6.5 then
                        case when changed_lines <= 2.5 then
                           return 0.6111111111111112 # (0.6111111111111112 out of 1.0)
                        else  # if changed_lines > 2.5
                           return 0.2222222222222222 # (0.2222222222222222 out of 1.0)
                        end                       else  # if removed_lines > 6.5
                        case when vocabulary_diff <= 0.5 then
                           return 0.8095238095238095 # (0.8095238095238095 out of 1.0)
                        else  # if vocabulary_diff > 0.5
                           return 0.5 # (0.5 out of 1.0)
                        end                       end                     end                   else  # if hunks_num > 12.5
                     return 0.14285714285714285 # (0.14285714285714285 out of 1.0)
                  end                 end               end             else  # if low_ccp_group > 0.5
              case when McCabe_max_diff <= -0.5 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if McCabe_max_diff > -0.5
                case when Comments_before <= 32.0 then
                   return 0.2727272727272727 # (0.2727272727272727 out of 1.0)
                else  # if Comments_before > 32.0
                   return 0.0 # (0.0 out of 1.0)
                end               end             end           else  # if added_functions > 1.5
            case when Single comments_diff <= 0.5 then
               return 0.9615384615384616 # (0.9615384615384616 out of 1.0)
            else  # if Single comments_diff > 0.5
               return 0.42857142857142855 # (0.42857142857142855 out of 1.0)
            end           end         else  # if added_lines > 211.0
          case when avg_coupling_code_size_cut_diff <= 0.03750000149011612 then
            case when low_McCabe_max_diff <= 0.5 then
               return 0.7647058823529411 # (0.7647058823529411 out of 1.0)
            else  # if low_McCabe_max_diff > 0.5
               return 0.9444444444444444 # (0.9444444444444444 out of 1.0)
            end           else  # if avg_coupling_code_size_cut_diff > 0.03750000149011612
             return 0.35294117647058826 # (0.35294117647058826 out of 1.0)
          end         end       end     else  # if Single comments_before > 99.0
      case when McCabe_sum_after <= 342.5 then
        case when N1_diff <= -71.0 then
           return 0.5555555555555556 # (0.5555555555555556 out of 1.0)
        else  # if N1_diff > -71.0
          case when removed_lines <= 2.5 then
             return 0.4666666666666667 # (0.4666666666666667 out of 1.0)
          else  # if removed_lines > 2.5
            case when Comments_diff <= 1.5 then
              case when LOC_before <= 1499.0 then
                case when LLOC_diff <= -7.5 then
                   return 0.09090909090909091 # (0.09090909090909091 out of 1.0)
                else  # if LLOC_diff > -7.5
                   return 0.0 # (0.0 out of 1.0)
                end               else  # if LOC_before > 1499.0
                 return 0.35714285714285715 # (0.35714285714285715 out of 1.0)
              end             else  # if Comments_diff > 1.5
               return 0.0 # (0.0 out of 1.0)
            end           end         end       else  # if McCabe_sum_after > 342.5
        case when Single comments_diff <= 0.5 then
          case when avg_coupling_code_size_cut_diff <= 0.12980769574642181 then
             return 0.7058823529411765 # (0.7058823529411765 out of 1.0)
          else  # if avg_coupling_code_size_cut_diff > 0.12980769574642181
             return 0.125 # (0.125 out of 1.0)
          end         else  # if Single comments_diff > 0.5
           return 0.7777777777777778 # (0.7777777777777778 out of 1.0)
        end       end     end   else  # if Comments_diff > 16.5
     return 0.8484848484848485 # (0.8484848484848485 out of 1.0)
  end )