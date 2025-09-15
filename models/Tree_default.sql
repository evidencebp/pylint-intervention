create or replace function Tree_default (N1_diff int64, Single comments_diff int64, h2_diff int64, new_function int64, added_lines int64, difficulty_diff int64, too-many-return-statements int64, effort_diff int64, length_diff int64, McCabe_sum_after int64, removed_lines int64, McCabe_sum_before int64, low_McCabe_sum_before int64, high_McCabe_max_diff int64, prev_count_x int64, prev_count int64, LOC_before int64, SLOC_diff int64, low_McCabe_sum_diff int64, cur_count int64, calculated_length_diff int64, Blank_before int64, Comments_after int64, bugs_diff int64, too-many-statements int64, volume_diff int64, only_removal int64, too-many-branches int64, low_McCabe_max_diff int64, low_McCabe_max_before int64, McCabe_max_diff int64, is_refactor int64, cur_count_x int64, Single comments_before int64, McCabe_max_after int64, Blank_diff int64, McCabe_max_before int64, added_functions int64, Multi_diff int64, SLOC_before int64, prev_count_y int64, massive_change int64, LOC_diff int64, time_diff int64, h1_diff int64, vocabulary_diff int64, LLOC_diff int64, high_ccp_group int64, hunks_num int64, Single comments_after int64, high_McCabe_sum_before int64, modified_McCabe_max_diff int64, N2_diff int64, same_day_duration_avg_diff int64, low_ccp_group int64, Comments_before int64, cur_count_y int64, high_McCabe_sum_diff int64, changed_lines int64, high_McCabe_max_before int64, Comments_diff int64, LLOC_before int64, one_file_fix_rate_diff int64, too-many-nested-blocks int64, McCabe_sum_diff int64, refactor_mle_diff int64, avg_coupling_code_size_cut_diff int64, mostly_delete int64) as (
  case when low_ccp_group <= 0.5 then
    case when LOC_before <= 377.5 then
      case when Single comments_after <= 55.5 then
        case when too-many-nested-blocks <= 0.5 then
          case when refactor_mle_diff <= -0.5633785724639893 then
            case when Blank_diff <= -1.5 then
               return 1.0 # (1.0 out of 1.0)
            else  # if Blank_diff > -1.5
               return 0.0 # (0.0 out of 1.0)
            end           else  # if refactor_mle_diff > -0.5633785724639893
             return 1.0 # (1.0 out of 1.0)
          end         else  # if too-many-nested-blocks > 0.5
          case when length_diff <= -8.5 then
             return 0.0 # (0.0 out of 1.0)
          else  # if length_diff > -8.5
             return 1.0 # (1.0 out of 1.0)
          end         end       else  # if Single comments_after > 55.5
         return 0.0 # (0.0 out of 1.0)
      end     else  # if LOC_before > 377.5
      case when one_file_fix_rate_diff <= -0.10583669319748878 then
        case when McCabe_sum_after <= 151.0 then
          case when refactor_mle_diff <= 0.47453536093235016 then
            case when Single comments_before <= 13.5 then
               return 1.0 # (1.0 out of 1.0)
            else  # if Single comments_before > 13.5
               return 0.0 # (0.0 out of 1.0)
            end           else  # if refactor_mle_diff > 0.47453536093235016
             return 1.0 # (1.0 out of 1.0)
          end         else  # if McCabe_sum_after > 151.0
          case when SLOC_before <= 954.0 then
            case when refactor_mle_diff <= 0.1098703034222126 then
               return 1.0 # (1.0 out of 1.0)
            else  # if refactor_mle_diff > 0.1098703034222126
               return 0.0 # (0.0 out of 1.0)
            end           else  # if SLOC_before > 954.0
            case when McCabe_sum_after <= 225.0 then
               return 1.0 # (1.0 out of 1.0)
            else  # if McCabe_sum_after > 225.0
               return 0.0 # (0.0 out of 1.0)
            end           end         end       else  # if one_file_fix_rate_diff > -0.10583669319748878
        case when McCabe_max_after <= 12.5 then
          case when Comments_after <= 129.5 then
            case when same_day_duration_avg_diff <= -198.52777862548828 then
               return 0.0 # (0.0 out of 1.0)
            else  # if same_day_duration_avg_diff > -198.52777862548828
              case when hunks_num <= 1.5 then
                case when McCabe_sum_after <= 116.0 then
                   return 1.0 # (1.0 out of 1.0)
                else  # if McCabe_sum_after > 116.0
                   return 0.0 # (0.0 out of 1.0)
                end               else  # if hunks_num > 1.5
                 return 1.0 # (1.0 out of 1.0)
              end             end           else  # if Comments_after > 129.5
             return 0.0 # (0.0 out of 1.0)
          end         else  # if McCabe_max_after > 12.5
          case when same_day_duration_avg_diff <= -86.25 then
            case when McCabe_max_after <= 13.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if McCabe_max_after > 13.5
               return 1.0 # (1.0 out of 1.0)
            end           else  # if same_day_duration_avg_diff > -86.25
            case when one_file_fix_rate_diff <= -0.0530753992497921 then
               return 1.0 # (1.0 out of 1.0)
            else  # if one_file_fix_rate_diff > -0.0530753992497921
              case when McCabe_sum_after <= 59.0 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if McCabe_sum_after > 59.0
                case when refactor_mle_diff <= 0.4425845444202423 then
                  case when vocabulary_diff <= 13.0 then
                    case when SLOC_before <= 568.5 then
                       return 0.0 # (0.0 out of 1.0)
                    else  # if SLOC_before > 568.5
                      case when LOC_before <= 876.0 then
                         return 1.0 # (1.0 out of 1.0)
                      else  # if LOC_before > 876.0
                        case when refactor_mle_diff <= 0.13911614194512367 then
                          case when LOC_diff <= 21.0 then
                             return 0.0 # (0.0 out of 1.0)
                          else  # if LOC_diff > 21.0
                             return 1.0 # (1.0 out of 1.0)
                          end                         else  # if refactor_mle_diff > 0.13911614194512367
                          case when avg_coupling_code_size_cut_diff <= 0.8333333134651184 then
                             return 1.0 # (1.0 out of 1.0)
                          else  # if avg_coupling_code_size_cut_diff > 0.8333333134651184
                             return 0.0 # (0.0 out of 1.0)
                          end                         end                       end                     end                   else  # if vocabulary_diff > 13.0
                     return 1.0 # (1.0 out of 1.0)
                  end                 else  # if refactor_mle_diff > 0.4425845444202423
                   return 1.0 # (1.0 out of 1.0)
                end               end             end           end         end       end     end   else  # if low_ccp_group > 0.5
    case when Single comments_diff <= -18.5 then
       return 1.0 # (1.0 out of 1.0)
    else  # if Single comments_diff > -18.5
      case when Comments_diff <= 20.5 then
        case when McCabe_sum_before <= 526.0 then
          case when same_day_duration_avg_diff <= 658.5833282470703 then
            case when modified_McCabe_max_diff <= 0.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if modified_McCabe_max_diff > 0.5
              case when McCabe_max_before <= 18.5 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if McCabe_max_before > 18.5
                 return 0.0 # (0.0 out of 1.0)
              end             end           else  # if same_day_duration_avg_diff > 658.5833282470703
             return 1.0 # (1.0 out of 1.0)
          end         else  # if McCabe_sum_before > 526.0
          case when Comments_before <= 461.5 then
             return 1.0 # (1.0 out of 1.0)
          else  # if Comments_before > 461.5
             return 0.0 # (0.0 out of 1.0)
          end         end       else  # if Comments_diff > 20.5
         return 1.0 # (1.0 out of 1.0)
      end     end   end )