create or replace function RandomForest_2 (h1_diff int64, simplifiable-if-statement int64, McCabe_max_after int64, McCabe_sum_before int64, Single comments_before int64, low_McCabe_max_diff int64, high_ccp_group int64, pointless-statement int64, too-many-branches int64, high_McCabe_max_before int64, superfluous-parens int64, Multi_diff int64, wildcard-import int64, high_McCabe_sum_before int64, LLOC_before int64, cur_count int64, unnecessary-semicolon int64, Comments_after int64, mostly_delete int64, simplifiable-condition int64, avg_coupling_code_size_cut_diff int64, added_functions int64, McCabe_max_diff int64, McCabe_sum_diff int64, LLOC_diff int64, LOC_before int64, Comments_diff int64, prev_count_x int64, effort_diff int64, try-except-raise int64, difficulty_diff int64, line-too-long int64, Simplify-boolean-expression int64, SLOC_diff int64, McCabe_sum_after int64, refactor_mle_diff int64, one_file_fix_rate_diff int64, is_refactor int64, too-many-lines int64, too-many-boolean-expressions int64, Single comments_diff int64, low_McCabe_sum_diff int64, cur_count_y int64, comparison-of-constants int64, Comments_before int64, too-many-return-statements int64, vocabulary_diff int64, massive_change int64, hunks_num int64, modified_McCabe_max_diff int64, high_McCabe_sum_diff int64, N2_diff int64, broad-exception-caught int64, length_diff int64, unnecessary-pass int64, time_diff int64, changed_lines int64, Single comments_after int64, h2_diff int64, low_McCabe_sum_before int64, cur_count_x int64, McCabe_max_before int64, using-constant-test int64, added_lines int64, same_day_duration_avg_diff int64, prev_count_y int64, Blank_diff int64, LOC_diff int64, only_removal int64, low_McCabe_max_before int64, bugs_diff int64, too-many-statements int64, simplifiable-if-expression int64, calculated_length_diff int64, volume_diff int64, Blank_before int64, high_McCabe_max_diff int64, SLOC_before int64, too-many-nested-blocks int64, removed_lines int64, low_ccp_group int64, N1_diff int64, prev_count int64) as (
  case when LOC_before <= 1216.5 then
    case when low_ccp_group <= 0.5 then
      case when Single comments_before <= 23.5 then
        case when McCabe_sum_after <= 175.5 then
          case when McCabe_sum_after <= 11.5 then
             return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
          else  # if McCabe_sum_after > 11.5
            case when low_McCabe_max_before <= 0.5 then
              case when McCabe_sum_after <= 110.0 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if McCabe_sum_after > 110.0
                 return 0.8888888888888888 # (0.8888888888888888 out of 1.0)
              end             else  # if low_McCabe_max_before > 0.5
              case when avg_coupling_code_size_cut_diff <= 0.06666667014360428 then
                 return 0.6428571428571429 # (0.6428571428571429 out of 1.0)
              else  # if avg_coupling_code_size_cut_diff > 0.06666667014360428
                 return 0.9333333333333333 # (0.9333333333333333 out of 1.0)
              end             end           end         else  # if McCabe_sum_after > 175.5
           return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
        end       else  # if Single comments_before > 23.5
        case when removed_lines <= 139.5 then
          case when McCabe_sum_after <= 59.0 then
            case when Single comments_diff <= -1.0 then
               return 1.0 # (1.0 out of 1.0)
            else  # if Single comments_diff > -1.0
               return 0.42857142857142855 # (0.42857142857142855 out of 1.0)
            end           else  # if McCabe_sum_after > 59.0
            case when Single comments_diff <= -2.5 then
              case when high_ccp_group <= 0.5 then
                 return 0.47368421052631576 # (0.47368421052631576 out of 1.0)
              else  # if high_ccp_group > 0.5
                 return 0.9 # (0.9 out of 1.0)
              end             else  # if Single comments_diff > -2.5
              case when LLOC_diff <= -11.5 then
                 return 0.1111111111111111 # (0.1111111111111111 out of 1.0)
              else  # if LLOC_diff > -11.5
                case when McCabe_sum_before <= 145.5 then
                  case when avg_coupling_code_size_cut_diff <= -0.041666667908430544 then
                     return 0.4666666666666667 # (0.4666666666666667 out of 1.0)
                  else  # if avg_coupling_code_size_cut_diff > -0.041666667908430544
                    case when hunks_num <= 3.5 then
                       return 0.125 # (0.125 out of 1.0)
                    else  # if hunks_num > 3.5
                       return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
                    end                   end                 else  # if McCabe_sum_before > 145.5
                   return 0.72 # (0.72 out of 1.0)
                end               end             end           end         else  # if removed_lines > 139.5
           return 0.2 # (0.2 out of 1.0)
        end       end     else  # if low_ccp_group > 0.5
      case when Single comments_after <= 449.5 then
        case when LLOC_diff <= -40.5 then
           return 0.5 # (0.5 out of 1.0)
        else  # if LLOC_diff > -40.5
          case when added_lines <= 7.5 then
             return 0.3125 # (0.3125 out of 1.0)
          else  # if added_lines > 7.5
            case when McCabe_sum_before <= 81.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if McCabe_sum_before > 81.5
               return 0.043478260869565216 # (0.043478260869565216 out of 1.0)
            end           end         end       else  # if Single comments_after > 449.5
         return 1.0 # (1.0 out of 1.0)
      end     end   else  # if LOC_before > 1216.5
    case when high_ccp_group <= 0.5 then
      case when changed_lines <= 806.0 then
        case when superfluous-parens <= 0.5 then
          case when Multi_diff <= 0.5 then
            case when Single comments_before <= 96.5 then
               return 0.29411764705882354 # (0.29411764705882354 out of 1.0)
            else  # if Single comments_before > 96.5
              case when LOC_diff <= -2.5 then
                 return 0.14285714285714285 # (0.14285714285714285 out of 1.0)
              else  # if LOC_diff > -2.5
                 return 0.0 # (0.0 out of 1.0)
              end             end           else  # if Multi_diff > 0.5
             return 0.2857142857142857 # (0.2857142857142857 out of 1.0)
          end         else  # if superfluous-parens > 0.5
          case when McCabe_sum_before <= 359.5 then
             return 0.1875 # (0.1875 out of 1.0)
          else  # if McCabe_sum_before > 359.5
             return 0.5294117647058824 # (0.5294117647058824 out of 1.0)
          end         end       else  # if changed_lines > 806.0
         return 0.5909090909090909 # (0.5909090909090909 out of 1.0)
      end     else  # if high_ccp_group > 0.5
      case when Blank_before <= 329.5 then
         return 0.8666666666666667 # (0.8666666666666667 out of 1.0)
      else  # if Blank_before > 329.5
         return 0.35294117647058826 # (0.35294117647058826 out of 1.0)
      end     end   end )