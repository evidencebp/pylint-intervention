create or replace function RandomForest_0 (prev_count int64, prev_count_x int64, prev_count_y int64, using-constant-test int64, Comments_diff int64, massive_change int64, McCabe_max_after int64, Comments_before int64, too-many-statements int64, cur_count_x int64, h1_diff int64, McCabe_sum_diff int64, LLOC_before int64, McCabe_sum_before int64, high_McCabe_max_before int64, avg_coupling_code_size_cut_diff int64, is_refactor int64, N2_diff int64, too-many-branches int64, SLOC_before int64, too-many-nested-blocks int64, too-many-lines int64, bugs_diff int64, time_diff int64, Single comments_after int64, simplifiable-condition int64, Multi_diff int64, high_McCabe_sum_before int64, low_ccp_group int64, refactor_mle_diff int64, low_McCabe_max_diff int64, SLOC_diff int64, changed_lines int64, hunks_num int64, McCabe_sum_after int64, cur_count_y int64, one_file_fix_rate_diff int64, low_McCabe_sum_before int64, modified_McCabe_max_diff int64, superfluous-parens int64, mostly_delete int64, added_functions int64, Comments_after int64, N1_diff int64, McCabe_max_diff int64, simplifiable-if-statement int64, LOC_before int64, low_McCabe_max_before int64, McCabe_max_before int64, try-except-raise int64, line-too-long int64, unnecessary-semicolon int64, wildcard-import int64, difficulty_diff int64, Simplify-boolean-expression int64, cur_count int64, low_McCabe_sum_diff int64, pointless-statement int64, length_diff int64, broad-exception-caught int64, h2_diff int64, high_McCabe_sum_diff int64, only_removal int64, comparison-of-constants int64, Single comments_diff int64, too-many-boolean-expressions int64, Blank_before int64, calculated_length_diff int64, Single comments_before int64, removed_lines int64, simplifiable-if-expression int64, LOC_diff int64, volume_diff int64, high_McCabe_max_diff int64, high_ccp_group int64, same_day_duration_avg_diff int64, Blank_diff int64, effort_diff int64, too-many-return-statements int64, added_lines int64, unnecessary-pass int64, vocabulary_diff int64, LLOC_diff int64) as (
  case when removed_lines <= 212.0 then
    case when McCabe_max_before <= 5.5 then
      case when prev_count_y <= 1.5 then
        case when hunks_num <= 2.5 then
           return 0.9375 # (0.9375 out of 1.0)
        else  # if hunks_num > 2.5
           return 0.7083333333333334 # (0.7083333333333334 out of 1.0)
        end       else  # if prev_count_y > 1.5
         return 0.5333333333333333 # (0.5333333333333333 out of 1.0)
      end     else  # if McCabe_max_before > 5.5
      case when high_ccp_group <= 0.5 then
        case when added_lines <= 199.5 then
          case when added_functions <= 0.5 then
            case when Comments_diff <= 1.5 then
              case when Multi_diff <= 0.5 then
                case when added_lines <= 1.5 then
                  case when McCabe_sum_after <= 180.0 then
                     return 0.6 # (0.6 out of 1.0)
                  else  # if McCabe_sum_after > 180.0
                     return 0.42105263157894735 # (0.42105263157894735 out of 1.0)
                  end                 else  # if added_lines > 1.5
                  case when one_file_fix_rate_diff <= 0.02083333395421505 then
                    case when McCabe_max_after <= 29.5 then
                      case when added_lines <= 38.5 then
                         return 0.0 # (0.0 out of 1.0)
                      else  # if added_lines > 38.5
                        case when McCabe_max_after <= 16.5 then
                           return 0.24 # (0.24 out of 1.0)
                        else  # if McCabe_max_after > 16.5
                           return 0.6111111111111112 # (0.6111111111111112 out of 1.0)
                        end                       end                     else  # if McCabe_max_after > 29.5
                      case when h2_diff <= -16.5 then
                         return 0.0 # (0.0 out of 1.0)
                      else  # if h2_diff > -16.5
                         return 0.058823529411764705 # (0.058823529411764705 out of 1.0)
                      end                     end                   else  # if one_file_fix_rate_diff > 0.02083333395421505
                    case when changed_lines <= 26.5 then
                       return 0.6 # (0.6 out of 1.0)
                    else  # if changed_lines > 26.5
                       return 0.2222222222222222 # (0.2222222222222222 out of 1.0)
                    end                   end                 end               else  # if Multi_diff > 0.5
                 return 0.5 # (0.5 out of 1.0)
              end             else  # if Comments_diff > 1.5
               return 0.06666666666666667 # (0.06666666666666667 out of 1.0)
            end           else  # if added_functions > 0.5
            case when length_diff <= -6.0 then
               return 0.7692307692307693 # (0.7692307692307693 out of 1.0)
            else  # if length_diff > -6.0
              case when Single comments_after <= 214.5 then
                case when Blank_before <= 84.5 then
                   return 0.55 # (0.55 out of 1.0)
                else  # if Blank_before > 84.5
                  case when length_diff <= 7.0 then
                     return 0.1111111111111111 # (0.1111111111111111 out of 1.0)
                  else  # if length_diff > 7.0
                     return 0.36363636363636365 # (0.36363636363636365 out of 1.0)
                  end                 end               else  # if Single comments_after > 214.5
                 return 1.0 # (1.0 out of 1.0)
              end             end           end         else  # if added_lines > 199.5
          case when LOC_before <= 982.0 then
             return 0.9444444444444444 # (0.9444444444444444 out of 1.0)
          else  # if LOC_before > 982.0
            case when vocabulary_diff <= -69.5 then
               return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
            else  # if vocabulary_diff > -69.5
               return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
            end           end         end       else  # if high_ccp_group > 0.5
        case when Blank_before <= 115.5 then
          case when McCabe_sum_after <= 136.5 then
             return 0.8 # (0.8 out of 1.0)
          else  # if McCabe_sum_after > 136.5
             return 0.2692307692307692 # (0.2692307692307692 out of 1.0)
          end         else  # if Blank_before > 115.5
          case when changed_lines <= 244.5 then
            case when removed_lines <= 14.0 then
               return 0.7894736842105263 # (0.7894736842105263 out of 1.0)
            else  # if removed_lines > 14.0
               return 1.0 # (1.0 out of 1.0)
            end           else  # if changed_lines > 244.5
             return 0.5 # (0.5 out of 1.0)
          end         end       end     end   else  # if removed_lines > 212.0
    case when same_day_duration_avg_diff <= 5.392293810844421 then
       return 0.08333333333333333 # (0.08333333333333333 out of 1.0)
    else  # if same_day_duration_avg_diff > 5.392293810844421
       return 0.19047619047619047 # (0.19047619047619047 out of 1.0)
    end   end )