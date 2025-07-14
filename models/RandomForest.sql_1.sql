create or replace function RandomForest_1 (effort_diff int64, too-many-nested-blocks int64, Single comments_diff int64, N1_diff int64, avg_coupling_code_size_cut_diff int64, Simplify-boolean-expression int64, try-except-raise int64, h1_diff int64, added_functions int64, too-many-boolean-expressions int64, LLOC_diff int64, cur_count_x int64, wildcard-import int64, mostly_delete int64, LOC_diff int64, difficulty_diff int64, Comments_before int64, prev_count_y int64, time_diff int64, pointless-statement int64, vocabulary_diff int64, modified_McCabe_max_diff int64, prev_count int64, McCabe_sum_before int64, McCabe_max_after int64, Blank_diff int64, using-constant-test int64, McCabe_max_before int64, is_refactor int64, Comments_after int64, SLOC_before int64, superfluous-parens int64, too-many-branches int64, massive_change int64, comparison-of-constants int64, broad-exception-caught int64, Blank_before int64, N2_diff int64, McCabe_sum_after int64, too-many-statements int64, refactor_mle_diff int64, LOC_before int64, simplifiable-if-statement int64, only_removal int64, h2_diff int64, unnecessary-semicolon int64, too-many-lines int64, LLOC_before int64, volume_diff int64, too-many-return-statements int64, high_ccp_group int64, Single comments_before int64, simplifiable-if-expression int64, changed_lines int64, Multi_diff int64, one_file_fix_rate_diff int64, prev_count_x int64, simplifiable-condition int64, cur_count_y int64, calculated_length_diff int64, SLOC_diff int64, line-too-long int64, McCabe_max_diff int64, Comments_diff int64, cur_count int64, Single comments_after int64, removed_lines int64, added_lines int64, length_diff int64, unnecessary-pass int64, hunks_num int64, bugs_diff int64, same_day_duration_avg_diff int64, McCabe_sum_diff int64) as (
  case when added_lines <= 1.5 then
    case when Blank_before <= 65.0 then
       return 0.9629629629629629 # (26.0 out of 27.0)
    else  # if Blank_before > 65.0
      case when Blank_before <= 122.0 then
         return 0.2857142857142857 # (4.0 out of 14.0)
      else  # if Blank_before > 122.0
        case when McCabe_sum_after <= 261.0 then
           return 0.8 # (20.0 out of 25.0)
        else  # if McCabe_sum_after > 261.0
           return 0.4375 # (7.0 out of 16.0)
        end       end     end   else  # if added_lines > 1.5
    case when McCabe_sum_after <= 59.5 then
      case when Single comments_diff <= -4.5 then
        case when modified_McCabe_max_diff <= -0.5 then
           return 1.0 # (34.0 out of 34.0)
        else  # if modified_McCabe_max_diff > -0.5
           return 0.7 # (14.0 out of 20.0)
        end       else  # if Single comments_diff > -4.5
        case when added_lines <= 92.0 then
          case when avg_coupling_code_size_cut_diff <= 0.28900881111621857 then
            case when same_day_duration_avg_diff <= -35.372222900390625 then
               return 0.7272727272727273 # (16.0 out of 22.0)
            else  # if same_day_duration_avg_diff > -35.372222900390625
               return 0.32142857142857145 # (9.0 out of 28.0)
            end           else  # if avg_coupling_code_size_cut_diff > 0.28900881111621857
             return 0.7647058823529411 # (13.0 out of 17.0)
          end         else  # if added_lines > 92.0
           return 0.09523809523809523 # (2.0 out of 21.0)
        end       end     else  # if McCabe_sum_after > 59.5
      case when high_ccp_group <= 0.5 then
        case when Blank_before <= 260.5 then
          case when hunks_num <= 19.5 then
            case when McCabe_sum_before <= 87.5 then
              case when h2_diff <= 1.0 then
                 return 0.0 # (0.0 out of 23.0)
              else  # if h2_diff > 1.0
                 return 0.0625 # (1.0 out of 16.0)
              end             else  # if McCabe_sum_before > 87.5
              case when refactor_mle_diff <= -0.363955557346344 then
                 return 0.5714285714285714 # (8.0 out of 14.0)
              else  # if refactor_mle_diff > -0.363955557346344
                case when SLOC_diff <= -65.5 then
                   return 0.0 # (0.0 out of 30.0)
                else  # if SLOC_diff > -65.5
                  case when Comments_diff <= 1.0 then
                    case when Comments_before <= 29.0 then
                       return 0.6 # (9.0 out of 15.0)
                    else  # if Comments_before > 29.0
                      case when LOC_diff <= 3.5 then
                        case when h2_diff <= -14.5 then
                           return 0.07692307692307693 # (1.0 out of 13.0)
                        else  # if h2_diff > -14.5
                          case when N2_diff <= -1.0 then
                             return 0.5 # (11.0 out of 22.0)
                          else  # if N2_diff > -1.0
                             return 0.34615384615384615 # (9.0 out of 26.0)
                          end                         end                       else  # if LOC_diff > 3.5
                         return 0.05555555555555555 # (1.0 out of 18.0)
                      end                     end                   else  # if Comments_diff > 1.0
                     return 0.125 # (3.0 out of 24.0)
                  end                 end               end             end           else  # if hunks_num > 19.5
             return 0.6153846153846154 # (8.0 out of 13.0)
          end         else  # if Blank_before > 260.5
          case when McCabe_max_after <= 31.5 then
            case when removed_lines <= 62.5 then
              case when LOC_before <= 2040.5 then
                 return 0.11764705882352941 # (2.0 out of 17.0)
              else  # if LOC_before > 2040.5
                 return 0.46153846153846156 # (6.0 out of 13.0)
              end             else  # if removed_lines > 62.5
               return 0.7058823529411765 # (12.0 out of 17.0)
            end           else  # if McCabe_max_after > 31.5
             return 0.75 # (24.0 out of 32.0)
          end         end       else  # if high_ccp_group > 0.5
        case when LLOC_diff <= 0.5 then
          case when SLOC_before <= 603.0 then
             return 0.6666666666666666 # (14.0 out of 21.0)
          else  # if SLOC_before > 603.0
             return 0.9583333333333334 # (23.0 out of 24.0)
          end         else  # if LLOC_diff > 0.5
          case when McCabe_max_diff <= 0.5 then
             return 0.6842105263157895 # (13.0 out of 19.0)
          else  # if McCabe_max_diff > 0.5
             return 0.10526315789473684 # (2.0 out of 19.0)
          end         end       end     end   end )