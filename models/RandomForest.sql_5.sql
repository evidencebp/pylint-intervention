create or replace function RandomForest_5 (low_McCabe_sum_before int64, changed_lines int64, low_McCabe_max_diff int64, try-except-raise int64, Comments_before int64, high_McCabe_sum_diff int64, low_McCabe_max_before int64, Multi_diff int64, effort_diff int64, difficulty_diff int64, only_removal int64, length_diff int64, comparison-of-constants int64, LOC_diff int64, h2_diff int64, line-too-long int64, h1_diff int64, using-constant-test int64, broad-exception-caught int64, time_diff int64, calculated_length_diff int64, too-many-branches int64, SLOC_before int64, low_ccp_group int64, avg_coupling_code_size_cut_diff int64, new_function int64, wildcard-import int64, McCabe_max_before int64, superfluous-parens int64, low_McCabe_sum_diff int64, pointless-statement int64, one_file_fix_rate_diff int64, cur_count_x int64, same_day_duration_avg_diff int64, too-many-nested-blocks int64, simplifiable-condition int64, too-many-lines int64, SLOC_diff int64, cur_count_y int64, LLOC_before int64, Comments_after int64, high_ccp_group int64, bugs_diff int64, unnecessary-pass int64, prev_count_x int64, massive_change int64, McCabe_max_after int64, removed_lines int64, Comments_diff int64, Single comments_diff int64, too-many-statements int64, Simplify-boolean-expression int64, is_refactor int64, refactor_mle_diff int64, added_lines int64, mostly_delete int64, volume_diff int64, too-many-boolean-expressions int64, N2_diff int64, Blank_before int64, vocabulary_diff int64, McCabe_sum_before int64, high_McCabe_sum_before int64, N1_diff int64, LOC_before int64, LLOC_diff int64, high_McCabe_max_diff int64, simplifiable-if-statement int64, prev_count_y int64, hunks_num int64, Blank_diff int64, prev_count int64, Single comments_before int64, McCabe_max_diff int64, McCabe_sum_diff int64, modified_McCabe_max_diff int64, McCabe_sum_after int64, too-many-return-statements int64, Single comments_after int64, unnecessary-semicolon int64, added_functions int64, cur_count int64, simplifiable-if-expression int64, high_McCabe_max_before int64) as (
  case when hunks_num <= 11.5 then
    case when Single comments_after <= 1.5 then
       return 0.9047619047619048 # (0.9047619047619048 out of 1.0)
    else  # if Single comments_after > 1.5
      case when Comments_diff <= 20.5 then
        case when high_ccp_group <= 0.5 then
          case when N1_diff <= -47.5 then
             return 0.9090909090909091 # (0.9090909090909091 out of 1.0)
          else  # if N1_diff > -47.5
            case when changed_lines <= 138.5 then
              case when low_ccp_group <= 0.5 then
                case when h2_diff <= -2.5 then
                  case when SLOC_diff <= -53.0 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if SLOC_diff > -53.0
                    case when Comments_before <= 58.0 then
                       return 0.09090909090909091 # (0.09090909090909091 out of 1.0)
                    else  # if Comments_before > 58.0
                       return 0.5789473684210527 # (0.5789473684210527 out of 1.0)
                    end                   end                 else  # if h2_diff > -2.5
                  case when Blank_before <= 65.0 then
                     return 0.8064516129032258 # (0.8064516129032258 out of 1.0)
                  else  # if Blank_before > 65.0
                    case when avg_coupling_code_size_cut_diff <= 1.2247923612594604 then
                      case when Blank_diff <= -0.5 then
                         return 0.55 # (0.55 out of 1.0)
                      else  # if Blank_diff > -0.5
                        case when McCabe_max_before <= 23.5 then
                          case when hunks_num <= 1.5 then
                             return 0.2727272727272727 # (0.2727272727272727 out of 1.0)
                          else  # if hunks_num > 1.5
                             return 0.07142857142857142 # (0.07142857142857142 out of 1.0)
                          end                         else  # if McCabe_max_before > 23.5
                           return 0.2727272727272727 # (0.2727272727272727 out of 1.0)
                        end                       end                     else  # if avg_coupling_code_size_cut_diff > 1.2247923612594604
                       return 0.8 # (0.8 out of 1.0)
                    end                   end                 end               else  # if low_ccp_group > 0.5
                case when Single comments_diff <= 0.5 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if Single comments_diff > 0.5
                   return 0.3125 # (0.3125 out of 1.0)
                end               end             else  # if changed_lines > 138.5
              case when LLOC_diff <= 3.0 then
                case when hunks_num <= 5.0 then
                   return 0.6 # (0.6 out of 1.0)
                else  # if hunks_num > 5.0
                   return 0.9 # (0.9 out of 1.0)
                end               else  # if LLOC_diff > 3.0
                 return 0.5 # (0.5 out of 1.0)
              end             end           end         else  # if high_ccp_group > 0.5
          case when LOC_before <= 2308.0 then
            case when Comments_after <= 21.5 then
               return 0.5238095238095238 # (0.5238095238095238 out of 1.0)
            else  # if Comments_after > 21.5
              case when removed_lines <= 3.5 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if removed_lines > 3.5
                case when refactor_mle_diff <= 0.005040935706347227 then
                   return 0.7083333333333334 # (0.7083333333333334 out of 1.0)
                else  # if refactor_mle_diff > 0.005040935706347227
                   return 1.0 # (1.0 out of 1.0)
                end               end             end           else  # if LOC_before > 2308.0
             return 0.5 # (0.5 out of 1.0)
          end         end       else  # if Comments_diff > 20.5
         return 0.8275862068965517 # (0.8275862068965517 out of 1.0)
      end     end   else  # if hunks_num > 11.5
    case when SLOC_diff <= 40.5 then
      case when one_file_fix_rate_diff <= -0.22500000149011612 then
         return 0.0 # (0.0 out of 1.0)
      else  # if one_file_fix_rate_diff > -0.22500000149011612
        case when one_file_fix_rate_diff <= -0.0062500000931322575 then
           return 0.36363636363636365 # (0.36363636363636365 out of 1.0)
        else  # if one_file_fix_rate_diff > -0.0062500000931322575
          case when removed_lines <= 60.0 then
            case when Blank_diff <= -2.0 then
               return 0.07142857142857142 # (0.07142857142857142 out of 1.0)
            else  # if Blank_diff > -2.0
               return 0.0 # (0.0 out of 1.0)
            end           else  # if removed_lines > 60.0
             return 0.36363636363636365 # (0.36363636363636365 out of 1.0)
          end         end       end     else  # if SLOC_diff > 40.5
       return 0.5714285714285714 # (0.5714285714285714 out of 1.0)
    end   end )