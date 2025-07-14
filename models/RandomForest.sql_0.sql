create or replace function RandomForest_0 (effort_diff int64, too-many-nested-blocks int64, Single comments_diff int64, N1_diff int64, avg_coupling_code_size_cut_diff int64, Simplify-boolean-expression int64, try-except-raise int64, h1_diff int64, added_functions int64, too-many-boolean-expressions int64, LLOC_diff int64, cur_count_x int64, wildcard-import int64, mostly_delete int64, LOC_diff int64, difficulty_diff int64, Comments_before int64, prev_count_y int64, time_diff int64, pointless-statement int64, vocabulary_diff int64, modified_McCabe_max_diff int64, prev_count int64, McCabe_sum_before int64, McCabe_max_after int64, Blank_diff int64, using-constant-test int64, McCabe_max_before int64, is_refactor int64, Comments_after int64, SLOC_before int64, superfluous-parens int64, too-many-branches int64, massive_change int64, comparison-of-constants int64, broad-exception-caught int64, Blank_before int64, N2_diff int64, McCabe_sum_after int64, too-many-statements int64, refactor_mle_diff int64, LOC_before int64, simplifiable-if-statement int64, only_removal int64, h2_diff int64, unnecessary-semicolon int64, too-many-lines int64, LLOC_before int64, volume_diff int64, too-many-return-statements int64, high_ccp_group int64, Single comments_before int64, simplifiable-if-expression int64, changed_lines int64, Multi_diff int64, one_file_fix_rate_diff int64, prev_count_x int64, simplifiable-condition int64, cur_count_y int64, calculated_length_diff int64, SLOC_diff int64, line-too-long int64, McCabe_max_diff int64, Comments_diff int64, cur_count int64, Single comments_after int64, removed_lines int64, added_lines int64, length_diff int64, unnecessary-pass int64, hunks_num int64, bugs_diff int64, same_day_duration_avg_diff int64, McCabe_sum_diff int64) as (
  case when Comments_diff <= -21.0 then
    case when Blank_diff <= -84.5 then
       return 0.3333333333333333 # (5.0 out of 15.0)
    else  # if Blank_diff > -84.5
      case when vocabulary_diff <= -108.5 then
         return 0.8823529411764706 # (15.0 out of 17.0)
      else  # if vocabulary_diff > -108.5
         return 1.0 # (22.0 out of 22.0)
      end     end   else  # if Comments_diff > -21.0
    case when Single comments_before <= 219.5 then
      case when LOC_diff <= -12.5 then
        case when SLOC_diff <= -47.5 then
          case when SLOC_diff <= -62.0 then
            case when Comments_diff <= -6.0 then
               return 0.5555555555555556 # (10.0 out of 18.0)
            else  # if Comments_diff > -6.0
              case when h2_diff <= -26.0 then
                 return 0.0 # (0.0 out of 21.0)
              else  # if h2_diff > -26.0
                 return 0.2777777777777778 # (5.0 out of 18.0)
              end             end           else  # if SLOC_diff > -62.0
             return 0.9444444444444444 # (17.0 out of 18.0)
          end         else  # if SLOC_diff > -47.5
          case when refactor_mle_diff <= -0.16073383390903473 then
             return 0.02631578947368421 # (1.0 out of 38.0)
          else  # if refactor_mle_diff > -0.16073383390903473
            case when one_file_fix_rate_diff <= -0.2142857164144516 then
               return 0.21052631578947367 # (4.0 out of 19.0)
            else  # if one_file_fix_rate_diff > -0.2142857164144516
              case when McCabe_max_after <= 11.0 then
                 return 0.6470588235294118 # (11.0 out of 17.0)
              else  # if McCabe_max_after > 11.0
                 return 0.125 # (3.0 out of 24.0)
              end             end           end         end       else  # if LOC_diff > -12.5
        case when added_lines <= 184.0 then
          case when Blank_before <= 53.5 then
            case when LOC_diff <= 1.5 then
               return 0.8148148148148148 # (22.0 out of 27.0)
            else  # if LOC_diff > 1.5
              case when changed_lines <= 106.5 then
                 return 0.30303030303030304 # (10.0 out of 33.0)
              else  # if changed_lines > 106.5
                 return 0.875 # (14.0 out of 16.0)
              end             end           else  # if Blank_before > 53.5
            case when refactor_mle_diff <= -0.007477590348571539 then
              case when avg_coupling_code_size_cut_diff <= 1.7777777314186096 then
                case when added_lines <= 17.5 then
                  case when Comments_before <= 56.5 then
                    case when LOC_before <= 732.0 then
                       return 0.46153846153846156 # (6.0 out of 13.0)
                    else  # if LOC_before > 732.0
                       return 0.2222222222222222 # (4.0 out of 18.0)
                    end                   else  # if Comments_before > 56.5
                     return 0.6153846153846154 # (16.0 out of 26.0)
                  end                 else  # if added_lines > 17.5
                  case when LLOC_before <= 503.0 then
                     return 0.10526315789473684 # (2.0 out of 19.0)
                  else  # if LLOC_before > 503.0
                     return 0.29411764705882354 # (5.0 out of 17.0)
                  end                 end               else  # if avg_coupling_code_size_cut_diff > 1.7777777314186096
                 return 0.875 # (14.0 out of 16.0)
              end             else  # if refactor_mle_diff > -0.007477590348571539
              case when SLOC_diff <= -0.5 then
                 return 0.5714285714285714 # (8.0 out of 14.0)
              else  # if SLOC_diff > -0.5
                case when McCabe_max_before <= 14.0 then
                  case when McCabe_max_before <= 8.0 then
                     return 0.29411764705882354 # (5.0 out of 17.0)
                  else  # if McCabe_max_before > 8.0
                     return 0.5 # (7.0 out of 14.0)
                  end                 else  # if McCabe_max_before > 14.0
                  case when same_day_duration_avg_diff <= 1.6761363744735718 then
                     return 0.2608695652173913 # (6.0 out of 23.0)
                  else  # if same_day_duration_avg_diff > 1.6761363744735718
                    case when McCabe_max_before <= 21.5 then
                       return 0.0 # (0.0 out of 19.0)
                    else  # if McCabe_max_before > 21.5
                       return 0.1111111111111111 # (2.0 out of 18.0)
                    end                   end                 end               end             end           end         else  # if added_lines > 184.0
           return 0.8095238095238095 # (17.0 out of 21.0)
        end       end     else  # if Single comments_before > 219.5
      case when SLOC_before <= 1871.0 then
        case when added_lines <= 3.0 then
           return 0.9259259259259259 # (25.0 out of 27.0)
        else  # if added_lines > 3.0
           return 0.6470588235294118 # (11.0 out of 17.0)
        end       else  # if SLOC_before > 1871.0
         return 0.3888888888888889 # (7.0 out of 18.0)
      end     end   end )