create or replace function RandomForest_6 (SLOC_before int64, simplifiable-condition int64, bugs_diff int64, Blank_before int64, LLOC_diff int64, try-except-raise int64, LLOC_before int64, changed_lines int64, h2_diff int64, prev_count_x int64, too-many-lines int64, cur_count_y int64, Comments_before int64, McCabe_sum_after int64, cur_count_x int64, vocabulary_diff int64, Single comments_before int64, N2_diff int64, high_ccp_group int64, massive_change int64, added_lines int64, prev_count int64, refactor_mle_diff int64, superfluous-parens int64, avg_coupling_code_size_cut_diff int64, McCabe_sum_diff int64, LOC_before int64, too-many-return-statements int64, too-many-branches int64, too-many-nested-blocks int64, difficulty_diff int64, time_diff int64, Single comments_after int64, calculated_length_diff int64, Simplify-boolean-expression int64, unnecessary-semicolon int64, mostly_delete int64, effort_diff int64, Multi_diff int64, McCabe_max_diff int64, is_refactor int64, only_removal int64, LOC_diff int64, one_file_fix_rate_diff int64, Comments_after int64, comparison-of-constants int64, McCabe_max_after int64, length_diff int64, simplifiable-if-statement int64, removed_lines int64, unnecessary-pass int64, Comments_diff int64, cur_count int64, same_day_duration_avg_diff int64, hunks_num int64, N1_diff int64, line-too-long int64, volume_diff int64, using-constant-test int64, too-many-boolean-expressions int64, modified_McCabe_max_diff int64, h1_diff int64, added_functions int64, SLOC_diff int64, too-many-statements int64, pointless-statement int64, wildcard-import int64, McCabe_max_before int64, prev_count_y int64, broad-exception-caught int64, Blank_diff int64, McCabe_sum_before int64, simplifiable-if-expression int64, Single comments_diff int64) as (
  case when Single comments_before <= 1.5 then
     return 1.0 # (16.0 out of 16.0)
  else  # if Single comments_before > 1.5
    case when SLOC_before <= 555.0 then
      case when N2_diff <= -9.5 then
        case when changed_lines <= 138.5 then
           return 0.2857142857142857 # (4.0 out of 14.0)
        else  # if changed_lines > 138.5
          case when LLOC_before <= 267.5 then
             return 0.9583333333333334 # (23.0 out of 24.0)
          else  # if LLOC_before > 267.5
             return 0.8333333333333334 # (15.0 out of 18.0)
          end         end       else  # if N2_diff > -9.5
        case when Single comments_before <= 5.5 then
           return 0.7037037037037037 # (19.0 out of 27.0)
        else  # if Single comments_before > 5.5
          case when Single comments_before <= 13.5 then
            case when Blank_diff <= -0.5 then
               return 0.0 # (0.0 out of 17.0)
            else  # if Blank_diff > -0.5
               return 0.4090909090909091 # (9.0 out of 22.0)
            end           else  # if Single comments_before > 13.5
            case when added_lines <= 11.5 then
              case when McCabe_max_after <= 8.5 then
                 return 0.7142857142857143 # (10.0 out of 14.0)
              else  # if McCabe_max_after > 8.5
                case when hunks_num <= 1.5 then
                   return 0.375 # (6.0 out of 16.0)
                else  # if hunks_num > 1.5
                   return 0.09523809523809523 # (2.0 out of 21.0)
                end               end             else  # if added_lines > 11.5
              case when McCabe_sum_before <= 106.0 then
                case when SLOC_before <= 252.5 then
                   return 0.8 # (16.0 out of 20.0)
                else  # if SLOC_before > 252.5
                  case when McCabe_sum_diff <= 1.0 then
                     return 0.47058823529411764 # (8.0 out of 17.0)
                  else  # if McCabe_sum_diff > 1.0
                     return 0.16666666666666666 # (3.0 out of 18.0)
                  end                 end               else  # if McCabe_sum_before > 106.0
                 return 0.84 # (21.0 out of 25.0)
              end             end           end         end       end     else  # if SLOC_before > 555.0
      case when refactor_mle_diff <= -0.06388264708220959 then
        case when superfluous-parens <= 0.5 then
          case when Blank_before <= 259.5 then
            case when avg_coupling_code_size_cut_diff <= 0.790909081697464 then
              case when McCabe_sum_before <= 157.0 then
                 return 0.0 # (0.0 out of 37.0)
              else  # if McCabe_sum_before > 157.0
                 return 0.13333333333333333 # (2.0 out of 15.0)
              end             else  # if avg_coupling_code_size_cut_diff > 0.790909081697464
               return 0.17647058823529413 # (3.0 out of 17.0)
            end           else  # if Blank_before > 259.5
             return 0.41379310344827586 # (12.0 out of 29.0)
          end         else  # if superfluous-parens > 0.5
           return 0.5806451612903226 # (18.0 out of 31.0)
        end       else  # if refactor_mle_diff > -0.06388264708220959
        case when Comments_diff <= 2.5 then
          case when refactor_mle_diff <= -0.015323200728744268 then
             return 0.8666666666666667 # (13.0 out of 15.0)
          else  # if refactor_mle_diff > -0.015323200728744268
            case when Comments_before <= 70.0 then
              case when Single comments_before <= 52.0 then
                case when McCabe_max_diff <= -0.5 then
                   return 0.47058823529411764 # (8.0 out of 17.0)
                else  # if McCabe_max_diff > -0.5
                   return 0.7857142857142857 # (11.0 out of 14.0)
                end               else  # if Single comments_before > 52.0
                 return 0.35714285714285715 # (10.0 out of 28.0)
              end             else  # if Comments_before > 70.0
              case when SLOC_diff <= -95.5 then
                 return 0.6923076923076923 # (9.0 out of 13.0)
              else  # if SLOC_diff > -95.5
                case when avg_coupling_code_size_cut_diff <= -0.6789682507514954 then
                   return 0.037037037037037035 # (1.0 out of 27.0)
                else  # if avg_coupling_code_size_cut_diff > -0.6789682507514954
                  case when same_day_duration_avg_diff <= -21.780677795410156 then
                     return 0.47368421052631576 # (9.0 out of 19.0)
                  else  # if same_day_duration_avg_diff > -21.780677795410156
                     return 0.0625 # (2.0 out of 32.0)
                  end                 end               end             end           end         else  # if Comments_diff > 2.5
          case when McCabe_sum_after <= 195.5 then
             return 0.95 # (19.0 out of 20.0)
          else  # if McCabe_sum_after > 195.5
             return 0.5294117647058824 # (9.0 out of 17.0)
          end         end       end     end   end )