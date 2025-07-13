create or replace function RandomForest_9 (LOC_diff int64, Comments_after int64, volume_diff int64, LOC_before int64, McCabe_max_diff int64, Blank_diff int64, unnecessary-pass int64, McCabe_max_before int64, prev_count_x int64, prev_count_y int64, N2_diff int64, LLOC_before int64, prev_count int64, too-many-branches int64, added_functions int64, length_diff int64, h2_diff int64, removed_lines int64, too-many-nested-blocks int64, comparison-of-constants int64, bugs_diff int64, N1_diff int64, Comments_diff int64, line-too-long int64, McCabe_sum_diff int64, superfluous-parens int64, Multi_diff int64, changed_lines int64, McCabe_sum_before int64, calculated_length_diff int64, Single comments_after int64, time_diff int64, Single comments_diff int64, Comments_before int64, added_lines int64, effort_diff int64, refactor_mle_diff int64, Blank_before int64, too-many-return-statements int64, pointless-statement int64, too-many-statements int64, cur_count_y int64, unnecessary-semicolon int64, cur_count_x int64, using-constant-test int64, McCabe_sum_after int64, McCabe_max_after int64, too-many-lines int64, LLOC_diff int64, difficulty_diff int64, simplifiable-if-statement int64, vocabulary_diff int64, SLOC_before int64, modified_McCabe_max_diff int64, wildcard-import int64, one_file_fix_rate_diff int64, simplifiable-condition int64, SLOC_diff int64, h1_diff int64, same_day_duration_avg_diff int64, Single comments_before int64, cur_count int64, try-except-raise int64, Simplify-boolean-expression int64, simplifiable-if-expression int64, broad-exception-caught int64, hunks_num int64, too-many-boolean-expressions int64, avg_coupling_code_size_cut_diff int64) as (
  case when McCabe_max_after <= 39.5 then
    case when Comments_diff <= -21.0 then
      case when same_day_duration_avg_diff <= -0.5047757625579834 then
         return 0.5833333333333334 # (7.0 out of 12.0)
      else  # if same_day_duration_avg_diff > -0.5047757625579834
         return 1.0 # (17.0 out of 17.0)
      end     else  # if Comments_diff > -21.0
      case when McCabe_sum_diff <= -14.5 then
        case when refactor_mle_diff <= -0.03591666743159294 then
           return 0.0 # (0.0 out of 41.0)
        else  # if refactor_mle_diff > -0.03591666743159294
          case when LOC_before <= 1041.5 then
             return 0.14285714285714285 # (2.0 out of 14.0)
          else  # if LOC_before > 1041.5
             return 0.5238095238095238 # (11.0 out of 21.0)
          end         end       else  # if McCabe_sum_diff > -14.5
        case when McCabe_max_after <= 18.5 then
          case when h2_diff <= -7.0 then
             return 0.7777777777777778 # (21.0 out of 27.0)
          else  # if h2_diff > -7.0
            case when SLOC_diff <= 34.5 then
              case when McCabe_sum_after <= 19.5 then
                case when same_day_duration_avg_diff <= 9.119444370269775 then
                  case when prev_count_x <= 25.5 then
                    case when McCabe_sum_before <= 9.0 then
                      case when same_day_duration_avg_diff <= -93.79220962524414 then
                        case when line-too-long <= 0.5 then
                          case when too-many-statements <= 0.5 then
                            case when superfluous-parens <= 0.5 then
                               return 0.44871794871794873 # (35.0 out of 78.0)
                            else  # if superfluous-parens > 0.5
                               return 0.5 # (14.0 out of 28.0)
                            end                           else  # if too-many-statements > 0.5
                             return 0.2692307692307692 # (7.0 out of 26.0)
                          end                         else  # if line-too-long > 0.5
                          case when refactor_mle_diff <= 0.1270398534834385 then
                             return 0.3333333333333333 # (12.0 out of 36.0)
                          else  # if refactor_mle_diff > 0.1270398534834385
                             return 0.17647058823529413 # (3.0 out of 17.0)
                          end                         end                       else  # if same_day_duration_avg_diff > -93.79220962524414
                        case when refactor_mle_diff <= -0.3571142852306366 then
                           return 0.3076923076923077 # (12.0 out of 39.0)
                        else  # if refactor_mle_diff > -0.3571142852306366
                          case when same_day_duration_avg_diff <= -11.343685150146484 then
                            case when cur_count_x <= 1.5 then
                              case when too-many-branches <= 0.5 then
                                case when same_day_duration_avg_diff <= -35.1101188659668 then
                                  case when same_day_duration_avg_diff <= -65.47143173217773 then
                                     return 0.7368421052631579 # (28.0 out of 38.0)
                                  else  # if same_day_duration_avg_diff > -65.47143173217773
                                    case when prev_count_x <= 0.5 then
                                       return 0.5166666666666667 # (31.0 out of 60.0)
                                    else  # if prev_count_x > 0.5
                                       return 0.4444444444444444 # (8.0 out of 18.0)
                                    end                                   end                                 else  # if same_day_duration_avg_diff > -35.1101188659668
                                  case when line-too-long <= 0.5 then
                                    case when refactor_mle_diff <= -0.03296688199043274 then
                                       return 0.6470588235294118 # (22.0 out of 34.0)
                                    else  # if refactor_mle_diff > -0.03296688199043274
                                       return 0.825 # (33.0 out of 40.0)
                                    end                                   else  # if line-too-long > 0.5
                                     return 0.7692307692307693 # (10.0 out of 13.0)
                                  end                                 end                               else  # if too-many-branches > 0.5
                                 return 0.7333333333333333 # (11.0 out of 15.0)
                              end                             else  # if cur_count_x > 1.5
                              case when prev_count_x <= 9.5 then
                                case when line-too-long <= 0.5 then
                                  case when refactor_mle_diff <= -0.09014726430177689 then
                                     return 0.8125 # (13.0 out of 16.0)
                                  else  # if refactor_mle_diff > -0.09014726430177689
                                     return 0.4 # (10.0 out of 25.0)
                                  end                                 else  # if line-too-long > 0.5
                                   return 0.2631578947368421 # (5.0 out of 19.0)
                                end                               else  # if prev_count_x > 9.5
                                 return 0.75 # (12.0 out of 16.0)
                              end                             end                           else  # if same_day_duration_avg_diff > -11.343685150146484
                            case when refactor_mle_diff <= -0.10620620101690292 then
                               return 0.6984126984126984 # (44.0 out of 63.0)
                            else  # if refactor_mle_diff > -0.10620620101690292
                               return 0.3235294117647059 # (44.0 out of 136.0)
                            end                           end                         end                       end                     else  # if McCabe_sum_before > 9.0
                      case when same_day_duration_avg_diff <= -50.2690486907959 then
                         return 1.0 # (15.0 out of 15.0)
                      else  # if same_day_duration_avg_diff > -50.2690486907959
                         return 0.5238095238095238 # (11.0 out of 21.0)
                      end                     end                   else  # if prev_count_x > 25.5
                     return 0.8 # (16.0 out of 20.0)
                  end                 else  # if same_day_duration_avg_diff > 9.119444370269775
                  case when LLOC_before <= 3.0 then
                     return 0.3658008658008658 # (169.0 out of 462.0)
                  else  # if LLOC_before > 3.0
                     return 0.85 # (17.0 out of 20.0)
                  end                 end               else  # if McCabe_sum_after > 19.5
                case when one_file_fix_rate_diff <= -0.06969697214663029 then
                  case when refactor_mle_diff <= -0.11297626420855522 then
                     return 0.25 # (3.0 out of 12.0)
                  else  # if refactor_mle_diff > -0.11297626420855522
                     return 0.75 # (15.0 out of 20.0)
                  end                 else  # if one_file_fix_rate_diff > -0.06969697214663029
                  case when hunks_num <= 2.5 then
                    case when Blank_before <= 146.5 then
                       return 0.34210526315789475 # (13.0 out of 38.0)
                    else  # if Blank_before > 146.5
                       return 0.75 # (15.0 out of 20.0)
                    end                   else  # if hunks_num > 2.5
                    case when LOC_diff <= -22.0 then
                       return 0.375 # (6.0 out of 16.0)
                    else  # if LOC_diff > -22.0
                      case when Comments_after <= 23.5 then
                         return 0.2631578947368421 # (5.0 out of 19.0)
                      else  # if Comments_after > 23.5
                        case when changed_lines <= 44.5 then
                           return 0.0625 # (1.0 out of 16.0)
                        else  # if changed_lines > 44.5
                           return 0.0 # (0.0 out of 18.0)
                        end                       end                     end                   end                 end               end             else  # if SLOC_diff > 34.5
              case when removed_lines <= 117.0 then
                 return 0.7142857142857143 # (10.0 out of 14.0)
              else  # if removed_lines > 117.0
                 return 1.0 # (16.0 out of 16.0)
              end             end           end         else  # if McCabe_max_after > 18.5
          case when SLOC_before <= 885.0 then
            case when hunks_num <= 11.5 then
              case when Blank_diff <= -0.5 then
                 return 0.6190476190476191 # (13.0 out of 21.0)
              else  # if Blank_diff > -0.5
                case when one_file_fix_rate_diff <= 0.02380952425301075 then
                  case when McCabe_sum_after <= 128.0 then
                     return 0.1111111111111111 # (2.0 out of 18.0)
                  else  # if McCabe_sum_after > 128.0
                     return 0.2631578947368421 # (5.0 out of 19.0)
                  end                 else  # if one_file_fix_rate_diff > 0.02380952425301075
                   return 0.5333333333333333 # (8.0 out of 15.0)
                end               end             else  # if hunks_num > 11.5
               return 0.0 # (0.0 out of 38.0)
            end           else  # if SLOC_before > 885.0
            case when Comments_after <= 198.5 then
               return 0.7142857142857143 # (20.0 out of 28.0)
            else  # if Comments_after > 198.5
               return 0.30434782608695654 # (7.0 out of 23.0)
            end           end         end       end     end   else  # if McCabe_max_after > 39.5
    case when changed_lines <= 54.0 then
      case when Comments_before <= 116.5 then
         return 0.7142857142857143 # (15.0 out of 21.0)
      else  # if Comments_before > 116.5
         return 0.3333333333333333 # (8.0 out of 24.0)
      end     else  # if changed_lines > 54.0
      case when removed_lines <= 170.5 then
         return 0.96 # (24.0 out of 25.0)
      else  # if removed_lines > 170.5
         return 0.6666666666666666 # (8.0 out of 12.0)
      end     end   end )