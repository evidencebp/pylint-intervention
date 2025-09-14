create or replace function RandomForest_5 (SLOC_before int64, too-many-nested-blocks int64, simplifiable-condition int64, Blank_diff int64, comparison-of-constants int64, McCabe_sum_diff int64, volume_diff int64, Multi_diff int64, only_removal int64, too-many-boolean-expressions int64, using-constant-test int64, same_day_duration_avg_diff int64, too-many-return-statements int64, avg_coupling_code_size_cut_diff int64, h1_diff int64, LLOC_before int64, SLOC_diff int64, changed_lines int64, N2_diff int64, is_refactor int64, pointless-statement int64, Single comments_after int64, length_diff int64, high_McCabe_max_before int64, unnecessary-semicolon int64, LOC_diff int64, McCabe_max_diff int64, LOC_before int64, Comments_diff int64, broad-exception-caught int64, prev_count int64, time_diff int64, cur_count_y int64, line-too-long int64, Blank_before int64, simplifiable-if-statement int64, too-many-statements int64, prev_count_y int64, refactor_mle_diff int64, modified_McCabe_max_diff int64, superfluous-parens int64, hunks_num int64, bugs_diff int64, Single comments_before int64, removed_lines int64, low_McCabe_sum_before int64, effort_diff int64, LLOC_diff int64, low_ccp_group int64, difficulty_diff int64, h2_diff int64, McCabe_max_before int64, Comments_before int64, McCabe_sum_after int64, prev_count_x int64, N1_diff int64, high_ccp_group int64, cur_count int64, try-except-raise int64, too-many-branches int64, wildcard-import int64, low_McCabe_max_diff int64, cur_count_x int64, Comments_after int64, Simplify-boolean-expression int64, vocabulary_diff int64, mostly_delete int64, calculated_length_diff int64, Single comments_diff int64, unnecessary-pass int64, high_McCabe_sum_before int64, high_McCabe_max_diff int64, simplifiable-if-expression int64, one_file_fix_rate_diff int64, massive_change int64, added_functions int64, too-many-lines int64, McCabe_max_after int64, high_McCabe_sum_diff int64, added_lines int64, low_McCabe_sum_diff int64, low_McCabe_max_before int64, McCabe_sum_before int64) as (
  case when LOC_before <= 126.0 then
     return 1.0 # (1.0 out of 1.0)
  else  # if LOC_before > 126.0
    case when Comments_after <= 6.5 then
      case when LLOC_before <= 179.0 then
         return 0.9130434782608695 # (0.9130434782608695 out of 1.0)
      else  # if LLOC_before > 179.0
         return 0.75 # (0.75 out of 1.0)
      end     else  # if Comments_after > 6.5
      case when SLOC_diff <= 38.0 then
        case when vocabulary_diff <= -53.5 then
          case when avg_coupling_code_size_cut_diff <= 0.5214285850524902 then
             return 0.9166666666666666 # (0.9166666666666666 out of 1.0)
          else  # if avg_coupling_code_size_cut_diff > 0.5214285850524902
             return 0.2857142857142857 # (0.2857142857142857 out of 1.0)
          end         else  # if vocabulary_diff > -53.5
          case when low_ccp_group <= 0.5 then
            case when prev_count_x <= 1.5 then
              case when SLOC_diff <= -17.5 then
                case when vocabulary_diff <= -2.0 then
                  case when avg_coupling_code_size_cut_diff <= 0.16298701893538237 then
                    case when SLOC_diff <= -76.0 then
                       return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
                    else  # if SLOC_diff > -76.0
                       return 0.05405405405405406 # (0.05405405405405406 out of 1.0)
                    end                   else  # if avg_coupling_code_size_cut_diff > 0.16298701893538237
                     return 0.4375 # (0.4375 out of 1.0)
                  end                 else  # if vocabulary_diff > -2.0
                   return 0.6956521739130435 # (0.6956521739130435 out of 1.0)
                end               else  # if SLOC_diff > -17.5
                case when McCabe_max_diff <= 0.5 then
                  case when changed_lines <= 136.0 then
                    case when removed_lines <= 17.0 then
                      case when high_ccp_group <= 0.5 then
                        case when Single comments_before <= 52.5 then
                          case when same_day_duration_avg_diff <= -6.943749904632568 then
                             return 0.6428571428571429 # (0.6428571428571429 out of 1.0)
                          else  # if same_day_duration_avg_diff > -6.943749904632568
                             return 0.25 # (0.25 out of 1.0)
                          end                         else  # if Single comments_before > 52.5
                           return 0.8666666666666667 # (0.8666666666666667 out of 1.0)
                        end                       else  # if high_ccp_group > 0.5
                        case when Single comments_before <= 65.5 then
                           return 0.8846153846153846 # (0.8846153846153846 out of 1.0)
                        else  # if Single comments_before > 65.5
                           return 0.6842105263157895 # (0.6842105263157895 out of 1.0)
                        end                       end                     else  # if removed_lines > 17.0
                      case when one_file_fix_rate_diff <= 0.0912698432803154 then
                         return 0.52 # (0.52 out of 1.0)
                      else  # if one_file_fix_rate_diff > 0.0912698432803154
                         return 0.07142857142857142 # (0.07142857142857142 out of 1.0)
                      end                     end                   else  # if changed_lines > 136.0
                    case when LLOC_diff <= 4.0 then
                       return 0.8333333333333334 # (0.8333333333333334 out of 1.0)
                    else  # if LLOC_diff > 4.0
                       return 0.9411764705882353 # (0.9411764705882353 out of 1.0)
                    end                   end                 else  # if McCabe_max_diff > 0.5
                   return 0.25 # (0.25 out of 1.0)
                end               end             else  # if prev_count_x > 1.5
              case when prev_count_x <= 2.5 then
                 return 0.25925925925925924 # (0.25925925925925924 out of 1.0)
              else  # if prev_count_x > 2.5
                 return 0.0 # (0.0 out of 1.0)
              end             end           else  # if low_ccp_group > 0.5
            case when removed_lines <= 43.0 then
              case when LLOC_diff <= 1.5 then
                case when avg_coupling_code_size_cut_diff <= 0.506722703576088 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if avg_coupling_code_size_cut_diff > 0.506722703576088
                   return 0.07142857142857142 # (0.07142857142857142 out of 1.0)
                end               else  # if LLOC_diff > 1.5
                 return 0.14285714285714285 # (0.14285714285714285 out of 1.0)
              end             else  # if removed_lines > 43.0
              case when vocabulary_diff <= -0.5 then
                 return 0.4 # (0.4 out of 1.0)
              else  # if vocabulary_diff > -0.5
                 return 0.0 # (0.0 out of 1.0)
              end             end           end         end       else  # if SLOC_diff > 38.0
        case when Blank_before <= 84.0 then
           return 1.0 # (1.0 out of 1.0)
        else  # if Blank_before > 84.0
          case when same_day_duration_avg_diff <= -12.641608238220215 then
             return 0.65 # (0.65 out of 1.0)
          else  # if same_day_duration_avg_diff > -12.641608238220215
             return 0.3888888888888889 # (0.3888888888888889 out of 1.0)
          end         end       end     end   end )