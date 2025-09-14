create or replace function RandomForest_0 (h1_diff int64, simplifiable-if-statement int64, McCabe_max_after int64, McCabe_sum_before int64, Single comments_before int64, low_McCabe_max_diff int64, high_ccp_group int64, pointless-statement int64, too-many-branches int64, high_McCabe_max_before int64, superfluous-parens int64, Multi_diff int64, wildcard-import int64, high_McCabe_sum_before int64, LLOC_before int64, cur_count int64, unnecessary-semicolon int64, Comments_after int64, mostly_delete int64, simplifiable-condition int64, avg_coupling_code_size_cut_diff int64, added_functions int64, McCabe_max_diff int64, McCabe_sum_diff int64, LLOC_diff int64, LOC_before int64, Comments_diff int64, prev_count_x int64, effort_diff int64, try-except-raise int64, difficulty_diff int64, line-too-long int64, Simplify-boolean-expression int64, SLOC_diff int64, McCabe_sum_after int64, refactor_mle_diff int64, one_file_fix_rate_diff int64, is_refactor int64, too-many-lines int64, too-many-boolean-expressions int64, Single comments_diff int64, low_McCabe_sum_diff int64, cur_count_y int64, comparison-of-constants int64, Comments_before int64, too-many-return-statements int64, vocabulary_diff int64, massive_change int64, hunks_num int64, modified_McCabe_max_diff int64, high_McCabe_sum_diff int64, N2_diff int64, broad-exception-caught int64, length_diff int64, unnecessary-pass int64, time_diff int64, changed_lines int64, Single comments_after int64, h2_diff int64, low_McCabe_sum_before int64, cur_count_x int64, McCabe_max_before int64, using-constant-test int64, added_lines int64, same_day_duration_avg_diff int64, prev_count_y int64, Blank_diff int64, LOC_diff int64, only_removal int64, low_McCabe_max_before int64, bugs_diff int64, too-many-statements int64, simplifiable-if-expression int64, calculated_length_diff int64, volume_diff int64, Blank_before int64, high_McCabe_max_diff int64, SLOC_before int64, too-many-nested-blocks int64, removed_lines int64, low_ccp_group int64, N1_diff int64, prev_count int64) as (
  case when hunks_num <= 10.5 then
    case when McCabe_sum_diff <= -34.5 then
       return 0.868421052631579 # (0.868421052631579 out of 1.0)
    else  # if McCabe_sum_diff > -34.5
      case when SLOC_diff <= -66.0 then
        case when LOC_before <= 1073.0 then
           return 0.0 # (0.0 out of 1.0)
        else  # if LOC_before > 1073.0
           return 0.2 # (0.2 out of 1.0)
        end       else  # if SLOC_diff > -66.0
        case when LOC_diff <= -53.5 then
          case when Comments_after <= 18.5 then
             return 0.46153846153846156 # (0.46153846153846156 out of 1.0)
          else  # if Comments_after > 18.5
             return 0.9230769230769231 # (0.9230769230769231 out of 1.0)
          end         else  # if LOC_diff > -53.5
          case when McCabe_max_before <= 5.5 then
            case when high_ccp_group <= 0.5 then
               return 0.6153846153846154 # (0.6153846153846154 out of 1.0)
            else  # if high_ccp_group > 0.5
               return 1.0 # (1.0 out of 1.0)
            end           else  # if McCabe_max_before > 5.5
            case when changed_lines <= 64.5 then
              case when Comments_diff <= 1.5 then
                case when changed_lines <= 20.5 then
                  case when avg_coupling_code_size_cut_diff <= -1.126893937587738 then
                     return 0.15384615384615385 # (0.15384615384615385 out of 1.0)
                  else  # if avg_coupling_code_size_cut_diff > -1.126893937587738
                    case when Single comments_after <= 32.5 then
                      case when refactor_mle_diff <= -0.11544642969965935 then
                         return 0.23529411764705882 # (0.23529411764705882 out of 1.0)
                      else  # if refactor_mle_diff > -0.11544642969965935
                         return 0.75 # (0.75 out of 1.0)
                      end                     else  # if Single comments_after > 32.5
                      case when high_ccp_group <= 0.5 then
                        case when Blank_before <= 145.5 then
                           return 0.45454545454545453 # (0.45454545454545453 out of 1.0)
                        else  # if Blank_before > 145.5
                           return 0.6190476190476191 # (0.6190476190476191 out of 1.0)
                        end                       else  # if high_ccp_group > 0.5
                         return 0.9444444444444444 # (0.9444444444444444 out of 1.0)
                      end                     end                   end                 else  # if changed_lines > 20.5
                  case when Blank_diff <= -0.5 then
                    case when Single comments_before <= 76.5 then
                       return 0.25 # (0.25 out of 1.0)
                    else  # if Single comments_before > 76.5
                       return 0.0 # (0.0 out of 1.0)
                    end                   else  # if Blank_diff > -0.5
                    case when McCabe_sum_before <= 85.5 then
                       return 0.7058823529411765 # (0.7058823529411765 out of 1.0)
                    else  # if McCabe_sum_before > 85.5
                       return 0.2692307692307692 # (0.2692307692307692 out of 1.0)
                    end                   end                 end               else  # if Comments_diff > 1.5
                 return 0.0 # (0.0 out of 1.0)
              end             else  # if changed_lines > 64.5
              case when Comments_diff <= 20.5 then
                case when Single comments_diff <= 3.0 then
                  case when Blank_before <= 91.5 then
                    case when Comments_after <= 32.5 then
                       return 0.8333333333333334 # (0.8333333333333334 out of 1.0)
                    else  # if Comments_after > 32.5
                       return 0.14285714285714285 # (0.14285714285714285 out of 1.0)
                    end                   else  # if Blank_before > 91.5
                     return 0.8823529411764706 # (0.8823529411764706 out of 1.0)
                  end                 else  # if Single comments_diff > 3.0
                   return 0.09090909090909091 # (0.09090909090909091 out of 1.0)
                end               else  # if Comments_diff > 20.5
                 return 1.0 # (1.0 out of 1.0)
              end             end           end         end       end     end   else  # if hunks_num > 10.5
    case when refactor_mle_diff <= 0.3291272670030594 then
      case when low_ccp_group <= 0.5 then
        case when removed_lines <= 100.5 then
          case when vocabulary_diff <= -3.5 then
             return 0.22727272727272727 # (0.22727272727272727 out of 1.0)
          else  # if vocabulary_diff > -3.5
             return 0.4090909090909091 # (0.4090909090909091 out of 1.0)
          end         else  # if removed_lines > 100.5
          case when McCabe_sum_diff <= 1.0 then
             return 0.5 # (0.5 out of 1.0)
          else  # if McCabe_sum_diff > 1.0
             return 0.84 # (0.84 out of 1.0)
          end         end       else  # if low_ccp_group > 0.5
        case when N2_diff <= -2.0 then
           return 0.16666666666666666 # (0.16666666666666666 out of 1.0)
        else  # if N2_diff > -2.0
           return 0.0 # (0.0 out of 1.0)
        end       end     else  # if refactor_mle_diff > 0.3291272670030594
       return 0.0 # (0.0 out of 1.0)
    end   end )