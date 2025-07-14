create or replace function RandomForest_9 (SLOC_before int64, simplifiable-condition int64, bugs_diff int64, Blank_before int64, LLOC_diff int64, try-except-raise int64, LLOC_before int64, changed_lines int64, h2_diff int64, prev_count_x int64, too-many-lines int64, cur_count_y int64, Comments_before int64, McCabe_sum_after int64, cur_count_x int64, vocabulary_diff int64, Single comments_before int64, N2_diff int64, high_ccp_group int64, massive_change int64, added_lines int64, prev_count int64, refactor_mle_diff int64, superfluous-parens int64, avg_coupling_code_size_cut_diff int64, McCabe_sum_diff int64, LOC_before int64, too-many-return-statements int64, too-many-branches int64, too-many-nested-blocks int64, difficulty_diff int64, time_diff int64, Single comments_after int64, calculated_length_diff int64, Simplify-boolean-expression int64, unnecessary-semicolon int64, mostly_delete int64, effort_diff int64, Multi_diff int64, McCabe_max_diff int64, is_refactor int64, only_removal int64, LOC_diff int64, one_file_fix_rate_diff int64, Comments_after int64, comparison-of-constants int64, McCabe_max_after int64, length_diff int64, simplifiable-if-statement int64, removed_lines int64, unnecessary-pass int64, Comments_diff int64, cur_count int64, same_day_duration_avg_diff int64, hunks_num int64, N1_diff int64, line-too-long int64, volume_diff int64, using-constant-test int64, too-many-boolean-expressions int64, modified_McCabe_max_diff int64, h1_diff int64, added_functions int64, SLOC_diff int64, too-many-statements int64, pointless-statement int64, wildcard-import int64, McCabe_max_before int64, prev_count_y int64, broad-exception-caught int64, Blank_diff int64, McCabe_sum_before int64, simplifiable-if-expression int64, Single comments_diff int64) as (
  case when Blank_diff <= -54.5 then
    case when Comments_before <= 116.5 then
       return 1.0 # (24.0 out of 24.0)
    else  # if Comments_before > 116.5
       return 0.5294117647058824 # (9.0 out of 17.0)
    end   else  # if Blank_diff > -54.5
    case when McCabe_sum_before <= 129.5 then
      case when McCabe_max_diff <= -4.5 then
        case when Single comments_diff <= -2.5 then
           return 0.5 # (10.0 out of 20.0)
        else  # if Single comments_diff > -2.5
           return 0.043478260869565216 # (1.0 out of 23.0)
        end       else  # if McCabe_max_diff > -4.5
        case when vocabulary_diff <= 2.5 then
          case when Single comments_before <= 23.0 then
            case when hunks_num <= 3.5 then
              case when McCabe_max_after <= 11.0 then
                case when McCabe_max_after <= 5.5 then
                   return 0.9047619047619048 # (19.0 out of 21.0)
                else  # if McCabe_max_after > 5.5
                   return 0.7333333333333333 # (11.0 out of 15.0)
                end               else  # if McCabe_max_after > 11.0
                 return 0.9444444444444444 # (17.0 out of 18.0)
              end             else  # if hunks_num > 3.5
               return 0.6666666666666666 # (20.0 out of 30.0)
            end           else  # if Single comments_before > 23.0
            case when Single comments_after <= 400.0 then
              case when McCabe_max_before <= 19.5 then
                case when hunks_num <= 7.5 then
                  case when Comments_after <= 40.0 then
                     return 0.5454545454545454 # (12.0 out of 22.0)
                  else  # if Comments_after > 40.0
                    case when one_file_fix_rate_diff <= -0.0476190485060215 then
                       return 0.06666666666666667 # (1.0 out of 15.0)
                    else  # if one_file_fix_rate_diff > -0.0476190485060215
                       return 0.2857142857142857 # (4.0 out of 14.0)
                    end                   end                 else  # if hunks_num > 7.5
                   return 0.6086956521739131 # (14.0 out of 23.0)
                end               else  # if McCabe_max_before > 19.5
                 return 0.5625 # (9.0 out of 16.0)
              end             else  # if Single comments_after > 400.0
               return 0.9444444444444444 # (17.0 out of 18.0)
            end           end         else  # if vocabulary_diff > 2.5
           return 0.32142857142857145 # (9.0 out of 28.0)
        end       end     else  # if McCabe_sum_before > 129.5
      case when Comments_diff <= -1.5 then
        case when LLOC_diff <= -81.5 then
           return 0.25925925925925924 # (7.0 out of 27.0)
        else  # if LLOC_diff > -81.5
          case when McCabe_sum_after <= 203.5 then
             return 0.0 # (0.0 out of 17.0)
          else  # if McCabe_sum_after > 203.5
             return 0.14285714285714285 # (4.0 out of 28.0)
          end         end       else  # if Comments_diff > -1.5
        case when avg_coupling_code_size_cut_diff <= 1.9375 then
          case when Single comments_after <= 214.5 then
            case when LOC_diff <= 11.5 then
              case when McCabe_sum_before <= 211.5 then
                case when McCabe_max_diff <= -0.5 then
                   return 0.23529411764705882 # (4.0 out of 17.0)
                else  # if McCabe_max_diff > -0.5
                  case when Blank_before <= 111.0 then
                     return 0.08 # (2.0 out of 25.0)
                  else  # if Blank_before > 111.0
                    case when avg_coupling_code_size_cut_diff <= -0.10524425283074379 then
                       return 0.7857142857142857 # (11.0 out of 14.0)
                    else  # if avg_coupling_code_size_cut_diff > -0.10524425283074379
                       return 0.25 # (5.0 out of 20.0)
                    end                   end                 end               else  # if McCabe_sum_before > 211.5
                case when McCabe_max_before <= 24.5 then
                   return 0.13043478260869565 # (3.0 out of 23.0)
                else  # if McCabe_max_before > 24.5
                   return 0.0 # (0.0 out of 29.0)
                end               end             else  # if LOC_diff > 11.5
              case when changed_lines <= 288.5 then
                 return 0.6666666666666666 # (12.0 out of 18.0)
              else  # if changed_lines > 288.5
                 return 0.21052631578947367 # (4.0 out of 19.0)
              end             end           else  # if Single comments_after > 214.5
            case when one_file_fix_rate_diff <= -0.047222224064171314 then
               return 0.7142857142857143 # (15.0 out of 21.0)
            else  # if one_file_fix_rate_diff > -0.047222224064171314
               return 0.45 # (9.0 out of 20.0)
            end           end         else  # if avg_coupling_code_size_cut_diff > 1.9375
           return 0.9444444444444444 # (17.0 out of 18.0)
        end       end     end   end )