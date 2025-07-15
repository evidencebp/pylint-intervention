create or replace function RandomForest_4 (using-constant-test int64, simplifiable-if-statement int64, Comments_after int64, same_day_duration_avg_diff int64, Single comments_before int64, one_file_fix_rate_diff int64, too-many-boolean-expressions int64, Single comments_diff int64, high_McCabe_sum_before int64, pointless-statement int64, bugs_diff int64, McCabe_max_before int64, length_diff int64, LOC_diff int64, N2_diff int64, superfluous-parens int64, too-many-nested-blocks int64, effort_diff int64, cur_count_x int64, high_McCabe_max_before int64, comparison-of-constants int64, SLOC_diff int64, hunks_num int64, high_McCabe_max_diff int64, prev_count int64, McCabe_sum_after int64, cur_count_y int64, refactor_mle_diff int64, too-many-return-statements int64, too-many-statements int64, too-many-lines int64, only_removal int64, removed_lines int64, cur_count int64, volume_diff int64, is_refactor int64, prev_count_y int64, calculated_length_diff int64, Simplify-boolean-expression int64, h1_diff int64, McCabe_max_diff int64, wildcard-import int64, McCabe_sum_before int64, line-too-long int64, N1_diff int64, too-many-branches int64, h2_diff int64, McCabe_max_after int64, unnecessary-pass int64, avg_coupling_code_size_cut_diff int64, high_ccp_group int64, vocabulary_diff int64, try-except-raise int64, broad-exception-caught int64, simplifiable-condition int64, LLOC_before int64, added_functions int64, LLOC_diff int64, difficulty_diff int64, McCabe_sum_diff int64, Multi_diff int64, massive_change int64, mostly_delete int64, Comments_before int64, changed_lines int64, Comments_diff int64, time_diff int64, Blank_before int64, high_McCabe_sum_diff int64, added_lines int64, prev_count_x int64, unnecessary-semicolon int64, Blank_diff int64, modified_McCabe_max_diff int64, Single comments_after int64, LOC_before int64, simplifiable-if-expression int64, SLOC_before int64) as (
  case when Comments_before <= 3.5 then
    case when same_day_duration_avg_diff <= 52.571428298950195 then
       return 0.9333333333333333 # (14.0 out of 15.0)
    else  # if same_day_duration_avg_diff > 52.571428298950195
       return 0.8235294117647058 # (14.0 out of 17.0)
    end   else  # if Comments_before > 3.5
    case when removed_lines <= 60.5 then
      case when McCabe_sum_after <= 369.0 then
        case when Single comments_before <= 102.5 then
          case when McCabe_max_after <= 6.5 then
            case when SLOC_before <= 181.5 then
               return 0.45454545454545453 # (10.0 out of 22.0)
            else  # if SLOC_before > 181.5
               return 0.7741935483870968 # (24.0 out of 31.0)
            end           else  # if McCabe_max_after > 6.5
            case when Blank_diff <= -17.5 then
              case when avg_coupling_code_size_cut_diff <= -0.2222222238779068 then
                 return 0.7222222222222222 # (13.0 out of 18.0)
              else  # if avg_coupling_code_size_cut_diff > -0.2222222238779068
                 return 0.47058823529411764 # (8.0 out of 17.0)
              end             else  # if Blank_diff > -17.5
              case when SLOC_before <= 392.0 then
                case when changed_lines <= 59.0 then
                  case when SLOC_before <= 223.5 then
                     return 0.42857142857142855 # (6.0 out of 14.0)
                  else  # if SLOC_before > 223.5
                     return 0.1111111111111111 # (3.0 out of 27.0)
                  end                 else  # if changed_lines > 59.0
                   return 0.0 # (0.0 out of 28.0)
                end               else  # if SLOC_before > 392.0
                case when vocabulary_diff <= -24.0 then
                   return 0.0 # (0.0 out of 20.0)
                else  # if vocabulary_diff > -24.0
                  case when Comments_after <= 20.5 then
                     return 0.2727272727272727 # (6.0 out of 22.0)
                  else  # if Comments_after > 20.5
                    case when Single comments_before <= 39.5 then
                       return 0.875 # (14.0 out of 16.0)
                    else  # if Single comments_before > 39.5
                      case when LOC_before <= 838.0 then
                         return 0.7333333333333333 # (22.0 out of 30.0)
                      else  # if LOC_before > 838.0
                        case when LOC_diff <= -11.0 then
                           return 0.5 # (8.0 out of 16.0)
                        else  # if LOC_diff > -11.0
                           return 0.20833333333333334 # (5.0 out of 24.0)
                        end                       end                     end                   end                 end               end             end           end         else  # if Single comments_before > 102.5
          case when same_day_duration_avg_diff <= 90.31904602050781 then
            case when McCabe_sum_before <= 146.0 then
               return 0.0 # (0.0 out of 39.0)
            else  # if McCabe_sum_before > 146.0
              case when Blank_before <= 177.5 then
                 return 0.5 # (8.0 out of 16.0)
              else  # if Blank_before > 177.5
                 return 0.05 # (1.0 out of 20.0)
              end             end           else  # if same_day_duration_avg_diff > 90.31904602050781
             return 0.375 # (6.0 out of 16.0)
          end         end       else  # if McCabe_sum_after > 369.0
        case when refactor_mle_diff <= -0.030453700572252274 then
           return 0.8947368421052632 # (17.0 out of 19.0)
        else  # if refactor_mle_diff > -0.030453700572252274
           return 0.5 # (7.0 out of 14.0)
        end       end     else  # if removed_lines > 60.5
      case when avg_coupling_code_size_cut_diff <= 0.5905987620353699 then
        case when Comments_after <= 195.0 then
          case when SLOC_diff <= -58.5 then
             return 0.9473684210526315 # (18.0 out of 19.0)
          else  # if SLOC_diff > -58.5
            case when McCabe_sum_before <= 59.5 then
               return 0.7058823529411765 # (12.0 out of 17.0)
            else  # if McCabe_sum_before > 59.5
              case when Comments_diff <= 3.5 then
                case when SLOC_diff <= 43.0 then
                   return 0.2608695652173913 # (6.0 out of 23.0)
                else  # if SLOC_diff > 43.0
                   return 0.9285714285714286 # (13.0 out of 14.0)
                end               else  # if Comments_diff > 3.5
                 return 0.25 # (6.0 out of 24.0)
              end             end           end         else  # if Comments_after > 195.0
           return 0.9310344827586207 # (27.0 out of 29.0)
        end       else  # if avg_coupling_code_size_cut_diff > 0.5905987620353699
        case when Single comments_diff <= 3.5 then
           return 0.5 # (9.0 out of 18.0)
        else  # if Single comments_diff > 3.5
           return 0.06666666666666667 # (1.0 out of 15.0)
        end       end     end   end )