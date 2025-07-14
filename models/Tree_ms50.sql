create or replace function Tree_ms50 (effort_diff int64, too-many-nested-blocks int64, Single comments_diff int64, N1_diff int64, avg_coupling_code_size_cut_diff int64, Simplify-boolean-expression int64, try-except-raise int64, h1_diff int64, added_functions int64, too-many-boolean-expressions int64, LLOC_diff int64, cur_count_x int64, wildcard-import int64, mostly_delete int64, LOC_diff int64, difficulty_diff int64, Comments_before int64, prev_count_y int64, time_diff int64, pointless-statement int64, vocabulary_diff int64, modified_McCabe_max_diff int64, prev_count int64, McCabe_sum_before int64, McCabe_max_after int64, Blank_diff int64, using-constant-test int64, McCabe_max_before int64, is_refactor int64, Comments_after int64, SLOC_before int64, superfluous-parens int64, too-many-branches int64, massive_change int64, comparison-of-constants int64, broad-exception-caught int64, Blank_before int64, N2_diff int64, McCabe_sum_after int64, too-many-statements int64, refactor_mle_diff int64, LOC_before int64, simplifiable-if-statement int64, only_removal int64, h2_diff int64, unnecessary-semicolon int64, too-many-lines int64, LLOC_before int64, volume_diff int64, too-many-return-statements int64, high_ccp_group int64, Single comments_before int64, simplifiable-if-expression int64, changed_lines int64, Multi_diff int64, one_file_fix_rate_diff int64, prev_count_x int64, simplifiable-condition int64, cur_count_y int64, calculated_length_diff int64, SLOC_diff int64, line-too-long int64, McCabe_max_diff int64, Comments_diff int64, cur_count int64, Single comments_after int64, removed_lines int64, added_lines int64, length_diff int64, unnecessary-pass int64, hunks_num int64, bugs_diff int64, same_day_duration_avg_diff int64, McCabe_sum_diff int64) as (
  case when high_ccp_group <= 0.5 then
    case when changed_lines <= 138.5 then
      case when LOC_diff <= 38.5 then
        case when changed_lines <= 32.0 then
          case when Single comments_after <= 23.0 then
            case when refactor_mle_diff <= -0.1607961505651474 then
               return 0.4 # (4.0 out of 10.0)
            else  # if refactor_mle_diff > -0.1607961505651474
              case when changed_lines <= 8.0 then
                 return 0.8333333333333334 # (10.0 out of 12.0)
              else  # if changed_lines > 8.0
                 return 0.6 # (6.0 out of 10.0)
              end             end           else  # if Single comments_after > 23.0
            case when SLOC_before <= 593.0 then
              case when removed_lines <= 11.5 then
                case when LLOC_before <= 204.5 then
                   return 0.2 # (2.0 out of 10.0)
                else  # if LLOC_before > 204.5
                   return 0.0 # (0.0 out of 22.0)
                end               else  # if removed_lines > 11.5
                 return 0.45454545454545453 # (5.0 out of 11.0)
              end             else  # if SLOC_before > 593.0
              case when Comments_before <= 181.5 then
                case when McCabe_sum_before <= 233.0 then
                   return 0.9375 # (15.0 out of 16.0)
                else  # if McCabe_sum_before > 233.0
                   return 0.2727272727272727 # (3.0 out of 11.0)
                end               else  # if Comments_before > 181.5
                case when McCabe_max_after <= 30.0 then
                   return 0.4166666666666667 # (5.0 out of 12.0)
                else  # if McCabe_max_after > 30.0
                   return 0.0 # (0.0 out of 12.0)
                end               end             end           end         else  # if changed_lines > 32.0
          case when Single comments_before <= 41.5 then
            case when Single comments_after <= 21.0 then
              case when LOC_diff <= 3.5 then
                 return 0.0 # (0.0 out of 28.0)
              else  # if LOC_diff > 3.5
                 return 0.35714285714285715 # (5.0 out of 14.0)
              end             else  # if Single comments_after > 21.0
              case when h2_diff <= -0.5 then
                 return 0.7857142857142857 # (11.0 out of 14.0)
              else  # if h2_diff > -0.5
                 return 0.2 # (2.0 out of 10.0)
              end             end           else  # if Single comments_before > 41.5
            case when SLOC_before <= 978.0 then
              case when McCabe_max_before <= 20.5 then
                case when Blank_before <= 113.5 then
                   return 0.0 # (0.0 out of 14.0)
                else  # if Blank_before > 113.5
                   return 0.26666666666666666 # (4.0 out of 15.0)
                end               else  # if McCabe_max_before > 20.5
                 return 0.0 # (0.0 out of 41.0)
              end             else  # if SLOC_before > 978.0
               return 0.29411764705882354 # (5.0 out of 17.0)
            end           end         end       else  # if LOC_diff > 38.5
         return 0.8421052631578947 # (16.0 out of 19.0)
      end     else  # if changed_lines > 138.5
      case when McCabe_max_after <= 7.5 then
        case when Single comments_diff <= -1.5 then
          case when LLOC_before <= 146.0 then
             return 0.9 # (9.0 out of 10.0)
          else  # if LLOC_before > 146.0
             return 1.0 # (22.0 out of 22.0)
          end         else  # if Single comments_diff > -1.5
           return 0.5333333333333333 # (8.0 out of 15.0)
        end       else  # if McCabe_max_after > 7.5
        case when refactor_mle_diff <= 0.3291272670030594 then
          case when added_functions <= 8.5 then
            case when N1_diff <= -82.0 then
               return 0.9285714285714286 # (13.0 out of 14.0)
            else  # if N1_diff > -82.0
              case when McCabe_sum_after <= 85.5 then
                 return 0.1875 # (3.0 out of 16.0)
              else  # if McCabe_sum_after > 85.5
                case when McCabe_max_after <= 15.5 then
                   return 1.0 # (11.0 out of 11.0)
                else  # if McCabe_max_after > 15.5
                  case when refactor_mle_diff <= -0.1398288793861866 then
                     return 0.25 # (4.0 out of 16.0)
                  else  # if refactor_mle_diff > -0.1398288793861866
                    case when LLOC_diff <= -17.5 then
                       return 0.36363636363636365 # (4.0 out of 11.0)
                    else  # if LLOC_diff > -17.5
                      case when LOC_before <= 1255.5 then
                         return 1.0 # (10.0 out of 10.0)
                      else  # if LOC_before > 1255.5
                         return 0.5454545454545454 # (6.0 out of 11.0)
                      end                     end                   end                 end               end             end           else  # if added_functions > 8.5
             return 0.1875 # (3.0 out of 16.0)
          end         else  # if refactor_mle_diff > 0.3291272670030594
           return 0.0 # (0.0 out of 11.0)
        end       end     end   else  # if high_ccp_group > 0.5
    case when LOC_before <= 718.0 then
      case when same_day_duration_avg_diff <= 40.03510284423828 then
        case when Multi_diff <= -2.0 then
           return 0.9 # (9.0 out of 10.0)
        else  # if Multi_diff > -2.0
           return 1.0 # (26.0 out of 26.0)
        end       else  # if same_day_duration_avg_diff > 40.03510284423828
        case when Blank_diff <= -1.5 then
           return 0.5 # (5.0 out of 10.0)
        else  # if Blank_diff > -1.5
           return 0.9 # (9.0 out of 10.0)
        end       end     else  # if LOC_before > 718.0
      case when McCabe_sum_after <= 195.5 then
        case when one_file_fix_rate_diff <= -0.10128205269575119 then
          case when one_file_fix_rate_diff <= -0.30000000447034836 then
             return 0.0 # (0.0 out of 13.0)
          else  # if one_file_fix_rate_diff > -0.30000000447034836
             return 0.2 # (2.0 out of 10.0)
          end         else  # if one_file_fix_rate_diff > -0.10128205269575119
          case when refactor_mle_diff <= -0.11428030207753181 then
             return 0.23076923076923078 # (3.0 out of 13.0)
          else  # if refactor_mle_diff > -0.11428030207753181
             return 0.8 # (12.0 out of 15.0)
          end         end       else  # if McCabe_sum_after > 195.5
        case when Blank_before <= 263.5 then
          case when McCabe_sum_after <= 242.0 then
             return 1.0 # (12.0 out of 12.0)
          else  # if McCabe_sum_after > 242.0
             return 0.9 # (9.0 out of 10.0)
          end         else  # if Blank_before > 263.5
           return 0.6 # (6.0 out of 10.0)
        end       end     end   end )