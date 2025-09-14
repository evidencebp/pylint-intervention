create or replace function RandomForest_4 (h1_diff int64, simplifiable-if-statement int64, McCabe_max_after int64, McCabe_sum_before int64, Single comments_before int64, low_McCabe_max_diff int64, high_ccp_group int64, pointless-statement int64, too-many-branches int64, high_McCabe_max_before int64, superfluous-parens int64, Multi_diff int64, wildcard-import int64, high_McCabe_sum_before int64, LLOC_before int64, cur_count int64, unnecessary-semicolon int64, Comments_after int64, mostly_delete int64, simplifiable-condition int64, avg_coupling_code_size_cut_diff int64, added_functions int64, McCabe_max_diff int64, McCabe_sum_diff int64, LLOC_diff int64, LOC_before int64, Comments_diff int64, prev_count_x int64, effort_diff int64, try-except-raise int64, difficulty_diff int64, line-too-long int64, Simplify-boolean-expression int64, SLOC_diff int64, McCabe_sum_after int64, refactor_mle_diff int64, one_file_fix_rate_diff int64, is_refactor int64, too-many-lines int64, too-many-boolean-expressions int64, Single comments_diff int64, low_McCabe_sum_diff int64, cur_count_y int64, comparison-of-constants int64, Comments_before int64, too-many-return-statements int64, vocabulary_diff int64, massive_change int64, hunks_num int64, modified_McCabe_max_diff int64, high_McCabe_sum_diff int64, N2_diff int64, broad-exception-caught int64, length_diff int64, unnecessary-pass int64, time_diff int64, changed_lines int64, Single comments_after int64, h2_diff int64, low_McCabe_sum_before int64, cur_count_x int64, McCabe_max_before int64, using-constant-test int64, added_lines int64, same_day_duration_avg_diff int64, prev_count_y int64, Blank_diff int64, LOC_diff int64, only_removal int64, low_McCabe_max_before int64, bugs_diff int64, too-many-statements int64, simplifiable-if-expression int64, calculated_length_diff int64, volume_diff int64, Blank_before int64, high_McCabe_max_diff int64, SLOC_before int64, too-many-nested-blocks int64, removed_lines int64, low_ccp_group int64, N1_diff int64, prev_count int64) as (
  case when Blank_diff <= -19.0 then
    case when McCabe_sum_before <= 327.0 then
      case when avg_coupling_code_size_cut_diff <= -0.8787879049777985 then
         return 1.0 # (1.0 out of 1.0)
      else  # if avg_coupling_code_size_cut_diff > -0.8787879049777985
        case when McCabe_max_after <= 14.5 then
           return 0.8571428571428571 # (0.8571428571428571 out of 1.0)
        else  # if McCabe_max_after > 14.5
           return 0.375 # (0.375 out of 1.0)
        end       end     else  # if McCabe_sum_before > 327.0
       return 0.3888888888888889 # (0.3888888888888889 out of 1.0)
    end   else  # if Blank_diff > -19.0
    case when Blank_before <= 40.5 then
      case when LOC_diff <= -16.0 then
         return 0.125 # (0.125 out of 1.0)
      else  # if LOC_diff > -16.0
        case when length_diff <= 1.0 then
          case when Blank_before <= 32.5 then
             return 0.6129032258064516 # (0.6129032258064516 out of 1.0)
          else  # if Blank_before > 32.5
             return 0.8888888888888888 # (0.8888888888888888 out of 1.0)
          end         else  # if length_diff > 1.0
           return 1.0 # (1.0 out of 1.0)
        end       end     else  # if Blank_before > 40.5
      case when LOC_diff <= -9.5 then
        case when hunks_num <= 4.5 then
          case when LLOC_diff <= -19.0 then
            case when McCabe_max_diff <= -0.5 then
               return 0.0 # (0.0 out of 1.0)
            else  # if McCabe_max_diff > -0.5
               return 0.26666666666666666 # (0.26666666666666666 out of 1.0)
            end           else  # if LLOC_diff > -19.0
             return 0.5714285714285714 # (0.5714285714285714 out of 1.0)
          end         else  # if hunks_num > 4.5
          case when McCabe_max_before <= 30.5 then
            case when Blank_diff <= -4.0 then
              case when Multi_diff <= -1.5 then
                 return 0.8095238095238095 # (0.8095238095238095 out of 1.0)
              else  # if Multi_diff > -1.5
                 return 0.7083333333333334 # (0.7083333333333334 out of 1.0)
              end             else  # if Blank_diff > -4.0
               return 0.5263157894736842 # (0.5263157894736842 out of 1.0)
            end           else  # if McCabe_max_before > 30.5
             return 0.2857142857142857 # (0.2857142857142857 out of 1.0)
          end         end       else  # if LOC_diff > -9.5
        case when high_ccp_group <= 0.5 then
          case when McCabe_max_before <= 5.5 then
             return 0.5833333333333334 # (0.5833333333333334 out of 1.0)
          else  # if McCabe_max_before > 5.5
            case when line-too-long <= 0.5 then
              case when removed_lines <= 92.5 then
                case when LOC_before <= 2562.5 then
                  case when Comments_after <= 100.0 then
                    case when Comments_after <= 57.0 then
                      case when Blank_before <= 102.5 then
                         return 0.15625 # (0.15625 out of 1.0)
                      else  # if Blank_before > 102.5
                         return 0.05263157894736842 # (0.05263157894736842 out of 1.0)
                      end                     else  # if Comments_after > 57.0
                       return 0.3076923076923077 # (0.3076923076923077 out of 1.0)
                    end                   else  # if Comments_after > 100.0
                     return 0.0 # (0.0 out of 1.0)
                  end                 else  # if LOC_before > 2562.5
                   return 0.2857142857142857 # (0.2857142857142857 out of 1.0)
                end               else  # if removed_lines > 92.5
                case when McCabe_sum_diff <= 1.0 then
                   return 0.2 # (0.2 out of 1.0)
                else  # if McCabe_sum_diff > 1.0
                   return 0.43478260869565216 # (0.43478260869565216 out of 1.0)
                end               end             else  # if line-too-long > 0.5
              case when hunks_num <= 7.5 then
                 return 0.29411764705882354 # (0.29411764705882354 out of 1.0)
              else  # if hunks_num > 7.5
                 return 0.29411764705882354 # (0.29411764705882354 out of 1.0)
              end             end           end         else  # if high_ccp_group > 0.5
          case when McCabe_sum_before <= 183.0 then
            case when Comments_before <= 44.5 then
              case when only_removal <= 0.5 then
                 return 0.9285714285714286 # (0.9285714285714286 out of 1.0)
              else  # if only_removal > 0.5
                 return 0.6875 # (0.6875 out of 1.0)
              end             else  # if Comments_before > 44.5
               return 0.08 # (0.08 out of 1.0)
            end           else  # if McCabe_sum_before > 183.0
             return 1.0 # (1.0 out of 1.0)
          end         end       end     end   end )