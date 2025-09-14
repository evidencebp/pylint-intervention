create or replace function RandomForest_8 (prev_count int64, prev_count_x int64, prev_count_y int64, using-constant-test int64, Comments_diff int64, massive_change int64, McCabe_max_after int64, Comments_before int64, too-many-statements int64, cur_count_x int64, h1_diff int64, McCabe_sum_diff int64, LLOC_before int64, McCabe_sum_before int64, high_McCabe_max_before int64, avg_coupling_code_size_cut_diff int64, is_refactor int64, N2_diff int64, too-many-branches int64, SLOC_before int64, too-many-nested-blocks int64, too-many-lines int64, bugs_diff int64, time_diff int64, Single comments_after int64, simplifiable-condition int64, Multi_diff int64, high_McCabe_sum_before int64, low_ccp_group int64, refactor_mle_diff int64, low_McCabe_max_diff int64, SLOC_diff int64, changed_lines int64, hunks_num int64, McCabe_sum_after int64, cur_count_y int64, one_file_fix_rate_diff int64, low_McCabe_sum_before int64, modified_McCabe_max_diff int64, superfluous-parens int64, mostly_delete int64, added_functions int64, Comments_after int64, N1_diff int64, McCabe_max_diff int64, simplifiable-if-statement int64, LOC_before int64, low_McCabe_max_before int64, McCabe_max_before int64, try-except-raise int64, line-too-long int64, unnecessary-semicolon int64, wildcard-import int64, difficulty_diff int64, Simplify-boolean-expression int64, cur_count int64, low_McCabe_sum_diff int64, pointless-statement int64, length_diff int64, broad-exception-caught int64, h2_diff int64, high_McCabe_sum_diff int64, only_removal int64, comparison-of-constants int64, Single comments_diff int64, too-many-boolean-expressions int64, Blank_before int64, calculated_length_diff int64, Single comments_before int64, removed_lines int64, simplifiable-if-expression int64, LOC_diff int64, volume_diff int64, high_McCabe_max_diff int64, high_ccp_group int64, same_day_duration_avg_diff int64, Blank_diff int64, effort_diff int64, too-many-return-statements int64, added_lines int64, unnecessary-pass int64, vocabulary_diff int64, LLOC_diff int64) as (
  case when LLOC_before <= 109.5 then
    case when Comments_after <= 8.5 then
       return 1.0 # (1.0 out of 1.0)
    else  # if Comments_after > 8.5
       return 0.5454545454545454 # (0.5454545454545454 out of 1.0)
    end   else  # if LLOC_before > 109.5
    case when vocabulary_diff <= -47.0 then
      case when refactor_mle_diff <= -0.3146984204649925 then
         return 1.0 # (1.0 out of 1.0)
      else  # if refactor_mle_diff > -0.3146984204649925
        case when one_file_fix_rate_diff <= -0.1200757585465908 then
           return 0.2777777777777778 # (0.2777777777777778 out of 1.0)
        else  # if one_file_fix_rate_diff > -0.1200757585465908
           return 0.75 # (0.75 out of 1.0)
        end       end     else  # if vocabulary_diff > -47.0
      case when high_ccp_group <= 0.5 then
        case when low_ccp_group <= 0.5 then
          case when same_day_duration_avg_diff <= -3.4289772510528564 then
            case when LOC_diff <= -9.5 then
              case when avg_coupling_code_size_cut_diff <= -0.13711002096533775 then
                 return 0.25 # (0.25 out of 1.0)
              else  # if avg_coupling_code_size_cut_diff > -0.13711002096533775
                 return 0.7058823529411765 # (0.7058823529411765 out of 1.0)
              end             else  # if LOC_diff > -9.5
              case when LOC_before <= 478.5 then
                 return 0.4166666666666667 # (0.4166666666666667 out of 1.0)
              else  # if LOC_before > 478.5
                case when avg_coupling_code_size_cut_diff <= 0.7435515820980072 then
                  case when McCabe_max_before <= 33.5 then
                    case when added_lines <= 12.0 then
                       return 0.8823529411764706 # (0.8823529411764706 out of 1.0)
                    else  # if added_lines > 12.0
                       return 1.0 # (1.0 out of 1.0)
                    end                   else  # if McCabe_max_before > 33.5
                     return 0.47619047619047616 # (0.47619047619047616 out of 1.0)
                  end                 else  # if avg_coupling_code_size_cut_diff > 0.7435515820980072
                   return 0.42105263157894735 # (0.42105263157894735 out of 1.0)
                end               end             end           else  # if same_day_duration_avg_diff > -3.4289772510528564
            case when length_diff <= -32.5 then
               return 0.46153846153846156 # (0.46153846153846156 out of 1.0)
            else  # if length_diff > -32.5
              case when LOC_before <= 2318.0 then
                case when avg_coupling_code_size_cut_diff <= -0.0357142873108387 then
                  case when LLOC_diff <= -0.5 then
                     return 0.10526315789473684 # (0.10526315789473684 out of 1.0)
                  else  # if LLOC_diff > -0.5
                     return 0.14285714285714285 # (0.14285714285714285 out of 1.0)
                  end                 else  # if avg_coupling_code_size_cut_diff > -0.0357142873108387
                   return 0.6 # (0.6 out of 1.0)
                end               else  # if LOC_before > 2318.0
                 return 0.04 # (0.04 out of 1.0)
              end             end           end         else  # if low_ccp_group > 0.5
          case when mostly_delete <= 0.5 then
            case when LOC_diff <= -15.0 then
              case when refactor_mle_diff <= -0.1064053364098072 then
                 return 0.47619047619047616 # (0.47619047619047616 out of 1.0)
              else  # if refactor_mle_diff > -0.1064053364098072
                 return 0.0 # (0.0 out of 1.0)
              end             else  # if LOC_diff > -15.0
              case when McCabe_max_before <= 12.5 then
                 return 0.125 # (0.125 out of 1.0)
              else  # if McCabe_max_before > 12.5
                case when LLOC_before <= 617.0 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if LLOC_before > 617.0
                   return 0.058823529411764705 # (0.058823529411764705 out of 1.0)
                end               end             end           else  # if mostly_delete > 0.5
             return 0.4 # (0.4 out of 1.0)
          end         end       else  # if high_ccp_group > 0.5
        case when modified_McCabe_max_diff <= 0.5 then
          case when SLOC_before <= 1154.0 then
            case when McCabe_max_before <= 26.5 then
              case when SLOC_before <= 495.5 then
                 return 0.8636363636363636 # (0.8636363636363636 out of 1.0)
              else  # if SLOC_before > 495.5
                 return 1.0 # (1.0 out of 1.0)
              end             else  # if McCabe_max_before > 26.5
               return 0.7368421052631579 # (0.7368421052631579 out of 1.0)
            end           else  # if SLOC_before > 1154.0
             return 0.6 # (0.6 out of 1.0)
          end         else  # if modified_McCabe_max_diff > 0.5
           return 0.55 # (0.55 out of 1.0)
        end       end     end   end )