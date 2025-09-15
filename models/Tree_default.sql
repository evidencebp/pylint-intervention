create or replace function Tree_default (same_day_duration_avg_diff int64, low_McCabe_max_before int64, Single comments_before int64, one_file_fix_rate_diff int64, length_diff int64, Comments_after int64, Single comments_diff int64, too-many-statements int64, cur_count int64, Comments_diff int64, bugs_diff int64, McCabe_max_after int64, h2_diff int64, low_ccp_group int64, changed_lines int64, high_McCabe_sum_before int64, volume_diff int64, Multi_diff int64, LLOC_before int64, high_McCabe_max_diff int64, hunks_num int64, LOC_before int64, calculated_length_diff int64, low_McCabe_sum_before int64, McCabe_sum_before int64, high_ccp_group int64, McCabe_max_before int64, mostly_delete int64, LLOC_diff int64, effort_diff int64, too-many-nested-blocks int64, cur_count_y int64, h1_diff int64, low_McCabe_max_diff int64, Single comments_after int64, massive_change int64, SLOC_diff int64, added_lines int64, prev_count_x int64, N2_diff int64, high_McCabe_sum_diff int64, Blank_diff int64, LOC_diff int64, new_function int64, prev_count int64, prev_count_y int64, SLOC_before int64, McCabe_sum_after int64, high_McCabe_max_before int64, avg_coupling_code_size_cut_diff int64, Blank_before int64, McCabe_max_diff int64, refactor_mle_diff int64, is_refactor int64, low_McCabe_sum_diff int64, added_functions int64, modified_McCabe_max_diff int64, too-many-branches int64, time_diff int64, only_removal int64, N1_diff int64, Comments_before int64, McCabe_sum_diff int64, vocabulary_diff int64, removed_lines int64, too-many-return-statements int64, difficulty_diff int64, cur_count_x int64) as (
  case when low_ccp_group <= 0.5 then
    case when Blank_before <= 53.5 then
      case when SLOC_diff <= -9.5 then
        case when too-many-branches <= 0.5 then
           return 0.0 # (0.0 out of 1.0)
        else  # if too-many-branches > 0.5
           return 1.0 # (1.0 out of 1.0)
        end       else  # if SLOC_diff > -9.5
        case when too-many-return-statements <= 0.5 then
          case when too-many-nested-blocks <= 0.5 then
             return 1.0 # (1.0 out of 1.0)
          else  # if too-many-nested-blocks > 0.5
            case when refactor_mle_diff <= -0.015392857603728771 then
               return 0.0 # (0.0 out of 1.0)
            else  # if refactor_mle_diff > -0.015392857603728771
               return 1.0 # (1.0 out of 1.0)
            end           end         else  # if too-many-return-statements > 0.5
           return 0.0 # (0.0 out of 1.0)
        end       end     else  # if Blank_before > 53.5
      case when same_day_duration_avg_diff <= -103.56983184814453 then
        case when N2_diff <= -79.5 then
           return 0.0 # (0.0 out of 1.0)
        else  # if N2_diff > -79.5
           return 1.0 # (1.0 out of 1.0)
        end       else  # if same_day_duration_avg_diff > -103.56983184814453
        case when Single comments_before <= 114.5 then
          case when Blank_before <= 87.5 then
            case when McCabe_max_after <= 28.5 then
              case when McCabe_sum_before <= 46.5 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if McCabe_sum_before > 46.5
                 return 0.0 # (0.0 out of 1.0)
              end             else  # if McCabe_max_after > 28.5
              case when one_file_fix_rate_diff <= -0.194581288844347 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if one_file_fix_rate_diff > -0.194581288844347
                case when N2_diff <= -13.5 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if N2_diff > -13.5
                   return 1.0 # (1.0 out of 1.0)
                end               end             end           else  # if Blank_before > 87.5
            case when McCabe_max_after <= 17.5 then
              case when hunks_num <= 11.0 then
                case when changed_lines <= 50.5 then
                  case when refactor_mle_diff <= -0.234128899872303 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if refactor_mle_diff > -0.234128899872303
                    case when Comments_before <= 53.0 then
                       return 1.0 # (1.0 out of 1.0)
                    else  # if Comments_before > 53.0
                      case when Blank_before <= 189.0 then
                         return 0.0 # (0.0 out of 1.0)
                      else  # if Blank_before > 189.0
                         return 1.0 # (1.0 out of 1.0)
                      end                     end                   end                 else  # if changed_lines > 50.5
                   return 1.0 # (1.0 out of 1.0)
                end               else  # if hunks_num > 11.0
                 return 0.0 # (0.0 out of 1.0)
              end             else  # if McCabe_max_after > 17.5
              case when high_ccp_group <= 0.5 then
                case when too-many-statements <= 0.5 then
                  case when Comments_after <= 72.5 then
                     return 1.0 # (1.0 out of 1.0)
                  else  # if Comments_after > 72.5
                     return 0.0 # (0.0 out of 1.0)
                  end                 else  # if too-many-statements > 0.5
                   return 0.0 # (0.0 out of 1.0)
                end               else  # if high_ccp_group > 0.5
                case when refactor_mle_diff <= -0.13844040036201477 then
                  case when Comments_before <= 47.5 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if Comments_before > 47.5
                     return 1.0 # (1.0 out of 1.0)
                  end                 else  # if refactor_mle_diff > -0.13844040036201477
                  case when one_file_fix_rate_diff <= -0.08379121124744415 then
                    case when high_McCabe_max_before <= 0.5 then
                       return 0.0 # (0.0 out of 1.0)
                    else  # if high_McCabe_max_before > 0.5
                       return 1.0 # (1.0 out of 1.0)
                    end                   else  # if one_file_fix_rate_diff > -0.08379121124744415
                     return 1.0 # (1.0 out of 1.0)
                  end                 end               end             end           end         else  # if Single comments_before > 114.5
          case when modified_McCabe_max_diff <= -35.5 then
             return 1.0 # (1.0 out of 1.0)
          else  # if modified_McCabe_max_diff > -35.5
            case when avg_coupling_code_size_cut_diff <= 1.9090805053710938 then
               return 0.0 # (0.0 out of 1.0)
            else  # if avg_coupling_code_size_cut_diff > 1.9090805053710938
              case when SLOC_before <= 1297.5 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if SLOC_before > 1297.5
                 return 0.0 # (0.0 out of 1.0)
              end             end           end         end       end     end   else  # if low_ccp_group > 0.5
    case when Single comments_diff <= -18.5 then
       return 1.0 # (1.0 out of 1.0)
    else  # if Single comments_diff > -18.5
      case when Single comments_before <= 290.5 then
        case when same_day_duration_avg_diff <= 658.5833282470703 then
          case when refactor_mle_diff <= 0.4816414415836334 then
            case when one_file_fix_rate_diff <= 0.4833333343267441 then
               return 0.0 # (0.0 out of 1.0)
            else  # if one_file_fix_rate_diff > 0.4833333343267441
              case when modified_McCabe_max_diff <= -1.0 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if modified_McCabe_max_diff > -1.0
                 return 1.0 # (1.0 out of 1.0)
              end             end           else  # if refactor_mle_diff > 0.4816414415836334
            case when LLOC_before <= 541.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if LLOC_before > 541.5
               return 1.0 # (1.0 out of 1.0)
            end           end         else  # if same_day_duration_avg_diff > 658.5833282470703
           return 1.0 # (1.0 out of 1.0)
        end       else  # if Single comments_before > 290.5
        case when added_functions <= 0.5 then
           return 0.0 # (0.0 out of 1.0)
        else  # if added_functions > 0.5
           return 1.0 # (1.0 out of 1.0)
        end       end     end   end )