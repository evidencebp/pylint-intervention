create or replace function RandomForest_1 (h1_diff int64, SLOC_before int64, avg_coupling_code_size_cut_diff int64, Multi_diff int64, using-constant-test int64, high_McCabe_sum_diff int64, difficulty_diff int64, LLOC_diff int64, length_diff int64, Comments_after int64, McCabe_max_before int64, low_McCabe_sum_before int64, cur_count int64, LOC_before int64, low_McCabe_max_before int64, massive_change int64, too-many-return-statements int64, Comments_diff int64, added_lines int64, broad-exception-caught int64, comparison-of-constants int64, Single comments_diff int64, refactor_mle_diff int64, prev_count_x int64, McCabe_sum_before int64, modified_McCabe_max_diff int64, Simplify-boolean-expression int64, Blank_diff int64, added_functions int64, LLOC_before int64, cur_count_x int64, high_McCabe_sum_before int64, volume_diff int64, low_McCabe_max_diff int64, LOC_diff int64, calculated_length_diff int64, changed_lines int64, N2_diff int64, h2_diff int64, too-many-lines int64, unnecessary-pass int64, simplifiable-if-statement int64, prev_count int64, too-many-nested-blocks int64, Comments_before int64, SLOC_diff int64, McCabe_sum_after int64, bugs_diff int64, cur_count_y int64, Single comments_after int64, McCabe_max_diff int64, N1_diff int64, wildcard-import int64, McCabe_sum_diff int64, prev_count_y int64, superfluous-parens int64, hunks_num int64, try-except-raise int64, simplifiable-if-expression int64, McCabe_max_after int64, high_McCabe_max_diff int64, too-many-statements int64, simplifiable-condition int64, only_removal int64, unnecessary-semicolon int64, effort_diff int64, is_refactor int64, same_day_duration_avg_diff int64, one_file_fix_rate_diff int64, high_McCabe_max_before int64, vocabulary_diff int64, too-many-branches int64, mostly_delete int64, high_ccp_group int64, low_ccp_group int64, removed_lines int64, Single comments_before int64, low_McCabe_sum_diff int64, time_diff int64, Blank_before int64, line-too-long int64, too-many-boolean-expressions int64, pointless-statement int64) as (
  case when Single comments_after <= 218.5 then
    case when refactor_mle_diff <= -0.39523424208164215 then
      case when Single comments_before <= 52.5 then
         return 0.6818181818181818 # (0.6818181818181818 out of 1.0)
      else  # if Single comments_before > 52.5
         return 1.0 # (1.0 out of 1.0)
      end     else  # if refactor_mle_diff > -0.39523424208164215
      case when high_ccp_group <= 0.5 then
        case when length_diff <= -111.0 then
           return 0.7692307692307693 # (0.7692307692307693 out of 1.0)
        else  # if length_diff > -111.0
          case when low_McCabe_max_before <= 0.5 then
            case when LOC_diff <= 43.5 then
              case when low_ccp_group <= 0.5 then
                case when Single comments_diff <= -2.5 then
                  case when Comments_after <= 47.5 then
                     return 0.6923076923076923 # (0.6923076923076923 out of 1.0)
                  else  # if Comments_after > 47.5
                     return 0.16666666666666666 # (0.16666666666666666 out of 1.0)
                  end                 else  # if Single comments_diff > -2.5
                  case when Single comments_after <= 123.5 then
                    case when h2_diff <= -5.5 then
                       return 0.03571428571428571 # (0.03571428571428571 out of 1.0)
                    else  # if h2_diff > -5.5
                      case when modified_McCabe_max_diff <= -0.5 then
                         return 0.45714285714285713 # (0.45714285714285713 out of 1.0)
                      else  # if modified_McCabe_max_diff > -0.5
                        case when SLOC_before <= 449.5 then
                           return 0.0 # (0.0 out of 1.0)
                        else  # if SLOC_before > 449.5
                           return 0.17857142857142858 # (0.17857142857142858 out of 1.0)
                        end                       end                     end                   else  # if Single comments_after > 123.5
                     return 0.4583333333333333 # (0.4583333333333333 out of 1.0)
                  end                 end               else  # if low_ccp_group > 0.5
                case when Comments_before <= 36.0 then
                   return 0.07407407407407407 # (0.07407407407407407 out of 1.0)
                else  # if Comments_before > 36.0
                   return 0.0 # (0.0 out of 1.0)
                end               end             else  # if LOC_diff > 43.5
               return 0.5 # (0.5 out of 1.0)
            end           else  # if low_McCabe_max_before > 0.5
            case when changed_lines <= 11.5 then
               return 0.76 # (0.76 out of 1.0)
            else  # if changed_lines > 11.5
              case when one_file_fix_rate_diff <= 0.1180555559694767 then
                case when McCabe_sum_after <= 43.0 then
                   return 0.2857142857142857 # (0.2857142857142857 out of 1.0)
                else  # if McCabe_sum_after > 43.0
                   return 0.65625 # (0.65625 out of 1.0)
                end               else  # if one_file_fix_rate_diff > 0.1180555559694767
                 return 0.0 # (0.0 out of 1.0)
              end             end           end         end       else  # if high_ccp_group > 0.5
        case when Comments_before <= 75.0 then
          case when hunks_num <= 14.5 then
            case when McCabe_max_after <= 7.0 then
               return 1.0 # (1.0 out of 1.0)
            else  # if McCabe_max_after > 7.0
              case when Single comments_after <= 32.0 then
                 return 0.6538461538461539 # (0.6538461538461539 out of 1.0)
              else  # if Single comments_after > 32.0
                 return 1.0 # (1.0 out of 1.0)
              end             end           else  # if hunks_num > 14.5
             return 0.4166666666666667 # (0.4166666666666667 out of 1.0)
          end         else  # if Comments_before > 75.0
           return 0.4411764705882353 # (0.4411764705882353 out of 1.0)
        end       end     end   else  # if Single comments_after > 218.5
    case when McCabe_sum_after <= 535.0 then
      case when hunks_num <= 3.5 then
         return 1.0 # (1.0 out of 1.0)
      else  # if hunks_num > 3.5
         return 0.9047619047619048 # (0.9047619047619048 out of 1.0)
      end     else  # if McCabe_sum_after > 535.0
       return 0.4827586206896552 # (0.4827586206896552 out of 1.0)
    end   end )