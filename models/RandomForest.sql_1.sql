create or replace function RandomForest_1 (LOC_diff int64, Comments_after int64, volume_diff int64, LOC_before int64, McCabe_max_diff int64, Blank_diff int64, unnecessary-pass int64, McCabe_max_before int64, prev_count_x int64, prev_count_y int64, N2_diff int64, LLOC_before int64, prev_count int64, too-many-branches int64, added_functions int64, length_diff int64, h2_diff int64, removed_lines int64, too-many-nested-blocks int64, comparison-of-constants int64, bugs_diff int64, N1_diff int64, Comments_diff int64, line-too-long int64, McCabe_sum_diff int64, superfluous-parens int64, Multi_diff int64, changed_lines int64, McCabe_sum_before int64, calculated_length_diff int64, Single comments_after int64, time_diff int64, Single comments_diff int64, Comments_before int64, added_lines int64, effort_diff int64, refactor_mle_diff int64, Blank_before int64, too-many-return-statements int64, pointless-statement int64, too-many-statements int64, cur_count_y int64, unnecessary-semicolon int64, cur_count_x int64, using-constant-test int64, McCabe_sum_after int64, McCabe_max_after int64, too-many-lines int64, LLOC_diff int64, difficulty_diff int64, simplifiable-if-statement int64, vocabulary_diff int64, SLOC_before int64, modified_McCabe_max_diff int64, wildcard-import int64, one_file_fix_rate_diff int64, simplifiable-condition int64, SLOC_diff int64, h1_diff int64, same_day_duration_avg_diff int64, Single comments_before int64, cur_count int64, try-except-raise int64, Simplify-boolean-expression int64, simplifiable-if-expression int64, broad-exception-caught int64, hunks_num int64, too-many-boolean-expressions int64, avg_coupling_code_size_cut_diff int64) as (
  case when Comments_diff <= -11.5 then
    case when McCabe_max_diff <= -6.5 then
       return 0.92 # (23.0 out of 25.0)
    else  # if McCabe_max_diff > -6.5
      case when McCabe_sum_after <= 81.0 then
         return 0.29411764705882354 # (5.0 out of 17.0)
      else  # if McCabe_sum_after > 81.0
         return 0.7333333333333333 # (11.0 out of 15.0)
      end     end   else  # if Comments_diff > -11.5
    case when N2_diff <= 0.5 then
      case when hunks_num <= 11.5 then
        case when cur_count_x <= 1.5 then
          case when prev_count_y <= 2.5 then
            case when vocabulary_diff <= -23.5 then
               return 0.15384615384615385 # (4.0 out of 26.0)
            else  # if vocabulary_diff > -23.5
              case when avg_coupling_code_size_cut_diff <= 1.8357142806053162 then
                case when Blank_diff <= 6.5 then
                  case when pointless-statement <= 0.5 then
                    case when McCabe_max_diff <= -7.5 then
                       return 0.058823529411764705 # (1.0 out of 17.0)
                    else  # if McCabe_max_diff > -7.5
                      case when cur_count_x <= 0.5 then
                        case when McCabe_max_before <= 28.5 then
                          case when Comments_diff <= -3.5 then
                             return 0.8823529411764706 # (15.0 out of 17.0)
                          else  # if Comments_diff > -3.5
                            case when changed_lines <= 2.5 then
                              case when Single comments_after <= 0.5 then
                                 return 0.5263157894736842 # (60.0 out of 114.0)
                              else  # if Single comments_after > 0.5
                                 return 0.9032258064516129 # (28.0 out of 31.0)
                              end                             else  # if changed_lines > 2.5
                              case when LLOC_before <= 584.0 then
                                case when Comments_after <= 13.5 then
                                   return 0.7916666666666666 # (19.0 out of 24.0)
                                else  # if Comments_after > 13.5
                                  case when LOC_diff <= -14.0 then
                                     return 0.38095238095238093 # (8.0 out of 21.0)
                                  else  # if LOC_diff > -14.0
                                    case when SLOC_before <= 271.5 then
                                       return 0.0 # (0.0 out of 25.0)
                                    else  # if SLOC_before > 271.5
                                      case when LOC_before <= 752.5 then
                                         return 0.2857142857142857 # (4.0 out of 14.0)
                                      else  # if LOC_before > 752.5
                                         return 0.1875 # (3.0 out of 16.0)
                                      end                                     end                                   end                                 end                               else  # if LLOC_before > 584.0
                                case when McCabe_max_before <= 17.5 then
                                   return 0.8333333333333334 # (15.0 out of 18.0)
                                else  # if McCabe_max_before > 17.5
                                   return 0.65 # (13.0 out of 20.0)
                                end                               end                             end                           end                         else  # if McCabe_max_before > 28.5
                          case when LOC_diff <= -1.5 then
                             return 0.4117647058823529 # (7.0 out of 17.0)
                          else  # if LOC_diff > -1.5
                            case when refactor_mle_diff <= -0.12902969121932983 then
                               return 0.1111111111111111 # (2.0 out of 18.0)
                            else  # if refactor_mle_diff > -0.12902969121932983
                               return 0.4117647058823529 # (7.0 out of 17.0)
                            end                           end                         end                       else  # if cur_count_x > 0.5
                        case when refactor_mle_diff <= 0.5086335390806198 then
                           return 0.40644171779141103 # (265.0 out of 652.0)
                        else  # if refactor_mle_diff > 0.5086335390806198
                           return 0.7333333333333333 # (11.0 out of 15.0)
                        end                       end                     end                   else  # if pointless-statement > 0.5
                     return 0.7666666666666667 # (23.0 out of 30.0)
                  end                 else  # if Blank_diff > 6.5
                   return 1.0 # (13.0 out of 13.0)
                end               else  # if avg_coupling_code_size_cut_diff > 1.8357142806053162
                case when Blank_before <= 55.0 then
                  case when prev_count_x <= 0.5 then
                     return 0.71875 # (46.0 out of 64.0)
                  else  # if prev_count_x > 0.5
                     return 0.6296296296296297 # (17.0 out of 27.0)
                  end                 else  # if Blank_before > 55.0
                   return 0.8095238095238095 # (17.0 out of 21.0)
                end               end             end           else  # if prev_count_y > 2.5
             return 0.13636363636363635 # (3.0 out of 22.0)
          end         else  # if cur_count_x > 1.5
          case when too-many-branches <= 0.5 then
             return 0.384375 # (123.0 out of 320.0)
          else  # if too-many-branches > 0.5
             return 0.2727272727272727 # (6.0 out of 22.0)
          end         end       else  # if hunks_num > 11.5
        case when Single comments_after <= 52.5 then
           return 0.32 # (8.0 out of 25.0)
        else  # if Single comments_after > 52.5
          case when Blank_before <= 135.0 then
             return 0.0 # (0.0 out of 26.0)
          else  # if Blank_before > 135.0
            case when Multi_diff <= -7.5 then
               return 0.0 # (0.0 out of 17.0)
            else  # if Multi_diff > -7.5
               return 0.26666666666666666 # (4.0 out of 15.0)
            end           end         end       end     else  # if N2_diff > 0.5
      case when N2_diff <= 2.5 then
         return 0.9705882352941176 # (33.0 out of 34.0)
      else  # if N2_diff > 2.5
        case when McCabe_sum_after <= 235.5 then
          case when LLOC_diff <= 9.5 then
             return 0.5909090909090909 # (13.0 out of 22.0)
          else  # if LLOC_diff > 9.5
             return 0.21052631578947367 # (4.0 out of 19.0)
          end         else  # if McCabe_sum_after > 235.5
           return 0.7916666666666666 # (19.0 out of 24.0)
        end       end     end   end )