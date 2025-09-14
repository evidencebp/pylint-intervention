create or replace function RandomForest_8 (low_McCabe_max_before int64, LLOC_before int64, low_McCabe_sum_diff int64, modified_McCabe_max_diff int64, bugs_diff int64, McCabe_max_before int64, Single comments_before int64, prev_count_y int64, added_lines int64, LLOC_diff int64, N2_diff int64, added_functions int64, prev_count int64, too-many-boolean-expressions int64, SLOC_diff int64, mostly_delete int64, time_diff int64, calculated_length_diff int64, McCabe_max_after int64, Comments_diff int64, line-too-long int64, McCabe_sum_after int64, one_file_fix_rate_diff int64, h1_diff int64, high_McCabe_max_diff int64, too-many-branches int64, SLOC_before int64, cur_count_y int64, prev_count_x int64, McCabe_sum_before int64, Comments_after int64, wildcard-import int64, unnecessary-semicolon int64, same_day_duration_avg_diff int64, effort_diff int64, too-many-statements int64, broad-exception-caught int64, LOC_before int64, cur_count int64, Comments_before int64, using-constant-test int64, LOC_diff int64, high_McCabe_sum_diff int64, only_removal int64, superfluous-parens int64, try-except-raise int64, Blank_before int64, McCabe_max_diff int64, N1_diff int64, massive_change int64, refactor_mle_diff int64, pointless-statement int64, too-many-lines int64, simplifiable-if-statement int64, high_McCabe_sum_before int64, vocabulary_diff int64, removed_lines int64, difficulty_diff int64, Simplify-boolean-expression int64, avg_coupling_code_size_cut_diff int64, Single comments_after int64, low_ccp_group int64, Multi_diff int64, is_refactor int64, hunks_num int64, Single comments_diff int64, length_diff int64, unnecessary-pass int64, Blank_diff int64, h2_diff int64, changed_lines int64, cur_count_x int64, low_McCabe_max_diff int64, high_McCabe_max_before int64, high_ccp_group int64, too-many-nested-blocks int64, McCabe_sum_diff int64, volume_diff int64, comparison-of-constants int64, too-many-return-statements int64, simplifiable-condition int64, simplifiable-if-expression int64, low_McCabe_sum_before int64) as (
  case when McCabe_sum_after <= 60.5 then
    case when Comments_before <= 10.5 then
      case when added_lines <= 30.0 then
         return 0.75 # (0.75 out of 1.0)
      else  # if added_lines > 30.0
         return 0.15384615384615385 # (0.15384615384615385 out of 1.0)
      end     else  # if Comments_before > 10.5
      case when too-many-branches <= 0.5 then
        case when Comments_diff <= -2.5 then
          case when SLOC_before <= 306.5 then
             return 1.0 # (1.0 out of 1.0)
          else  # if SLOC_before > 306.5
             return 0.7058823529411765 # (0.7058823529411765 out of 1.0)
          end         else  # if Comments_diff > -2.5
          case when LOC_before <= 259.0 then
             return 0.25 # (0.25 out of 1.0)
          else  # if LOC_before > 259.0
            case when changed_lines <= 10.5 then
               return 0.7142857142857143 # (0.7142857142857143 out of 1.0)
            else  # if changed_lines > 10.5
               return 0.4782608695652174 # (0.4782608695652174 out of 1.0)
            end           end         end       else  # if too-many-branches > 0.5
         return 1.0 # (1.0 out of 1.0)
      end     end   else  # if McCabe_sum_after > 60.5
    case when low_McCabe_sum_before <= 0.5 then
      case when LOC_before <= 1032.5 then
        case when LOC_diff <= -75.0 then
           return 0.029411764705882353 # (0.029411764705882353 out of 1.0)
        else  # if LOC_diff > -75.0
          case when Comments_after <= 68.5 then
            case when Comments_diff <= 0.5 then
              case when high_ccp_group <= 0.5 then
                case when avg_coupling_code_size_cut_diff <= -0.0357142873108387 then
                   return 0.21428571428571427 # (0.21428571428571427 out of 1.0)
                else  # if avg_coupling_code_size_cut_diff > -0.0357142873108387
                  case when LOC_before <= 818.5 then
                     return 0.7037037037037037 # (0.7037037037037037 out of 1.0)
                  else  # if LOC_before > 818.5
                     return 0.5 # (0.5 out of 1.0)
                  end                 end               else  # if high_ccp_group > 0.5
                 return 0.8695652173913043 # (0.8695652173913043 out of 1.0)
              end             else  # if Comments_diff > 0.5
              case when LLOC_diff <= 3.0 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if LLOC_diff > 3.0
                 return 0.30434782608695654 # (0.30434782608695654 out of 1.0)
              end             end           else  # if Comments_after > 68.5
            case when changed_lines <= 43.0 then
               return 0.3157894736842105 # (0.3157894736842105 out of 1.0)
            else  # if changed_lines > 43.0
               return 0.0 # (0.0 out of 1.0)
            end           end         end       else  # if LOC_before > 1032.5
        case when avg_coupling_code_size_cut_diff <= 0.7486111223697662 then
          case when same_day_duration_avg_diff <= -1.2718265056610107 then
            case when added_functions <= 1.5 then
              case when low_ccp_group <= 0.5 then
                 return 0.48484848484848486 # (0.48484848484848486 out of 1.0)
              else  # if low_ccp_group > 0.5
                 return 0.0 # (0.0 out of 1.0)
              end             else  # if added_functions > 1.5
               return 0.6363636363636364 # (0.6363636363636364 out of 1.0)
            end           else  # if same_day_duration_avg_diff > -1.2718265056610107
            case when removed_lines <= 17.5 then
              case when changed_lines <= 29.5 then
                 return 0.8 # (0.8 out of 1.0)
              else  # if changed_lines > 29.5
                 return 0.375 # (0.375 out of 1.0)
              end             else  # if removed_lines > 17.5
              case when same_day_duration_avg_diff <= 23.20449733734131 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if same_day_duration_avg_diff > 23.20449733734131
                 return 0.8421052631578947 # (0.8421052631578947 out of 1.0)
              end             end           end         else  # if avg_coupling_code_size_cut_diff > 0.7486111223697662
          case when added_lines <= 100.0 then
             return 0.5 # (0.5 out of 1.0)
          else  # if added_lines > 100.0
             return 0.09090909090909091 # (0.09090909090909091 out of 1.0)
          end         end       end     else  # if low_McCabe_sum_before > 0.5
       return 0.16666666666666666 # (0.16666666666666666 out of 1.0)
    end   end )