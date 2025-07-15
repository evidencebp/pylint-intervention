create or replace function RandomForest_7 (using-constant-test int64, simplifiable-if-statement int64, Comments_after int64, same_day_duration_avg_diff int64, Single comments_before int64, one_file_fix_rate_diff int64, too-many-boolean-expressions int64, Single comments_diff int64, high_McCabe_sum_before int64, pointless-statement int64, bugs_diff int64, McCabe_max_before int64, length_diff int64, LOC_diff int64, N2_diff int64, superfluous-parens int64, too-many-nested-blocks int64, effort_diff int64, cur_count_x int64, high_McCabe_max_before int64, comparison-of-constants int64, SLOC_diff int64, hunks_num int64, high_McCabe_max_diff int64, prev_count int64, McCabe_sum_after int64, cur_count_y int64, refactor_mle_diff int64, too-many-return-statements int64, too-many-statements int64, too-many-lines int64, only_removal int64, removed_lines int64, cur_count int64, volume_diff int64, is_refactor int64, prev_count_y int64, calculated_length_diff int64, Simplify-boolean-expression int64, h1_diff int64, McCabe_max_diff int64, wildcard-import int64, McCabe_sum_before int64, line-too-long int64, N1_diff int64, too-many-branches int64, h2_diff int64, McCabe_max_after int64, unnecessary-pass int64, avg_coupling_code_size_cut_diff int64, high_ccp_group int64, vocabulary_diff int64, try-except-raise int64, broad-exception-caught int64, simplifiable-condition int64, LLOC_before int64, added_functions int64, LLOC_diff int64, difficulty_diff int64, McCabe_sum_diff int64, Multi_diff int64, massive_change int64, mostly_delete int64, Comments_before int64, changed_lines int64, Comments_diff int64, time_diff int64, Blank_before int64, high_McCabe_sum_diff int64, added_lines int64, prev_count_x int64, unnecessary-semicolon int64, Blank_diff int64, modified_McCabe_max_diff int64, Single comments_after int64, LOC_before int64, simplifiable-if-expression int64, SLOC_before int64) as (
  case when LOC_diff <= -114.5 then
    case when Single comments_after <= 45.5 then
      case when McCabe_sum_before <= 124.0 then
         return 0.9615384615384616 # (25.0 out of 26.0)
      else  # if McCabe_sum_before > 124.0
         return 0.7575757575757576 # (25.0 out of 33.0)
      end     else  # if Single comments_after > 45.5
       return 0.47368421052631576 # (9.0 out of 19.0)
    end   else  # if LOC_diff > -114.5
    case when avg_coupling_code_size_cut_diff <= -1.5444444417953491 then
      case when length_diff <= -4.0 then
         return 0.37037037037037035 # (10.0 out of 27.0)
      else  # if length_diff > -4.0
        case when SLOC_before <= 312.5 then
           return 0.1875 # (3.0 out of 16.0)
        else  # if SLOC_before > 312.5
           return 0.0 # (0.0 out of 35.0)
        end       end     else  # if avg_coupling_code_size_cut_diff > -1.5444444417953491
      case when N2_diff <= -34.5 then
         return 0.07407407407407407 # (2.0 out of 27.0)
      else  # if N2_diff > -34.5
        case when Comments_before <= 23.5 then
          case when one_file_fix_rate_diff <= -0.1145833358168602 then
             return 0.9565217391304348 # (22.0 out of 23.0)
          else  # if one_file_fix_rate_diff > -0.1145833358168602
            case when McCabe_max_diff <= -2.5 then
               return 0.25 # (4.0 out of 16.0)
            else  # if McCabe_max_diff > -2.5
              case when Comments_after <= 18.0 then
                case when Comments_before <= 4.5 then
                   return 0.8 # (16.0 out of 20.0)
                else  # if Comments_before > 4.5
                  case when McCabe_max_after <= 11.5 then
                     return 0.4117647058823529 # (7.0 out of 17.0)
                  else  # if McCabe_max_after > 11.5
                     return 0.6923076923076923 # (9.0 out of 13.0)
                  end                 end               else  # if Comments_after > 18.0
                 return 0.9333333333333333 # (14.0 out of 15.0)
              end             end           end         else  # if Comments_before > 23.5
          case when SLOC_before <= 646.5 then
            case when McCabe_max_diff <= -3.5 then
               return 0.6666666666666666 # (12.0 out of 18.0)
            else  # if McCabe_max_diff > -3.5
              case when changed_lines <= 107.5 then
                case when Single comments_after <= 54.5 then
                  case when LOC_diff <= -5.5 then
                     return 0.5294117647058824 # (9.0 out of 17.0)
                  else  # if LOC_diff > -5.5
                    case when removed_lines <= 9.5 then
                       return 0.05263157894736842 # (1.0 out of 19.0)
                    else  # if removed_lines > 9.5
                       return 0.3333333333333333 # (5.0 out of 15.0)
                    end                   end                 else  # if Single comments_after > 54.5
                  case when added_lines <= 17.5 then
                     return 0.1 # (2.0 out of 20.0)
                  else  # if added_lines > 17.5
                     return 0.038461538461538464 # (1.0 out of 26.0)
                  end                 end               else  # if changed_lines > 107.5
                 return 0.64 # (16.0 out of 25.0)
              end             end           else  # if SLOC_before > 646.5
            case when high_ccp_group <= 0.5 then
              case when McCabe_sum_before <= 413.0 then
                case when removed_lines <= 19.5 then
                  case when length_diff <= -1.5 then
                     return 0.14285714285714285 # (2.0 out of 14.0)
                  else  # if length_diff > -1.5
                     return 0.4090909090909091 # (9.0 out of 22.0)
                  end                 else  # if removed_lines > 19.5
                  case when McCabe_max_before <= 20.5 then
                     return 0.5294117647058824 # (18.0 out of 34.0)
                  else  # if McCabe_max_before > 20.5
                     return 0.8333333333333334 # (20.0 out of 24.0)
                  end                 end               else  # if McCabe_sum_before > 413.0
                 return 0.21428571428571427 # (6.0 out of 28.0)
              end             else  # if high_ccp_group > 0.5
              case when refactor_mle_diff <= -0.0437841285020113 then
                 return 0.5333333333333333 # (8.0 out of 15.0)
              else  # if refactor_mle_diff > -0.0437841285020113
                 return 0.9444444444444444 # (34.0 out of 36.0)
              end             end           end         end       end     end   end )