create or replace function RandomForest_7 (McCabe_sum_before int64, changed_lines int64, prev_count_y int64, mostly_delete int64, h1_diff int64, too-many-lines int64, low_McCabe_sum_before int64, length_diff int64, LOC_before int64, simplifiable-if-expression int64, added_functions int64, broad-exception-caught int64, simplifiable-condition int64, prev_count_x int64, McCabe_max_diff int64, SLOC_before int64, LLOC_before int64, low_McCabe_max_diff int64, bugs_diff int64, same_day_duration_avg_diff int64, cur_count_x int64, only_removal int64, McCabe_max_after int64, Single comments_after int64, low_ccp_group int64, one_file_fix_rate_diff int64, effort_diff int64, difficulty_diff int64, removed_lines int64, Comments_diff int64, too-many-boolean-expressions int64, refactor_mle_diff int64, high_McCabe_max_before int64, hunks_num int64, LOC_diff int64, SLOC_diff int64, cur_count_y int64, vocabulary_diff int64, using-constant-test int64, Simplify-boolean-expression int64, low_McCabe_max_before int64, high_McCabe_sum_diff int64, high_McCabe_sum_before int64, McCabe_max_before int64, Comments_after int64, McCabe_sum_diff int64, unnecessary-pass int64, avg_coupling_code_size_cut_diff int64, simplifiable-if-statement int64, is_refactor int64, volume_diff int64, added_lines int64, high_McCabe_max_diff int64, superfluous-parens int64, cur_count int64, low_McCabe_sum_diff int64, calculated_length_diff int64, Multi_diff int64, N2_diff int64, h2_diff int64, Single comments_before int64, McCabe_sum_after int64, N1_diff int64, too-many-statements int64, comparison-of-constants int64, pointless-statement int64, time_diff int64, prev_count int64, Single comments_diff int64, massive_change int64, Blank_diff int64, too-many-nested-blocks int64, Comments_before int64, modified_McCabe_max_diff int64, LLOC_diff int64, Blank_before int64, try-except-raise int64, too-many-branches int64, too-many-return-statements int64, unnecessary-semicolon int64, wildcard-import int64, high_ccp_group int64, line-too-long int64) as (
  case when Blank_before <= 28.5 then
    case when length_diff <= 1.0 then
      case when LLOC_diff <= -1.0 then
         return 0.35294117647058826 # (0.35294117647058826 out of 1.0)
      else  # if LLOC_diff > -1.0
         return 0.7727272727272727 # (0.7727272727272727 out of 1.0)
      end     else  # if length_diff > 1.0
       return 1.0 # (1.0 out of 1.0)
    end   else  # if Blank_before > 28.5
    case when low_ccp_group <= 0.5 then
      case when Blank_before <= 40.5 then
         return 0.8695652173913043 # (0.8695652173913043 out of 1.0)
      else  # if Blank_before > 40.5
        case when Comments_diff <= 7.5 then
          case when McCabe_max_after <= 42.0 then
            case when same_day_duration_avg_diff <= 5.724523305892944 then
              case when high_ccp_group <= 0.5 then
                case when SLOC_before <= 664.0 then
                  case when McCabe_max_after <= 15.5 then
                    case when LLOC_before <= 286.0 then
                       return 0.4117647058823529 # (0.4117647058823529 out of 1.0)
                    else  # if LLOC_before > 286.0
                       return 0.8928571428571429 # (0.8928571428571429 out of 1.0)
                    end                   else  # if McCabe_max_after > 15.5
                     return 0.41935483870967744 # (0.41935483870967744 out of 1.0)
                  end                 else  # if SLOC_before > 664.0
                  case when Blank_diff <= -4.5 then
                     return 0.6 # (0.6 out of 1.0)
                  else  # if Blank_diff > -4.5
                    case when avg_coupling_code_size_cut_diff <= -0.7291666567325592 then
                       return 0.25 # (0.25 out of 1.0)
                    else  # if avg_coupling_code_size_cut_diff > -0.7291666567325592
                       return 0.3157894736842105 # (0.3157894736842105 out of 1.0)
                    end                   end                 end               else  # if high_ccp_group > 0.5
                case when added_lines <= 189.0 then
                  case when length_diff <= -1.0 then
                     return 0.8947368421052632 # (0.8947368421052632 out of 1.0)
                  else  # if length_diff > -1.0
                     return 0.8823529411764706 # (0.8823529411764706 out of 1.0)
                  end                 else  # if added_lines > 189.0
                   return 0.4375 # (0.4375 out of 1.0)
                end               end             else  # if same_day_duration_avg_diff > 5.724523305892944
              case when N1_diff <= -26.5 then
                 return 0.6428571428571429 # (0.6428571428571429 out of 1.0)
              else  # if N1_diff > -26.5
                case when added_lines <= 55.0 then
                  case when LLOC_before <= 950.5 then
                    case when Single comments_before <= 33.5 then
                       return 0.19047619047619047 # (0.19047619047619047 out of 1.0)
                    else  # if Single comments_before > 33.5
                       return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
                    end                   else  # if LLOC_before > 950.5
                     return 0.0625 # (0.0625 out of 1.0)
                  end                 else  # if added_lines > 55.0
                  case when removed_lines <= 37.5 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if removed_lines > 37.5
                     return 0.25 # (0.25 out of 1.0)
                  end                 end               end             end           else  # if McCabe_max_after > 42.0
            case when LOC_diff <= 1.5 then
               return 0.7142857142857143 # (0.7142857142857143 out of 1.0)
            else  # if LOC_diff > 1.5
               return 0.9473684210526315 # (0.9473684210526315 out of 1.0)
            end           end         else  # if Comments_diff > 7.5
           return 0.09090909090909091 # (0.09090909090909091 out of 1.0)
        end       end     else  # if low_ccp_group > 0.5
      case when Comments_diff <= -3.5 then
         return 0.5333333333333333 # (0.5333333333333333 out of 1.0)
      else  # if Comments_diff > -3.5
        case when SLOC_diff <= 2.5 then
           return 0.0 # (0.0 out of 1.0)
        else  # if SLOC_diff > 2.5
          case when LLOC_diff <= 2.5 then
             return 0.0 # (0.0 out of 1.0)
          else  # if LLOC_diff > 2.5
             return 0.34615384615384615 # (0.34615384615384615 out of 1.0)
          end         end       end     end   end )