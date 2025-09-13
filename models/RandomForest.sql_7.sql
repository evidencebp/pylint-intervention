create or replace function RandomForest_7 (h1_diff int64, SLOC_before int64, avg_coupling_code_size_cut_diff int64, Multi_diff int64, using-constant-test int64, high_McCabe_sum_diff int64, difficulty_diff int64, LLOC_diff int64, length_diff int64, Comments_after int64, McCabe_max_before int64, low_McCabe_sum_before int64, cur_count int64, LOC_before int64, low_McCabe_max_before int64, massive_change int64, too-many-return-statements int64, Comments_diff int64, added_lines int64, broad-exception-caught int64, comparison-of-constants int64, Single comments_diff int64, refactor_mle_diff int64, prev_count_x int64, McCabe_sum_before int64, modified_McCabe_max_diff int64, Simplify-boolean-expression int64, Blank_diff int64, added_functions int64, LLOC_before int64, cur_count_x int64, high_McCabe_sum_before int64, volume_diff int64, low_McCabe_max_diff int64, LOC_diff int64, calculated_length_diff int64, changed_lines int64, N2_diff int64, h2_diff int64, too-many-lines int64, unnecessary-pass int64, simplifiable-if-statement int64, prev_count int64, too-many-nested-blocks int64, Comments_before int64, SLOC_diff int64, McCabe_sum_after int64, bugs_diff int64, cur_count_y int64, Single comments_after int64, McCabe_max_diff int64, N1_diff int64, wildcard-import int64, McCabe_sum_diff int64, prev_count_y int64, superfluous-parens int64, hunks_num int64, try-except-raise int64, simplifiable-if-expression int64, McCabe_max_after int64, high_McCabe_max_diff int64, too-many-statements int64, simplifiable-condition int64, only_removal int64, unnecessary-semicolon int64, effort_diff int64, is_refactor int64, same_day_duration_avg_diff int64, one_file_fix_rate_diff int64, high_McCabe_max_before int64, vocabulary_diff int64, too-many-branches int64, mostly_delete int64, high_ccp_group int64, low_ccp_group int64, removed_lines int64, Single comments_before int64, low_McCabe_sum_diff int64, time_diff int64, Blank_before int64, line-too-long int64, too-many-boolean-expressions int64, pointless-statement int64) as (
  case when Single comments_diff <= -2.5 then
    case when removed_lines <= 6.0 then
      case when LOC_before <= 1334.0 then
         return 0.5833333333333334 # (0.5833333333333334 out of 1.0)
      else  # if LOC_before > 1334.0
         return 0.2608695652173913 # (0.2608695652173913 out of 1.0)
      end     else  # if removed_lines > 6.0
      case when avg_coupling_code_size_cut_diff <= 0.03750000149011612 then
        case when same_day_duration_avg_diff <= 75.83511924743652 then
          case when McCabe_sum_diff <= -19.0 then
             return 0.8 # (0.8 out of 1.0)
          else  # if McCabe_sum_diff > -19.0
            case when Single comments_before <= 51.0 then
               return 1.0 # (1.0 out of 1.0)
            else  # if Single comments_before > 51.0
               return 0.9444444444444444 # (0.9444444444444444 out of 1.0)
            end           end         else  # if same_day_duration_avg_diff > 75.83511924743652
           return 0.5 # (0.5 out of 1.0)
        end       else  # if avg_coupling_code_size_cut_diff > 0.03750000149011612
        case when h1_diff <= -1.5 then
           return 0.7857142857142857 # (0.7857142857142857 out of 1.0)
        else  # if h1_diff > -1.5
           return 0.1 # (0.1 out of 1.0)
        end       end     end   else  # if Single comments_diff > -2.5
    case when LOC_before <= 146.0 then
       return 0.9047619047619048 # (0.9047619047619048 out of 1.0)
    else  # if LOC_before > 146.0
      case when low_ccp_group <= 0.5 then
        case when N2_diff <= -31.5 then
          case when LOC_before <= 1009.0 then
             return 0.0 # (0.0 out of 1.0)
          else  # if LOC_before > 1009.0
             return 0.3125 # (0.3125 out of 1.0)
          end         else  # if N2_diff > -31.5
          case when refactor_mle_diff <= -0.4638381004333496 then
             return 0.8947368421052632 # (0.8947368421052632 out of 1.0)
          else  # if refactor_mle_diff > -0.4638381004333496
            case when Blank_diff <= -4.0 then
               return 0.8461538461538461 # (0.8461538461538461 out of 1.0)
            else  # if Blank_diff > -4.0
              case when changed_lines <= 292.0 then
                case when Comments_before <= 111.0 then
                  case when added_lines <= 61.0 then
                    case when length_diff <= -4.0 then
                       return 0.24 # (0.24 out of 1.0)
                    else  # if length_diff > -4.0
                      case when N2_diff <= -1.5 then
                         return 0.8095238095238095 # (0.8095238095238095 out of 1.0)
                      else  # if N2_diff > -1.5
                        case when same_day_duration_avg_diff <= -88.73181915283203 then
                           return 0.8235294117647058 # (0.8235294117647058 out of 1.0)
                        else  # if same_day_duration_avg_diff > -88.73181915283203
                          case when refactor_mle_diff <= 0.22028888761997223 then
                            case when Comments_before <= 18.0 then
                               return 0.23529411764705882 # (0.23529411764705882 out of 1.0)
                            else  # if Comments_before > 18.0
                              case when McCabe_max_before <= 22.5 then
                                 return 0.7916666666666666 # (0.7916666666666666 out of 1.0)
                              else  # if McCabe_max_before > 22.5
                                 return 0.5 # (0.5 out of 1.0)
                              end                             end                           else  # if refactor_mle_diff > 0.22028888761997223
                             return 0.19047619047619047 # (0.19047619047619047 out of 1.0)
                          end                         end                       end                     end                   else  # if added_lines > 61.0
                     return 0.8928571428571429 # (0.8928571428571429 out of 1.0)
                  end                 else  # if Comments_before > 111.0
                  case when avg_coupling_code_size_cut_diff <= 0.7098456025123596 then
                    case when McCabe_sum_after <= 218.0 then
                       return 0.0 # (0.0 out of 1.0)
                    else  # if McCabe_sum_after > 218.0
                       return 0.3103448275862069 # (0.3103448275862069 out of 1.0)
                    end                   else  # if avg_coupling_code_size_cut_diff > 0.7098456025123596
                     return 0.6428571428571429 # (0.6428571428571429 out of 1.0)
                  end                 end               else  # if changed_lines > 292.0
                 return 0.23076923076923078 # (0.23076923076923078 out of 1.0)
              end             end           end         end       else  # if low_ccp_group > 0.5
        case when Single comments_before <= 252.5 then
          case when McCabe_max_before <= 27.5 then
            case when SLOC_diff <= -0.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if SLOC_diff > -0.5
              case when Blank_before <= 136.5 then
                 return 0.25 # (0.25 out of 1.0)
              else  # if Blank_before > 136.5
                 return 0.0 # (0.0 out of 1.0)
              end             end           else  # if McCabe_max_before > 27.5
             return 0.3125 # (0.3125 out of 1.0)
          end         else  # if Single comments_before > 252.5
           return 0.6875 # (0.6875 out of 1.0)
        end       end     end   end )