create or replace function RandomForest_7 (prev_count int64, simplifiable-if-expression int64, N1_diff int64, cur_count int64, wildcard-import int64, too-many-return-statements int64, low_McCabe_max_diff int64, length_diff int64, volume_diff int64, high_McCabe_sum_diff int64, high_McCabe_max_before int64, simplifiable-condition int64, Blank_before int64, high_ccp_group int64, McCabe_max_before int64, bugs_diff int64, too-many-nested-blocks int64, refactor_mle_diff int64, difficulty_diff int64, LLOC_diff int64, LOC_diff int64, simplifiable-if-statement int64, one_file_fix_rate_diff int64, SLOC_before int64, LOC_before int64, mostly_delete int64, changed_lines int64, Single comments_before int64, removed_lines int64, added_functions int64, h1_diff int64, effort_diff int64, hunks_num int64, Multi_diff int64, same_day_duration_avg_diff int64, N2_diff int64, cur_count_y int64, Comments_diff int64, modified_McCabe_max_diff int64, h2_diff int64, time_diff int64, LLOC_before int64, calculated_length_diff int64, Single comments_after int64, massive_change int64, McCabe_sum_before int64, too-many-boolean-expressions int64, Simplify-boolean-expression int64, line-too-long int64, superfluous-parens int64, low_ccp_group int64, McCabe_max_diff int64, comparison-of-constants int64, high_McCabe_sum_before int64, low_McCabe_sum_diff int64, avg_coupling_code_size_cut_diff int64, is_refactor int64, Single comments_diff int64, unnecessary-semicolon int64, added_lines int64, prev_count_y int64, try-except-raise int64, low_McCabe_sum_before int64, vocabulary_diff int64, too-many-branches int64, McCabe_sum_after int64, broad-exception-caught int64, prev_count_x int64, only_removal int64, McCabe_max_after int64, pointless-statement int64, low_McCabe_max_before int64, too-many-lines int64, McCabe_sum_diff int64, high_McCabe_max_diff int64, using-constant-test int64, SLOC_diff int64, Blank_diff int64, Comments_after int64, cur_count_x int64, unnecessary-pass int64, too-many-statements int64, Comments_before int64) as (
  case when Comments_after <= 1.5 then
     return 0.95 # (0.95 out of 1.0)
  else  # if Comments_after > 1.5
    case when McCabe_sum_diff <= -33.5 then
      case when LOC_diff <= -263.0 then
        case when Single comments_diff <= -45.5 then
           return 1.0 # (1.0 out of 1.0)
        else  # if Single comments_diff > -45.5
           return 0.7857142857142857 # (0.7857142857142857 out of 1.0)
        end       else  # if LOC_diff > -263.0
         return 0.4230769230769231 # (0.4230769230769231 out of 1.0)
      end     else  # if McCabe_sum_diff > -33.5
      case when low_McCabe_max_before <= 0.5 then
        case when LLOC_diff <= -60.5 then
          case when LLOC_before <= 624.0 then
             return 0.18181818181818182 # (0.18181818181818182 out of 1.0)
          else  # if LLOC_before > 624.0
             return 0.0 # (0.0 out of 1.0)
          end         else  # if LLOC_diff > -60.5
          case when LLOC_before <= 1197.0 then
            case when Comments_after <= 100.5 then
              case when Comments_diff <= 1.5 then
                case when refactor_mle_diff <= 0.30409444868564606 then
                  case when low_ccp_group <= 0.5 then
                    case when Blank_diff <= -1.5 then
                      case when LOC_before <= 553.5 then
                         return 0.1111111111111111 # (0.1111111111111111 out of 1.0)
                      else  # if LOC_before > 553.5
                         return 0.6521739130434783 # (0.6521739130434783 out of 1.0)
                      end                     else  # if Blank_diff > -1.5
                      case when McCabe_sum_after <= 48.5 then
                         return 0.9375 # (0.9375 out of 1.0)
                      else  # if McCabe_sum_after > 48.5
                        case when SLOC_diff <= 14.5 then
                          case when McCabe_max_after <= 19.0 then
                             return 0.2222222222222222 # (0.2222222222222222 out of 1.0)
                          else  # if McCabe_max_after > 19.0
                            case when LOC_before <= 889.0 then
                               return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
                            else  # if LOC_before > 889.0
                               return 0.5 # (0.5 out of 1.0)
                            end                           end                         else  # if SLOC_diff > 14.5
                           return 1.0 # (1.0 out of 1.0)
                        end                       end                     end                   else  # if low_ccp_group > 0.5
                    case when changed_lines <= 84.0 then
                       return 0.04 # (0.04 out of 1.0)
                    else  # if changed_lines > 84.0
                       return 0.3125 # (0.3125 out of 1.0)
                    end                   end                 else  # if refactor_mle_diff > 0.30409444868564606
                   return 0.8181818181818182 # (0.8181818181818182 out of 1.0)
                end               else  # if Comments_diff > 1.5
                 return 0.10714285714285714 # (0.10714285714285714 out of 1.0)
              end             else  # if Comments_after > 100.5
              case when LLOC_diff <= -0.5 then
                case when McCabe_max_before <= 23.5 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if McCabe_max_before > 23.5
                   return 0.07692307692307693 # (0.07692307692307693 out of 1.0)
                end               else  # if LLOC_diff > -0.5
                case when LOC_diff <= 4.0 then
                   return 0.4583333333333333 # (0.4583333333333333 out of 1.0)
                else  # if LOC_diff > 4.0
                   return 0.15625 # (0.15625 out of 1.0)
                end               end             end           else  # if LLOC_before > 1197.0
            case when McCabe_sum_before <= 583.0 then
               return 0.9583333333333334 # (0.9583333333333334 out of 1.0)
            else  # if McCabe_sum_before > 583.0
               return 0.29411764705882354 # (0.29411764705882354 out of 1.0)
            end           end         end       else  # if low_McCabe_max_before > 0.5
        case when Comments_diff <= 18.0 then
          case when LOC_diff <= -1.5 then
            case when one_file_fix_rate_diff <= -0.018382353708148003 then
               return 0.5625 # (0.5625 out of 1.0)
            else  # if one_file_fix_rate_diff > -0.018382353708148003
              case when LOC_diff <= -23.5 then
                 return 0.5263157894736842 # (0.5263157894736842 out of 1.0)
              else  # if LOC_diff > -23.5
                 return 0.19047619047619047 # (0.19047619047619047 out of 1.0)
              end             end           else  # if LOC_diff > -1.5
            case when hunks_num <= 1.5 then
               return 0.43478260869565216 # (0.43478260869565216 out of 1.0)
            else  # if hunks_num > 1.5
              case when changed_lines <= 93.0 then
                 return 0.9130434782608695 # (0.9130434782608695 out of 1.0)
              else  # if changed_lines > 93.0
                 return 0.5833333333333334 # (0.5833333333333334 out of 1.0)
              end             end           end         else  # if Comments_diff > 18.0
           return 0.9545454545454546 # (0.9545454545454546 out of 1.0)
        end       end     end   end )