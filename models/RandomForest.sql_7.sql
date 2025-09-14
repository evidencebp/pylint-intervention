create or replace function RandomForest_7 (low_McCabe_max_before int64, LLOC_before int64, low_McCabe_sum_diff int64, modified_McCabe_max_diff int64, bugs_diff int64, McCabe_max_before int64, Single comments_before int64, prev_count_y int64, added_lines int64, LLOC_diff int64, N2_diff int64, added_functions int64, prev_count int64, too-many-boolean-expressions int64, SLOC_diff int64, mostly_delete int64, time_diff int64, calculated_length_diff int64, McCabe_max_after int64, Comments_diff int64, line-too-long int64, McCabe_sum_after int64, one_file_fix_rate_diff int64, h1_diff int64, high_McCabe_max_diff int64, too-many-branches int64, SLOC_before int64, cur_count_y int64, prev_count_x int64, McCabe_sum_before int64, Comments_after int64, wildcard-import int64, unnecessary-semicolon int64, same_day_duration_avg_diff int64, effort_diff int64, too-many-statements int64, broad-exception-caught int64, LOC_before int64, cur_count int64, Comments_before int64, using-constant-test int64, LOC_diff int64, high_McCabe_sum_diff int64, only_removal int64, superfluous-parens int64, try-except-raise int64, Blank_before int64, McCabe_max_diff int64, N1_diff int64, massive_change int64, refactor_mle_diff int64, pointless-statement int64, too-many-lines int64, simplifiable-if-statement int64, high_McCabe_sum_before int64, vocabulary_diff int64, removed_lines int64, difficulty_diff int64, Simplify-boolean-expression int64, avg_coupling_code_size_cut_diff int64, Single comments_after int64, low_ccp_group int64, Multi_diff int64, is_refactor int64, hunks_num int64, Single comments_diff int64, length_diff int64, unnecessary-pass int64, Blank_diff int64, h2_diff int64, changed_lines int64, cur_count_x int64, low_McCabe_max_diff int64, high_McCabe_max_before int64, high_ccp_group int64, too-many-nested-blocks int64, McCabe_sum_diff int64, volume_diff int64, comparison-of-constants int64, too-many-return-statements int64, simplifiable-condition int64, simplifiable-if-expression int64, low_McCabe_sum_before int64) as (
  case when McCabe_sum_before <= 92.5 then
    case when refactor_mle_diff <= 0.16808952391147614 then
      case when Multi_diff <= 1.0 then
        case when Single comments_diff <= -2.5 then
          case when refactor_mle_diff <= -0.04925714433193207 then
             return 0.8666666666666667 # (0.8666666666666667 out of 1.0)
          else  # if refactor_mle_diff > -0.04925714433193207
             return 1.0 # (1.0 out of 1.0)
          end         else  # if Single comments_diff > -2.5
          case when N2_diff <= -9.5 then
             return 0.125 # (0.125 out of 1.0)
          else  # if N2_diff > -9.5
            case when Blank_before <= 28.5 then
              case when Blank_before <= 18.5 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if Blank_before > 18.5
                 return 0.8260869565217391 # (0.8260869565217391 out of 1.0)
              end             else  # if Blank_before > 28.5
              case when Blank_before <= 34.5 then
                 return 0.2631578947368421 # (0.2631578947368421 out of 1.0)
              else  # if Blank_before > 34.5
                case when LLOC_diff <= -7.5 then
                   return 0.4666666666666667 # (0.4666666666666667 out of 1.0)
                else  # if LLOC_diff > -7.5
                  case when refactor_mle_diff <= -0.11493333429098129 then
                     return 0.7878787878787878 # (0.7878787878787878 out of 1.0)
                  else  # if refactor_mle_diff > -0.11493333429098129
                     return 0.5 # (0.5 out of 1.0)
                  end                 end               end             end           end         end       else  # if Multi_diff > 1.0
         return 0.3076923076923077 # (0.3076923076923077 out of 1.0)
      end     else  # if refactor_mle_diff > 0.16808952391147614
      case when Comments_before <= 34.5 then
         return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
      else  # if Comments_before > 34.5
         return 0.21052631578947367 # (0.21052631578947367 out of 1.0)
      end     end   else  # if McCabe_sum_before > 92.5
    case when LOC_before <= 1533.5 then
      case when Comments_after <= 76.0 then
        case when Blank_before <= 107.0 then
          case when LOC_before <= 676.5 then
            case when hunks_num <= 4.5 then
               return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
            else  # if hunks_num > 4.5
               return 0.5 # (0.5 out of 1.0)
            end           else  # if LOC_before > 676.5
            case when LOC_before <= 974.0 then
               return 0.12 # (0.12 out of 1.0)
            else  # if LOC_before > 974.0
               return 0.0 # (0.0 out of 1.0)
            end           end         else  # if Blank_before > 107.0
          case when length_diff <= -122.0 then
             return 0.23809523809523808 # (0.23809523809523808 out of 1.0)
          else  # if length_diff > -122.0
            case when Single comments_after <= 61.5 then
              case when Comments_after <= 18.0 then
                 return 0.5333333333333333 # (0.5333333333333333 out of 1.0)
              else  # if Comments_after > 18.0
                case when Blank_before <= 138.5 then
                   return 1.0 # (1.0 out of 1.0)
                else  # if Blank_before > 138.5
                  case when McCabe_sum_after <= 190.0 then
                     return 0.8571428571428571 # (0.8571428571428571 out of 1.0)
                  else  # if McCabe_sum_after > 190.0
                     return 0.6875 # (0.6875 out of 1.0)
                  end                 end               end             else  # if Single comments_after > 61.5
               return 0.3 # (0.3 out of 1.0)
            end           end         end       else  # if Comments_after > 76.0
        case when SLOC_diff <= -0.5 then
           return 0.0 # (0.0 out of 1.0)
        else  # if SLOC_diff > -0.5
          case when refactor_mle_diff <= 0.03241442982107401 then
             return 0.13636363636363635 # (0.13636363636363635 out of 1.0)
          else  # if refactor_mle_diff > 0.03241442982107401
             return 0.2727272727272727 # (0.2727272727272727 out of 1.0)
          end         end       end     else  # if LOC_before > 1533.5
      case when added_functions <= 0.5 then
        case when Comments_diff <= 0.5 then
          case when Blank_before <= 265.5 then
             return 0.85 # (0.85 out of 1.0)
          else  # if Blank_before > 265.5
            case when Comments_after <= 155.0 then
               return 0.0625 # (0.0625 out of 1.0)
            else  # if Comments_after > 155.0
               return 0.7333333333333333 # (0.7333333333333333 out of 1.0)
            end           end         else  # if Comments_diff > 0.5
           return 0.15384615384615385 # (0.15384615384615385 out of 1.0)
        end       else  # if added_functions > 0.5
        case when McCabe_sum_after <= 502.5 then
           return 1.0 # (1.0 out of 1.0)
        else  # if McCabe_sum_after > 502.5
           return 0.7 # (0.7 out of 1.0)
        end       end     end   end )