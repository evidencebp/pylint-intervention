create or replace function RandomForest_2 (using-constant-test int64, simplifiable-if-statement int64, Comments_after int64, same_day_duration_avg_diff int64, Single comments_before int64, one_file_fix_rate_diff int64, too-many-boolean-expressions int64, Single comments_diff int64, high_McCabe_sum_before int64, pointless-statement int64, bugs_diff int64, McCabe_max_before int64, length_diff int64, LOC_diff int64, N2_diff int64, superfluous-parens int64, too-many-nested-blocks int64, effort_diff int64, cur_count_x int64, high_McCabe_max_before int64, comparison-of-constants int64, SLOC_diff int64, hunks_num int64, high_McCabe_max_diff int64, prev_count int64, McCabe_sum_after int64, cur_count_y int64, refactor_mle_diff int64, too-many-return-statements int64, too-many-statements int64, too-many-lines int64, only_removal int64, removed_lines int64, cur_count int64, volume_diff int64, is_refactor int64, prev_count_y int64, calculated_length_diff int64, Simplify-boolean-expression int64, h1_diff int64, McCabe_max_diff int64, wildcard-import int64, McCabe_sum_before int64, line-too-long int64, N1_diff int64, too-many-branches int64, h2_diff int64, McCabe_max_after int64, unnecessary-pass int64, avg_coupling_code_size_cut_diff int64, high_ccp_group int64, vocabulary_diff int64, try-except-raise int64, broad-exception-caught int64, simplifiable-condition int64, LLOC_before int64, added_functions int64, LLOC_diff int64, difficulty_diff int64, McCabe_sum_diff int64, Multi_diff int64, massive_change int64, mostly_delete int64, Comments_before int64, changed_lines int64, Comments_diff int64, time_diff int64, Blank_before int64, high_McCabe_sum_diff int64, added_lines int64, prev_count_x int64, unnecessary-semicolon int64, Blank_diff int64, modified_McCabe_max_diff int64, Single comments_after int64, LOC_before int64, simplifiable-if-expression int64, SLOC_before int64) as (
  case when high_ccp_group <= 0.5 then
    case when Single comments_before <= 261.0 then
      case when Single comments_after <= 16.5 then
        case when McCabe_sum_before <= 114.5 then
          case when LOC_diff <= -5.0 then
             return 0.0625 # (1.0 out of 16.0)
          else  # if LOC_diff > -5.0
            case when LOC_before <= 291.0 then
              case when Single comments_after <= 3.5 then
                 return 0.6 # (9.0 out of 15.0)
              else  # if Single comments_after > 3.5
                 return 0.7333333333333333 # (11.0 out of 15.0)
              end             else  # if LOC_before > 291.0
               return 0.4375 # (7.0 out of 16.0)
            end           end         else  # if McCabe_sum_before > 114.5
           return 0.6923076923076923 # (18.0 out of 26.0)
        end       else  # if Single comments_after > 16.5
        case when N1_diff <= -33.5 then
           return 0.6666666666666666 # (16.0 out of 24.0)
        else  # if N1_diff > -33.5
          case when one_file_fix_rate_diff <= -0.5357142984867096 then
             return 0.0 # (0.0 out of 15.0)
          else  # if one_file_fix_rate_diff > -0.5357142984867096
            case when LOC_diff <= 69.5 then
              case when Single comments_after <= 19.5 then
                 return 0.05263157894736842 # (1.0 out of 19.0)
              else  # if Single comments_after > 19.5
                case when LLOC_before <= 561.0 then
                  case when SLOC_before <= 571.0 then
                    case when Comments_after <= 35.0 then
                      case when removed_lines <= 16.0 then
                         return 0.35294117647058826 # (6.0 out of 17.0)
                      else  # if removed_lines > 16.0
                         return 1.0 # (14.0 out of 14.0)
                      end                     else  # if Comments_after > 35.0
                      case when McCabe_max_before <= 15.5 then
                         return 0.13793103448275862 # (4.0 out of 29.0)
                      else  # if McCabe_max_before > 15.5
                         return 0.0 # (0.0 out of 33.0)
                      end                     end                   else  # if SLOC_before > 571.0
                    case when SLOC_before <= 783.5 then
                      case when McCabe_max_before <= 22.5 then
                         return 0.8181818181818182 # (18.0 out of 22.0)
                      else  # if McCabe_max_before > 22.5
                         return 0.3076923076923077 # (4.0 out of 13.0)
                      end                     else  # if SLOC_before > 783.5
                       return 0.26666666666666666 # (4.0 out of 15.0)
                    end                   end                 else  # if LLOC_before > 561.0
                  case when Blank_before <= 309.5 then
                    case when SLOC_diff <= -20.0 then
                       return 0.0 # (0.0 out of 29.0)
                    else  # if SLOC_diff > -20.0
                      case when changed_lines <= 30.0 then
                         return 0.29411764705882354 # (5.0 out of 17.0)
                      else  # if changed_lines > 30.0
                         return 0.08 # (2.0 out of 25.0)
                      end                     end                   else  # if Blank_before > 309.5
                     return 0.5263157894736842 # (10.0 out of 19.0)
                  end                 end               end             else  # if LOC_diff > 69.5
               return 0.5833333333333334 # (14.0 out of 24.0)
            end           end         end       end     else  # if Single comments_before > 261.0
      case when Comments_before <= 379.5 then
         return 0.9090909090909091 # (20.0 out of 22.0)
      else  # if Comments_before > 379.5
        case when SLOC_diff <= 18.0 then
           return 0.375 # (6.0 out of 16.0)
        else  # if SLOC_diff > 18.0
           return 0.625 # (10.0 out of 16.0)
        end       end     end   else  # if high_ccp_group > 0.5
    case when N2_diff <= -36.5 then
       return 0.23076923076923078 # (3.0 out of 13.0)
    else  # if N2_diff > -36.5
      case when McCabe_sum_before <= 97.0 then
        case when avg_coupling_code_size_cut_diff <= -0.0476190485060215 then
           return 0.9642857142857143 # (27.0 out of 28.0)
        else  # if avg_coupling_code_size_cut_diff > -0.0476190485060215
           return 0.8846153846153846 # (23.0 out of 26.0)
        end       else  # if McCabe_sum_before > 97.0
        case when McCabe_sum_after <= 165.0 then
           return 0.46875 # (15.0 out of 32.0)
        else  # if McCabe_sum_after > 165.0
          case when avg_coupling_code_size_cut_diff <= 0.06730769574642181 then
             return 0.75 # (18.0 out of 24.0)
          else  # if avg_coupling_code_size_cut_diff > 0.06730769574642181
             return 1.0 # (20.0 out of 20.0)
          end         end       end     end   end )