create or replace function RandomForest_0 (using-constant-test int64, simplifiable-if-statement int64, Comments_after int64, same_day_duration_avg_diff int64, Single comments_before int64, one_file_fix_rate_diff int64, too-many-boolean-expressions int64, Single comments_diff int64, high_McCabe_sum_before int64, pointless-statement int64, bugs_diff int64, McCabe_max_before int64, length_diff int64, LOC_diff int64, N2_diff int64, superfluous-parens int64, too-many-nested-blocks int64, effort_diff int64, cur_count_x int64, high_McCabe_max_before int64, comparison-of-constants int64, SLOC_diff int64, hunks_num int64, high_McCabe_max_diff int64, prev_count int64, McCabe_sum_after int64, cur_count_y int64, refactor_mle_diff int64, too-many-return-statements int64, too-many-statements int64, too-many-lines int64, only_removal int64, removed_lines int64, cur_count int64, volume_diff int64, is_refactor int64, prev_count_y int64, calculated_length_diff int64, Simplify-boolean-expression int64, h1_diff int64, McCabe_max_diff int64, wildcard-import int64, McCabe_sum_before int64, line-too-long int64, N1_diff int64, too-many-branches int64, h2_diff int64, McCabe_max_after int64, unnecessary-pass int64, avg_coupling_code_size_cut_diff int64, high_ccp_group int64, vocabulary_diff int64, try-except-raise int64, broad-exception-caught int64, simplifiable-condition int64, LLOC_before int64, added_functions int64, LLOC_diff int64, difficulty_diff int64, McCabe_sum_diff int64, Multi_diff int64, massive_change int64, mostly_delete int64, Comments_before int64, changed_lines int64, Comments_diff int64, time_diff int64, Blank_before int64, high_McCabe_sum_diff int64, added_lines int64, prev_count_x int64, unnecessary-semicolon int64, Blank_diff int64, modified_McCabe_max_diff int64, Single comments_after int64, LOC_before int64, simplifiable-if-expression int64, SLOC_before int64) as (
  case when high_ccp_group <= 0.5 then
    case when h1_diff <= -4.5 then
       return 0.8888888888888888 # (24.0 out of 27.0)
    else  # if h1_diff > -4.5
      case when Single comments_before <= 261.0 then
        case when McCabe_max_before <= 18.5 then
          case when McCabe_sum_before <= 262.5 then
            case when SLOC_before <= 118.5 then
               return 0.7222222222222222 # (13.0 out of 18.0)
            else  # if SLOC_before > 118.5
              case when Blank_before <= 35.0 then
                 return 0.21052631578947367 # (4.0 out of 19.0)
              else  # if Blank_before > 35.0
                case when LLOC_before <= 570.5 then
                  case when McCabe_max_after <= 5.5 then
                     return 0.8823529411764706 # (15.0 out of 17.0)
                  else  # if McCabe_max_after > 5.5
                    case when McCabe_sum_before <= 43.0 then
                       return 0.125 # (2.0 out of 16.0)
                    else  # if McCabe_sum_before > 43.0
                      case when SLOC_diff <= 0.5 then
                        case when Single comments_before <= 66.5 then
                          case when LLOC_diff <= -1.5 then
                             return 0.8333333333333334 # (15.0 out of 18.0)
                          else  # if LLOC_diff > -1.5
                             return 0.2916666666666667 # (7.0 out of 24.0)
                          end                         else  # if Single comments_before > 66.5
                           return 0.8333333333333334 # (15.0 out of 18.0)
                        end                       else  # if SLOC_diff > 0.5
                        case when same_day_duration_avg_diff <= -14.647727489471436 then
                           return 0.46153846153846156 # (6.0 out of 13.0)
                        else  # if same_day_duration_avg_diff > -14.647727489471436
                           return 0.11764705882352941 # (2.0 out of 17.0)
                        end                       end                     end                   end                 else  # if LLOC_before > 570.5
                   return 0.21052631578947367 # (4.0 out of 19.0)
                end               end             end           else  # if McCabe_sum_before > 262.5
             return 0.8125 # (13.0 out of 16.0)
          end         else  # if McCabe_max_before > 18.5
          case when McCabe_sum_after <= 380.5 then
            case when McCabe_max_after <= 18.5 then
              case when Blank_before <= 109.0 then
                 return 0.0 # (0.0 out of 30.0)
              else  # if Blank_before > 109.0
                 return 0.14285714285714285 # (2.0 out of 14.0)
              end             else  # if McCabe_max_after > 18.5
              case when Single comments_before <= 102.0 then
                case when McCabe_sum_before <= 272.5 then
                  case when high_McCabe_max_before <= 0.5 then
                    case when Single comments_diff <= -0.5 then
                       return 0.42105263157894735 # (8.0 out of 19.0)
                    else  # if Single comments_diff > -0.5
                       return 0.6842105263157895 # (13.0 out of 19.0)
                    end                   else  # if high_McCabe_max_before > 0.5
                     return 0.47058823529411764 # (16.0 out of 34.0)
                  end                 else  # if McCabe_sum_before > 272.5
                   return 0.0 # (0.0 out of 21.0)
                end               else  # if Single comments_before > 102.0
                case when Blank_before <= 210.0 then
                   return 0.25 # (7.0 out of 28.0)
                else  # if Blank_before > 210.0
                   return 0.037037037037037035 # (1.0 out of 27.0)
                end               end             end           else  # if McCabe_sum_after > 380.5
             return 0.64 # (16.0 out of 25.0)
          end         end       else  # if Single comments_before > 261.0
        case when same_day_duration_avg_diff <= 10.757922649383545 then
           return 0.5714285714285714 # (8.0 out of 14.0)
        else  # if same_day_duration_avg_diff > 10.757922649383545
           return 0.9285714285714286 # (13.0 out of 14.0)
        end       end     end   else  # if high_ccp_group > 0.5
    case when Comments_after <= 100.5 then
      case when length_diff <= -24.0 then
         return 0.5625 # (9.0 out of 16.0)
      else  # if length_diff > -24.0
        case when LOC_before <= 876.0 then
          case when changed_lines <= 89.5 then
             return 0.9259259259259259 # (25.0 out of 27.0)
          else  # if changed_lines > 89.5
             return 1.0 # (28.0 out of 28.0)
          end         else  # if LOC_before > 876.0
          case when McCabe_sum_after <= 181.0 then
             return 0.5 # (10.0 out of 20.0)
          else  # if McCabe_sum_after > 181.0
             return 0.8235294117647058 # (14.0 out of 17.0)
          end         end       end     else  # if Comments_after > 100.5
       return 0.48 # (12.0 out of 25.0)
    end   end )