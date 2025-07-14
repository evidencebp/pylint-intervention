create or replace function RandomForest_7 (effort_diff int64, too-many-nested-blocks int64, Single comments_diff int64, N1_diff int64, avg_coupling_code_size_cut_diff int64, Simplify-boolean-expression int64, try-except-raise int64, h1_diff int64, added_functions int64, too-many-boolean-expressions int64, LLOC_diff int64, cur_count_x int64, wildcard-import int64, mostly_delete int64, LOC_diff int64, difficulty_diff int64, Comments_before int64, prev_count_y int64, time_diff int64, pointless-statement int64, vocabulary_diff int64, modified_McCabe_max_diff int64, prev_count int64, McCabe_sum_before int64, McCabe_max_after int64, Blank_diff int64, using-constant-test int64, McCabe_max_before int64, is_refactor int64, Comments_after int64, SLOC_before int64, superfluous-parens int64, too-many-branches int64, massive_change int64, comparison-of-constants int64, broad-exception-caught int64, Blank_before int64, N2_diff int64, McCabe_sum_after int64, too-many-statements int64, refactor_mle_diff int64, LOC_before int64, simplifiable-if-statement int64, only_removal int64, h2_diff int64, unnecessary-semicolon int64, too-many-lines int64, LLOC_before int64, volume_diff int64, too-many-return-statements int64, high_ccp_group int64, Single comments_before int64, simplifiable-if-expression int64, changed_lines int64, Multi_diff int64, one_file_fix_rate_diff int64, prev_count_x int64, simplifiable-condition int64, cur_count_y int64, calculated_length_diff int64, SLOC_diff int64, line-too-long int64, McCabe_max_diff int64, Comments_diff int64, cur_count int64, Single comments_after int64, removed_lines int64, added_lines int64, length_diff int64, unnecessary-pass int64, hunks_num int64, bugs_diff int64, same_day_duration_avg_diff int64, McCabe_sum_diff int64) as (
  case when removed_lines <= 57.0 then
    case when Comments_diff <= 1.5 then
      case when Comments_after <= 1.5 then
         return 0.8888888888888888 # (16.0 out of 18.0)
      else  # if Comments_after > 1.5
        case when Blank_before <= 50.5 then
          case when LLOC_diff <= -32.0 then
             return 0.0 # (0.0 out of 25.0)
          else  # if LLOC_diff > -32.0
            case when Comments_after <= 18.5 then
              case when Comments_before <= 9.5 then
                 return 0.2857142857142857 # (4.0 out of 14.0)
              else  # if Comments_before > 9.5
                 return 0.5555555555555556 # (10.0 out of 18.0)
              end             else  # if Comments_after > 18.5
               return 0.13333333333333333 # (2.0 out of 15.0)
            end           end         else  # if Blank_before > 50.5
          case when avg_coupling_code_size_cut_diff <= -1.2053571343421936 then
            case when Single comments_before <= 47.0 then
               return 0.0 # (0.0 out of 20.0)
            else  # if Single comments_before > 47.0
              case when SLOC_before <= 834.5 then
                 return 0.25 # (4.0 out of 16.0)
              else  # if SLOC_before > 834.5
                 return 0.6 # (9.0 out of 15.0)
              end             end           else  # if avg_coupling_code_size_cut_diff > -1.2053571343421936
            case when hunks_num <= 10.5 then
              case when removed_lines <= 11.5 then
                case when avg_coupling_code_size_cut_diff <= 0.5835084021091461 then
                  case when SLOC_before <= 913.5 then
                    case when McCabe_max_before <= 12.5 then
                       return 0.8888888888888888 # (24.0 out of 27.0)
                    else  # if McCabe_max_before > 12.5
                      case when same_day_duration_avg_diff <= 34.90612602233887 then
                         return 0.8260869565217391 # (19.0 out of 23.0)
                      else  # if same_day_duration_avg_diff > 34.90612602233887
                         return 0.13333333333333333 # (2.0 out of 15.0)
                      end                     end                   else  # if SLOC_before > 913.5
                     return 0.38095238095238093 # (8.0 out of 21.0)
                  end                 else  # if avg_coupling_code_size_cut_diff > 0.5835084021091461
                  case when Comments_diff <= -0.5 then
                     return 0.0625 # (1.0 out of 16.0)
                  else  # if Comments_diff > -0.5
                    case when McCabe_sum_before <= 134.5 then
                       return 0.26666666666666666 # (4.0 out of 15.0)
                    else  # if McCabe_sum_before > 134.5
                       return 0.25 # (4.0 out of 16.0)
                    end                   end                 end               else  # if removed_lines > 11.5
                case when same_day_duration_avg_diff <= -35.08359146118164 then
                   return 0.4583333333333333 # (11.0 out of 24.0)
                else  # if same_day_duration_avg_diff > -35.08359146118164
                  case when refactor_mle_diff <= -0.05554475076496601 then
                     return 1.0 # (31.0 out of 31.0)
                  else  # if refactor_mle_diff > -0.05554475076496601
                     return 0.6923076923076923 # (9.0 out of 13.0)
                  end                 end               end             else  # if hunks_num > 10.5
               return 0.15 # (3.0 out of 20.0)
            end           end         end       end     else  # if Comments_diff > 1.5
      case when McCabe_sum_diff <= -0.5 then
         return 0.05555555555555555 # (1.0 out of 18.0)
      else  # if McCabe_sum_diff > -0.5
         return 0.03225806451612903 # (1.0 out of 31.0)
      end     end   else  # if removed_lines > 57.0
    case when added_functions <= 7.5 then
      case when changed_lines <= 528.5 then
        case when removed_lines <= 161.0 then
          case when h2_diff <= -14.0 then
             return 1.0 # (22.0 out of 22.0)
          else  # if h2_diff > -14.0
            case when Comments_diff <= 3.0 then
              case when refactor_mle_diff <= -0.04788888990879059 then
                 return 0.9565217391304348 # (22.0 out of 23.0)
              else  # if refactor_mle_diff > -0.04788888990879059
                case when Comments_before <= 38.0 then
                   return 0.875 # (14.0 out of 16.0)
                else  # if Comments_before > 38.0
                   return 0.6470588235294118 # (11.0 out of 17.0)
                end               end             else  # if Comments_diff > 3.0
              case when Comments_diff <= 15.0 then
                 return 0.05555555555555555 # (1.0 out of 18.0)
              else  # if Comments_diff > 15.0
                 return 1.0 # (17.0 out of 17.0)
              end             end           end         else  # if removed_lines > 161.0
           return 0.4444444444444444 # (8.0 out of 18.0)
        end       else  # if changed_lines > 528.5
         return 0.25 # (7.0 out of 28.0)
      end     else  # if added_functions > 7.5
      case when changed_lines <= 655.5 then
         return 0.3076923076923077 # (4.0 out of 13.0)
      else  # if changed_lines > 655.5
         return 0.058823529411764705 # (1.0 out of 17.0)
      end     end   end )