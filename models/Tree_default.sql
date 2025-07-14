create or replace function Tree_default (hunks_num int64, McCabe_sum_after int64, added_lines int64, cur_count_y int64, changed_lines int64, N1_diff int64, added_functions int64, Single comments_before int64, McCabe_max_after int64, calculated_length_diff int64, h1_diff int64, difficulty_diff int64, too-many-nested-blocks int64, modified_McCabe_max_diff int64, removed_lines int64, prev_count int64, Blank_diff int64, prev_count_x int64, h2_diff int64, LLOC_before int64, Multi_diff int64, volume_diff int64, same_day_duration_avg_diff int64, N2_diff int64, one_file_fix_rate_diff int64, Comments_after int64, massive_change int64, Single comments_diff int64, Comments_before int64, SLOC_before int64, prev_count_y int64, vocabulary_diff int64, LOC_before int64, McCabe_sum_diff int64, high_ccp_group int64, McCabe_sum_before int64, is_refactor int64, cur_count_x int64, refactor_mle_diff int64, time_diff int64, bugs_diff int64, avg_coupling_code_size_cut_diff int64, LLOC_diff int64, Single comments_after int64, too-many-branches int64, McCabe_max_diff int64, too-many-statements int64, mostly_delete int64, effort_diff int64, length_diff int64, Blank_before int64, SLOC_diff int64, McCabe_max_before int64, LOC_diff int64, cur_count int64, too-many-return-statements int64, only_removal int64, Comments_diff int64) as (
  case when Single comments_diff <= -2.5 then
    case when removed_lines <= 12.5 then
      case when McCabe_sum_diff <= -24.0 then
         return 1.0 # (5.0 out of 5.0)
      else  # if McCabe_sum_diff > -24.0
         return 0.0 # (0.0 out of 13.0)
      end     else  # if removed_lines > 12.5
      case when McCabe_sum_before <= 355.0 then
        case when N2_diff <= 0.5 then
          case when Blank_diff <= -84.5 then
            case when LLOC_diff <= -626.5 then
               return 1.0 # (1.0 out of 1.0)
            else  # if LLOC_diff > -626.5
               return 0.0 # (0.0 out of 1.0)
            end           else  # if Blank_diff > -84.5
             return 1.0 # (35.0 out of 35.0)
          end         else  # if N2_diff > 0.5
           return 0.0 # (0.0 out of 2.0)
        end       else  # if McCabe_sum_before > 355.0
         return 0.0 # (0.0 out of 2.0)
      end     end   else  # if Single comments_diff > -2.5
    case when Blank_before <= 42.5 then
      case when length_diff <= -1.0 then
        case when N2_diff <= -4.5 then
           return 0.0 # (0.0 out of 6.0)
        else  # if N2_diff > -4.5
          case when LLOC_diff <= -4.5 then
             return 1.0 # (3.0 out of 3.0)
          else  # if LLOC_diff > -4.5
             return 0.0 # (0.0 out of 3.0)
          end         end       else  # if length_diff > -1.0
         return 1.0 # (15.0 out of 15.0)
      end     else  # if Blank_before > 42.5
      case when hunks_num <= 3.5 then
        case when LOC_before <= 837.5 then
          case when McCabe_max_diff <= -6.5 then
             return 0.0 # (0.0 out of 4.0)
          else  # if McCabe_max_diff > -6.5
            case when changed_lines <= 15.5 then
              case when McCabe_max_before <= 26.5 then
                case when one_file_fix_rate_diff <= 0.4115384668111801 then
                   return 0.0 # (0.0 out of 6.0)
                else  # if one_file_fix_rate_diff > 0.4115384668111801
                   return 1.0 # (1.0 out of 1.0)
                end               else  # if McCabe_max_before > 26.5
                 return 1.0 # (2.0 out of 2.0)
              end             else  # if changed_lines > 15.5
              case when Single comments_after <= 13.0 then
                case when added_lines <= 17.5 then
                   return 1.0 # (1.0 out of 1.0)
                else  # if added_lines > 17.5
                   return 0.0 # (0.0 out of 2.0)
                end               else  # if Single comments_after > 13.0
                 return 1.0 # (16.0 out of 16.0)
              end             end           end         else  # if LOC_before > 837.5
          case when high_ccp_group <= 0.5 then
            case when Blank_diff <= -15.5 then
               return 1.0 # (1.0 out of 1.0)
            else  # if Blank_diff > -15.5
              case when LLOC_before <= 406.0 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if LLOC_before > 406.0
                 return 0.0 # (0.0 out of 23.0)
              end             end           else  # if high_ccp_group > 0.5
            case when McCabe_sum_after <= 211.5 then
              case when one_file_fix_rate_diff <= 0.4833333343267441 then
                case when SLOC_diff <= -3.0 then
                  case when McCabe_sum_after <= 204.0 then
                     return 1.0 # (1.0 out of 1.0)
                  else  # if McCabe_sum_after > 204.0
                     return 0.0 # (0.0 out of 1.0)
                  end                 else  # if SLOC_diff > -3.0
                   return 0.0 # (0.0 out of 3.0)
                end               else  # if one_file_fix_rate_diff > 0.4833333343267441
                 return 1.0 # (1.0 out of 1.0)
              end             else  # if McCabe_sum_after > 211.5
               return 1.0 # (2.0 out of 2.0)
            end           end         end       else  # if hunks_num > 3.5
        case when Blank_before <= 478.0 then
          case when same_day_duration_avg_diff <= -105.83035659790039 then
             return 1.0 # (2.0 out of 2.0)
          else  # if same_day_duration_avg_diff > -105.83035659790039
            case when modified_McCabe_max_diff <= -26.5 then
              case when Comments_diff <= 5.5 then
                 return 1.0 # (2.0 out of 2.0)
              else  # if Comments_diff > 5.5
                 return 0.0 # (0.0 out of 1.0)
              end             else  # if modified_McCabe_max_diff > -26.5
              case when LLOC_before <= 423.0 then
                case when McCabe_sum_before <= 28.0 then
                   return 1.0 # (1.0 out of 1.0)
                else  # if McCabe_sum_before > 28.0
                   return 0.0 # (0.0 out of 42.0)
                end               else  # if LLOC_before > 423.0
                case when hunks_num <= 6.5 then
                  case when added_lines <= 16.5 then
                     return 0.0 # (0.0 out of 3.0)
                  else  # if added_lines > 16.5
                     return 1.0 # (5.0 out of 5.0)
                  end                 else  # if hunks_num > 6.5
                   return 0.0 # (0.0 out of 16.0)
                end               end             end           end         else  # if Blank_before > 478.0
          case when McCabe_sum_after <= 719.5 then
             return 1.0 # (3.0 out of 3.0)
          else  # if McCabe_sum_after > 719.5
            case when added_lines <= 43.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if added_lines > 43.5
              case when same_day_duration_avg_diff <= -12.407936573028564 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if same_day_duration_avg_diff > -12.407936573028564
                 return 1.0 # (1.0 out of 1.0)
              end             end           end         end       end     end   end )