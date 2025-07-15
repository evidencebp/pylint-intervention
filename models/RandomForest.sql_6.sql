create or replace function RandomForest_6 (using-constant-test int64, simplifiable-if-statement int64, Comments_after int64, same_day_duration_avg_diff int64, Single comments_before int64, one_file_fix_rate_diff int64, too-many-boolean-expressions int64, Single comments_diff int64, high_McCabe_sum_before int64, pointless-statement int64, bugs_diff int64, McCabe_max_before int64, length_diff int64, LOC_diff int64, N2_diff int64, superfluous-parens int64, too-many-nested-blocks int64, effort_diff int64, cur_count_x int64, high_McCabe_max_before int64, comparison-of-constants int64, SLOC_diff int64, hunks_num int64, high_McCabe_max_diff int64, prev_count int64, McCabe_sum_after int64, cur_count_y int64, refactor_mle_diff int64, too-many-return-statements int64, too-many-statements int64, too-many-lines int64, only_removal int64, removed_lines int64, cur_count int64, volume_diff int64, is_refactor int64, prev_count_y int64, calculated_length_diff int64, Simplify-boolean-expression int64, h1_diff int64, McCabe_max_diff int64, wildcard-import int64, McCabe_sum_before int64, line-too-long int64, N1_diff int64, too-many-branches int64, h2_diff int64, McCabe_max_after int64, unnecessary-pass int64, avg_coupling_code_size_cut_diff int64, high_ccp_group int64, vocabulary_diff int64, try-except-raise int64, broad-exception-caught int64, simplifiable-condition int64, LLOC_before int64, added_functions int64, LLOC_diff int64, difficulty_diff int64, McCabe_sum_diff int64, Multi_diff int64, massive_change int64, mostly_delete int64, Comments_before int64, changed_lines int64, Comments_diff int64, time_diff int64, Blank_before int64, high_McCabe_sum_diff int64, added_lines int64, prev_count_x int64, unnecessary-semicolon int64, Blank_diff int64, modified_McCabe_max_diff int64, Single comments_after int64, LOC_before int64, simplifiable-if-expression int64, SLOC_before int64) as (
  case when McCabe_max_after <= 7.5 then
    case when high_ccp_group <= 0.5 then
      case when changed_lines <= 121.5 then
        case when LOC_before <= 188.5 then
           return 0.5238095238095238 # (11.0 out of 21.0)
        else  # if LOC_before > 188.5
          case when changed_lines <= 16.0 then
             return 0.06666666666666667 # (1.0 out of 15.0)
          else  # if changed_lines > 16.0
             return 0.42857142857142855 # (9.0 out of 21.0)
          end         end       else  # if changed_lines > 121.5
        case when N2_diff <= -9.0 then
           return 1.0 # (21.0 out of 21.0)
        else  # if N2_diff > -9.0
           return 0.9285714285714286 # (13.0 out of 14.0)
        end       end     else  # if high_ccp_group > 0.5
       return 0.92 # (23.0 out of 25.0)
    end   else  # if McCabe_max_after > 7.5
    case when broad-exception-caught <= 0.5 then
      case when LOC_before <= 1051.5 then
        case when Comments_diff <= 3.5 then
          case when length_diff <= -25.5 then
            case when SLOC_diff <= -31.0 then
               return 0.0 # (0.0 out of 21.0)
            else  # if SLOC_diff > -31.0
               return 0.16666666666666666 # (2.0 out of 12.0)
            end           else  # if length_diff > -25.5
            case when added_lines <= 6.5 then
              case when added_lines <= 1.5 then
                case when McCabe_sum_after <= 103.0 then
                   return 0.4666666666666667 # (7.0 out of 15.0)
                else  # if McCabe_sum_after > 103.0
                   return 0.42105263157894735 # (8.0 out of 19.0)
                end               else  # if added_lines > 1.5
                 return 0.11538461538461539 # (3.0 out of 26.0)
              end             else  # if added_lines > 6.5
              case when massive_change <= 0.5 then
                case when changed_lines <= 19.5 then
                   return 0.9333333333333333 # (14.0 out of 15.0)
                else  # if changed_lines > 19.5
                  case when McCabe_sum_diff <= -8.5 then
                     return 0.3333333333333333 # (8.0 out of 24.0)
                  else  # if McCabe_sum_diff > -8.5
                    case when SLOC_before <= 594.0 then
                      case when LOC_before <= 587.5 then
                        case when McCabe_max_before <= 17.5 then
                           return 0.3333333333333333 # (10.0 out of 30.0)
                        else  # if McCabe_max_before > 17.5
                           return 0.7368421052631579 # (14.0 out of 19.0)
                        end                       else  # if LOC_before > 587.5
                         return 0.9090909090909091 # (30.0 out of 33.0)
                      end                     else  # if SLOC_before > 594.0
                       return 0.42857142857142855 # (6.0 out of 14.0)
                    end                   end                 end               else  # if massive_change > 0.5
                 return 0.25 # (4.0 out of 16.0)
              end             end           end         else  # if Comments_diff > 3.5
           return 0.15789473684210525 # (3.0 out of 19.0)
        end       else  # if LOC_before > 1051.5
        case when added_lines <= 6.5 then
          case when refactor_mle_diff <= -0.057648733258247375 then
             return 0.5714285714285714 # (12.0 out of 21.0)
          else  # if refactor_mle_diff > -0.057648733258247375
            case when changed_lines <= 5.5 then
               return 0.7857142857142857 # (11.0 out of 14.0)
            else  # if changed_lines > 5.5
               return 0.9473684210526315 # (18.0 out of 19.0)
            end           end         else  # if added_lines > 6.5
          case when length_diff <= -8.5 then
            case when Multi_diff <= -1.0 then
               return 0.8888888888888888 # (16.0 out of 18.0)
            else  # if Multi_diff > -1.0
              case when Blank_before <= 279.0 then
                 return 0.3333333333333333 # (4.0 out of 12.0)
              else  # if Blank_before > 279.0
                 return 0.7857142857142857 # (22.0 out of 28.0)
              end             end           else  # if length_diff > -8.5
            case when Comments_before <= 52.5 then
               return 0.7619047619047619 # (16.0 out of 21.0)
            else  # if Comments_before > 52.5
              case when Comments_diff <= 1.5 then
                case when LOC_before <= 2445.0 then
                   return 0.13333333333333333 # (2.0 out of 15.0)
                else  # if LOC_before > 2445.0
                   return 0.7857142857142857 # (11.0 out of 14.0)
                end               else  # if Comments_diff > 1.5
                 return 0.037037037037037035 # (1.0 out of 27.0)
              end             end           end         end       end     else  # if broad-exception-caught > 0.5
      case when McCabe_sum_before <= 222.5 then
         return 0.0 # (0.0 out of 18.0)
      else  # if McCabe_sum_before > 222.5
         return 0.3076923076923077 # (4.0 out of 13.0)
      end     end   end )