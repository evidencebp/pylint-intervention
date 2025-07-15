create or replace function RandomForest_5 (using-constant-test int64, simplifiable-if-statement int64, Comments_after int64, same_day_duration_avg_diff int64, Single comments_before int64, one_file_fix_rate_diff int64, too-many-boolean-expressions int64, Single comments_diff int64, high_McCabe_sum_before int64, pointless-statement int64, bugs_diff int64, McCabe_max_before int64, length_diff int64, LOC_diff int64, N2_diff int64, superfluous-parens int64, too-many-nested-blocks int64, effort_diff int64, cur_count_x int64, high_McCabe_max_before int64, comparison-of-constants int64, SLOC_diff int64, hunks_num int64, high_McCabe_max_diff int64, prev_count int64, McCabe_sum_after int64, cur_count_y int64, refactor_mle_diff int64, too-many-return-statements int64, too-many-statements int64, too-many-lines int64, only_removal int64, removed_lines int64, cur_count int64, volume_diff int64, is_refactor int64, prev_count_y int64, calculated_length_diff int64, Simplify-boolean-expression int64, h1_diff int64, McCabe_max_diff int64, wildcard-import int64, McCabe_sum_before int64, line-too-long int64, N1_diff int64, too-many-branches int64, h2_diff int64, McCabe_max_after int64, unnecessary-pass int64, avg_coupling_code_size_cut_diff int64, high_ccp_group int64, vocabulary_diff int64, try-except-raise int64, broad-exception-caught int64, simplifiable-condition int64, LLOC_before int64, added_functions int64, LLOC_diff int64, difficulty_diff int64, McCabe_sum_diff int64, Multi_diff int64, massive_change int64, mostly_delete int64, Comments_before int64, changed_lines int64, Comments_diff int64, time_diff int64, Blank_before int64, high_McCabe_sum_diff int64, added_lines int64, prev_count_x int64, unnecessary-semicolon int64, Blank_diff int64, modified_McCabe_max_diff int64, Single comments_after int64, LOC_before int64, simplifiable-if-expression int64, SLOC_before int64) as (
  case when McCabe_sum_before <= 92.5 then
    case when LOC_before <= 190.0 then
      case when avg_coupling_code_size_cut_diff <= -0.19208194687962532 then
         return 0.7692307692307693 # (10.0 out of 13.0)
      else  # if avg_coupling_code_size_cut_diff > -0.19208194687962532
         return 0.84 # (21.0 out of 25.0)
      end     else  # if LOC_before > 190.0
      case when Single comments_before <= 4.5 then
         return 0.8 # (16.0 out of 20.0)
      else  # if Single comments_before > 4.5
        case when vocabulary_diff <= -32.5 then
           return 1.0 # (11.0 out of 11.0)
        else  # if vocabulary_diff > -32.5
          case when same_day_duration_avg_diff <= -21.075980186462402 then
            case when added_lines <= 44.5 then
               return 0.5 # (12.0 out of 24.0)
            else  # if added_lines > 44.5
               return 0.7916666666666666 # (19.0 out of 24.0)
            end           else  # if same_day_duration_avg_diff > -21.075980186462402
            case when Comments_diff <= 3.5 then
              case when refactor_mle_diff <= -0.20017500221729279 then
                 return 0.04 # (1.0 out of 25.0)
              else  # if refactor_mle_diff > -0.20017500221729279
                case when same_day_duration_avg_diff <= 22.051435470581055 then
                   return 0.058823529411764705 # (1.0 out of 17.0)
                else  # if same_day_duration_avg_diff > 22.051435470581055
                   return 0.391304347826087 # (9.0 out of 23.0)
                end               end             else  # if Comments_diff > 3.5
               return 0.8 # (12.0 out of 15.0)
            end           end         end       end     end   else  # if McCabe_sum_before > 92.5
    case when McCabe_max_diff <= -18.5 then
       return 1.0 # (16.0 out of 16.0)
    else  # if McCabe_max_diff > -18.5
      case when Single comments_after <= 262.5 then
        case when Comments_before <= 17.5 then
           return 0.6428571428571429 # (18.0 out of 28.0)
        else  # if Comments_before > 17.5
          case when McCabe_max_before <= 20.5 then
            case when McCabe_sum_diff <= -19.5 then
               return 0.75 # (9.0 out of 12.0)
            else  # if McCabe_sum_diff > -19.5
              case when h1_diff <= -0.5 then
                 return 0.6 # (9.0 out of 15.0)
              else  # if h1_diff > -0.5
                case when same_day_duration_avg_diff <= 31.477554321289062 then
                  case when length_diff <= -1.5 then
                     return 0.21739130434782608 # (5.0 out of 23.0)
                  else  # if length_diff > -1.5
                    case when same_day_duration_avg_diff <= -46.106672286987305 then
                       return 0.45 # (9.0 out of 20.0)
                    else  # if same_day_duration_avg_diff > -46.106672286987305
                       return 0.6818181818181818 # (15.0 out of 22.0)
                    end                   end                 else  # if same_day_duration_avg_diff > 31.477554321289062
                   return 0.1935483870967742 # (6.0 out of 31.0)
                end               end             end           else  # if McCabe_max_before > 20.5
            case when modified_McCabe_max_diff <= -1.5 then
              case when McCabe_sum_before <= 245.0 then
                 return 0.7 # (14.0 out of 20.0)
              else  # if McCabe_sum_before > 245.0
                 return 0.2608695652173913 # (6.0 out of 23.0)
              end             else  # if modified_McCabe_max_diff > -1.5
              case when SLOC_diff <= -2.5 then
                case when h2_diff <= -7.5 then
                   return 0.0 # (0.0 out of 39.0)
                else  # if h2_diff > -7.5
                   return 0.043478260869565216 # (1.0 out of 23.0)
                end               else  # if SLOC_diff > -2.5
                case when Comments_before <= 59.0 then
                   return 0.5384615384615384 # (14.0 out of 26.0)
                else  # if Comments_before > 59.0
                  case when LOC_diff <= 4.5 then
                     return 0.3333333333333333 # (8.0 out of 24.0)
                  else  # if LOC_diff > 4.5
                    case when SLOC_before <= 920.0 then
                       return 0.05555555555555555 # (1.0 out of 18.0)
                    else  # if SLOC_before > 920.0
                       return 0.15 # (3.0 out of 20.0)
                    end                   end                 end               end             end           end         end       else  # if Single comments_after > 262.5
        case when N1_diff <= -4.5 then
           return 0.5 # (9.0 out of 18.0)
        else  # if N1_diff > -4.5
           return 0.8 # (20.0 out of 25.0)
        end       end     end   end )