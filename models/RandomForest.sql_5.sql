create or replace function RandomForest_5 (SLOC_before int64, simplifiable-condition int64, bugs_diff int64, Blank_before int64, LLOC_diff int64, try-except-raise int64, LLOC_before int64, changed_lines int64, h2_diff int64, prev_count_x int64, too-many-lines int64, cur_count_y int64, Comments_before int64, McCabe_sum_after int64, cur_count_x int64, vocabulary_diff int64, Single comments_before int64, N2_diff int64, high_ccp_group int64, massive_change int64, added_lines int64, prev_count int64, refactor_mle_diff int64, superfluous-parens int64, avg_coupling_code_size_cut_diff int64, McCabe_sum_diff int64, LOC_before int64, too-many-return-statements int64, too-many-branches int64, too-many-nested-blocks int64, difficulty_diff int64, time_diff int64, Single comments_after int64, calculated_length_diff int64, Simplify-boolean-expression int64, unnecessary-semicolon int64, mostly_delete int64, effort_diff int64, Multi_diff int64, McCabe_max_diff int64, is_refactor int64, only_removal int64, LOC_diff int64, one_file_fix_rate_diff int64, Comments_after int64, comparison-of-constants int64, McCabe_max_after int64, length_diff int64, simplifiable-if-statement int64, removed_lines int64, unnecessary-pass int64, Comments_diff int64, cur_count int64, same_day_duration_avg_diff int64, hunks_num int64, N1_diff int64, line-too-long int64, volume_diff int64, using-constant-test int64, too-many-boolean-expressions int64, modified_McCabe_max_diff int64, h1_diff int64, added_functions int64, SLOC_diff int64, too-many-statements int64, pointless-statement int64, wildcard-import int64, McCabe_max_before int64, prev_count_y int64, broad-exception-caught int64, Blank_diff int64, McCabe_sum_before int64, simplifiable-if-expression int64, Single comments_diff int64) as (
  case when avg_coupling_code_size_cut_diff <= -1.1597222089767456 then
    case when SLOC_diff <= -0.5 then
      case when refactor_mle_diff <= 0.08285928145051003 then
         return 0.37037037037037035 # (10.0 out of 27.0)
      else  # if refactor_mle_diff > 0.08285928145051003
         return 0.8 # (12.0 out of 15.0)
      end     else  # if SLOC_diff > -0.5
      case when added_lines <= 50.0 then
        case when SLOC_diff <= 2.5 then
           return 0.06666666666666667 # (1.0 out of 15.0)
        else  # if SLOC_diff > 2.5
           return 0.0 # (0.0 out of 37.0)
        end       else  # if added_lines > 50.0
         return 0.24 # (6.0 out of 25.0)
      end     end   else  # if avg_coupling_code_size_cut_diff > -1.1597222089767456
    case when prev_count <= 3.5 then
      case when high_ccp_group <= 0.5 then
        case when Single comments_after <= 186.5 then
          case when Single comments_after <= 4.0 then
             return 0.7419354838709677 # (23.0 out of 31.0)
          else  # if Single comments_after > 4.0
            case when h1_diff <= -4.5 then
               return 0.8666666666666667 # (13.0 out of 15.0)
            else  # if h1_diff > -4.5
              case when N1_diff <= -13.5 then
                case when h1_diff <= -0.5 then
                   return 0.21739130434782608 # (5.0 out of 23.0)
                else  # if h1_diff > -0.5
                   return 0.0 # (0.0 out of 18.0)
                end               else  # if N1_diff > -13.5
                case when added_lines <= 61.5 then
                  case when removed_lines <= 10.5 then
                    case when McCabe_max_after <= 12.5 then
                      case when LOC_before <= 463.5 then
                         return 0.3333333333333333 # (6.0 out of 18.0)
                      else  # if LOC_before > 463.5
                         return 0.2857142857142857 # (4.0 out of 14.0)
                      end                     else  # if McCabe_max_after > 12.5
                      case when McCabe_sum_diff <= -0.5 then
                         return 0.6470588235294118 # (11.0 out of 17.0)
                      else  # if McCabe_sum_diff > -0.5
                         return 0.45 # (9.0 out of 20.0)
                      end                     end                   else  # if removed_lines > 10.5
                    case when added_lines <= 29.5 then
                       return 0.06666666666666667 # (2.0 out of 30.0)
                    else  # if added_lines > 29.5
                       return 0.22727272727272727 # (5.0 out of 22.0)
                    end                   end                 else  # if added_lines > 61.5
                  case when added_functions <= 0.5 then
                    case when Blank_before <= 184.5 then
                       return 0.5416666666666666 # (13.0 out of 24.0)
                    else  # if Blank_before > 184.5
                       return 0.2222222222222222 # (4.0 out of 18.0)
                    end                   else  # if added_functions > 0.5
                     return 0.8387096774193549 # (26.0 out of 31.0)
                  end                 end               end             end           end         else  # if Single comments_after > 186.5
          case when LOC_before <= 4431.0 then
            case when LLOC_before <= 1064.5 then
               return 0.7241379310344828 # (21.0 out of 29.0)
            else  # if LLOC_before > 1064.5
               return 0.9130434782608695 # (21.0 out of 23.0)
            end           else  # if LOC_before > 4431.0
             return 0.13333333333333333 # (2.0 out of 15.0)
          end         end       else  # if high_ccp_group > 0.5
        case when SLOC_before <= 409.0 then
           return 1.0 # (40.0 out of 40.0)
        else  # if SLOC_before > 409.0
          case when one_file_fix_rate_diff <= 0.32500000298023224 then
            case when removed_lines <= 4.5 then
               return 1.0 # (20.0 out of 20.0)
            else  # if removed_lines > 4.5
              case when Single comments_after <= 59.5 then
                 return 0.2857142857142857 # (4.0 out of 14.0)
              else  # if Single comments_after > 59.5
                 return 0.8666666666666667 # (13.0 out of 15.0)
              end             end           else  # if one_file_fix_rate_diff > 0.32500000298023224
             return 0.2857142857142857 # (6.0 out of 21.0)
          end         end       end     else  # if prev_count > 3.5
       return 0.0 # (0.0 out of 23.0)
    end   end )