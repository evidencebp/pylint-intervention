create or replace function RandomForest_8 (h1_diff int64, simplifiable-if-statement int64, McCabe_max_after int64, McCabe_sum_before int64, Single comments_before int64, low_McCabe_max_diff int64, high_ccp_group int64, pointless-statement int64, too-many-branches int64, high_McCabe_max_before int64, superfluous-parens int64, Multi_diff int64, wildcard-import int64, high_McCabe_sum_before int64, LLOC_before int64, cur_count int64, unnecessary-semicolon int64, Comments_after int64, mostly_delete int64, simplifiable-condition int64, avg_coupling_code_size_cut_diff int64, added_functions int64, McCabe_max_diff int64, McCabe_sum_diff int64, LLOC_diff int64, LOC_before int64, Comments_diff int64, prev_count_x int64, effort_diff int64, try-except-raise int64, difficulty_diff int64, line-too-long int64, Simplify-boolean-expression int64, SLOC_diff int64, McCabe_sum_after int64, refactor_mle_diff int64, one_file_fix_rate_diff int64, is_refactor int64, too-many-lines int64, too-many-boolean-expressions int64, Single comments_diff int64, low_McCabe_sum_diff int64, cur_count_y int64, comparison-of-constants int64, Comments_before int64, too-many-return-statements int64, vocabulary_diff int64, massive_change int64, hunks_num int64, modified_McCabe_max_diff int64, high_McCabe_sum_diff int64, N2_diff int64, broad-exception-caught int64, length_diff int64, unnecessary-pass int64, time_diff int64, changed_lines int64, Single comments_after int64, h2_diff int64, low_McCabe_sum_before int64, cur_count_x int64, McCabe_max_before int64, using-constant-test int64, added_lines int64, same_day_duration_avg_diff int64, prev_count_y int64, Blank_diff int64, LOC_diff int64, only_removal int64, low_McCabe_max_before int64, bugs_diff int64, too-many-statements int64, simplifiable-if-expression int64, calculated_length_diff int64, volume_diff int64, Blank_before int64, high_McCabe_max_diff int64, SLOC_before int64, too-many-nested-blocks int64, removed_lines int64, low_ccp_group int64, N1_diff int64, prev_count int64) as (
  case when LLOC_before <= 76.5 then
     return 0.8695652173913043 # (0.8695652173913043 out of 1.0)
  else  # if LLOC_before > 76.5
    case when Multi_diff <= -25.5 then
      case when McCabe_sum_diff <= -16.5 then
         return 0.875 # (0.875 out of 1.0)
      else  # if McCabe_sum_diff > -16.5
         return 0.36363636363636365 # (0.36363636363636365 out of 1.0)
      end     else  # if Multi_diff > -25.5
      case when McCabe_sum_after <= 30.5 then
        case when LOC_diff <= -6.5 then
           return 0.07692307692307693 # (0.07692307692307693 out of 1.0)
        else  # if LOC_diff > -6.5
          case when changed_lines <= 15.5 then
             return 0.23809523809523808 # (0.23809523809523808 out of 1.0)
          else  # if changed_lines > 15.5
             return 0.5 # (0.5 out of 1.0)
          end         end       else  # if McCabe_sum_after > 30.5
        case when McCabe_sum_before <= 84.0 then
          case when Blank_diff <= -0.5 then
             return 0.36666666666666664 # (0.36666666666666664 out of 1.0)
          else  # if Blank_diff > -0.5
            case when avg_coupling_code_size_cut_diff <= -0.1963585540652275 then
               return 0.5 # (0.5 out of 1.0)
            else  # if avg_coupling_code_size_cut_diff > -0.1963585540652275
              case when McCabe_sum_after <= 82.5 then
                 return 0.7575757575757576 # (0.7575757575757576 out of 1.0)
              else  # if McCabe_sum_after > 82.5
                 return 1.0 # (1.0 out of 1.0)
              end             end           end         else  # if McCabe_sum_before > 84.0
          case when low_ccp_group <= 0.5 then
            case when same_day_duration_avg_diff <= 20.77976131439209 then
              case when LLOC_before <= 363.5 then
                 return 0.9473684210526315 # (0.9473684210526315 out of 1.0)
              else  # if LLOC_before > 363.5
                case when too-many-statements <= 0.5 then
                  case when Comments_before <= 18.5 then
                     return 0.3 # (0.3 out of 1.0)
                  else  # if Comments_before > 18.5
                    case when Comments_after <= 45.5 then
                       return 1.0 # (1.0 out of 1.0)
                    else  # if Comments_after > 45.5
                      case when Single comments_before <= 123.5 then
                        case when Blank_before <= 150.0 then
                           return 0.05263157894736842 # (0.05263157894736842 out of 1.0)
                        else  # if Blank_before > 150.0
                           return 0.5769230769230769 # (0.5769230769230769 out of 1.0)
                        end                       else  # if Single comments_before > 123.5
                         return 0.7692307692307693 # (0.7692307692307693 out of 1.0)
                      end                     end                   end                 else  # if too-many-statements > 0.5
                  case when refactor_mle_diff <= -0.0069703159388154745 then
                     return 0.55 # (0.55 out of 1.0)
                  else  # if refactor_mle_diff > -0.0069703159388154745
                     return 0.05555555555555555 # (0.05555555555555555 out of 1.0)
                  end                 end               end             else  # if same_day_duration_avg_diff > 20.77976131439209
              case when Blank_before <= 106.0 then
                case when Single comments_before <= 33.0 then
                   return 0.21428571428571427 # (0.21428571428571427 out of 1.0)
                else  # if Single comments_before > 33.0
                   return 0.1 # (0.1 out of 1.0)
                end               else  # if Blank_before > 106.0
                case when McCabe_max_before <= 29.5 then
                  case when McCabe_sum_diff <= -0.5 then
                     return 0.5 # (0.5 out of 1.0)
                  else  # if McCabe_sum_diff > -0.5
                     return 0.11764705882352941 # (0.11764705882352941 out of 1.0)
                  end                 else  # if McCabe_max_before > 29.5
                   return 0.6296296296296297 # (0.6296296296296297 out of 1.0)
                end               end             end           else  # if low_ccp_group > 0.5
            case when added_functions <= 0.5 then
              case when Blank_before <= 94.5 then
                 return 0.06666666666666667 # (0.06666666666666667 out of 1.0)
              else  # if Blank_before > 94.5
                 return 0.0 # (0.0 out of 1.0)
              end             else  # if added_functions > 0.5
              case when LLOC_before <= 536.5 then
                 return 0.05555555555555555 # (0.05555555555555555 out of 1.0)
              else  # if LLOC_before > 536.5
                 return 0.42857142857142855 # (0.42857142857142855 out of 1.0)
              end             end           end         end       end     end   end )