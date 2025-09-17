create or replace function Tree_default (length_diff int64, N1_diff int64, N2_diff int64, McCabe_sum_diff int64, bugs_diff int64, McCabe_sum_after int64, too-many-branches int64, is_refactor int64, high_ccp_group int64, mostly_delete int64, cur_count_y int64, low_ccp_group int64, prev_count_x int64, difficulty_diff int64, removed_lines int64, Blank_before int64, LOC_before int64, low_McCabe_sum_before int64, cur_count_x int64, Comments_diff int64, Comments_before int64, h2_diff int64, Comments_after int64, McCabe_sum_before int64, McCabe_max_after int64, high_McCabe_max_diff int64, added_functions int64, SLOC_diff int64, avg_coupling_code_size_cut_diff int64, too-many-nested-blocks int64, changed_lines int64, high_McCabe_sum_before int64, prev_count int64, high_McCabe_sum_diff int64, vocabulary_diff int64, SLOC_before int64, LOC_diff int64, low_McCabe_max_diff int64, Single comments_before int64, one_file_fix_rate_diff int64, too-many-statements int64, added_lines int64, new_function int64, massive_change int64, LLOC_before int64, calculated_length_diff int64, Single comments_diff int64, modified_McCabe_max_diff int64, McCabe_max_before int64, LLOC_diff int64, refactor_mle_diff int64, low_McCabe_sum_diff int64, hunks_num int64, low_McCabe_max_before int64, too-many-return-statements int64, only_removal int64, same_day_duration_avg_diff int64, h1_diff int64, time_diff int64, prev_count_y int64, effort_diff int64, Multi_diff int64, Blank_diff int64, cur_count int64, volume_diff int64, high_McCabe_max_before int64, Single comments_after int64, McCabe_max_diff int64) as (
  case when Single comments_diff <= -2.5 then
    case when avg_coupling_code_size_cut_diff <= 0.5208333432674408 then
      case when changed_lines <= 137.0 then
        case when hunks_num <= 6.5 then
          case when hunks_num <= 2.5 then
             return 1.0 # (1.0 out of 1.0)
          else  # if hunks_num > 2.5
            case when avg_coupling_code_size_cut_diff <= 0.1666666716337204 then
               return 0.0 # (0.0 out of 1.0)
            else  # if avg_coupling_code_size_cut_diff > 0.1666666716337204
               return 1.0 # (1.0 out of 1.0)
            end           end         else  # if hunks_num > 6.5
           return 1.0 # (1.0 out of 1.0)
        end       else  # if changed_lines > 137.0
        case when McCabe_max_diff <= -2.5 then
           return 1.0 # (1.0 out of 1.0)
        else  # if McCabe_max_diff > -2.5
          case when modified_McCabe_max_diff <= -3.0 then
             return 1.0 # (1.0 out of 1.0)
          else  # if modified_McCabe_max_diff > -3.0
             return 0.0 # (0.0 out of 1.0)
          end         end       end     else  # if avg_coupling_code_size_cut_diff > 0.5208333432674408
      case when modified_McCabe_max_diff <= -38.5 then
         return 1.0 # (1.0 out of 1.0)
      else  # if modified_McCabe_max_diff > -38.5
        case when LOC_diff <= -112.5 then
           return 0.0 # (0.0 out of 1.0)
        else  # if LOC_diff > -112.5
          case when Comments_diff <= -4.0 then
             return 1.0 # (1.0 out of 1.0)
          else  # if Comments_diff > -4.0
             return 0.0 # (0.0 out of 1.0)
          end         end       end     end   else  # if Single comments_diff > -2.5
    case when LOC_diff <= 60.0 then
      case when low_ccp_group <= 0.5 then
        case when LOC_before <= 467.5 then
          case when Comments_before <= 39.5 then
            case when LLOC_diff <= -16.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if LLOC_diff > -16.5
              case when removed_lines <= 8.5 then
                case when refactor_mle_diff <= -0.4925714358687401 then
                   return 0.0 # (0.0 out of 1.0)
                else  # if refactor_mle_diff > -0.4925714358687401
                  case when refactor_mle_diff <= 0.15703824162483215 then
                    case when too-many-nested-blocks <= 0.5 then
                       return 1.0 # (1.0 out of 1.0)
                    else  # if too-many-nested-blocks > 0.5
                       return 0.0 # (0.0 out of 1.0)
                    end                   else  # if refactor_mle_diff > 0.15703824162483215
                     return 0.0 # (0.0 out of 1.0)
                  end                 end               else  # if removed_lines > 8.5
                 return 1.0 # (1.0 out of 1.0)
              end             end           else  # if Comments_before > 39.5
             return 0.0 # (0.0 out of 1.0)
          end         else  # if LOC_before > 467.5
          case when one_file_fix_rate_diff <= -0.0055555556900799274 then
            case when changed_lines <= 6.5 then
              case when same_day_duration_avg_diff <= 7.796730041503906 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if same_day_duration_avg_diff > 7.796730041503906
                 return 0.0 # (0.0 out of 1.0)
              end             else  # if changed_lines > 6.5
               return 0.0 # (0.0 out of 1.0)
            end           else  # if one_file_fix_rate_diff > -0.0055555556900799274
            case when avg_coupling_code_size_cut_diff <= -1.064393937587738 then
               return 0.0 # (0.0 out of 1.0)
            else  # if avg_coupling_code_size_cut_diff > -1.064393937587738
              case when hunks_num <= 3.5 then
                case when avg_coupling_code_size_cut_diff <= 0.7224026024341583 then
                  case when refactor_mle_diff <= 0.5295142978429794 then
                     return 1.0 # (1.0 out of 1.0)
                  else  # if refactor_mle_diff > 0.5295142978429794
                     return 0.0 # (0.0 out of 1.0)
                  end                 else  # if avg_coupling_code_size_cut_diff > 0.7224026024341583
                  case when removed_lines <= 3.0 then
                     return 0.0 # (0.0 out of 1.0)
                  else  # if removed_lines > 3.0
                     return 1.0 # (1.0 out of 1.0)
                  end                 end               else  # if hunks_num > 3.5
                case when SLOC_diff <= 14.5 then
                  case when vocabulary_diff <= -13.5 then
                    case when added_lines <= 261.5 then
                       return 1.0 # (1.0 out of 1.0)
                    else  # if added_lines > 261.5
                       return 0.0 # (0.0 out of 1.0)
                    end                   else  # if vocabulary_diff > -13.5
                    case when avg_coupling_code_size_cut_diff <= -0.9791666567325592 then
                       return 1.0 # (1.0 out of 1.0)
                    else  # if avg_coupling_code_size_cut_diff > -0.9791666567325592
                       return 0.0 # (0.0 out of 1.0)
                    end                   end                 else  # if SLOC_diff > 14.5
                   return 1.0 # (1.0 out of 1.0)
                end               end             end           end         end       else  # if low_ccp_group > 0.5
        case when McCabe_sum_before <= 275.0 then
          case when modified_McCabe_max_diff <= 0.5 then
             return 0.0 # (0.0 out of 1.0)
          else  # if modified_McCabe_max_diff > 0.5
            case when one_file_fix_rate_diff <= 0.1666666716337204 then
               return 0.0 # (0.0 out of 1.0)
            else  # if one_file_fix_rate_diff > 0.1666666716337204
               return 1.0 # (1.0 out of 1.0)
            end           end         else  # if McCabe_sum_before > 275.0
          case when LLOC_diff <= -8.0 then
             return 0.0 # (0.0 out of 1.0)
          else  # if LLOC_diff > -8.0
             return 1.0 # (1.0 out of 1.0)
          end         end       end     else  # if LOC_diff > 60.0
      case when LOC_diff <= 199.5 then
         return 1.0 # (1.0 out of 1.0)
      else  # if LOC_diff > 199.5
        case when low_McCabe_max_before <= 0.5 then
           return 0.0 # (0.0 out of 1.0)
        else  # if low_McCabe_max_before > 0.5
           return 1.0 # (1.0 out of 1.0)
        end       end     end   end )