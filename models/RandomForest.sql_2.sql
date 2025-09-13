create or replace function RandomForest_2 (prev_count int64, simplifiable-if-expression int64, N1_diff int64, cur_count int64, wildcard-import int64, too-many-return-statements int64, low_McCabe_max_diff int64, length_diff int64, volume_diff int64, high_McCabe_sum_diff int64, high_McCabe_max_before int64, simplifiable-condition int64, Blank_before int64, high_ccp_group int64, McCabe_max_before int64, bugs_diff int64, too-many-nested-blocks int64, refactor_mle_diff int64, difficulty_diff int64, LLOC_diff int64, LOC_diff int64, simplifiable-if-statement int64, one_file_fix_rate_diff int64, SLOC_before int64, LOC_before int64, mostly_delete int64, changed_lines int64, Single comments_before int64, removed_lines int64, added_functions int64, h1_diff int64, effort_diff int64, hunks_num int64, Multi_diff int64, same_day_duration_avg_diff int64, N2_diff int64, cur_count_y int64, Comments_diff int64, modified_McCabe_max_diff int64, h2_diff int64, time_diff int64, LLOC_before int64, calculated_length_diff int64, Single comments_after int64, massive_change int64, McCabe_sum_before int64, too-many-boolean-expressions int64, Simplify-boolean-expression int64, line-too-long int64, superfluous-parens int64, low_ccp_group int64, McCabe_max_diff int64, comparison-of-constants int64, high_McCabe_sum_before int64, low_McCabe_sum_diff int64, avg_coupling_code_size_cut_diff int64, is_refactor int64, Single comments_diff int64, unnecessary-semicolon int64, added_lines int64, prev_count_y int64, try-except-raise int64, low_McCabe_sum_before int64, vocabulary_diff int64, too-many-branches int64, McCabe_sum_after int64, broad-exception-caught int64, prev_count_x int64, only_removal int64, McCabe_max_after int64, pointless-statement int64, low_McCabe_max_before int64, too-many-lines int64, McCabe_sum_diff int64, high_McCabe_max_diff int64, using-constant-test int64, SLOC_diff int64, Blank_diff int64, Comments_after int64, cur_count_x int64, unnecessary-pass int64, too-many-statements int64, Comments_before int64) as (
  case when mostly_delete <= 0.5 then
    case when LOC_before <= 127.5 then
       return 0.95 # (0.95 out of 1.0)
    else  # if LOC_before > 127.5
      case when low_ccp_group <= 0.5 then
        case when LLOC_before <= 2041.0 then
          case when SLOC_before <= 1677.5 then
            case when McCabe_sum_after <= 131.5 then
              case when too-many-statements <= 0.5 then
                case when McCabe_sum_after <= 81.5 then
                  case when one_file_fix_rate_diff <= 0.1576923131942749 then
                    case when refactor_mle_diff <= -0.006639281287789345 then
                      case when Comments_before <= 24.0 then
                         return 0.8181818181818182 # (0.8181818181818182 out of 1.0)
                      else  # if Comments_before > 24.0
                         return 0.32 # (0.32 out of 1.0)
                      end                     else  # if refactor_mle_diff > -0.006639281287789345
                      case when hunks_num <= 3.0 then
                         return 0.8333333333333334 # (0.8333333333333334 out of 1.0)
                      else  # if hunks_num > 3.0
                         return 0.8 # (0.8 out of 1.0)
                      end                     end                   else  # if one_file_fix_rate_diff > 0.1576923131942749
                     return 0.3448275862068966 # (0.3448275862068966 out of 1.0)
                  end                 else  # if McCabe_sum_after > 81.5
                  case when Blank_before <= 111.5 then
                     return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
                  else  # if Blank_before > 111.5
                     return 1.0 # (1.0 out of 1.0)
                  end                 end               else  # if too-many-statements > 0.5
                case when Single comments_after <= 41.5 then
                   return 0.5384615384615384 # (0.5384615384615384 out of 1.0)
                else  # if Single comments_after > 41.5
                   return 0.22727272727272727 # (0.22727272727272727 out of 1.0)
                end               end             else  # if McCabe_sum_after > 131.5
              case when McCabe_sum_after <= 203.0 then
                case when LLOC_diff <= -23.5 then
                   return 0.1 # (0.1 out of 1.0)
                else  # if LLOC_diff > -23.5
                  case when refactor_mle_diff <= -0.07446722313761711 then
                    case when removed_lines <= 18.5 then
                       return 0.35294117647058826 # (0.35294117647058826 out of 1.0)
                    else  # if removed_lines > 18.5
                       return 0.26666666666666666 # (0.26666666666666666 out of 1.0)
                    end                   else  # if refactor_mle_diff > -0.07446722313761711
                     return 0.5862068965517241 # (0.5862068965517241 out of 1.0)
                  end                 end               else  # if McCabe_sum_after > 203.0
                case when high_McCabe_max_before <= 0.5 then
                   return 0.7666666666666667 # (0.7666666666666667 out of 1.0)
                else  # if high_McCabe_max_before > 0.5
                  case when N2_diff <= -3.0 then
                     return 0.17647058823529413 # (0.17647058823529413 out of 1.0)
                  else  # if N2_diff > -3.0
                     return 0.5333333333333333 # (0.5333333333333333 out of 1.0)
                  end                 end               end             end           else  # if SLOC_before > 1677.5
             return 0.8888888888888888 # (0.8888888888888888 out of 1.0)
          end         else  # if LLOC_before > 2041.0
           return 0.18518518518518517 # (0.18518518518518517 out of 1.0)
        end       else  # if low_ccp_group > 0.5
        case when SLOC_before <= 1248.5 then
          case when length_diff <= -13.5 then
             return 0.25 # (0.25 out of 1.0)
          else  # if length_diff > -13.5
            case when changed_lines <= 19.0 then
               return 0.25 # (0.25 out of 1.0)
            else  # if changed_lines > 19.0
              case when SLOC_diff <= 13.0 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if SLOC_diff > 13.0
                 return 0.10526315789473684 # (0.10526315789473684 out of 1.0)
              end             end           end         else  # if SLOC_before > 1248.5
           return 0.625 # (0.625 out of 1.0)
        end       end     end   else  # if mostly_delete > 0.5
    case when hunks_num <= 2.5 then
       return 0.8076923076923077 # (0.8076923076923077 out of 1.0)
    else  # if hunks_num > 2.5
       return 0.5 # (0.5 out of 1.0)
    end   end )