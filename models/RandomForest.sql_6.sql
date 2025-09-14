create or replace function RandomForest_6 (h1_diff int64, simplifiable-if-statement int64, McCabe_max_after int64, McCabe_sum_before int64, Single comments_before int64, low_McCabe_max_diff int64, high_ccp_group int64, pointless-statement int64, too-many-branches int64, high_McCabe_max_before int64, superfluous-parens int64, Multi_diff int64, wildcard-import int64, high_McCabe_sum_before int64, LLOC_before int64, cur_count int64, unnecessary-semicolon int64, Comments_after int64, mostly_delete int64, simplifiable-condition int64, avg_coupling_code_size_cut_diff int64, added_functions int64, McCabe_max_diff int64, McCabe_sum_diff int64, LLOC_diff int64, LOC_before int64, Comments_diff int64, prev_count_x int64, effort_diff int64, try-except-raise int64, difficulty_diff int64, line-too-long int64, Simplify-boolean-expression int64, SLOC_diff int64, McCabe_sum_after int64, refactor_mle_diff int64, one_file_fix_rate_diff int64, is_refactor int64, too-many-lines int64, too-many-boolean-expressions int64, Single comments_diff int64, low_McCabe_sum_diff int64, cur_count_y int64, comparison-of-constants int64, Comments_before int64, too-many-return-statements int64, vocabulary_diff int64, massive_change int64, hunks_num int64, modified_McCabe_max_diff int64, high_McCabe_sum_diff int64, N2_diff int64, broad-exception-caught int64, length_diff int64, unnecessary-pass int64, time_diff int64, changed_lines int64, Single comments_after int64, h2_diff int64, low_McCabe_sum_before int64, cur_count_x int64, McCabe_max_before int64, using-constant-test int64, added_lines int64, same_day_duration_avg_diff int64, prev_count_y int64, Blank_diff int64, LOC_diff int64, only_removal int64, low_McCabe_max_before int64, bugs_diff int64, too-many-statements int64, simplifiable-if-expression int64, calculated_length_diff int64, volume_diff int64, Blank_before int64, high_McCabe_max_diff int64, SLOC_before int64, too-many-nested-blocks int64, removed_lines int64, low_ccp_group int64, N1_diff int64, prev_count int64) as (
  case when McCabe_max_before <= 22.5 then
    case when Single comments_before <= 438.0 then
      case when Multi_diff <= -48.0 then
         return 0.9411764705882353 # (0.9411764705882353 out of 1.0)
      else  # if Multi_diff > -48.0
        case when high_ccp_group <= 0.5 then
          case when LLOC_diff <= 5.0 then
            case when LOC_diff <= -1.5 then
              case when removed_lines <= 18.5 then
                case when Comments_before <= 24.0 then
                   return 0.30434782608695654 # (0.30434782608695654 out of 1.0)
                else  # if Comments_before > 24.0
                  case when LLOC_diff <= -14.5 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if LLOC_diff > -14.5
                     return 0.14285714285714285 # (0.14285714285714285 out of 1.0)
                  end                 end               else  # if removed_lines > 18.5
                case when SLOC_diff <= -33.0 then
                   return 0.7894736842105263 # (0.7894736842105263 out of 1.0)
                else  # if SLOC_diff > -33.0
                   return 0.4117647058823529 # (0.4117647058823529 out of 1.0)
                end               end             else  # if LOC_diff > -1.5
              case when Blank_diff <= 0.5 then
                case when Comments_before <= 74.0 then
                  case when added_lines <= 8.5 then
                     return 0.7419354838709677 # (0.7419354838709677 out of 1.0)
                  else  # if added_lines > 8.5
                     return 0.4117647058823529 # (0.4117647058823529 out of 1.0)
                  end                 else  # if Comments_before > 74.0
                   return 0.3157894736842105 # (0.3157894736842105 out of 1.0)
                end               else  # if Blank_diff > 0.5
                case when McCabe_sum_before <= 91.5 then
                   return 0.8695652173913043 # (0.8695652173913043 out of 1.0)
                else  # if McCabe_sum_before > 91.5
                   return 0.7058823529411765 # (0.7058823529411765 out of 1.0)
                end               end             end           else  # if LLOC_diff > 5.0
            case when h2_diff <= 4.5 then
               return 0.07692307692307693 # (0.07692307692307693 out of 1.0)
            else  # if h2_diff > 4.5
               return 0.3 # (0.3 out of 1.0)
            end           end         else  # if high_ccp_group > 0.5
          case when SLOC_diff <= -2.0 then
             return 0.7741935483870968 # (0.7741935483870968 out of 1.0)
          else  # if SLOC_diff > -2.0
            case when McCabe_sum_after <= 55.5 then
               return 0.9411764705882353 # (0.9411764705882353 out of 1.0)
            else  # if McCabe_sum_after > 55.5
               return 1.0 # (1.0 out of 1.0)
            end           end         end       end     else  # if Single comments_before > 438.0
       return 0.8888888888888888 # (0.8888888888888888 out of 1.0)
    end   else  # if McCabe_max_before > 22.5
    case when refactor_mle_diff <= -0.011192635633051395 then
      case when Single comments_diff <= 2.5 then
        case when McCabe_sum_after <= 157.5 then
          case when refactor_mle_diff <= -0.14136184751987457 then
             return 0.30434782608695654 # (0.30434782608695654 out of 1.0)
          else  # if refactor_mle_diff > -0.14136184751987457
             return 0.7142857142857143 # (0.7142857142857143 out of 1.0)
          end         else  # if McCabe_sum_after > 157.5
          case when Single comments_diff <= -0.5 then
             return 0.5 # (0.5 out of 1.0)
          else  # if Single comments_diff > -0.5
            case when Blank_diff <= 0.5 then
               return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
            else  # if Blank_diff > 0.5
               return 0.8333333333333334 # (0.8333333333333334 out of 1.0)
            end           end         end       else  # if Single comments_diff > 2.5
         return 0.22727272727272727 # (0.22727272727272727 out of 1.0)
      end     else  # if refactor_mle_diff > -0.011192635633051395
      case when superfluous-parens <= 0.5 then
        case when Single comments_before <= 104.5 then
          case when changed_lines <= 111.5 then
            case when vocabulary_diff <= -0.5 then
               return 0.5714285714285714 # (0.5714285714285714 out of 1.0)
            else  # if vocabulary_diff > -0.5
               return 0.11764705882352941 # (0.11764705882352941 out of 1.0)
            end           else  # if changed_lines > 111.5
            case when McCabe_max_diff <= -1.5 then
               return 0.06666666666666667 # (0.06666666666666667 out of 1.0)
            else  # if McCabe_max_diff > -1.5
               return 0.2 # (0.2 out of 1.0)
            end           end         else  # if Single comments_before > 104.5
          case when length_diff <= -12.5 then
             return 0.16666666666666666 # (0.16666666666666666 out of 1.0)
          else  # if length_diff > -12.5
             return 0.0 # (0.0 out of 1.0)
          end         end       else  # if superfluous-parens > 0.5
         return 0.5 # (0.5 out of 1.0)
      end     end   end )