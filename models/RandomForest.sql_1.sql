create or replace function RandomForest_1 (prev_count int64, simplifiable-if-expression int64, N1_diff int64, cur_count int64, wildcard-import int64, too-many-return-statements int64, low_McCabe_max_diff int64, length_diff int64, volume_diff int64, high_McCabe_sum_diff int64, high_McCabe_max_before int64, simplifiable-condition int64, Blank_before int64, high_ccp_group int64, McCabe_max_before int64, bugs_diff int64, too-many-nested-blocks int64, refactor_mle_diff int64, difficulty_diff int64, LLOC_diff int64, LOC_diff int64, simplifiable-if-statement int64, one_file_fix_rate_diff int64, SLOC_before int64, LOC_before int64, mostly_delete int64, changed_lines int64, Single comments_before int64, removed_lines int64, added_functions int64, h1_diff int64, effort_diff int64, hunks_num int64, Multi_diff int64, same_day_duration_avg_diff int64, N2_diff int64, cur_count_y int64, Comments_diff int64, modified_McCabe_max_diff int64, h2_diff int64, time_diff int64, LLOC_before int64, calculated_length_diff int64, Single comments_after int64, massive_change int64, McCabe_sum_before int64, too-many-boolean-expressions int64, Simplify-boolean-expression int64, line-too-long int64, superfluous-parens int64, low_ccp_group int64, McCabe_max_diff int64, comparison-of-constants int64, high_McCabe_sum_before int64, low_McCabe_sum_diff int64, avg_coupling_code_size_cut_diff int64, is_refactor int64, Single comments_diff int64, unnecessary-semicolon int64, added_lines int64, prev_count_y int64, try-except-raise int64, low_McCabe_sum_before int64, vocabulary_diff int64, too-many-branches int64, McCabe_sum_after int64, broad-exception-caught int64, prev_count_x int64, only_removal int64, McCabe_max_after int64, pointless-statement int64, low_McCabe_max_before int64, too-many-lines int64, McCabe_sum_diff int64, high_McCabe_max_diff int64, using-constant-test int64, SLOC_diff int64, Blank_diff int64, Comments_after int64, cur_count_x int64, unnecessary-pass int64, too-many-statements int64, Comments_before int64) as (
  case when McCabe_sum_after <= 90.0 then
    case when Comments_diff <= 10.5 then
      case when refactor_mle_diff <= 0.3591666668653488 then
        case when removed_lines <= 73.0 then
          case when Comments_after <= 1.5 then
             return 1.0 # (1.0 out of 1.0)
          else  # if Comments_after > 1.5
            case when McCabe_max_diff <= -4.5 then
               return 0.7407407407407407 # (0.7407407407407407 out of 1.0)
            else  # if McCabe_max_diff > -4.5
              case when low_McCabe_sum_before <= 0.5 then
                case when McCabe_sum_before <= 79.5 then
                   return 0.25 # (0.25 out of 1.0)
                else  # if McCabe_sum_before > 79.5
                   return 0.0 # (0.0 out of 1.0)
                end               else  # if low_McCabe_sum_before > 0.5
                case when LOC_before <= 312.0 then
                  case when LLOC_diff <= -0.5 then
                     return 0.10526315789473684 # (0.10526315789473684 out of 1.0)
                  else  # if LLOC_diff > -0.5
                     return 0.3548387096774194 # (0.3548387096774194 out of 1.0)
                  end                 else  # if LOC_before > 312.0
                  case when same_day_duration_avg_diff <= 1.4083333015441895 then
                     return 0.8 # (0.8 out of 1.0)
                  else  # if same_day_duration_avg_diff > 1.4083333015441895
                     return 0.4375 # (0.4375 out of 1.0)
                  end                 end               end             end           end         else  # if removed_lines > 73.0
          case when McCabe_max_after <= 11.5 then
             return 0.8846153846153846 # (0.8846153846153846 out of 1.0)
          else  # if McCabe_max_after > 11.5
             return 0.5714285714285714 # (0.5714285714285714 out of 1.0)
          end         end       else  # if refactor_mle_diff > 0.3591666668653488
         return 0.9166666666666666 # (0.9166666666666666 out of 1.0)
      end     else  # if Comments_diff > 10.5
       return 1.0 # (1.0 out of 1.0)
    end   else  # if McCabe_sum_after > 90.0
    case when added_functions <= 8.5 then
      case when changed_lines <= 139.0 then
        case when high_ccp_group <= 0.5 then
          case when low_ccp_group <= 0.5 then
            case when SLOC_diff <= -30.5 then
              case when LOC_before <= 1195.5 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if LOC_before > 1195.5
                 return 0.07692307692307693 # (0.07692307692307693 out of 1.0)
              end             else  # if SLOC_diff > -30.5
              case when Comments_before <= 47.5 then
                 return 0.625 # (0.625 out of 1.0)
              else  # if Comments_before > 47.5
                case when avg_coupling_code_size_cut_diff <= -0.16568627953529358 then
                   return 0.5882352941176471 # (0.5882352941176471 out of 1.0)
                else  # if avg_coupling_code_size_cut_diff > -0.16568627953529358
                   return 0.23529411764705882 # (0.23529411764705882 out of 1.0)
                end               end             end           else  # if low_ccp_group > 0.5
            case when LOC_before <= 1909.0 then
               return 0.0 # (0.0 out of 1.0)
            else  # if LOC_before > 1909.0
               return 0.1111111111111111 # (0.1111111111111111 out of 1.0)
            end           end         else  # if high_ccp_group > 0.5
          case when refactor_mle_diff <= -0.0790850818157196 then
             return 0.4444444444444444 # (0.4444444444444444 out of 1.0)
          else  # if refactor_mle_diff > -0.0790850818157196
            case when N2_diff <= -1.0 then
               return 0.8 # (0.8 out of 1.0)
            else  # if N2_diff > -1.0
               return 1.0 # (1.0 out of 1.0)
            end           end         end       else  # if changed_lines > 139.0
        case when added_functions <= 3.5 then
          case when Blank_before <= 137.5 then
             return 0.09090909090909091 # (0.09090909090909091 out of 1.0)
          else  # if Blank_before > 137.5
            case when Single comments_before <= 94.5 then
              case when Single comments_before <= 57.5 then
                 return 0.7368421052631579 # (0.7368421052631579 out of 1.0)
              else  # if Single comments_before > 57.5
                 return 1.0 # (1.0 out of 1.0)
              end             else  # if Single comments_before > 94.5
               return 0.45161290322580644 # (0.45161290322580644 out of 1.0)
            end           end         else  # if added_functions > 3.5
           return 1.0 # (1.0 out of 1.0)
        end       end     else  # if added_functions > 8.5
       return 0.05263157894736842 # (0.05263157894736842 out of 1.0)
    end   end )