create or replace function RandomForest_8 (SLOC_before int64, simplifiable-condition int64, bugs_diff int64, Blank_before int64, LLOC_diff int64, try-except-raise int64, LLOC_before int64, changed_lines int64, h2_diff int64, prev_count_x int64, too-many-lines int64, cur_count_y int64, Comments_before int64, McCabe_sum_after int64, cur_count_x int64, vocabulary_diff int64, Single comments_before int64, N2_diff int64, high_ccp_group int64, massive_change int64, added_lines int64, prev_count int64, refactor_mle_diff int64, superfluous-parens int64, avg_coupling_code_size_cut_diff int64, McCabe_sum_diff int64, LOC_before int64, too-many-return-statements int64, too-many-branches int64, too-many-nested-blocks int64, difficulty_diff int64, time_diff int64, Single comments_after int64, calculated_length_diff int64, Simplify-boolean-expression int64, unnecessary-semicolon int64, mostly_delete int64, effort_diff int64, Multi_diff int64, McCabe_max_diff int64, is_refactor int64, only_removal int64, LOC_diff int64, one_file_fix_rate_diff int64, Comments_after int64, comparison-of-constants int64, McCabe_max_after int64, length_diff int64, simplifiable-if-statement int64, removed_lines int64, unnecessary-pass int64, Comments_diff int64, cur_count int64, same_day_duration_avg_diff int64, hunks_num int64, N1_diff int64, line-too-long int64, volume_diff int64, using-constant-test int64, too-many-boolean-expressions int64, modified_McCabe_max_diff int64, h1_diff int64, added_functions int64, SLOC_diff int64, too-many-statements int64, pointless-statement int64, wildcard-import int64, McCabe_max_before int64, prev_count_y int64, broad-exception-caught int64, Blank_diff int64, McCabe_sum_before int64, simplifiable-if-expression int64, Single comments_diff int64) as (
  case when Comments_before <= 3.5 then
    case when McCabe_sum_after <= 17.5 then
       return 1.0 # (32.0 out of 32.0)
    else  # if McCabe_sum_after > 17.5
       return 0.9285714285714286 # (13.0 out of 14.0)
    end   else  # if Comments_before > 3.5
    case when high_ccp_group <= 0.5 then
      case when length_diff <= -228.5 then
         return 0.75 # (18.0 out of 24.0)
      else  # if length_diff > -228.5
        case when LOC_before <= 1251.0 then
          case when McCabe_max_before <= 18.5 then
            case when Single comments_after <= 96.5 then
              case when hunks_num <= 8.5 then
                case when Single comments_diff <= -2.5 then
                   return 0.7142857142857143 # (10.0 out of 14.0)
                else  # if Single comments_diff > -2.5
                  case when avg_coupling_code_size_cut_diff <= -1.3311931490898132 then
                     return 0.047619047619047616 # (1.0 out of 21.0)
                  else  # if avg_coupling_code_size_cut_diff > -1.3311931490898132
                    case when Blank_diff <= -6.5 then
                       return 0.07692307692307693 # (1.0 out of 13.0)
                    else  # if Blank_diff > -6.5
                      case when Comments_after <= 25.0 then
                        case when Comments_after <= 12.5 then
                           return 0.5 # (8.0 out of 16.0)
                        else  # if Comments_after > 12.5
                           return 0.7647058823529411 # (13.0 out of 17.0)
                        end                       else  # if Comments_after > 25.0
                        case when McCabe_sum_diff <= -0.5 then
                           return 0.4375 # (7.0 out of 16.0)
                        else  # if McCabe_sum_diff > -0.5
                           return 0.09523809523809523 # (2.0 out of 21.0)
                        end                       end                     end                   end                 end               else  # if hunks_num > 8.5
                case when added_functions <= 0.5 then
                   return 0.47058823529411764 # (8.0 out of 17.0)
                else  # if added_functions > 0.5
                   return 0.7857142857142857 # (11.0 out of 14.0)
                end               end             else  # if Single comments_after > 96.5
               return 0.8421052631578947 # (16.0 out of 19.0)
            end           else  # if McCabe_max_before > 18.5
            case when h2_diff <= -15.5 then
              case when McCabe_sum_after <= 137.0 then
                 return 0.0 # (0.0 out of 24.0)
              else  # if McCabe_sum_after > 137.0
                 return 0.125 # (2.0 out of 16.0)
              end             else  # if h2_diff > -15.5
              case when Comments_after <= 62.0 then
                case when McCabe_sum_diff <= 0.5 then
                  case when LLOC_diff <= -0.5 then
                     return 0.8333333333333334 # (15.0 out of 18.0)
                  else  # if LLOC_diff > -0.5
                     return 0.3684210526315789 # (7.0 out of 19.0)
                  end                 else  # if McCabe_sum_diff > 0.5
                   return 0.15384615384615385 # (2.0 out of 13.0)
                end               else  # if Comments_after > 62.0
                 return 0.16666666666666666 # (4.0 out of 24.0)
              end             end           end         else  # if LOC_before > 1251.0
          case when Blank_before <= 310.5 then
            case when LOC_before <= 1671.0 then
              case when LLOC_diff <= -5.0 then
                 return 0.15384615384615385 # (2.0 out of 13.0)
              else  # if LLOC_diff > -5.0
                 return 0.02857142857142857 # (1.0 out of 35.0)
              end             else  # if LOC_before > 1671.0
               return 0.25806451612903225 # (8.0 out of 31.0)
            end           else  # if Blank_before > 310.5
            case when Single comments_after <= 262.5 then
               return 0.21739130434782608 # (5.0 out of 23.0)
            else  # if Single comments_after > 262.5
               return 0.5384615384615384 # (14.0 out of 26.0)
            end           end         end       end     else  # if high_ccp_group > 0.5
      case when Blank_before <= 76.0 then
         return 0.92 # (23.0 out of 25.0)
      else  # if Blank_before > 76.0
        case when LOC_before <= 722.5 then
           return 1.0 # (14.0 out of 14.0)
        else  # if LOC_before > 722.5
          case when removed_lines <= 4.5 then
            case when changed_lines <= 0.5 then
               return 0.5294117647058824 # (9.0 out of 17.0)
            else  # if changed_lines > 0.5
               return 0.6428571428571429 # (9.0 out of 14.0)
            end           else  # if removed_lines > 4.5
            case when avg_coupling_code_size_cut_diff <= 0.13333334028720856 then
              case when changed_lines <= 98.5 then
                 return 0.2 # (3.0 out of 15.0)
              else  # if changed_lines > 98.5
                 return 0.125 # (2.0 out of 16.0)
              end             else  # if avg_coupling_code_size_cut_diff > 0.13333334028720856
               return 0.5789473684210527 # (11.0 out of 19.0)
            end           end         end       end     end   end )