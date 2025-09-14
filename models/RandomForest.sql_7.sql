create or replace function RandomForest_7 (prev_count int64, prev_count_x int64, prev_count_y int64, using-constant-test int64, Comments_diff int64, massive_change int64, McCabe_max_after int64, Comments_before int64, too-many-statements int64, cur_count_x int64, h1_diff int64, McCabe_sum_diff int64, LLOC_before int64, McCabe_sum_before int64, high_McCabe_max_before int64, avg_coupling_code_size_cut_diff int64, is_refactor int64, N2_diff int64, too-many-branches int64, SLOC_before int64, too-many-nested-blocks int64, too-many-lines int64, bugs_diff int64, time_diff int64, Single comments_after int64, simplifiable-condition int64, Multi_diff int64, high_McCabe_sum_before int64, low_ccp_group int64, refactor_mle_diff int64, low_McCabe_max_diff int64, SLOC_diff int64, changed_lines int64, hunks_num int64, McCabe_sum_after int64, cur_count_y int64, one_file_fix_rate_diff int64, low_McCabe_sum_before int64, modified_McCabe_max_diff int64, superfluous-parens int64, mostly_delete int64, added_functions int64, Comments_after int64, N1_diff int64, McCabe_max_diff int64, simplifiable-if-statement int64, LOC_before int64, low_McCabe_max_before int64, McCabe_max_before int64, try-except-raise int64, line-too-long int64, unnecessary-semicolon int64, wildcard-import int64, difficulty_diff int64, Simplify-boolean-expression int64, cur_count int64, low_McCabe_sum_diff int64, pointless-statement int64, length_diff int64, broad-exception-caught int64, h2_diff int64, high_McCabe_sum_diff int64, only_removal int64, comparison-of-constants int64, Single comments_diff int64, too-many-boolean-expressions int64, Blank_before int64, calculated_length_diff int64, Single comments_before int64, removed_lines int64, simplifiable-if-expression int64, LOC_diff int64, volume_diff int64, high_McCabe_max_diff int64, high_ccp_group int64, same_day_duration_avg_diff int64, Blank_diff int64, effort_diff int64, too-many-return-statements int64, added_lines int64, unnecessary-pass int64, vocabulary_diff int64, LLOC_diff int64) as (
  case when McCabe_sum_diff <= -37.5 then
    case when hunks_num <= 6.5 then
       return 0.9130434782608695 # (0.9130434782608695 out of 1.0)
    else  # if hunks_num > 6.5
       return 0.6538461538461539 # (0.6538461538461539 out of 1.0)
    end   else  # if McCabe_sum_diff > -37.5
    case when McCabe_sum_before <= 92.5 then
      case when low_ccp_group <= 0.5 then
        case when high_ccp_group <= 0.5 then
          case when h2_diff <= -1.5 then
             return 0.35 # (0.35 out of 1.0)
          else  # if h2_diff > -1.5
            case when Comments_diff <= -2.5 then
               return 0.375 # (0.375 out of 1.0)
            else  # if Comments_diff > -2.5
              case when McCabe_max_after <= 13.5 then
                case when refactor_mle_diff <= -0.20839758217334747 then
                   return 0.5333333333333333 # (0.5333333333333333 out of 1.0)
                else  # if refactor_mle_diff > -0.20839758217334747
                  case when same_day_duration_avg_diff <= -3.2035714387893677 then
                     return 0.8333333333333334 # (0.8333333333333334 out of 1.0)
                  else  # if same_day_duration_avg_diff > -3.2035714387893677
                     return 0.9473684210526315 # (0.9473684210526315 out of 1.0)
                  end                 end               else  # if McCabe_max_after > 13.5
                 return 0.46153846153846156 # (0.46153846153846156 out of 1.0)
              end             end           end         else  # if high_ccp_group > 0.5
          case when Single comments_diff <= -0.5 then
             return 0.8695652173913043 # (0.8695652173913043 out of 1.0)
          else  # if Single comments_diff > -0.5
             return 1.0 # (1.0 out of 1.0)
          end         end       else  # if low_ccp_group > 0.5
        case when Comments_after <= 21.5 then
           return 0.0 # (0.0 out of 1.0)
        else  # if Comments_after > 21.5
          case when Single comments_before <= 74.5 then
             return 0.6296296296296297 # (0.6296296296296297 out of 1.0)
          else  # if Single comments_before > 74.5
             return 0.9285714285714286 # (0.9285714285714286 out of 1.0)
          end         end       end     else  # if McCabe_sum_before > 92.5
      case when high_ccp_group <= 0.5 then
        case when McCabe_sum_after <= 101.0 then
           return 0.0 # (0.0 out of 1.0)
        else  # if McCabe_sum_after > 101.0
          case when Comments_after <= 24.0 then
             return 0.6071428571428571 # (0.6071428571428571 out of 1.0)
          else  # if Comments_after > 24.0
            case when low_ccp_group <= 0.5 then
              case when McCabe_max_before <= 15.5 then
                 return 0.6 # (0.6 out of 1.0)
              else  # if McCabe_max_before > 15.5
                case when LLOC_before <= 936.0 then
                  case when Single comments_after <= 91.5 then
                    case when N1_diff <= -0.5 then
                       return 0.0 # (0.0 out of 1.0)
                    else  # if N1_diff > -0.5
                       return 0.25 # (0.25 out of 1.0)
                    end                   else  # if Single comments_after > 91.5
                     return 0.5 # (0.5 out of 1.0)
                  end                 else  # if LLOC_before > 936.0
                  case when McCabe_sum_before <= 491.5 then
                     return 0.7058823529411765 # (0.7058823529411765 out of 1.0)
                  else  # if McCabe_sum_before > 491.5
                     return 0.2 # (0.2 out of 1.0)
                  end                 end               end             else  # if low_ccp_group > 0.5
              case when modified_McCabe_max_diff <= -0.5 then
                 return 0.25925925925925924 # (0.25925925925925924 out of 1.0)
              else  # if modified_McCabe_max_diff > -0.5
                 return 0.0 # (0.0 out of 1.0)
              end             end           end         end       else  # if high_ccp_group > 0.5
        case when one_file_fix_rate_diff <= -0.12841269746422768 then
          case when LLOC_before <= 776.5 then
             return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
          else  # if LLOC_before > 776.5
             return 0.625 # (0.625 out of 1.0)
          end         else  # if one_file_fix_rate_diff > -0.12841269746422768
          case when Blank_before <= 118.0 then
             return 0.47058823529411764 # (0.47058823529411764 out of 1.0)
          else  # if Blank_before > 118.0
            case when LOC_diff <= 2.5 then
               return 0.9523809523809523 # (0.9523809523809523 out of 1.0)
            else  # if LOC_diff > 2.5
               return 0.7857142857142857 # (0.7857142857142857 out of 1.0)
            end           end         end       end     end   end )