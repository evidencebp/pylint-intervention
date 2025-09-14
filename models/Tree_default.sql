create or replace function Tree_default (is_refactor int64, McCabe_max_before int64, N1_diff int64, high_McCabe_sum_before int64, same_day_duration_avg_diff int64, Comments_before int64, hunks_num int64, added_lines int64, prev_count int64, low_McCabe_max_before int64, high_McCabe_max_diff int64, vocabulary_diff int64, modified_McCabe_max_diff int64, avg_coupling_code_size_cut_diff int64, too-many-nested-blocks int64, low_McCabe_max_diff int64, changed_lines int64, effort_diff int64, removed_lines int64, Blank_before int64, SLOC_diff int64, length_diff int64, low_ccp_group int64, calculated_length_diff int64, McCabe_max_diff int64, McCabe_max_after int64, LOC_diff int64, too-many-return-statements int64, Single comments_after int64, McCabe_sum_diff int64, LLOC_diff int64, too-many-statements int64, Comments_after int64, low_McCabe_sum_diff int64, McCabe_sum_before int64, difficulty_diff int64, Single comments_before int64, massive_change int64, prev_count_x int64, refactor_mle_diff int64, cur_count_y int64, N2_diff int64, prev_count_y int64, Single comments_diff int64, cur_count int64, high_McCabe_max_before int64, one_file_fix_rate_diff int64, h1_diff int64, low_McCabe_sum_before int64, time_diff int64, LOC_before int64, SLOC_before int64, too-many-branches int64, volume_diff int64, McCabe_sum_after int64, mostly_delete int64, Multi_diff int64, high_McCabe_sum_diff int64, Blank_diff int64, bugs_diff int64, h2_diff int64, cur_count_x int64, added_functions int64, LLOC_before int64, high_ccp_group int64, Comments_diff int64, only_removal int64) as (
  case when hunks_num <= 11.5 then
    case when prev_count <= 2.5 then
      case when low_ccp_group <= 0.5 then
        case when same_day_duration_avg_diff <= 260.30834197998047 then
          case when SLOC_before <= 1108.0 then
            case when avg_coupling_code_size_cut_diff <= -4.055555582046509 then
               return 0.0 # (0.0 out of 1.0)
            else  # if avg_coupling_code_size_cut_diff > -4.055555582046509
              case when McCabe_sum_before <= 68.5 then
                case when too-many-return-statements <= 0.5 then
                  case when too-many-nested-blocks <= 0.5 then
                    case when refactor_mle_diff <= -0.6030027717351913 then
                       return 0.0 # (0.0 out of 1.0)
                    else  # if refactor_mle_diff > -0.6030027717351913
                      case when vocabulary_diff <= -19.5 then
                        case when Comments_diff <= -3.5 then
                           return 1.0 # (1.0 out of 1.0)
                        else  # if Comments_diff > -3.5
                           return 0.0 # (0.0 out of 1.0)
                        end                       else  # if vocabulary_diff > -19.5
                         return 1.0 # (1.0 out of 1.0)
                      end                     end                   else  # if too-many-nested-blocks > 0.5
                     return 0.0 # (0.0 out of 1.0)
                  end                 else  # if too-many-return-statements > 0.5
                   return 0.0 # (0.0 out of 1.0)
                end               else  # if McCabe_sum_before > 68.5
                case when McCabe_sum_before <= 81.0 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if McCabe_sum_before > 81.0
                  case when changed_lines <= 99.5 then
                    case when one_file_fix_rate_diff <= -0.2045019157230854 then
                       return 0.0 # (0.0 out of 1.0)
                    else  # if one_file_fix_rate_diff > -0.2045019157230854
                      case when avg_coupling_code_size_cut_diff <= -1.126893937587738 then
                         return 0.0 # (0.0 out of 1.0)
                      else  # if avg_coupling_code_size_cut_diff > -1.126893937587738
                        case when McCabe_max_diff <= -5.5 then
                           return 0.0 # (0.0 out of 1.0)
                        else  # if McCabe_max_diff > -5.5
                          case when hunks_num <= 3.5 then
                            case when refactor_mle_diff <= -0.1250360943377018 then
                              case when McCabe_sum_diff <= -1.0 then
                                 return 1.0 # (1.0 out of 1.0)
                              else  # if McCabe_sum_diff > -1.0
                                 return 0.0 # (0.0 out of 1.0)
                              end                             else  # if refactor_mle_diff > -0.1250360943377018
                               return 1.0 # (1.0 out of 1.0)
                            end                           else  # if hunks_num > 3.5
                            case when Comments_after <= 58.5 then
                               return 1.0 # (1.0 out of 1.0)
                            else  # if Comments_after > 58.5
                               return 0.0 # (0.0 out of 1.0)
                            end                           end                         end                       end                     end                   else  # if changed_lines > 99.5
                    case when Blank_before <= 81.0 then
                      case when added_lines <= 74.5 then
                         return 1.0 # (1.0 out of 1.0)
                      else  # if added_lines > 74.5
                         return 0.0 # (0.0 out of 1.0)
                      end                     else  # if Blank_before > 81.0
                      case when Blank_diff <= -72.0 then
                         return 0.0 # (0.0 out of 1.0)
                      else  # if Blank_diff > -72.0
                         return 1.0 # (1.0 out of 1.0)
                      end                     end                   end                 end               end             end           else  # if SLOC_before > 1108.0
            case when removed_lines <= 63.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if removed_lines > 63.5
              case when avg_coupling_code_size_cut_diff <= 0.8333333134651184 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if avg_coupling_code_size_cut_diff > 0.8333333134651184
                 return 0.0 # (0.0 out of 1.0)
              end             end           end         else  # if same_day_duration_avg_diff > 260.30834197998047
           return 0.0 # (0.0 out of 1.0)
        end       else  # if low_ccp_group > 0.5
        case when LLOC_before <= 232.0 then
           return 0.0 # (0.0 out of 1.0)
        else  # if LLOC_before > 232.0
          case when same_day_duration_avg_diff <= -31.693363189697266 then
             return 0.0 # (0.0 out of 1.0)
          else  # if same_day_duration_avg_diff > -31.693363189697266
            case when h2_diff <= 1.5 then
              case when Single comments_after <= 7.5 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if Single comments_after > 7.5
                case when added_functions <= 1.5 then
                  case when removed_lines <= 6.0 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if removed_lines > 6.0
                    case when too-many-nested-blocks <= 0.5 then
                       return 1.0 # (1.0 out of 1.0)
                    else  # if too-many-nested-blocks > 0.5
                       return 0.0 # (0.0 out of 1.0)
                    end                   end                 else  # if added_functions > 1.5
                   return 0.0 # (0.0 out of 1.0)
                end               end             else  # if h2_diff > 1.5
               return 0.0 # (0.0 out of 1.0)
            end           end         end       end     else  # if prev_count > 2.5
       return 0.0 # (0.0 out of 1.0)
    end   else  # if hunks_num > 11.5
    case when removed_lines <= 68.5 then
       return 0.0 # (0.0 out of 1.0)
    else  # if removed_lines > 68.5
      case when Blank_diff <= -8.5 then
         return 0.0 # (0.0 out of 1.0)
      else  # if Blank_diff > -8.5
        case when one_file_fix_rate_diff <= 0.10000000149011612 then
          case when LLOC_before <= 284.5 then
             return 0.0 # (0.0 out of 1.0)
          else  # if LLOC_before > 284.5
             return 1.0 # (1.0 out of 1.0)
          end         else  # if one_file_fix_rate_diff > 0.10000000149011612
           return 0.0 # (0.0 out of 1.0)
        end       end     end   end )