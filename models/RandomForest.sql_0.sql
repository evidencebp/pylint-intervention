create or replace function RandomForest_0 (SLOC_before int64, simplifiable-condition int64, bugs_diff int64, Blank_before int64, LLOC_diff int64, try-except-raise int64, LLOC_before int64, changed_lines int64, h2_diff int64, prev_count_x int64, too-many-lines int64, cur_count_y int64, Comments_before int64, McCabe_sum_after int64, cur_count_x int64, vocabulary_diff int64, Single comments_before int64, N2_diff int64, high_ccp_group int64, massive_change int64, added_lines int64, prev_count int64, refactor_mle_diff int64, superfluous-parens int64, avg_coupling_code_size_cut_diff int64, McCabe_sum_diff int64, LOC_before int64, too-many-return-statements int64, too-many-branches int64, too-many-nested-blocks int64, difficulty_diff int64, time_diff int64, Single comments_after int64, calculated_length_diff int64, Simplify-boolean-expression int64, unnecessary-semicolon int64, mostly_delete int64, effort_diff int64, Multi_diff int64, McCabe_max_diff int64, is_refactor int64, only_removal int64, LOC_diff int64, one_file_fix_rate_diff int64, Comments_after int64, comparison-of-constants int64, McCabe_max_after int64, length_diff int64, simplifiable-if-statement int64, removed_lines int64, unnecessary-pass int64, Comments_diff int64, cur_count int64, same_day_duration_avg_diff int64, hunks_num int64, N1_diff int64, line-too-long int64, volume_diff int64, using-constant-test int64, too-many-boolean-expressions int64, modified_McCabe_max_diff int64, h1_diff int64, added_functions int64, SLOC_diff int64, too-many-statements int64, pointless-statement int64, wildcard-import int64, McCabe_max_before int64, prev_count_y int64, broad-exception-caught int64, Blank_diff int64, McCabe_sum_before int64, simplifiable-if-expression int64, Single comments_diff int64) as (
  case when avg_coupling_code_size_cut_diff <= 0.014798607211560011 then
    case when too-many-nested-blocks <= 0.5 then
      case when one_file_fix_rate_diff <= 0.1695970743894577 then
        case when Blank_before <= 29.5 then
          case when LLOC_before <= 148.5 then
             return 1.0 # (33.0 out of 33.0)
          else  # if LLOC_before > 148.5
             return 0.9411764705882353 # (16.0 out of 17.0)
          end         else  # if Blank_before > 29.5
          case when SLOC_diff <= -48.0 then
            case when avg_coupling_code_size_cut_diff <= -0.17895299196243286 then
              case when Comments_diff <= -5.5 then
                 return 0.95 # (19.0 out of 20.0)
              else  # if Comments_diff > -5.5
                 return 0.5714285714285714 # (8.0 out of 14.0)
              end             else  # if avg_coupling_code_size_cut_diff > -0.17895299196243286
               return 1.0 # (19.0 out of 19.0)
            end           else  # if SLOC_diff > -48.0
            case when removed_lines <= 76.5 then
              case when Comments_diff <= 1.5 then
                case when high_ccp_group <= 0.5 then
                  case when Single comments_after <= 91.0 then
                    case when N2_diff <= -1.0 then
                       return 0.1111111111111111 # (3.0 out of 27.0)
                    else  # if N2_diff > -1.0
                       return 0.4 # (8.0 out of 20.0)
                    end                   else  # if Single comments_after > 91.0
                     return 0.625 # (10.0 out of 16.0)
                  end                 else  # if high_ccp_group > 0.5
                   return 0.7894736842105263 # (15.0 out of 19.0)
                end               else  # if Comments_diff > 1.5
                 return 0.0 # (0.0 out of 24.0)
              end             else  # if removed_lines > 76.5
              case when removed_lines <= 160.0 then
                case when LOC_before <= 998.5 then
                   return 0.8 # (20.0 out of 25.0)
                else  # if LOC_before > 998.5
                   return 0.6 # (9.0 out of 15.0)
                end               else  # if removed_lines > 160.0
                 return 0.3333333333333333 # (8.0 out of 24.0)
              end             end           end         end       else  # if one_file_fix_rate_diff > 0.1695970743894577
        case when McCabe_max_after <= 7.5 then
           return 0.5333333333333333 # (8.0 out of 15.0)
        else  # if McCabe_max_after > 7.5
          case when changed_lines <= 16.5 then
             return 0.0 # (0.0 out of 14.0)
          else  # if changed_lines > 16.5
             return 0.2 # (5.0 out of 25.0)
          end         end       end     else  # if too-many-nested-blocks > 0.5
       return 0.25 # (5.0 out of 20.0)
    end   else  # if avg_coupling_code_size_cut_diff > 0.014798607211560011
    case when LLOC_before <= 649.0 then
      case when N1_diff <= -8.5 then
        case when added_lines <= 193.5 then
           return 0.0 # (0.0 out of 19.0)
        else  # if added_lines > 193.5
           return 0.4090909090909091 # (9.0 out of 22.0)
        end       else  # if N1_diff > -8.5
        case when avg_coupling_code_size_cut_diff <= 2.450000047683716 then
          case when added_lines <= 60.5 then
            case when Comments_after <= 44.5 then
              case when removed_lines <= 0.5 then
                 return 0.7368421052631579 # (14.0 out of 19.0)
              else  # if removed_lines > 0.5
                case when added_lines <= 11.0 then
                   return 0.35294117647058826 # (6.0 out of 17.0)
                else  # if added_lines > 11.0
                   return 0.55 # (11.0 out of 20.0)
                end               end             else  # if Comments_after > 44.5
               return 0.13636363636363635 # (3.0 out of 22.0)
            end           else  # if added_lines > 60.5
             return 0.8695652173913043 # (20.0 out of 23.0)
          end         else  # if avg_coupling_code_size_cut_diff > 2.450000047683716
           return 0.8076923076923077 # (21.0 out of 26.0)
        end       end     else  # if LLOC_before > 649.0
      case when LOC_before <= 1641.0 then
         return 0.030303030303030304 # (1.0 out of 33.0)
      else  # if LOC_before > 1641.0
        case when Comments_before <= 380.5 then
          case when same_day_duration_avg_diff <= -13.042247533798218 then
             return 0.5384615384615384 # (7.0 out of 13.0)
          else  # if same_day_duration_avg_diff > -13.042247533798218
             return 0.47368421052631576 # (9.0 out of 19.0)
          end         else  # if Comments_before > 380.5
           return 0.0 # (0.0 out of 20.0)
        end       end     end   end )