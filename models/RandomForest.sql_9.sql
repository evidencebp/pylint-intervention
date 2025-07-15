create or replace function RandomForest_9 (using-constant-test int64, simplifiable-if-statement int64, Comments_after int64, same_day_duration_avg_diff int64, Single comments_before int64, one_file_fix_rate_diff int64, too-many-boolean-expressions int64, Single comments_diff int64, high_McCabe_sum_before int64, pointless-statement int64, bugs_diff int64, McCabe_max_before int64, length_diff int64, LOC_diff int64, N2_diff int64, superfluous-parens int64, too-many-nested-blocks int64, effort_diff int64, cur_count_x int64, high_McCabe_max_before int64, comparison-of-constants int64, SLOC_diff int64, hunks_num int64, high_McCabe_max_diff int64, prev_count int64, McCabe_sum_after int64, cur_count_y int64, refactor_mle_diff int64, too-many-return-statements int64, too-many-statements int64, too-many-lines int64, only_removal int64, removed_lines int64, cur_count int64, volume_diff int64, is_refactor int64, prev_count_y int64, calculated_length_diff int64, Simplify-boolean-expression int64, h1_diff int64, McCabe_max_diff int64, wildcard-import int64, McCabe_sum_before int64, line-too-long int64, N1_diff int64, too-many-branches int64, h2_diff int64, McCabe_max_after int64, unnecessary-pass int64, avg_coupling_code_size_cut_diff int64, high_ccp_group int64, vocabulary_diff int64, try-except-raise int64, broad-exception-caught int64, simplifiable-condition int64, LLOC_before int64, added_functions int64, LLOC_diff int64, difficulty_diff int64, McCabe_sum_diff int64, Multi_diff int64, massive_change int64, mostly_delete int64, Comments_before int64, changed_lines int64, Comments_diff int64, time_diff int64, Blank_before int64, high_McCabe_sum_diff int64, added_lines int64, prev_count_x int64, unnecessary-semicolon int64, Blank_diff int64, modified_McCabe_max_diff int64, Single comments_after int64, LOC_before int64, simplifiable-if-expression int64, SLOC_before int64) as (
  case when same_day_duration_avg_diff <= 277.68055725097656 then
    case when h1_diff <= 0.5 then
      case when McCabe_max_before <= 6.5 then
        case when hunks_num <= 6.0 then
          case when avg_coupling_code_size_cut_diff <= -0.43809525668621063 then
             return 0.9333333333333333 # (14.0 out of 15.0)
          else  # if avg_coupling_code_size_cut_diff > -0.43809525668621063
             return 0.5185185185185185 # (14.0 out of 27.0)
          end         else  # if hunks_num > 6.0
           return 0.9411764705882353 # (16.0 out of 17.0)
        end       else  # if McCabe_max_before > 6.5
        case when McCabe_max_after <= 2.5 then
           return 0.07407407407407407 # (2.0 out of 27.0)
        else  # if McCabe_max_after > 2.5
          case when modified_McCabe_max_diff <= 0.5 then
            case when McCabe_sum_before <= 342.5 then
              case when changed_lines <= 138.5 then
                case when McCabe_max_before <= 23.5 then
                  case when Blank_before <= 43.5 then
                     return 0.07407407407407407 # (2.0 out of 27.0)
                  else  # if Blank_before > 43.5
                    case when length_diff <= -2.5 then
                      case when SLOC_diff <= -30.5 then
                         return 0.0 # (0.0 out of 28.0)
                      else  # if SLOC_diff > -30.5
                        case when McCabe_max_after <= 13.5 then
                           return 0.4 # (8.0 out of 20.0)
                        else  # if McCabe_max_after > 13.5
                           return 0.045454545454545456 # (1.0 out of 22.0)
                        end                       end                     else  # if length_diff > -2.5
                      case when modified_McCabe_max_diff <= -0.5 then
                         return 0.5909090909090909 # (13.0 out of 22.0)
                      else  # if modified_McCabe_max_diff > -0.5
                        case when LOC_before <= 645.0 then
                           return 0.11538461538461539 # (3.0 out of 26.0)
                        else  # if LOC_before > 645.0
                           return 0.72 # (18.0 out of 25.0)
                        end                       end                     end                   end                 else  # if McCabe_max_before > 23.5
                  case when Blank_diff <= 0.5 then
                    case when LOC_diff <= -14.5 then
                       return 0.3684210526315789 # (7.0 out of 19.0)
                    else  # if LOC_diff > -14.5
                      case when SLOC_before <= 722.5 then
                         return 0.8421052631578947 # (16.0 out of 19.0)
                      else  # if SLOC_before > 722.5
                         return 0.6086956521739131 # (14.0 out of 23.0)
                      end                     end                   else  # if Blank_diff > 0.5
                     return 0.3333333333333333 # (6.0 out of 18.0)
                  end                 end               else  # if changed_lines > 138.5
                case when McCabe_max_after <= 7.5 then
                   return 1.0 # (20.0 out of 20.0)
                else  # if McCabe_max_after > 7.5
                  case when Single comments_after <= 69.5 then
                    case when McCabe_sum_before <= 106.0 then
                       return 0.42857142857142855 # (6.0 out of 14.0)
                    else  # if McCabe_sum_before > 106.0
                      case when h2_diff <= -17.0 then
                         return 0.6428571428571429 # (9.0 out of 14.0)
                      else  # if h2_diff > -17.0
                         return 0.9333333333333333 # (14.0 out of 15.0)
                      end                     end                   else  # if Single comments_after > 69.5
                     return 0.375 # (12.0 out of 32.0)
                  end                 end               end             else  # if McCabe_sum_before > 342.5
              case when hunks_num <= 3.5 then
                 return 0.65 # (13.0 out of 20.0)
              else  # if hunks_num > 3.5
                 return 0.8620689655172413 # (25.0 out of 29.0)
              end             end           else  # if modified_McCabe_max_diff > 0.5
            case when added_functions <= 0.5 then
              case when modified_McCabe_max_diff <= 1.5 then
                 return 0.16666666666666666 # (2.0 out of 12.0)
              else  # if modified_McCabe_max_diff > 1.5
                 return 0.05263157894736842 # (1.0 out of 19.0)
              end             else  # if added_functions > 0.5
               return 0.34615384615384615 # (9.0 out of 26.0)
            end           end         end       end     else  # if h1_diff > 0.5
      case when avg_coupling_code_size_cut_diff <= 0.34285715222358704 then
         return 0.8888888888888888 # (24.0 out of 27.0)
      else  # if avg_coupling_code_size_cut_diff > 0.34285715222358704
         return 0.47058823529411764 # (8.0 out of 17.0)
      end     end   else  # if same_day_duration_avg_diff > 277.68055725097656
     return 0.0 # (0.0 out of 20.0)
  end )