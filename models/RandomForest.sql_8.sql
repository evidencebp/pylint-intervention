create or replace function RandomForest_8 (effort_diff int64, too-many-nested-blocks int64, Single comments_diff int64, N1_diff int64, avg_coupling_code_size_cut_diff int64, Simplify-boolean-expression int64, try-except-raise int64, h1_diff int64, added_functions int64, too-many-boolean-expressions int64, LLOC_diff int64, cur_count_x int64, wildcard-import int64, mostly_delete int64, LOC_diff int64, difficulty_diff int64, Comments_before int64, prev_count_y int64, time_diff int64, pointless-statement int64, vocabulary_diff int64, modified_McCabe_max_diff int64, prev_count int64, McCabe_sum_before int64, McCabe_max_after int64, Blank_diff int64, using-constant-test int64, McCabe_max_before int64, is_refactor int64, Comments_after int64, SLOC_before int64, superfluous-parens int64, too-many-branches int64, massive_change int64, comparison-of-constants int64, broad-exception-caught int64, Blank_before int64, N2_diff int64, McCabe_sum_after int64, too-many-statements int64, refactor_mle_diff int64, LOC_before int64, simplifiable-if-statement int64, only_removal int64, h2_diff int64, unnecessary-semicolon int64, too-many-lines int64, LLOC_before int64, volume_diff int64, too-many-return-statements int64, high_ccp_group int64, Single comments_before int64, simplifiable-if-expression int64, changed_lines int64, Multi_diff int64, one_file_fix_rate_diff int64, prev_count_x int64, simplifiable-condition int64, cur_count_y int64, calculated_length_diff int64, SLOC_diff int64, line-too-long int64, McCabe_max_diff int64, Comments_diff int64, cur_count int64, Single comments_after int64, removed_lines int64, added_lines int64, length_diff int64, unnecessary-pass int64, hunks_num int64, bugs_diff int64, same_day_duration_avg_diff int64, McCabe_sum_diff int64) as (
  case when Single comments_diff <= -16.5 then
    case when Multi_diff <= -58.0 then
       return 0.38461538461538464 # (5.0 out of 13.0)
    else  # if Multi_diff > -58.0
      case when McCabe_sum_after <= 91.5 then
         return 0.8571428571428571 # (12.0 out of 14.0)
      else  # if McCabe_sum_after > 91.5
         return 0.8947368421052632 # (17.0 out of 19.0)
      end     end   else  # if Single comments_diff > -16.5
    case when McCabe_sum_diff <= -14.5 then
      case when Comments_diff <= -6.0 then
         return 0.6086956521739131 # (14.0 out of 23.0)
      else  # if Comments_diff > -6.0
        case when SLOC_diff <= -54.5 then
          case when McCabe_sum_diff <= -29.0 then
             return 0.0 # (0.0 out of 18.0)
          else  # if McCabe_sum_diff > -29.0
             return 0.23529411764705882 # (4.0 out of 17.0)
          end         else  # if SLOC_diff > -54.5
           return 0.0 # (0.0 out of 20.0)
        end       end     else  # if McCabe_sum_diff > -14.5
      case when Single comments_before <= 25.5 then
        case when Comments_before <= 10.5 then
          case when Single comments_after <= 3.5 then
             return 0.7619047619047619 # (16.0 out of 21.0)
          else  # if Single comments_after > 3.5
            case when McCabe_max_before <= 10.5 then
               return 0.09090909090909091 # (2.0 out of 22.0)
            else  # if McCabe_max_before > 10.5
               return 0.45454545454545453 # (5.0 out of 11.0)
            end           end         else  # if Comments_before > 10.5
          case when McCabe_sum_after <= 152.5 then
            case when same_day_duration_avg_diff <= 15.213690757751465 then
              case when LOC_before <= 478.5 then
                 return 0.9032258064516129 # (28.0 out of 31.0)
              else  # if LOC_before > 478.5
                 return 0.85 # (17.0 out of 20.0)
              end             else  # if same_day_duration_avg_diff > 15.213690757751465
               return 0.5333333333333333 # (8.0 out of 15.0)
            end           else  # if McCabe_sum_after > 152.5
             return 0.4666666666666667 # (7.0 out of 15.0)
          end         end       else  # if Single comments_before > 25.5
        case when one_file_fix_rate_diff <= 0.010869565419852734 then
          case when Comments_diff <= 19.0 then
            case when McCabe_sum_diff <= -6.5 then
              case when Single comments_before <= 64.0 then
                 return 0.8125 # (13.0 out of 16.0)
              else  # if Single comments_before > 64.0
                 return 0.35714285714285715 # (5.0 out of 14.0)
              end             else  # if McCabe_sum_diff > -6.5
              case when McCabe_sum_after <= 359.5 then
                case when McCabe_max_before <= 6.5 then
                   return 0.56 # (14.0 out of 25.0)
                else  # if McCabe_max_before > 6.5
                  case when LOC_before <= 387.0 then
                     return 0.42857142857142855 # (6.0 out of 14.0)
                  else  # if LOC_before > 387.0
                    case when McCabe_sum_before <= 191.0 then
                      case when Blank_before <= 117.5 then
                         return 0.0 # (0.0 out of 58.0)
                      else  # if Blank_before > 117.5
                        case when Comments_diff <= 0.5 then
                           return 0.2962962962962963 # (8.0 out of 27.0)
                        else  # if Comments_diff > 0.5
                           return 0.058823529411764705 # (1.0 out of 17.0)
                        end                       end                     else  # if McCabe_sum_before > 191.0
                      case when McCabe_sum_before <= 237.0 then
                         return 0.4117647058823529 # (7.0 out of 17.0)
                      else  # if McCabe_sum_before > 237.0
                         return 0.19230769230769232 # (5.0 out of 26.0)
                      end                     end                   end                 end               else  # if McCabe_sum_after > 359.5
                 return 0.7083333333333334 # (17.0 out of 24.0)
              end             end           else  # if Comments_diff > 19.0
             return 0.9 # (18.0 out of 20.0)
          end         else  # if one_file_fix_rate_diff > 0.010869565419852734
          case when McCabe_max_after <= 24.5 then
            case when Blank_before <= 114.5 then
               return 0.7647058823529411 # (13.0 out of 17.0)
            else  # if Blank_before > 114.5
               return 0.2857142857142857 # (8.0 out of 28.0)
            end           else  # if McCabe_max_after > 24.5
             return 0.7105263157894737 # (27.0 out of 38.0)
          end         end       end     end   end )