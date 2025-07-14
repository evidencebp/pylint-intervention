create or replace function RandomForest_1 (SLOC_before int64, simplifiable-condition int64, bugs_diff int64, Blank_before int64, LLOC_diff int64, try-except-raise int64, LLOC_before int64, changed_lines int64, h2_diff int64, prev_count_x int64, too-many-lines int64, cur_count_y int64, Comments_before int64, McCabe_sum_after int64, cur_count_x int64, vocabulary_diff int64, Single comments_before int64, N2_diff int64, high_ccp_group int64, massive_change int64, added_lines int64, prev_count int64, refactor_mle_diff int64, superfluous-parens int64, avg_coupling_code_size_cut_diff int64, McCabe_sum_diff int64, LOC_before int64, too-many-return-statements int64, too-many-branches int64, too-many-nested-blocks int64, difficulty_diff int64, time_diff int64, Single comments_after int64, calculated_length_diff int64, Simplify-boolean-expression int64, unnecessary-semicolon int64, mostly_delete int64, effort_diff int64, Multi_diff int64, McCabe_max_diff int64, is_refactor int64, only_removal int64, LOC_diff int64, one_file_fix_rate_diff int64, Comments_after int64, comparison-of-constants int64, McCabe_max_after int64, length_diff int64, simplifiable-if-statement int64, removed_lines int64, unnecessary-pass int64, Comments_diff int64, cur_count int64, same_day_duration_avg_diff int64, hunks_num int64, N1_diff int64, line-too-long int64, volume_diff int64, using-constant-test int64, too-many-boolean-expressions int64, modified_McCabe_max_diff int64, h1_diff int64, added_functions int64, SLOC_diff int64, too-many-statements int64, pointless-statement int64, wildcard-import int64, McCabe_max_before int64, prev_count_y int64, broad-exception-caught int64, Blank_diff int64, McCabe_sum_before int64, simplifiable-if-expression int64, Single comments_diff int64) as (
  case when Single comments_after <= 2.5 then
    case when Single comments_before <= 1.5 then
       return 1.0 # (17.0 out of 17.0)
    else  # if Single comments_before > 1.5
       return 0.8571428571428571 # (12.0 out of 14.0)
    end   else  # if Single comments_after > 2.5
    case when added_functions <= 7.5 then
      case when avg_coupling_code_size_cut_diff <= -1.126893937587738 then
        case when Single comments_diff <= -2.5 then
           return 0.6666666666666666 # (16.0 out of 24.0)
        else  # if Single comments_diff > -2.5
          case when Single comments_before <= 88.5 then
            case when Comments_after <= 20.5 then
               return 0.08695652173913043 # (2.0 out of 23.0)
            else  # if Comments_after > 20.5
              case when changed_lines <= 70.5 then
                 return 0.4 # (6.0 out of 15.0)
              else  # if changed_lines > 70.5
                 return 0.7058823529411765 # (12.0 out of 17.0)
              end             end           else  # if Single comments_before > 88.5
            case when same_day_duration_avg_diff <= 65.85714340209961 then
               return 0.0 # (0.0 out of 26.0)
            else  # if same_day_duration_avg_diff > 65.85714340209961
               return 0.15384615384615385 # (2.0 out of 13.0)
            end           end         end       else  # if avg_coupling_code_size_cut_diff > -1.126893937587738
        case when Comments_diff <= -4.5 then
          case when modified_McCabe_max_diff <= -2.5 then
             return 0.9354838709677419 # (29.0 out of 31.0)
          else  # if modified_McCabe_max_diff > -2.5
            case when h2_diff <= -54.0 then
               return 0.2 # (4.0 out of 20.0)
            else  # if h2_diff > -54.0
              case when Comments_before <= 46.5 then
                 return 0.5 # (9.0 out of 18.0)
              else  # if Comments_before > 46.5
                 return 0.96 # (24.0 out of 25.0)
              end             end           end         else  # if Comments_diff > -4.5
          case when SLOC_diff <= 35.0 then
            case when high_ccp_group <= 0.5 then
              case when Multi_diff <= -2.5 then
                 return 0.08823529411764706 # (3.0 out of 34.0)
              else  # if Multi_diff > -2.5
                case when avg_coupling_code_size_cut_diff <= 1.8833333253860474 then
                  case when Single comments_diff <= -1.5 then
                     return 0.0625 # (1.0 out of 16.0)
                  else  # if Single comments_diff > -1.5
                    case when changed_lines <= 107.5 then
                      case when McCabe_sum_diff <= 1.5 then
                        case when Comments_before <= 23.0 then
                           return 0.8666666666666667 # (13.0 out of 15.0)
                        else  # if Comments_before > 23.0
                          case when refactor_mle_diff <= 0.05504581518471241 then
                            case when McCabe_max_after <= 14.5 then
                               return 0.0 # (0.0 out of 17.0)
                            else  # if McCabe_max_after > 14.5
                              case when Blank_before <= 160.5 then
                                 return 0.14285714285714285 # (2.0 out of 14.0)
                              else  # if Blank_before > 160.5
                                 return 0.2777777777777778 # (5.0 out of 18.0)
                              end                             end                           else  # if refactor_mle_diff > 0.05504581518471241
                            case when McCabe_sum_after <= 110.5 then
                               return 0.07142857142857142 # (1.0 out of 14.0)
                            else  # if McCabe_sum_after > 110.5
                               return 0.5263157894736842 # (10.0 out of 19.0)
                            end                           end                         end                       else  # if McCabe_sum_diff > 1.5
                         return 0.058823529411764705 # (1.0 out of 17.0)
                      end                     else  # if changed_lines > 107.5
                       return 0.5517241379310345 # (16.0 out of 29.0)
                    end                   end                 else  # if avg_coupling_code_size_cut_diff > 1.8833333253860474
                   return 0.7619047619047619 # (16.0 out of 21.0)
                end               end             else  # if high_ccp_group > 0.5
              case when McCabe_sum_before <= 168.0 then
                case when LLOC_diff <= 0.5 then
                   return 0.6666666666666666 # (18.0 out of 27.0)
                else  # if LLOC_diff > 0.5
                   return 0.25 # (4.0 out of 16.0)
                end               else  # if McCabe_sum_before > 168.0
                 return 0.90625 # (29.0 out of 32.0)
              end             end           else  # if SLOC_diff > 35.0
            case when Blank_diff <= 6.0 then
               return 1.0 # (17.0 out of 17.0)
            else  # if Blank_diff > 6.0
               return 0.84 # (21.0 out of 25.0)
            end           end         end       end     else  # if added_functions > 7.5
       return 0.038461538461538464 # (1.0 out of 26.0)
    end   end )