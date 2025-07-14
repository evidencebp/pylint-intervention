create or replace function RandomForest_7 (SLOC_before int64, simplifiable-condition int64, bugs_diff int64, Blank_before int64, LLOC_diff int64, try-except-raise int64, LLOC_before int64, changed_lines int64, h2_diff int64, prev_count_x int64, too-many-lines int64, cur_count_y int64, Comments_before int64, McCabe_sum_after int64, cur_count_x int64, vocabulary_diff int64, Single comments_before int64, N2_diff int64, high_ccp_group int64, massive_change int64, added_lines int64, prev_count int64, refactor_mle_diff int64, superfluous-parens int64, avg_coupling_code_size_cut_diff int64, McCabe_sum_diff int64, LOC_before int64, too-many-return-statements int64, too-many-branches int64, too-many-nested-blocks int64, difficulty_diff int64, time_diff int64, Single comments_after int64, calculated_length_diff int64, Simplify-boolean-expression int64, unnecessary-semicolon int64, mostly_delete int64, effort_diff int64, Multi_diff int64, McCabe_max_diff int64, is_refactor int64, only_removal int64, LOC_diff int64, one_file_fix_rate_diff int64, Comments_after int64, comparison-of-constants int64, McCabe_max_after int64, length_diff int64, simplifiable-if-statement int64, removed_lines int64, unnecessary-pass int64, Comments_diff int64, cur_count int64, same_day_duration_avg_diff int64, hunks_num int64, N1_diff int64, line-too-long int64, volume_diff int64, using-constant-test int64, too-many-boolean-expressions int64, modified_McCabe_max_diff int64, h1_diff int64, added_functions int64, SLOC_diff int64, too-many-statements int64, pointless-statement int64, wildcard-import int64, McCabe_max_before int64, prev_count_y int64, broad-exception-caught int64, Blank_diff int64, McCabe_sum_before int64, simplifiable-if-expression int64, Single comments_diff int64) as (
  case when LOC_before <= 295.5 then
    case when McCabe_sum_after <= 16.5 then
      case when hunks_num <= 1.5 then
         return 1.0 # (25.0 out of 25.0)
      else  # if hunks_num > 1.5
         return 0.7333333333333333 # (22.0 out of 30.0)
      end     else  # if McCabe_sum_after > 16.5
      case when McCabe_max_after <= 10.5 then
         return 0.2727272727272727 # (6.0 out of 22.0)
      else  # if McCabe_max_after > 10.5
         return 0.6818181818181818 # (15.0 out of 22.0)
      end     end   else  # if LOC_before > 295.5
    case when h1_diff <= -1.5 then
      case when Multi_diff <= -3.0 then
        case when same_day_duration_avg_diff <= 12.64197301864624 then
           return 0.75 # (9.0 out of 12.0)
        else  # if same_day_duration_avg_diff > 12.64197301864624
           return 0.9333333333333333 # (14.0 out of 15.0)
        end       else  # if Multi_diff > -3.0
         return 0.2857142857142857 # (4.0 out of 14.0)
      end     else  # if h1_diff > -1.5
      case when McCabe_sum_diff <= -7.5 then
        case when changed_lines <= 117.5 then
          case when Comments_after <= 55.5 then
            case when SLOC_before <= 677.5 then
               return 0.0625 # (1.0 out of 16.0)
            else  # if SLOC_before > 677.5
               return 0.0 # (0.0 out of 22.0)
            end           else  # if Comments_after > 55.5
             return 0.2727272727272727 # (6.0 out of 22.0)
          end         else  # if changed_lines > 117.5
          case when Blank_diff <= -30.5 then
             return 0.20833333333333334 # (5.0 out of 24.0)
          else  # if Blank_diff > -30.5
            case when changed_lines <= 247.0 then
               return 0.8 # (12.0 out of 15.0)
            else  # if changed_lines > 247.0
               return 0.26666666666666666 # (4.0 out of 15.0)
            end           end         end       else  # if McCabe_sum_diff > -7.5
        case when McCabe_sum_after <= 26.5 then
           return 0.08 # (2.0 out of 25.0)
        else  # if McCabe_sum_after > 26.5
          case when Single comments_after <= 187.0 then
            case when Comments_after <= 53.5 then
              case when Comments_before <= 38.5 then
                case when Comments_diff <= -0.5 then
                   return 0.1875 # (3.0 out of 16.0)
                else  # if Comments_diff > -0.5
                  case when McCabe_sum_before <= 174.0 then
                    case when added_functions <= 0.5 then
                      case when added_lines <= 7.0 then
                         return 0.4230769230769231 # (11.0 out of 26.0)
                      else  # if added_lines > 7.0
                        case when LLOC_before <= 241.5 then
                           return 0.9230769230769231 # (12.0 out of 13.0)
                        else  # if LLOC_before > 241.5
                           return 0.75 # (15.0 out of 20.0)
                        end                       end                     else  # if added_functions > 0.5
                       return 0.3225806451612903 # (10.0 out of 31.0)
                    end                   else  # if McCabe_sum_before > 174.0
                     return 0.21428571428571427 # (3.0 out of 14.0)
                  end                 end               else  # if Comments_before > 38.5
                case when SLOC_diff <= -2.5 then
                   return 1.0 # (18.0 out of 18.0)
                else  # if SLOC_diff > -2.5
                   return 0.6153846153846154 # (8.0 out of 13.0)
                end               end             else  # if Comments_after > 53.5
              case when Comments_diff <= -0.5 then
                 return 0.5454545454545454 # (12.0 out of 22.0)
              else  # if Comments_diff > -0.5
                case when SLOC_diff <= 0.5 then
                  case when SLOC_before <= 654.0 then
                     return 0.0 # (0.0 out of 15.0)
                  else  # if SLOC_before > 654.0
                     return 0.44 # (11.0 out of 25.0)
                  end                 else  # if SLOC_diff > 0.5
                  case when Single comments_before <= 99.5 then
                     return 0.2857142857142857 # (6.0 out of 21.0)
                  else  # if Single comments_before > 99.5
                     return 0.0 # (0.0 out of 28.0)
                  end                 end               end             end           else  # if Single comments_after > 187.0
            case when added_functions <= 0.5 then
               return 0.48484848484848486 # (16.0 out of 33.0)
            else  # if added_functions > 0.5
               return 0.9230769230769231 # (24.0 out of 26.0)
            end           end         end       end     end   end )