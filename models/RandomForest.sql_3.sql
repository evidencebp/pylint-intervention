create or replace function RandomForest_3 (using-constant-test int64, simplifiable-if-statement int64, Comments_after int64, same_day_duration_avg_diff int64, Single comments_before int64, one_file_fix_rate_diff int64, too-many-boolean-expressions int64, Single comments_diff int64, high_McCabe_sum_before int64, pointless-statement int64, bugs_diff int64, McCabe_max_before int64, length_diff int64, LOC_diff int64, N2_diff int64, superfluous-parens int64, too-many-nested-blocks int64, effort_diff int64, cur_count_x int64, high_McCabe_max_before int64, comparison-of-constants int64, SLOC_diff int64, hunks_num int64, high_McCabe_max_diff int64, prev_count int64, McCabe_sum_after int64, cur_count_y int64, refactor_mle_diff int64, too-many-return-statements int64, too-many-statements int64, too-many-lines int64, only_removal int64, removed_lines int64, cur_count int64, volume_diff int64, is_refactor int64, prev_count_y int64, calculated_length_diff int64, Simplify-boolean-expression int64, h1_diff int64, McCabe_max_diff int64, wildcard-import int64, McCabe_sum_before int64, line-too-long int64, N1_diff int64, too-many-branches int64, h2_diff int64, McCabe_max_after int64, unnecessary-pass int64, avg_coupling_code_size_cut_diff int64, high_ccp_group int64, vocabulary_diff int64, try-except-raise int64, broad-exception-caught int64, simplifiable-condition int64, LLOC_before int64, added_functions int64, LLOC_diff int64, difficulty_diff int64, McCabe_sum_diff int64, Multi_diff int64, massive_change int64, mostly_delete int64, Comments_before int64, changed_lines int64, Comments_diff int64, time_diff int64, Blank_before int64, high_McCabe_sum_diff int64, added_lines int64, prev_count_x int64, unnecessary-semicolon int64, Blank_diff int64, modified_McCabe_max_diff int64, Single comments_after int64, LOC_before int64, simplifiable-if-expression int64, SLOC_before int64) as (
  case when h2_diff <= -28.5 then
    case when vocabulary_diff <= -49.5 then
      case when N2_diff <= -130.0 then
         return 0.5238095238095238 # (11.0 out of 21.0)
      else  # if N2_diff > -130.0
         return 0.3157894736842105 # (6.0 out of 19.0)
      end     else  # if vocabulary_diff > -49.5
       return 0.0 # (0.0 out of 19.0)
    end   else  # if h2_diff > -28.5
    case when Single comments_before <= 415.5 then
      case when Single comments_after <= 58.5 then
        case when modified_McCabe_max_diff <= -1.5 then
          case when Single comments_diff <= -1.5 then
            case when avg_coupling_code_size_cut_diff <= -0.38256411999464035 then
               return 1.0 # (22.0 out of 22.0)
            else  # if avg_coupling_code_size_cut_diff > -0.38256411999464035
               return 0.84 # (21.0 out of 25.0)
            end           else  # if Single comments_diff > -1.5
            case when SLOC_before <= 256.5 then
               return 0.14285714285714285 # (2.0 out of 14.0)
            else  # if SLOC_before > 256.5
               return 0.7666666666666667 # (23.0 out of 30.0)
            end           end         else  # if modified_McCabe_max_diff > -1.5
          case when high_ccp_group <= 0.5 then
            case when Comments_before <= 8.5 then
               return 0.7241379310344828 # (21.0 out of 29.0)
            else  # if Comments_before > 8.5
              case when added_lines <= 172.0 then
                case when McCabe_sum_before <= 166.0 then
                  case when Comments_before <= 25.0 then
                     return 0.5 # (12.0 out of 24.0)
                  else  # if Comments_before > 25.0
                    case when refactor_mle_diff <= -0.1450617015361786 then
                       return 0.3333333333333333 # (7.0 out of 21.0)
                    else  # if refactor_mle_diff > -0.1450617015361786
                      case when refactor_mle_diff <= 0.02822023816406727 then
                         return 0.0 # (0.0 out of 21.0)
                      else  # if refactor_mle_diff > 0.02822023816406727
                         return 0.28 # (7.0 out of 25.0)
                      end                     end                   end                 else  # if McCabe_sum_before > 166.0
                   return 0.08 # (2.0 out of 25.0)
                end               else  # if added_lines > 172.0
                 return 0.7741935483870968 # (24.0 out of 31.0)
              end             end           else  # if high_ccp_group > 0.5
            case when removed_lines <= 6.5 then
               return 0.6551724137931034 # (19.0 out of 29.0)
            else  # if removed_lines > 6.5
               return 0.8148148148148148 # (22.0 out of 27.0)
            end           end         end       else  # if Single comments_after > 58.5
        case when LLOC_before <= 604.5 then
          case when hunks_num <= 5.5 then
             return 0.3090909090909091 # (17.0 out of 55.0)
          else  # if hunks_num > 5.5
            case when h2_diff <= -0.5 then
               return 0.0 # (0.0 out of 17.0)
            else  # if h2_diff > -0.5
              case when same_day_duration_avg_diff <= -14.980126857757568 then
                 return 0.09090909090909091 # (1.0 out of 11.0)
              else  # if same_day_duration_avg_diff > -14.980126857757568
                 return 0.06666666666666667 # (1.0 out of 15.0)
              end             end           end         else  # if LLOC_before > 604.5
          case when avg_coupling_code_size_cut_diff <= 0.08015873283147812 then
            case when same_day_duration_avg_diff <= 65.66716003417969 then
              case when avg_coupling_code_size_cut_diff <= -0.7613445222377777 then
                 return 0.5294117647058824 # (9.0 out of 17.0)
              else  # if avg_coupling_code_size_cut_diff > -0.7613445222377777
                 return 0.9047619047619048 # (19.0 out of 21.0)
              end             else  # if same_day_duration_avg_diff > 65.66716003417969
               return 0.36363636363636365 # (4.0 out of 11.0)
            end           else  # if avg_coupling_code_size_cut_diff > 0.08015873283147812
            case when McCabe_max_before <= 17.5 then
               return 0.17647058823529413 # (3.0 out of 17.0)
            else  # if McCabe_max_before > 17.5
              case when Single comments_after <= 237.5 then
                 return 0.6111111111111112 # (11.0 out of 18.0)
              else  # if Single comments_after > 237.5
                 return 0.3684210526315789 # (7.0 out of 19.0)
              end             end           end         end       end     else  # if Single comments_before > 415.5
       return 0.9411764705882353 # (16.0 out of 17.0)
    end   end )