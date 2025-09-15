create or replace function Tree_default (Blank_diff int64, bugs_diff int64, hunks_num int64, low_McCabe_sum_before int64, low_McCabe_max_diff int64, effort_diff int64, McCabe_max_diff int64, McCabe_sum_diff int64, Comments_before int64, massive_change int64, too-many-branches int64, low_McCabe_sum_diff int64, Blank_before int64, McCabe_sum_after int64, high_ccp_group int64, high_McCabe_sum_before int64, too-many-return-statements int64, cur_count_y int64, Comments_diff int64, Multi_diff int64, refactor_mle_diff int64, cur_count int64, new_function int64, added_lines int64, Comments_after int64, Single comments_diff int64, McCabe_max_before int64, LOC_before int64, SLOC_before int64, modified_McCabe_max_diff int64, h2_diff int64, too-many-statements int64, Single comments_after int64, high_McCabe_max_diff int64, vocabulary_diff int64, prev_count_y int64, LOC_diff int64, too-many-nested-blocks int64, N1_diff int64, changed_lines int64, calculated_length_diff int64, difficulty_diff int64, mostly_delete int64, low_ccp_group int64, McCabe_max_after int64, cur_count_x int64, length_diff int64, only_removal int64, avg_coupling_code_size_cut_diff int64, prev_count_x int64, one_file_fix_rate_diff int64, high_McCabe_max_before int64, Single comments_before int64, SLOC_diff int64, time_diff int64, low_McCabe_max_before int64, added_functions int64, N2_diff int64, high_McCabe_sum_diff int64, is_refactor int64, volume_diff int64, LLOC_diff int64, same_day_duration_avg_diff int64, LLOC_before int64, prev_count int64, McCabe_sum_before int64, removed_lines int64, h1_diff int64) as (
  case when Blank_before <= 42.5 then
    case when McCabe_sum_before <= 117.5 then
      case when McCabe_max_diff <= -13.5 then
         return 0.0 # (0.0 out of 1.0)
      else  # if McCabe_max_diff > -13.5
        case when refactor_mle_diff <= -0.8767350614070892 then
           return 0.0 # (0.0 out of 1.0)
        else  # if refactor_mle_diff > -0.8767350614070892
          case when too-many-nested-blocks <= 0.5 then
             return 1.0 # (1.0 out of 1.0)
          else  # if too-many-nested-blocks > 0.5
            case when Single comments_before <= 22.5 then
               return 1.0 # (1.0 out of 1.0)
            else  # if Single comments_before > 22.5
               return 0.0 # (0.0 out of 1.0)
            end           end         end       end     else  # if McCabe_sum_before > 117.5
       return 0.0 # (0.0 out of 1.0)
    end   else  # if Blank_before > 42.5
    case when McCabe_sum_before <= 40.5 then
       return 0.0 # (0.0 out of 1.0)
    else  # if McCabe_sum_before > 40.5
      case when Blank_diff <= -1.5 then
        case when one_file_fix_rate_diff <= 0.34166666865348816 then
          case when avg_coupling_code_size_cut_diff <= 0.5208333432674408 then
            case when Comments_after <= 16.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if Comments_after > 16.5
              case when Single comments_diff <= 109.5 then
                case when refactor_mle_diff <= 0.7046507894992828 then
                  case when same_day_duration_avg_diff <= 310.1000061035156 then
                    case when LLOC_before <= 2312.5 then
                      case when too-many-statements <= 0.5 then
                         return 1.0 # (1.0 out of 1.0)
                      else  # if too-many-statements > 0.5
                        case when refactor_mle_diff <= -0.2671849802136421 then
                           return 0.0 # (0.0 out of 1.0)
                        else  # if refactor_mle_diff > -0.2671849802136421
                          case when Comments_after <= 94.5 then
                            case when McCabe_sum_after <= 233.0 then
                              case when Single comments_before <= 25.0 then
                                 return 0.0 # (0.0 out of 1.0)
                              else  # if Single comments_before > 25.0
                                 return 1.0 # (1.0 out of 1.0)
                              end                             else  # if McCabe_sum_after > 233.0
                               return 0.0 # (0.0 out of 1.0)
                            end                           else  # if Comments_after > 94.5
                             return 0.0 # (0.0 out of 1.0)
                          end                         end                       end                     else  # if LLOC_before > 2312.5
                       return 0.0 # (0.0 out of 1.0)
                    end                   else  # if same_day_duration_avg_diff > 310.1000061035156
                     return 0.0 # (0.0 out of 1.0)
                  end                 else  # if refactor_mle_diff > 0.7046507894992828
                   return 0.0 # (0.0 out of 1.0)
                end               else  # if Single comments_diff > 109.5
                 return 0.0 # (0.0 out of 1.0)
              end             end           else  # if avg_coupling_code_size_cut_diff > 0.5208333432674408
            case when N1_diff <= -19.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if N1_diff > -19.5
              case when LLOC_diff <= -13.5 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if LLOC_diff > -13.5
                 return 0.0 # (0.0 out of 1.0)
              end             end           end         else  # if one_file_fix_rate_diff > 0.34166666865348816
           return 0.0 # (0.0 out of 1.0)
        end       else  # if Blank_diff > -1.5
        case when refactor_mle_diff <= -0.1971895471215248 then
          case when McCabe_max_before <= 19.5 then
            case when Multi_diff <= 2.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if Multi_diff > 2.5
              case when Comments_after <= 41.0 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if Comments_after > 41.0
                 return 0.0 # (0.0 out of 1.0)
              end             end           else  # if McCabe_max_before > 19.5
             return 1.0 # (1.0 out of 1.0)
          end         else  # if refactor_mle_diff > -0.1971895471215248
          case when LOC_before <= 414.0 then
            case when Multi_diff <= 11.0 then
              case when McCabe_max_after <= 23.5 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if McCabe_max_after > 23.5
                case when McCabe_sum_before <= 81.0 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if McCabe_sum_before > 81.0
                   return 1.0 # (1.0 out of 1.0)
                end               end             else  # if Multi_diff > 11.0
               return 0.0 # (0.0 out of 1.0)
            end           else  # if LOC_before > 414.0
            case when high_ccp_group <= 0.5 then
              case when McCabe_max_after <= 27.5 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if McCabe_max_after > 27.5
                case when LOC_before <= 933.0 then
                   return 1.0 # (1.0 out of 1.0)
                else  # if LOC_before > 933.0
                   return 0.0 # (0.0 out of 1.0)
                end               end             else  # if high_ccp_group > 0.5
              case when one_file_fix_rate_diff <= -0.11775252595543861 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if one_file_fix_rate_diff > -0.11775252595543861
                case when refactor_mle_diff <= -0.1276846081018448 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if refactor_mle_diff > -0.1276846081018448
                  case when removed_lines <= 422.0 then
                     return 1.0 # (1.0 out of 1.0)
                  else  # if removed_lines > 422.0
                     return 0.0 # (0.0 out of 1.0)
                  end                 end               end             end           end         end       end     end   end )