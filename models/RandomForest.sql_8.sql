create or replace function RandomForest_8 (prev_count int64, simplifiable-if-expression int64, N1_diff int64, cur_count int64, wildcard-import int64, too-many-return-statements int64, low_McCabe_max_diff int64, length_diff int64, volume_diff int64, high_McCabe_sum_diff int64, high_McCabe_max_before int64, simplifiable-condition int64, Blank_before int64, high_ccp_group int64, McCabe_max_before int64, bugs_diff int64, too-many-nested-blocks int64, refactor_mle_diff int64, difficulty_diff int64, LLOC_diff int64, LOC_diff int64, simplifiable-if-statement int64, one_file_fix_rate_diff int64, SLOC_before int64, LOC_before int64, mostly_delete int64, changed_lines int64, Single comments_before int64, removed_lines int64, added_functions int64, h1_diff int64, effort_diff int64, hunks_num int64, Multi_diff int64, same_day_duration_avg_diff int64, N2_diff int64, cur_count_y int64, Comments_diff int64, modified_McCabe_max_diff int64, h2_diff int64, time_diff int64, LLOC_before int64, calculated_length_diff int64, Single comments_after int64, massive_change int64, McCabe_sum_before int64, too-many-boolean-expressions int64, Simplify-boolean-expression int64, line-too-long int64, superfluous-parens int64, low_ccp_group int64, McCabe_max_diff int64, comparison-of-constants int64, high_McCabe_sum_before int64, low_McCabe_sum_diff int64, avg_coupling_code_size_cut_diff int64, is_refactor int64, Single comments_diff int64, unnecessary-semicolon int64, added_lines int64, prev_count_y int64, try-except-raise int64, low_McCabe_sum_before int64, vocabulary_diff int64, too-many-branches int64, McCabe_sum_after int64, broad-exception-caught int64, prev_count_x int64, only_removal int64, McCabe_max_after int64, pointless-statement int64, low_McCabe_max_before int64, too-many-lines int64, McCabe_sum_diff int64, high_McCabe_max_diff int64, using-constant-test int64, SLOC_diff int64, Blank_diff int64, Comments_after int64, cur_count_x int64, unnecessary-pass int64, too-many-statements int64, Comments_before int64) as (
  case when Comments_diff <= -2.5 then
    case when McCabe_max_diff <= -0.5 then
      case when LOC_before <= 385.5 then
         return 1.0 # (1.0 out of 1.0)
      else  # if LOC_before > 385.5
        case when N1_diff <= -14.5 then
          case when Blank_before <= 159.5 then
             return 1.0 # (1.0 out of 1.0)
          else  # if Blank_before > 159.5
             return 0.5454545454545454 # (0.5454545454545454 out of 1.0)
          end         else  # if N1_diff > -14.5
           return 0.29411764705882354 # (0.29411764705882354 out of 1.0)
        end       end     else  # if McCabe_max_diff > -0.5
      case when Single comments_before <= 57.5 then
         return 0.14285714285714285 # (0.14285714285714285 out of 1.0)
      else  # if Single comments_before > 57.5
        case when same_day_duration_avg_diff <= 1.2577521800994873 then
           return 0.3125 # (0.3125 out of 1.0)
        else  # if same_day_duration_avg_diff > 1.2577521800994873
           return 0.8823529411764706 # (0.8823529411764706 out of 1.0)
        end       end     end   else  # if Comments_diff > -2.5
    case when SLOC_diff <= -38.5 then
      case when avg_coupling_code_size_cut_diff <= 0.012987012974917889 then
         return 0.12 # (0.12 out of 1.0)
      else  # if avg_coupling_code_size_cut_diff > 0.012987012974917889
         return 0.0 # (0.0 out of 1.0)
      end     else  # if SLOC_diff > -38.5
      case when Single comments_after <= 80.0 then
        case when McCabe_max_after <= 50.5 then
          case when Comments_after <= 1.5 then
             return 1.0 # (1.0 out of 1.0)
          else  # if Comments_after > 1.5
            case when LLOC_before <= 129.5 then
              case when low_ccp_group <= 0.5 then
                 return 0.47619047619047616 # (0.47619047619047616 out of 1.0)
              else  # if low_ccp_group > 0.5
                 return 0.10526315789473684 # (0.10526315789473684 out of 1.0)
              end             else  # if LLOC_before > 129.5
              case when Single comments_after <= 23.5 then
                case when one_file_fix_rate_diff <= -0.07051282376050949 then
                   return 0.8 # (0.8 out of 1.0)
                else  # if one_file_fix_rate_diff > -0.07051282376050949
                  case when Blank_before <= 67.0 then
                     return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
                  else  # if Blank_before > 67.0
                     return 0.37037037037037035 # (0.37037037037037035 out of 1.0)
                  end                 end               else  # if Single comments_after > 23.5
                case when low_ccp_group <= 0.5 then
                  case when vocabulary_diff <= 1.5 then
                    case when Single comments_after <= 39.5 then
                       return 0.85 # (0.85 out of 1.0)
                    else  # if Single comments_after > 39.5
                      case when LOC_before <= 759.5 then
                         return 0.1111111111111111 # (0.1111111111111111 out of 1.0)
                      else  # if LOC_before > 759.5
                        case when LOC_diff <= -1.5 then
                           return 0.4 # (0.4 out of 1.0)
                        else  # if LOC_diff > -1.5
                           return 0.7058823529411765 # (0.7058823529411765 out of 1.0)
                        end                       end                     end                   else  # if vocabulary_diff > 1.5
                     return 0.14285714285714285 # (0.14285714285714285 out of 1.0)
                  end                 else  # if low_ccp_group > 0.5
                   return 0.09523809523809523 # (0.09523809523809523 out of 1.0)
                end               end             end           end         else  # if McCabe_max_after > 50.5
           return 0.8421052631578947 # (0.8421052631578947 out of 1.0)
        end       else  # if Single comments_after > 80.0
        case when added_functions <= 0.5 then
          case when LOC_diff <= 0.5 then
            case when LOC_diff <= -0.5 then
               return 0.14285714285714285 # (0.14285714285714285 out of 1.0)
            else  # if LOC_diff > -0.5
               return 0.4117647058823529 # (0.4117647058823529 out of 1.0)
            end           else  # if LOC_diff > 0.5
            case when McCabe_max_after <= 23.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if McCabe_max_after > 23.5
               return 0.058823529411764705 # (0.058823529411764705 out of 1.0)
            end           end         else  # if added_functions > 0.5
          case when Single comments_before <= 226.0 then
             return 0.28 # (0.28 out of 1.0)
          else  # if Single comments_before > 226.0
             return 0.8095238095238095 # (0.8095238095238095 out of 1.0)
          end         end       end     end   end )