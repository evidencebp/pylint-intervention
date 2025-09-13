create or replace function RandomForest_1 (McCabe_sum_before int64, changed_lines int64, prev_count_y int64, mostly_delete int64, h1_diff int64, too-many-lines int64, low_McCabe_sum_before int64, length_diff int64, LOC_before int64, simplifiable-if-expression int64, added_functions int64, broad-exception-caught int64, simplifiable-condition int64, prev_count_x int64, McCabe_max_diff int64, SLOC_before int64, LLOC_before int64, low_McCabe_max_diff int64, bugs_diff int64, same_day_duration_avg_diff int64, cur_count_x int64, only_removal int64, McCabe_max_after int64, Single comments_after int64, low_ccp_group int64, one_file_fix_rate_diff int64, effort_diff int64, difficulty_diff int64, removed_lines int64, Comments_diff int64, too-many-boolean-expressions int64, refactor_mle_diff int64, high_McCabe_max_before int64, hunks_num int64, LOC_diff int64, SLOC_diff int64, cur_count_y int64, vocabulary_diff int64, using-constant-test int64, Simplify-boolean-expression int64, low_McCabe_max_before int64, high_McCabe_sum_diff int64, high_McCabe_sum_before int64, McCabe_max_before int64, Comments_after int64, McCabe_sum_diff int64, unnecessary-pass int64, avg_coupling_code_size_cut_diff int64, simplifiable-if-statement int64, is_refactor int64, volume_diff int64, added_lines int64, high_McCabe_max_diff int64, superfluous-parens int64, cur_count int64, low_McCabe_sum_diff int64, calculated_length_diff int64, Multi_diff int64, N2_diff int64, h2_diff int64, Single comments_before int64, McCabe_sum_after int64, N1_diff int64, too-many-statements int64, comparison-of-constants int64, pointless-statement int64, time_diff int64, prev_count int64, Single comments_diff int64, massive_change int64, Blank_diff int64, too-many-nested-blocks int64, Comments_before int64, modified_McCabe_max_diff int64, LLOC_diff int64, Blank_before int64, try-except-raise int64, too-many-branches int64, too-many-return-statements int64, unnecessary-semicolon int64, wildcard-import int64, high_ccp_group int64, line-too-long int64) as (
  case when LOC_diff <= 58.5 then
    case when Comments_after <= 1.5 then
       return 1.0 # (1.0 out of 1.0)
    else  # if Comments_after > 1.5
      case when hunks_num <= 10.5 then
        case when low_ccp_group <= 0.5 then
          case when Comments_after <= 108.5 then
            case when SLOC_diff <= -23.0 then
              case when McCabe_sum_before <= 305.5 then
                case when N2_diff <= -21.5 then
                   return 0.8709677419354839 # (0.8709677419354839 out of 1.0)
                else  # if N2_diff > -21.5
                  case when h2_diff <= -3.5 then
                     return 0.44 # (0.44 out of 1.0)
                  else  # if h2_diff > -3.5
                     return 0.782608695652174 # (0.782608695652174 out of 1.0)
                  end                 end               else  # if McCabe_sum_before > 305.5
                 return 0.26666666666666666 # (0.26666666666666666 out of 1.0)
              end             else  # if SLOC_diff > -23.0
              case when McCabe_max_diff <= -1.5 then
                case when Comments_diff <= -0.5 then
                   return 0.5 # (0.5 out of 1.0)
                else  # if Comments_diff > -0.5
                   return 0.7 # (0.7 out of 1.0)
                end               else  # if McCabe_max_diff > -1.5
                case when McCabe_sum_after <= 31.5 then
                   return 0.76 # (0.76 out of 1.0)
                else  # if McCabe_sum_after > 31.5
                  case when LOC_before <= 591.0 then
                    case when McCabe_sum_diff <= 0.5 then
                       return 0.34782608695652173 # (0.34782608695652173 out of 1.0)
                    else  # if McCabe_sum_diff > 0.5
                       return 0.09090909090909091 # (0.09090909090909091 out of 1.0)
                    end                   else  # if LOC_before > 591.0
                    case when McCabe_max_before <= 13.5 then
                       return 0.2857142857142857 # (0.2857142857142857 out of 1.0)
                    else  # if McCabe_max_before > 13.5
                      case when McCabe_sum_after <= 156.0 then
                         return 0.44 # (0.44 out of 1.0)
                      else  # if McCabe_sum_after > 156.0
                         return 0.8571428571428571 # (0.8571428571428571 out of 1.0)
                      end                     end                   end                 end               end             end           else  # if Comments_after > 108.5
            case when Blank_diff <= 0.5 then
              case when same_day_duration_avg_diff <= 28.95535659790039 then
                case when N1_diff <= -0.5 then
                   return 0.42105263157894735 # (0.42105263157894735 out of 1.0)
                else  # if N1_diff > -0.5
                   return 0.0 # (0.0 out of 1.0)
                end               else  # if same_day_duration_avg_diff > 28.95535659790039
                 return 0.7 # (0.7 out of 1.0)
              end             else  # if Blank_diff > 0.5
               return 0.65 # (0.65 out of 1.0)
            end           end         else  # if low_ccp_group > 0.5
          case when vocabulary_diff <= -43.0 then
             return 1.0 # (1.0 out of 1.0)
          else  # if vocabulary_diff > -43.0
            case when McCabe_max_before <= 8.5 then
               return 0.18181818181818182 # (0.18181818181818182 out of 1.0)
            else  # if McCabe_max_before > 8.5
              case when McCabe_max_after <= 12.5 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if McCabe_max_after > 12.5
                case when LOC_before <= 816.0 then
                   return 0.11764705882352941 # (0.11764705882352941 out of 1.0)
                else  # if LOC_before > 816.0
                   return 0.0 # (0.0 out of 1.0)
                end               end             end           end         end       else  # if hunks_num > 10.5
        case when same_day_duration_avg_diff <= -12.695863246917725 then
          case when Single comments_after <= 45.5 then
             return 0.5882352941176471 # (0.5882352941176471 out of 1.0)
          else  # if Single comments_after > 45.5
            case when changed_lines <= 184.5 then
               return 0.13333333333333333 # (0.13333333333333333 out of 1.0)
            else  # if changed_lines > 184.5
               return 0.3125 # (0.3125 out of 1.0)
            end           end         else  # if same_day_duration_avg_diff > -12.695863246917725
          case when LLOC_diff <= -0.5 then
            case when LOC_diff <= -26.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if LOC_diff > -26.5
               return 0.0625 # (0.0625 out of 1.0)
            end           else  # if LLOC_diff > -0.5
             return 0.2222222222222222 # (0.2222222222222222 out of 1.0)
          end         end       end     end   else  # if LOC_diff > 58.5
    case when Single comments_diff <= 3.5 then
       return 0.9 # (0.9 out of 1.0)
    else  # if Single comments_diff > 3.5
       return 0.4 # (0.4 out of 1.0)
    end   end )