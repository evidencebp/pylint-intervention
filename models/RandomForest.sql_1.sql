create or replace function RandomForest_1 (SLOC_before int64, too-many-nested-blocks int64, simplifiable-condition int64, Blank_diff int64, comparison-of-constants int64, McCabe_sum_diff int64, volume_diff int64, Multi_diff int64, only_removal int64, too-many-boolean-expressions int64, using-constant-test int64, same_day_duration_avg_diff int64, too-many-return-statements int64, avg_coupling_code_size_cut_diff int64, h1_diff int64, LLOC_before int64, SLOC_diff int64, changed_lines int64, N2_diff int64, is_refactor int64, pointless-statement int64, Single comments_after int64, length_diff int64, high_McCabe_max_before int64, unnecessary-semicolon int64, LOC_diff int64, McCabe_max_diff int64, LOC_before int64, Comments_diff int64, broad-exception-caught int64, prev_count int64, time_diff int64, cur_count_y int64, line-too-long int64, Blank_before int64, simplifiable-if-statement int64, too-many-statements int64, prev_count_y int64, refactor_mle_diff int64, modified_McCabe_max_diff int64, superfluous-parens int64, hunks_num int64, bugs_diff int64, Single comments_before int64, removed_lines int64, low_McCabe_sum_before int64, effort_diff int64, LLOC_diff int64, low_ccp_group int64, difficulty_diff int64, h2_diff int64, McCabe_max_before int64, Comments_before int64, McCabe_sum_after int64, prev_count_x int64, N1_diff int64, high_ccp_group int64, cur_count int64, try-except-raise int64, too-many-branches int64, wildcard-import int64, low_McCabe_max_diff int64, cur_count_x int64, Comments_after int64, Simplify-boolean-expression int64, vocabulary_diff int64, mostly_delete int64, calculated_length_diff int64, Single comments_diff int64, unnecessary-pass int64, high_McCabe_sum_before int64, high_McCabe_max_diff int64, simplifiable-if-expression int64, one_file_fix_rate_diff int64, massive_change int64, added_functions int64, too-many-lines int64, McCabe_max_after int64, high_McCabe_sum_diff int64, added_lines int64, low_McCabe_sum_diff int64, low_McCabe_max_before int64, McCabe_sum_before int64) as (
  case when high_ccp_group <= 0.5 then
    case when Comments_diff <= -21.0 then
      case when McCabe_max_after <= 15.0 then
         return 0.95 # (0.95 out of 1.0)
      else  # if McCabe_max_after > 15.0
         return 0.6470588235294118 # (0.6470588235294118 out of 1.0)
      end     else  # if Comments_diff > -21.0
      case when SLOC_diff <= 31.5 then
        case when LLOC_before <= 1095.5 then
          case when low_ccp_group <= 0.5 then
            case when McCabe_max_diff <= -11.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if McCabe_max_diff > -11.5
              case when is_refactor <= 0.5 then
                case when removed_lines <= 2.5 then
                  case when SLOC_before <= 653.0 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if SLOC_before > 653.0
                     return 0.56 # (0.56 out of 1.0)
                  end                 else  # if removed_lines > 2.5
                  case when Comments_after <= 47.5 then
                    case when LOC_diff <= -14.5 then
                       return 0.38461538461538464 # (0.38461538461538464 out of 1.0)
                    else  # if LOC_diff > -14.5
                      case when SLOC_before <= 198.5 then
                         return 1.0 # (1.0 out of 1.0)
                      else  # if SLOC_before > 198.5
                        case when LOC_before <= 517.5 then
                           return 0.4375 # (0.4375 out of 1.0)
                        else  # if LOC_before > 517.5
                           return 0.7222222222222222 # (0.7222222222222222 out of 1.0)
                        end                       end                     end                   else  # if Comments_after > 47.5
                     return 0.2647058823529412 # (0.2647058823529412 out of 1.0)
                  end                 end               else  # if is_refactor > 0.5
                 return 0.5 # (0.5 out of 1.0)
              end             end           else  # if low_ccp_group > 0.5
            case when refactor_mle_diff <= 0.08893650770187378 then
              case when Comments_after <= 38.0 then
                case when avg_coupling_code_size_cut_diff <= 0.0018115942366421223 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if avg_coupling_code_size_cut_diff > 0.0018115942366421223
                   return 0.25 # (0.25 out of 1.0)
                end               else  # if Comments_after > 38.0
                 return 0.0 # (0.0 out of 1.0)
              end             else  # if refactor_mle_diff > 0.08893650770187378
               return 0.15384615384615385 # (0.15384615384615385 out of 1.0)
            end           end         else  # if LLOC_before > 1095.5
          case when McCabe_sum_diff <= -2.5 then
             return 0.65 # (0.65 out of 1.0)
          else  # if McCabe_sum_diff > -2.5
             return 0.5172413793103449 # (0.5172413793103449 out of 1.0)
          end         end       else  # if SLOC_diff > 31.5
        case when McCabe_max_before <= 32.5 then
          case when h2_diff <= 3.5 then
             return 0.9259259259259259 # (0.9259259259259259 out of 1.0)
          else  # if h2_diff > 3.5
             return 0.5625 # (0.5625 out of 1.0)
          end         else  # if McCabe_max_before > 32.5
           return 0.3125 # (0.3125 out of 1.0)
        end       end     end   else  # if high_ccp_group > 0.5
    case when LOC_before <= 743.5 then
      case when avg_coupling_code_size_cut_diff <= -0.7565173804759979 then
         return 1.0 # (1.0 out of 1.0)
      else  # if avg_coupling_code_size_cut_diff > -0.7565173804759979
        case when McCabe_sum_before <= 47.5 then
           return 0.7647058823529411 # (0.7647058823529411 out of 1.0)
        else  # if McCabe_sum_before > 47.5
           return 0.8333333333333334 # (0.8333333333333334 out of 1.0)
        end       end     else  # if LOC_before > 743.5
      case when LLOC_diff <= 1.0 then
        case when N2_diff <= -2.5 then
           return 0.38095238095238093 # (0.38095238095238093 out of 1.0)
        else  # if N2_diff > -2.5
          case when Blank_before <= 179.5 then
             return 0.5 # (0.5 out of 1.0)
          else  # if Blank_before > 179.5
             return 1.0 # (1.0 out of 1.0)
          end         end       else  # if LLOC_diff > 1.0
         return 0.25 # (0.25 out of 1.0)
      end     end   end )