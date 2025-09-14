create or replace function RandomForest_4 (prev_count int64, prev_count_x int64, prev_count_y int64, using-constant-test int64, Comments_diff int64, massive_change int64, McCabe_max_after int64, Comments_before int64, too-many-statements int64, cur_count_x int64, h1_diff int64, McCabe_sum_diff int64, LLOC_before int64, McCabe_sum_before int64, high_McCabe_max_before int64, avg_coupling_code_size_cut_diff int64, is_refactor int64, N2_diff int64, too-many-branches int64, SLOC_before int64, too-many-nested-blocks int64, too-many-lines int64, bugs_diff int64, time_diff int64, Single comments_after int64, simplifiable-condition int64, Multi_diff int64, high_McCabe_sum_before int64, low_ccp_group int64, refactor_mle_diff int64, low_McCabe_max_diff int64, SLOC_diff int64, changed_lines int64, hunks_num int64, McCabe_sum_after int64, cur_count_y int64, one_file_fix_rate_diff int64, low_McCabe_sum_before int64, modified_McCabe_max_diff int64, superfluous-parens int64, mostly_delete int64, added_functions int64, Comments_after int64, N1_diff int64, McCabe_max_diff int64, simplifiable-if-statement int64, LOC_before int64, low_McCabe_max_before int64, McCabe_max_before int64, try-except-raise int64, line-too-long int64, unnecessary-semicolon int64, wildcard-import int64, difficulty_diff int64, Simplify-boolean-expression int64, cur_count int64, low_McCabe_sum_diff int64, pointless-statement int64, length_diff int64, broad-exception-caught int64, h2_diff int64, high_McCabe_sum_diff int64, only_removal int64, comparison-of-constants int64, Single comments_diff int64, too-many-boolean-expressions int64, Blank_before int64, calculated_length_diff int64, Single comments_before int64, removed_lines int64, simplifiable-if-expression int64, LOC_diff int64, volume_diff int64, high_McCabe_max_diff int64, high_ccp_group int64, same_day_duration_avg_diff int64, Blank_diff int64, effort_diff int64, too-many-return-statements int64, added_lines int64, unnecessary-pass int64, vocabulary_diff int64, LLOC_diff int64) as (
  case when Blank_before <= 29.0 then
    case when Comments_after <= 1.5 then
       return 1.0 # (1.0 out of 1.0)
    else  # if Comments_after > 1.5
      case when Single comments_before <= 20.0 then
         return 0.6176470588235294 # (0.6176470588235294 out of 1.0)
      else  # if Single comments_before > 20.0
         return 1.0 # (1.0 out of 1.0)
      end     end   else  # if Blank_before > 29.0
    case when one_file_fix_rate_diff <= 0.4848484843969345 then
      case when low_ccp_group <= 0.5 then
        case when refactor_mle_diff <= 0.638700932264328 then
          case when Blank_before <= 111.5 then
            case when refactor_mle_diff <= -0.07836071029305458 then
              case when Comments_after <= 32.0 then
                case when refactor_mle_diff <= -0.1580333337187767 then
                   return 0.16666666666666666 # (0.16666666666666666 out of 1.0)
                else  # if refactor_mle_diff > -0.1580333337187767
                   return 0.4375 # (0.4375 out of 1.0)
                end               else  # if Comments_after > 32.0
                 return 0.03225806451612903 # (0.03225806451612903 out of 1.0)
              end             else  # if refactor_mle_diff > -0.07836071029305458
              case when LLOC_diff <= -21.0 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if LLOC_diff > -21.0
                case when Blank_before <= 67.0 then
                   return 0.7 # (0.7 out of 1.0)
                else  # if Blank_before > 67.0
                   return 0.1724137931034483 # (0.1724137931034483 out of 1.0)
                end               end             end           else  # if Blank_before > 111.5
            case when same_day_duration_avg_diff <= -44.53354835510254 then
              case when high_McCabe_sum_before <= 0.5 then
                 return 0.5588235294117647 # (0.5588235294117647 out of 1.0)
              else  # if high_McCabe_sum_before > 0.5
                 return 0.13043478260869565 # (0.13043478260869565 out of 1.0)
              end             else  # if same_day_duration_avg_diff > -44.53354835510254
              case when refactor_mle_diff <= 0.017811306286603212 then
                case when Single comments_after <= 174.5 then
                  case when LLOC_before <= 536.0 then
                    case when LOC_diff <= -26.0 then
                       return 0.9444444444444444 # (0.9444444444444444 out of 1.0)
                    else  # if LOC_diff > -26.0
                       return 0.7222222222222222 # (0.7222222222222222 out of 1.0)
                    end                   else  # if LLOC_before > 536.0
                    case when Single comments_before <= 90.0 then
                       return 1.0 # (1.0 out of 1.0)
                    else  # if Single comments_before > 90.0
                       return 0.9444444444444444 # (0.9444444444444444 out of 1.0)
                    end                   end                 else  # if Single comments_after > 174.5
                   return 0.625 # (0.625 out of 1.0)
                end               else  # if refactor_mle_diff > 0.017811306286603212
                case when superfluous-parens <= 0.5 then
                  case when Comments_before <= 53.5 then
                     return 0.42857142857142855 # (0.42857142857142855 out of 1.0)
                  else  # if Comments_before > 53.5
                     return 0.18518518518518517 # (0.18518518518518517 out of 1.0)
                  end                 else  # if superfluous-parens > 0.5
                   return 0.95 # (0.95 out of 1.0)
                end               end             end           end         else  # if refactor_mle_diff > 0.638700932264328
           return 0.10526315789473684 # (0.10526315789473684 out of 1.0)
        end       else  # if low_ccp_group > 0.5
        case when Comments_diff <= -20.5 then
           return 0.96 # (0.96 out of 1.0)
        else  # if Comments_diff > -20.5
          case when refactor_mle_diff <= -0.0992434211075306 then
            case when refactor_mle_diff <= -0.21249029785394669 then
               return 0.1 # (0.1 out of 1.0)
            else  # if refactor_mle_diff > -0.21249029785394669
               return 0.5 # (0.5 out of 1.0)
            end           else  # if refactor_mle_diff > -0.0992434211075306
            case when LLOC_before <= 588.0 then
               return 0.0 # (0.0 out of 1.0)
            else  # if LLOC_before > 588.0
               return 0.13333333333333333 # (0.13333333333333333 out of 1.0)
            end           end         end       end     else  # if one_file_fix_rate_diff > 0.4848484843969345
       return 0.717948717948718 # (0.717948717948718 out of 1.0)
    end   end )