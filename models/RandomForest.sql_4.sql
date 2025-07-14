create or replace function RandomForest_4 (SLOC_before int64, simplifiable-condition int64, bugs_diff int64, Blank_before int64, LLOC_diff int64, try-except-raise int64, LLOC_before int64, changed_lines int64, h2_diff int64, prev_count_x int64, too-many-lines int64, cur_count_y int64, Comments_before int64, McCabe_sum_after int64, cur_count_x int64, vocabulary_diff int64, Single comments_before int64, N2_diff int64, high_ccp_group int64, massive_change int64, added_lines int64, prev_count int64, refactor_mle_diff int64, superfluous-parens int64, avg_coupling_code_size_cut_diff int64, McCabe_sum_diff int64, LOC_before int64, too-many-return-statements int64, too-many-branches int64, too-many-nested-blocks int64, difficulty_diff int64, time_diff int64, Single comments_after int64, calculated_length_diff int64, Simplify-boolean-expression int64, unnecessary-semicolon int64, mostly_delete int64, effort_diff int64, Multi_diff int64, McCabe_max_diff int64, is_refactor int64, only_removal int64, LOC_diff int64, one_file_fix_rate_diff int64, Comments_after int64, comparison-of-constants int64, McCabe_max_after int64, length_diff int64, simplifiable-if-statement int64, removed_lines int64, unnecessary-pass int64, Comments_diff int64, cur_count int64, same_day_duration_avg_diff int64, hunks_num int64, N1_diff int64, line-too-long int64, volume_diff int64, using-constant-test int64, too-many-boolean-expressions int64, modified_McCabe_max_diff int64, h1_diff int64, added_functions int64, SLOC_diff int64, too-many-statements int64, pointless-statement int64, wildcard-import int64, McCabe_max_before int64, prev_count_y int64, broad-exception-caught int64, Blank_diff int64, McCabe_sum_before int64, simplifiable-if-expression int64, Single comments_diff int64) as (
  case when LLOC_before <= 400.0 then
    case when LOC_before <= 822.0 then
      case when McCabe_max_after <= 7.5 then
        case when McCabe_sum_before <= 0.5 then
           return 1.0 # (18.0 out of 18.0)
        else  # if McCabe_sum_before > 0.5
          case when Single comments_diff <= -2.5 then
            case when h2_diff <= -8.0 then
               return 1.0 # (13.0 out of 13.0)
            else  # if h2_diff > -8.0
               return 0.8823529411764706 # (15.0 out of 17.0)
            end           else  # if Single comments_diff > -2.5
            case when McCabe_max_before <= 6.5 then
              case when LOC_before <= 190.0 then
                 return 0.75 # (18.0 out of 24.0)
              else  # if LOC_before > 190.0
                 return 0.4 # (6.0 out of 15.0)
              end             else  # if McCabe_max_before > 6.5
               return 0.45454545454545453 # (10.0 out of 22.0)
            end           end         end       else  # if McCabe_max_after > 7.5
        case when high_ccp_group <= 0.5 then
          case when McCabe_sum_after <= 57.0 then
            case when refactor_mle_diff <= -0.14021027833223343 then
               return 0.5454545454545454 # (6.0 out of 11.0)
            else  # if refactor_mle_diff > -0.14021027833223343
               return 0.5789473684210527 # (11.0 out of 19.0)
            end           else  # if McCabe_sum_after > 57.0
            case when McCabe_max_after <= 20.5 then
              case when Blank_before <= 69.5 then
                 return 0.0 # (0.0 out of 16.0)
              else  # if Blank_before > 69.5
                case when hunks_num <= 4.5 then
                   return 0.10526315789473684 # (2.0 out of 19.0)
                else  # if hunks_num > 4.5
                   return 0.29411764705882354 # (5.0 out of 17.0)
                end               end             else  # if McCabe_max_after > 20.5
               return 0.5625 # (9.0 out of 16.0)
            end           end         else  # if high_ccp_group > 0.5
          case when added_lines <= 37.5 then
             return 0.5384615384615384 # (7.0 out of 13.0)
          else  # if added_lines > 37.5
             return 0.88 # (22.0 out of 25.0)
          end         end       end     else  # if LOC_before > 822.0
      case when SLOC_diff <= -3.5 then
         return 0.6538461538461539 # (17.0 out of 26.0)
      else  # if SLOC_diff > -3.5
         return 1.0 # (22.0 out of 22.0)
      end     end   else  # if LLOC_before > 400.0
    case when SLOC_diff <= -105.0 then
      case when Blank_diff <= -28.5 then
        case when same_day_duration_avg_diff <= -37.71973991394043 then
           return 0.05555555555555555 # (1.0 out of 18.0)
        else  # if same_day_duration_avg_diff > -37.71973991394043
           return 0.7 # (14.0 out of 20.0)
        end       else  # if Blank_diff > -28.5
         return 0.9166666666666666 # (22.0 out of 24.0)
      end     else  # if SLOC_diff > -105.0
      case when superfluous-parens <= 0.5 then
        case when vocabulary_diff <= -5.5 then
          case when Blank_before <= 158.5 then
             return 0.0 # (0.0 out of 28.0)
          else  # if Blank_before > 158.5
             return 0.2 # (4.0 out of 20.0)
          end         else  # if vocabulary_diff > -5.5
          case when same_day_duration_avg_diff <= 126.11428451538086 then
            case when high_ccp_group <= 0.5 then
              case when N1_diff <= -1.5 then
                 return 0.5 # (9.0 out of 18.0)
              else  # if N1_diff > -1.5
                case when LLOC_before <= 484.0 then
                   return 0.3333333333333333 # (4.0 out of 12.0)
                else  # if LLOC_before > 484.0
                  case when LLOC_before <= 626.5 then
                     return 0.037037037037037035 # (1.0 out of 27.0)
                  else  # if LLOC_before > 626.5
                     return 0.19230769230769232 # (5.0 out of 26.0)
                  end                 end               end             else  # if high_ccp_group > 0.5
              case when removed_lines <= 37.5 then
                 return 0.7692307692307693 # (20.0 out of 26.0)
              else  # if removed_lines > 37.5
                 return 0.15384615384615385 # (2.0 out of 13.0)
              end             end           else  # if same_day_duration_avg_diff > 126.11428451538086
             return 0.0 # (0.0 out of 17.0)
          end         end       else  # if superfluous-parens > 0.5
        case when McCabe_max_after <= 33.5 then
          case when McCabe_sum_after <= 190.5 then
             return 0.46153846153846156 # (6.0 out of 13.0)
          else  # if McCabe_sum_after > 190.5
             return 0.9473684210526315 # (18.0 out of 19.0)
          end         else  # if McCabe_max_after > 33.5
           return 0.3076923076923077 # (8.0 out of 26.0)
        end       end     end   end )