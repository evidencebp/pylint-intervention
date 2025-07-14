create or replace function RandomForest_4 (effort_diff int64, too-many-nested-blocks int64, Single comments_diff int64, N1_diff int64, avg_coupling_code_size_cut_diff int64, Simplify-boolean-expression int64, try-except-raise int64, h1_diff int64, added_functions int64, too-many-boolean-expressions int64, LLOC_diff int64, cur_count_x int64, wildcard-import int64, mostly_delete int64, LOC_diff int64, difficulty_diff int64, Comments_before int64, prev_count_y int64, time_diff int64, pointless-statement int64, vocabulary_diff int64, modified_McCabe_max_diff int64, prev_count int64, McCabe_sum_before int64, McCabe_max_after int64, Blank_diff int64, using-constant-test int64, McCabe_max_before int64, is_refactor int64, Comments_after int64, SLOC_before int64, superfluous-parens int64, too-many-branches int64, massive_change int64, comparison-of-constants int64, broad-exception-caught int64, Blank_before int64, N2_diff int64, McCabe_sum_after int64, too-many-statements int64, refactor_mle_diff int64, LOC_before int64, simplifiable-if-statement int64, only_removal int64, h2_diff int64, unnecessary-semicolon int64, too-many-lines int64, LLOC_before int64, volume_diff int64, too-many-return-statements int64, high_ccp_group int64, Single comments_before int64, simplifiable-if-expression int64, changed_lines int64, Multi_diff int64, one_file_fix_rate_diff int64, prev_count_x int64, simplifiable-condition int64, cur_count_y int64, calculated_length_diff int64, SLOC_diff int64, line-too-long int64, McCabe_max_diff int64, Comments_diff int64, cur_count int64, Single comments_after int64, removed_lines int64, added_lines int64, length_diff int64, unnecessary-pass int64, hunks_num int64, bugs_diff int64, same_day_duration_avg_diff int64, McCabe_sum_diff int64) as (
  case when McCabe_sum_before <= 37.5 then
    case when SLOC_diff <= 3.5 then
      case when removed_lines <= 8.5 then
         return 0.36363636363636365 # (8.0 out of 22.0)
      else  # if removed_lines > 8.5
         return 0.7586206896551724 # (22.0 out of 29.0)
      end     else  # if SLOC_diff > 3.5
       return 0.9230769230769231 # (24.0 out of 26.0)
    end   else  # if McCabe_sum_before > 37.5
    case when Single comments_after <= 360.0 then
      case when Single comments_diff <= 0.5 then
        case when refactor_mle_diff <= -0.35198332369327545 then
          case when SLOC_diff <= -42.5 then
             return 0.9473684210526315 # (18.0 out of 19.0)
          else  # if SLOC_diff > -42.5
             return 0.4666666666666667 # (7.0 out of 15.0)
          end         else  # if refactor_mle_diff > -0.35198332369327545
          case when same_day_duration_avg_diff <= 259.05555725097656 then
            case when removed_lines <= 60.0 then
              case when same_day_duration_avg_diff <= -46.52602767944336 then
                case when Blank_before <= 125.0 then
                  case when Comments_after <= 24.5 then
                     return 0.9375 # (15.0 out of 16.0)
                  else  # if Comments_after > 24.5
                    case when refactor_mle_diff <= -0.05267777852714062 then
                       return 0.2857142857142857 # (6.0 out of 21.0)
                    else  # if refactor_mle_diff > -0.05267777852714062
                       return 0.0 # (0.0 out of 15.0)
                    end                   end                 else  # if Blank_before > 125.0
                  case when Multi_diff <= -1.0 then
                     return 0.0 # (0.0 out of 24.0)
                  else  # if Multi_diff > -1.0
                     return 0.16666666666666666 # (4.0 out of 24.0)
                  end                 end               else  # if same_day_duration_avg_diff > -46.52602767944336
                case when h2_diff <= 1.5 then
                  case when Blank_before <= 85.5 then
                    case when McCabe_sum_diff <= -8.5 then
                       return 0.125 # (2.0 out of 16.0)
                    else  # if McCabe_sum_diff > -8.5
                       return 0.48148148148148145 # (13.0 out of 27.0)
                    end                   else  # if Blank_before > 85.5
                    case when N1_diff <= -1.5 then
                      case when LOC_diff <= -142.5 then
                         return 0.7142857142857143 # (15.0 out of 21.0)
                      else  # if LOC_diff > -142.5
                         return 0.30434782608695654 # (7.0 out of 23.0)
                      end                     else  # if N1_diff > -1.5
                      case when LLOC_before <= 405.0 then
                         return 0.9545454545454546 # (21.0 out of 22.0)
                      else  # if LLOC_before > 405.0
                         return 0.6 # (24.0 out of 40.0)
                      end                     end                   end                 else  # if h2_diff > 1.5
                   return 0.17857142857142858 # (5.0 out of 28.0)
                end               end             else  # if removed_lines > 60.0
              case when massive_change <= 0.5 then
                 return 0.9523809523809523 # (20.0 out of 21.0)
              else  # if massive_change > 0.5
                case when Comments_after <= 77.5 then
                   return 0.6296296296296297 # (17.0 out of 27.0)
                else  # if Comments_after > 77.5
                   return 0.2727272727272727 # (6.0 out of 22.0)
                end               end             end           else  # if same_day_duration_avg_diff > 259.05555725097656
             return 0.0 # (0.0 out of 18.0)
          end         end       else  # if Single comments_diff > 0.5
        case when LOC_before <= 1729.0 then
          case when Comments_before <= 48.5 then
            case when LLOC_diff <= 2.5 then
               return 0.35714285714285715 # (5.0 out of 14.0)
            else  # if LLOC_diff > 2.5
               return 0.1 # (2.0 out of 20.0)
            end           else  # if Comments_before > 48.5
            case when Single comments_after <= 71.5 then
               return 0.05555555555555555 # (1.0 out of 18.0)
            else  # if Single comments_after > 71.5
               return 0.0 # (0.0 out of 15.0)
            end           end         else  # if LOC_before > 1729.0
           return 0.42857142857142855 # (6.0 out of 14.0)
        end       end     else  # if Single comments_after > 360.0
      case when McCabe_sum_before <= 377.0 then
         return 0.875 # (21.0 out of 24.0)
      else  # if McCabe_sum_before > 377.0
         return 0.5789473684210527 # (11.0 out of 19.0)
      end     end   end )