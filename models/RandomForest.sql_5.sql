create or replace function RandomForest_5 (LOC_diff int64, Comments_after int64, volume_diff int64, LOC_before int64, McCabe_max_diff int64, Blank_diff int64, unnecessary-pass int64, McCabe_max_before int64, prev_count_x int64, prev_count_y int64, N2_diff int64, LLOC_before int64, prev_count int64, too-many-branches int64, added_functions int64, length_diff int64, h2_diff int64, removed_lines int64, too-many-nested-blocks int64, comparison-of-constants int64, bugs_diff int64, N1_diff int64, Comments_diff int64, line-too-long int64, McCabe_sum_diff int64, superfluous-parens int64, Multi_diff int64, changed_lines int64, McCabe_sum_before int64, calculated_length_diff int64, Single comments_after int64, time_diff int64, Single comments_diff int64, Comments_before int64, added_lines int64, effort_diff int64, refactor_mle_diff int64, Blank_before int64, too-many-return-statements int64, pointless-statement int64, too-many-statements int64, cur_count_y int64, unnecessary-semicolon int64, cur_count_x int64, using-constant-test int64, McCabe_sum_after int64, McCabe_max_after int64, too-many-lines int64, LLOC_diff int64, difficulty_diff int64, simplifiable-if-statement int64, vocabulary_diff int64, SLOC_before int64, modified_McCabe_max_diff int64, wildcard-import int64, one_file_fix_rate_diff int64, simplifiable-condition int64, SLOC_diff int64, h1_diff int64, same_day_duration_avg_diff int64, Single comments_before int64, cur_count int64, try-except-raise int64, Simplify-boolean-expression int64, simplifiable-if-expression int64, broad-exception-caught int64, hunks_num int64, too-many-boolean-expressions int64, avg_coupling_code_size_cut_diff int64) as (
  case when avg_coupling_code_size_cut_diff <= -1.2015084624290466 then
    case when one_file_fix_rate_diff <= 0.7321428656578064 then
      case when one_file_fix_rate_diff <= -0.4833333343267441 then
         return 0.7222222222222222 # (13.0 out of 18.0)
      else  # if one_file_fix_rate_diff > -0.4833333343267441
        case when McCabe_max_after <= 8.5 then
          case when Comments_after <= 13.0 then
            case when cur_count_x <= 5.5 then
               return 0.367816091954023 # (64.0 out of 174.0)
            else  # if cur_count_x > 5.5
               return 0.6923076923076923 # (9.0 out of 13.0)
            end           else  # if Comments_after > 13.0
             return 0.5263157894736842 # (10.0 out of 19.0)
          end         else  # if McCabe_max_after > 8.5
          case when McCabe_sum_before <= 279.5 then
            case when McCabe_sum_after <= 96.5 then
               return 0.11764705882352941 # (2.0 out of 17.0)
            else  # if McCabe_sum_after > 96.5
               return 0.0 # (0.0 out of 37.0)
            end           else  # if McCabe_sum_before > 279.5
             return 0.3333333333333333 # (5.0 out of 15.0)
          end         end       end     else  # if one_file_fix_rate_diff > 0.7321428656578064
       return 0.8636363636363636 # (19.0 out of 22.0)
    end   else  # if avg_coupling_code_size_cut_diff > -1.2015084624290466
    case when LOC_before <= 17.0 then
      case when pointless-statement <= 0.5 then
        case when too-many-boolean-expressions <= 0.5 then
          case when broad-exception-caught <= 0.5 then
            case when avg_coupling_code_size_cut_diff <= 3.2666666507720947 then
              case when too-many-statements <= 0.5 then
                case when one_file_fix_rate_diff <= -0.3049516826868057 then
                  case when refactor_mle_diff <= -0.17814243584871292 then
                     return 0.11538461538461539 # (3.0 out of 26.0)
                  else  # if refactor_mle_diff > -0.17814243584871292
                     return 0.36363636363636365 # (32.0 out of 88.0)
                  end                 else  # if one_file_fix_rate_diff > -0.3049516826868057
                  case when simplifiable-if-expression <= 0.5 then
                    case when refactor_mle_diff <= 0.09404562786221504 then
                      case when one_file_fix_rate_diff <= -0.1871657744050026 then
                         return 0.8695652173913043 # (20.0 out of 23.0)
                      else  # if one_file_fix_rate_diff > -0.1871657744050026
                        case when prev_count_x <= 46.5 then
                          case when same_day_duration_avg_diff <= 43.11904716491699 then
                             return 0.5714285714285714 # (164.0 out of 287.0)
                          else  # if same_day_duration_avg_diff > 43.11904716491699
                            case when prev_count_x <= 0.5 then
                              case when same_day_duration_avg_diff <= 115.79716491699219 then
                                 return 0.20833333333333334 # (5.0 out of 24.0)
                              else  # if same_day_duration_avg_diff > 115.79716491699219
                                 return 0.625 # (10.0 out of 16.0)
                              end                             else  # if prev_count_x > 0.5
                               return 0.32 # (8.0 out of 25.0)
                            end                           end                         else  # if prev_count_x > 46.5
                           return 0.23076923076923078 # (3.0 out of 13.0)
                        end                       end                     else  # if refactor_mle_diff > 0.09404562786221504
                      case when avg_coupling_code_size_cut_diff <= 0.9343253970146179 then
                         return 0.29523809523809524 # (31.0 out of 105.0)
                      else  # if avg_coupling_code_size_cut_diff > 0.9343253970146179
                        case when same_day_duration_avg_diff <= -44.33333396911621 then
                           return 0.35 # (7.0 out of 20.0)
                        else  # if same_day_duration_avg_diff > -44.33333396911621
                           return 0.71875 # (23.0 out of 32.0)
                        end                       end                     end                   else  # if simplifiable-if-expression > 0.5
                     return 0.45454545454545453 # (10.0 out of 22.0)
                  end                 end               else  # if too-many-statements > 0.5
                case when avg_coupling_code_size_cut_diff <= -0.012394958408549428 then
                  case when refactor_mle_diff <= -0.16063597798347473 then
                     return 0.35714285714285715 # (5.0 out of 14.0)
                  else  # if refactor_mle_diff > -0.16063597798347473
                    case when same_day_duration_avg_diff <= 58.764509201049805 then
                      case when prev_count_x <= 0.5 then
                         return 0.5714285714285714 # (16.0 out of 28.0)
                      else  # if prev_count_x > 0.5
                         return 0.47058823529411764 # (8.0 out of 17.0)
                      end                     else  # if same_day_duration_avg_diff > 58.764509201049805
                       return 0.75 # (12.0 out of 16.0)
                    end                   end                 else  # if avg_coupling_code_size_cut_diff > -0.012394958408549428
                  case when avg_coupling_code_size_cut_diff <= 0.24166666716337204 then
                     return 0.1935483870967742 # (6.0 out of 31.0)
                  else  # if avg_coupling_code_size_cut_diff > 0.24166666716337204
                    case when same_day_duration_avg_diff <= 1.397790014743805 then
                      case when same_day_duration_avg_diff <= -40.71875 then
                         return 0.42857142857142855 # (6.0 out of 14.0)
                      else  # if same_day_duration_avg_diff > -40.71875
                        case when avg_coupling_code_size_cut_diff <= 1.5182926654815674 then
                           return 0.7272727272727273 # (16.0 out of 22.0)
                        else  # if avg_coupling_code_size_cut_diff > 1.5182926654815674
                           return 0.5833333333333334 # (7.0 out of 12.0)
                        end                       end                     else  # if same_day_duration_avg_diff > 1.397790014743805
                      case when refactor_mle_diff <= -0.04788888990879059 then
                         return 0.07142857142857142 # (1.0 out of 14.0)
                      else  # if refactor_mle_diff > -0.04788888990879059
                         return 0.3333333333333333 # (9.0 out of 27.0)
                      end                     end                   end                 end               end             else  # if avg_coupling_code_size_cut_diff > 3.2666666507720947
               return 0.2413793103448276 # (7.0 out of 29.0)
            end           else  # if broad-exception-caught > 0.5
            case when refactor_mle_diff <= 0.004310000222176313 then
               return 0.38095238095238093 # (8.0 out of 21.0)
            else  # if refactor_mle_diff > 0.004310000222176313
               return 0.8571428571428571 # (12.0 out of 14.0)
            end           end         else  # if too-many-boolean-expressions > 0.5
           return 0.17391304347826086 # (4.0 out of 23.0)
        end       else  # if pointless-statement > 0.5
         return 0.7894736842105263 # (15.0 out of 19.0)
      end     else  # if LOC_before > 17.0
      case when Blank_before <= 29.0 then
        case when added_functions <= 0.5 then
          case when McCabe_max_after <= 5.5 then
             return 0.9523809523809523 # (20.0 out of 21.0)
          else  # if McCabe_max_after > 5.5
             return 0.6428571428571429 # (9.0 out of 14.0)
          end         else  # if added_functions > 0.5
           return 0.9444444444444444 # (17.0 out of 18.0)
        end       else  # if Blank_before > 29.0
        case when removed_lines <= 198.0 then
          case when McCabe_sum_diff <= -8.5 then
            case when N1_diff <= -26.5 then
              case when LOC_diff <= -366.5 then
                 return 0.5833333333333334 # (14.0 out of 24.0)
              else  # if LOC_diff > -366.5
                 return 0.7142857142857143 # (15.0 out of 21.0)
              end             else  # if N1_diff > -26.5
              case when McCabe_max_before <= 17.5 then
                 return 0.4117647058823529 # (7.0 out of 17.0)
              else  # if McCabe_max_before > 17.5
                case when McCabe_sum_diff <= -19.0 then
                   return 0.05263157894736842 # (1.0 out of 19.0)
                else  # if McCabe_sum_diff > -19.0
                   return 0.17391304347826086 # (4.0 out of 23.0)
                end               end             end           else  # if McCabe_sum_diff > -8.5
            case when removed_lines <= 122.0 then
              case when Multi_diff <= 4.5 then
                case when McCabe_sum_after <= 41.5 then
                  case when LLOC_before <= 177.0 then
                     return 0.5263157894736842 # (10.0 out of 19.0)
                  else  # if LLOC_before > 177.0
                     return 0.14285714285714285 # (2.0 out of 14.0)
                  end                 else  # if McCabe_sum_after > 41.5
                  case when McCabe_sum_before <= 63.5 then
                     return 0.9545454545454546 # (21.0 out of 22.0)
                  else  # if McCabe_sum_before > 63.5
                    case when Single comments_after <= 71.5 then
                      case when LOC_diff <= -4.0 then
                         return 0.9310344827586207 # (27.0 out of 29.0)
                      else  # if LOC_diff > -4.0
                        case when length_diff <= 1.0 then
                          case when McCabe_sum_after <= 145.5 then
                             return 0.375 # (12.0 out of 32.0)
                          else  # if McCabe_sum_after > 145.5
                             return 0.6666666666666666 # (20.0 out of 30.0)
                          end                         else  # if length_diff > 1.0
                           return 0.9411764705882353 # (16.0 out of 17.0)
                        end                       end                     else  # if Single comments_after > 71.5
                      case when hunks_num <= 1.5 then
                         return 0.7037037037037037 # (19.0 out of 27.0)
                      else  # if hunks_num > 1.5
                        case when LLOC_before <= 1076.5 then
                          case when same_day_duration_avg_diff <= 35.50384521484375 then
                             return 0.0 # (0.0 out of 23.0)
                          else  # if same_day_duration_avg_diff > 35.50384521484375
                             return 0.3125 # (5.0 out of 16.0)
                          end                         else  # if LLOC_before > 1076.5
                           return 0.7727272727272727 # (17.0 out of 22.0)
                        end                       end                     end                   end                 end               else  # if Multi_diff > 4.5
                 return 0.28 # (7.0 out of 25.0)
              end             else  # if removed_lines > 122.0
              case when refactor_mle_diff <= -0.011288095265626907 then
                 return 0.7692307692307693 # (10.0 out of 13.0)
              else  # if refactor_mle_diff > -0.011288095265626907
                 return 1.0 # (19.0 out of 19.0)
              end             end           end         else  # if removed_lines > 198.0
          case when LOC_diff <= 81.5 then
            case when Blank_before <= 91.0 then
               return 0.25 # (4.0 out of 16.0)
            else  # if Blank_before > 91.0
               return 0.05263157894736842 # (1.0 out of 19.0)
            end           else  # if LOC_diff > 81.5
             return 0.5217391304347826 # (12.0 out of 23.0)
          end         end       end     end   end )