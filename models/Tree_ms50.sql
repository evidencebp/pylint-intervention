create or replace function Tree_ms50 (LOC_diff int64, Comments_after int64, volume_diff int64, LOC_before int64, McCabe_max_diff int64, Blank_diff int64, unnecessary-pass int64, McCabe_max_before int64, prev_count_x int64, prev_count_y int64, N2_diff int64, LLOC_before int64, prev_count int64, too-many-branches int64, added_functions int64, length_diff int64, h2_diff int64, removed_lines int64, too-many-nested-blocks int64, comparison-of-constants int64, bugs_diff int64, N1_diff int64, Comments_diff int64, line-too-long int64, McCabe_sum_diff int64, superfluous-parens int64, Multi_diff int64, changed_lines int64, McCabe_sum_before int64, calculated_length_diff int64, Single comments_after int64, time_diff int64, Single comments_diff int64, Comments_before int64, added_lines int64, effort_diff int64, refactor_mle_diff int64, Blank_before int64, too-many-return-statements int64, pointless-statement int64, too-many-statements int64, cur_count_y int64, unnecessary-semicolon int64, cur_count_x int64, using-constant-test int64, McCabe_sum_after int64, McCabe_max_after int64, too-many-lines int64, LLOC_diff int64, difficulty_diff int64, simplifiable-if-statement int64, vocabulary_diff int64, SLOC_before int64, modified_McCabe_max_diff int64, wildcard-import int64, one_file_fix_rate_diff int64, simplifiable-condition int64, SLOC_diff int64, h1_diff int64, same_day_duration_avg_diff int64, Single comments_before int64, cur_count int64, try-except-raise int64, Simplify-boolean-expression int64, simplifiable-if-expression int64, broad-exception-caught int64, hunks_num int64, too-many-boolean-expressions int64, avg_coupling_code_size_cut_diff int64) as (
  case when SLOC_diff <= 38.0 then
    case when hunks_num <= 11.5 then
      case when Single comments_diff <= -2.5 then
        case when hunks_num <= 1.5 then
           return 0.07692307692307693 # (1.0 out of 13.0)
        else  # if hunks_num > 1.5
          case when McCabe_max_after <= 6.5 then
             return 1.0 # (30.0 out of 30.0)
          else  # if McCabe_max_after > 6.5
            case when SLOC_diff <= -46.5 then
              case when Single comments_after <= 43.0 then
                 return 0.5 # (5.0 out of 10.0)
              else  # if Single comments_after > 43.0
                case when Multi_diff <= -7.0 then
                   return 0.9 # (9.0 out of 10.0)
                else  # if Multi_diff > -7.0
                   return 1.0 # (18.0 out of 18.0)
                end               end             else  # if SLOC_diff > -46.5
              case when modified_McCabe_max_diff <= -0.5 then
                 return 0.6 # (9.0 out of 15.0)
              else  # if modified_McCabe_max_diff > -0.5
                 return 0.1 # (1.0 out of 10.0)
              end             end           end         end       else  # if Single comments_diff > -2.5
        case when same_day_duration_avg_diff <= -0.05050504952669144 then
          case when same_day_duration_avg_diff <= -40.4897518157959 then
            case when LOC_diff <= 7.5 then
              case when Comments_after <= 101.5 then
                case when pointless-statement <= 0.5 then
                  case when one_file_fix_rate_diff <= -0.16919191926717758 then
                    case when one_file_fix_rate_diff <= -0.25162337720394135 then
                      case when too-many-statements <= 0.5 then
                        case when refactor_mle_diff <= -0.05360841192305088 then
                          case when refactor_mle_diff <= -0.22628816217184067 then
                             return 0.45454545454545453 # (5.0 out of 11.0)
                          else  # if refactor_mle_diff > -0.22628816217184067
                             return 0.09090909090909091 # (1.0 out of 11.0)
                          end                         else  # if refactor_mle_diff > -0.05360841192305088
                          case when same_day_duration_avg_diff <= -91.3452377319336 then
                             return 0.42857142857142855 # (6.0 out of 14.0)
                          else  # if same_day_duration_avg_diff > -91.3452377319336
                             return 0.7 # (7.0 out of 10.0)
                          end                         end                       else  # if too-many-statements > 0.5
                         return 0.7 # (7.0 out of 10.0)
                      end                     else  # if one_file_fix_rate_diff > -0.25162337720394135
                       return 0.8235294117647058 # (14.0 out of 17.0)
                    end                   else  # if one_file_fix_rate_diff > -0.16919191926717758
                    case when same_day_duration_avg_diff <= -58.42618942260742 then
                      case when same_day_duration_avg_diff <= -123.35833358764648 then
                        case when one_file_fix_rate_diff <= 0.550000011920929 then
                          case when one_file_fix_rate_diff <= 0.3166666775941849 then
                            case when refactor_mle_diff <= -0.09835204109549522 then
                              case when same_day_duration_avg_diff <= -253.490478515625 then
                                 return 0.4666666666666667 # (7.0 out of 15.0)
                              else  # if same_day_duration_avg_diff > -253.490478515625
                                 return 0.11764705882352941 # (2.0 out of 17.0)
                              end                             else  # if refactor_mle_diff > -0.09835204109549522
                              case when too-many-statements <= 0.5 then
                                case when prev_count_x <= 0.5 then
                                  case when refactor_mle_diff <= 0.17445237934589386 then
                                     return 0.9090909090909091 # (10.0 out of 11.0)
                                  else  # if refactor_mle_diff > 0.17445237934589386
                                     return 0.6363636363636364 # (7.0 out of 11.0)
                                  end                                 else  # if prev_count_x > 0.5
                                   return 0.4 # (6.0 out of 15.0)
                                end                               else  # if too-many-statements > 0.5
                                 return 0.3076923076923077 # (4.0 out of 13.0)
                              end                             end                           else  # if one_file_fix_rate_diff > 0.3166666775941849
                             return 0.7692307692307693 # (10.0 out of 13.0)
                          end                         else  # if one_file_fix_rate_diff > 0.550000011920929
                           return 0.18181818181818182 # (2.0 out of 11.0)
                        end                       else  # if same_day_duration_avg_diff > -123.35833358764648
                        case when McCabe_max_before <= 14.5 then
                          case when one_file_fix_rate_diff <= 0.361111119389534 then
                            case when removed_lines <= 4.5 then
                              case when refactor_mle_diff <= 0.16214898228645325 then
                                case when refactor_mle_diff <= -0.032295944169163704 then
                                  case when refactor_mle_diff <= -0.1041116900742054 then
                                    case when avg_coupling_code_size_cut_diff <= 0.4583333283662796 then
                                      case when same_day_duration_avg_diff <= -77.69488143920898 then
                                         return 0.0 # (0.0 out of 22.0)
                                      else  # if same_day_duration_avg_diff > -77.69488143920898
                                         return 0.2 # (2.0 out of 10.0)
                                      end                                     else  # if avg_coupling_code_size_cut_diff > 0.4583333283662796
                                       return 0.3076923076923077 # (4.0 out of 13.0)
                                    end                                   else  # if refactor_mle_diff > -0.1041116900742054
                                     return 0.6 # (6.0 out of 10.0)
                                  end                                 else  # if refactor_mle_diff > -0.032295944169163704
                                  case when prev_count_x <= 2.5 then
                                     return 0.0 # (0.0 out of 23.0)
                                  else  # if prev_count_x > 2.5
                                     return 0.2 # (2.0 out of 10.0)
                                  end                                 end                               else  # if refactor_mle_diff > 0.16214898228645325
                                 return 0.375 # (6.0 out of 16.0)
                              end                             else  # if removed_lines > 4.5
                               return 0.45454545454545453 # (5.0 out of 11.0)
                            end                           else  # if one_file_fix_rate_diff > 0.361111119389534
                             return 0.47368421052631576 # (9.0 out of 19.0)
                          end                         else  # if McCabe_max_before > 14.5
                           return 0.6428571428571429 # (9.0 out of 14.0)
                        end                       end                     else  # if same_day_duration_avg_diff > -58.42618942260742
                      case when avg_coupling_code_size_cut_diff <= -0.17888471484184265 then
                        case when same_day_duration_avg_diff <= -49.407371520996094 then
                           return 1.0 # (15.0 out of 15.0)
                        else  # if same_day_duration_avg_diff > -49.407371520996094
                           return 0.5 # (7.0 out of 14.0)
                        end                       else  # if avg_coupling_code_size_cut_diff > -0.17888471484184265
                        case when refactor_mle_diff <= -0.0016203006962314248 then
                          case when avg_coupling_code_size_cut_diff <= 0.7452380955219269 then
                             return 0.2 # (2.0 out of 10.0)
                          else  # if avg_coupling_code_size_cut_diff > 0.7452380955219269
                             return 0.1 # (1.0 out of 10.0)
                          end                         else  # if refactor_mle_diff > -0.0016203006962314248
                          case when refactor_mle_diff <= 0.09939264878630638 then
                             return 0.5833333333333334 # (7.0 out of 12.0)
                          else  # if refactor_mle_diff > 0.09939264878630638
                             return 0.2727272727272727 # (3.0 out of 11.0)
                          end                         end                       end                     end                   end                 else  # if pointless-statement > 0.5
                   return 0.7692307692307693 # (10.0 out of 13.0)
                end               else  # if Comments_after > 101.5
                case when Comments_after <= 174.0 then
                   return 0.0 # (0.0 out of 14.0)
                else  # if Comments_after > 174.0
                   return 0.3 # (3.0 out of 10.0)
                end               end             else  # if LOC_diff > 7.5
               return 0.75 # (12.0 out of 16.0)
            end           else  # if same_day_duration_avg_diff > -40.4897518157959
            case when one_file_fix_rate_diff <= -0.40238095819950104 then
              case when LLOC_before <= 150.0 then
                case when one_file_fix_rate_diff <= -0.5178571343421936 then
                  case when one_file_fix_rate_diff <= -0.875 then
                     return 0.8333333333333334 # (10.0 out of 12.0)
                  else  # if one_file_fix_rate_diff > -0.875
                     return 0.7 # (7.0 out of 10.0)
                  end                 else  # if one_file_fix_rate_diff > -0.5178571343421936
                   return 0.5 # (5.0 out of 10.0)
                end               else  # if LLOC_before > 150.0
                 return 1.0 # (10.0 out of 10.0)
              end             else  # if one_file_fix_rate_diff > -0.40238095819950104
              case when one_file_fix_rate_diff <= -0.28312864899635315 then
                 return 0.14285714285714285 # (2.0 out of 14.0)
              else  # if one_file_fix_rate_diff > -0.28312864899635315
                case when Comments_after <= 43.5 then
                  case when same_day_duration_avg_diff <= -11.298230171203613 then
                    case when same_day_duration_avg_diff <= -14.866071701049805 then
                      case when avg_coupling_code_size_cut_diff <= -1.1443452835083008 then
                         return 0.8421052631578947 # (16.0 out of 19.0)
                      else  # if avg_coupling_code_size_cut_diff > -1.1443452835083008
                        case when Comments_after <= 9.0 then
                          case when one_file_fix_rate_diff <= 0.050735294818878174 then
                            case when same_day_duration_avg_diff <= -30.31666660308838 then
                              case when one_file_fix_rate_diff <= -0.01923076994717121 then
                                 return 0.8888888888888888 # (16.0 out of 18.0)
                              else  # if one_file_fix_rate_diff > -0.01923076994717121
                                 return 0.5 # (9.0 out of 18.0)
                              end                             else  # if same_day_duration_avg_diff > -30.31666660308838
                              case when same_day_duration_avg_diff <= -25.68333339691162 then
                                 return 0.0 # (0.0 out of 10.0)
                              else  # if same_day_duration_avg_diff > -25.68333339691162
                                case when refactor_mle_diff <= -0.027226736769080162 then
                                   return 0.375 # (6.0 out of 16.0)
                                else  # if refactor_mle_diff > -0.027226736769080162
                                   return 0.7692307692307693 # (10.0 out of 13.0)
                                end                               end                             end                           else  # if one_file_fix_rate_diff > 0.050735294818878174
                            case when refactor_mle_diff <= 0.013060606084764004 then
                              case when prev_count_x <= 0.5 then
                                case when avg_coupling_code_size_cut_diff <= 0.47232143580913544 then
                                   return 0.8181818181818182 # (9.0 out of 11.0)
                                else  # if avg_coupling_code_size_cut_diff > 0.47232143580913544
                                   return 0.5 # (5.0 out of 10.0)
                                end                               else  # if prev_count_x > 0.5
                                 return 1.0 # (13.0 out of 13.0)
                              end                             else  # if refactor_mle_diff > 0.013060606084764004
                               return 0.5714285714285714 # (8.0 out of 14.0)
                            end                           end                         else  # if Comments_after > 9.0
                           return 0.3333333333333333 # (4.0 out of 12.0)
                        end                       end                     else  # if same_day_duration_avg_diff > -14.866071701049805
                      case when prev_count_x <= 0.5 then
                         return 1.0 # (12.0 out of 12.0)
                      else  # if prev_count_x > 0.5
                         return 0.8 # (8.0 out of 10.0)
                      end                     end                   else  # if same_day_duration_avg_diff > -11.298230171203613
                    case when same_day_duration_avg_diff <= -2.1611111164093018 then
                      case when same_day_duration_avg_diff <= -3.6820013523101807 then
                        case when refactor_mle_diff <= 0.10975776612758636 then
                          case when too-many-statements <= 0.5 then
                            case when same_day_duration_avg_diff <= -6.907541513442993 then
                               return 0.4 # (6.0 out of 15.0)
                            else  # if same_day_duration_avg_diff > -6.907541513442993
                               return 0.18181818181818182 # (2.0 out of 11.0)
                            end                           else  # if too-many-statements > 0.5
                             return 0.6153846153846154 # (8.0 out of 13.0)
                          end                         else  # if refactor_mle_diff > 0.10975776612758636
                           return 0.7142857142857143 # (10.0 out of 14.0)
                        end                       else  # if same_day_duration_avg_diff > -3.6820013523101807
                         return 0.15384615384615385 # (2.0 out of 13.0)
                      end                     else  # if same_day_duration_avg_diff > -2.1611111164093018
                       return 0.6666666666666666 # (12.0 out of 18.0)
                    end                   end                 else  # if Comments_after > 43.5
                  case when McCabe_max_after <= 15.5 then
                     return 0.11764705882352941 # (2.0 out of 17.0)
                  else  # if McCabe_max_after > 15.5
                     return 0.5 # (9.0 out of 18.0)
                  end                 end               end             end           end         else  # if same_day_duration_avg_diff > -0.05050504952669144
          case when McCabe_max_before <= 51.0 then
            case when McCabe_max_diff <= -5.5 then
               return 0.0 # (0.0 out of 23.0)
            else  # if McCabe_max_diff > -5.5
              case when McCabe_max_after <= 34.0 then
                case when McCabe_sum_after <= 101.0 then
                  case when Comments_before <= 102.0 then
                    case when one_file_fix_rate_diff <= 0.26713287830352783 then
                      case when cur_count_x <= 66.5 then
                        case when prev_count_x <= 18.0 then
                          case when prev_count_y <= 0.5 then
                            case when one_file_fix_rate_diff <= 0.1665591448545456 then
                              case when too-many-boolean-expressions <= 0.5 then
                                case when avg_coupling_code_size_cut_diff <= 1.1547619104385376 then
                                  case when same_day_duration_avg_diff <= 139.0772705078125 then
                                    case when same_day_duration_avg_diff <= 63.5015869140625 then
                                      case when cur_count_x <= 3.5 then
                                        case when refactor_mle_diff <= 0.06844497099518776 then
                                          case when same_day_duration_avg_diff <= 55.85763931274414 then
                                            case when same_day_duration_avg_diff <= 24.349340438842773 then
                                              case when one_file_fix_rate_diff <= 0.009259259328246117 then
                                                case when refactor_mle_diff <= -0.07031123340129852 then
                                                  case when same_day_duration_avg_diff <= 15.383241653442383 then
                                                    case when same_day_duration_avg_diff <= 6.435606241226196 then
                                                       return 0.6 # (6.0 out of 10.0)
                                                    else  # if same_day_duration_avg_diff > 6.435606241226196
                                                       return 1.0 # (12.0 out of 12.0)
                                                    end                                                   else  # if same_day_duration_avg_diff > 15.383241653442383
                                                     return 0.5 # (5.0 out of 10.0)
                                                  end                                                 else  # if refactor_mle_diff > -0.07031123340129852
                                                  case when refactor_mle_diff <= 0.007682709489017725 then
                                                    case when same_day_duration_avg_diff <= 7.989898920059204 then
                                                       return 0.4 # (6.0 out of 15.0)
                                                    else  # if same_day_duration_avg_diff > 7.989898920059204
                                                       return 0.2 # (2.0 out of 10.0)
                                                    end                                                   else  # if refactor_mle_diff > 0.007682709489017725
                                                     return 0.6363636363636364 # (7.0 out of 11.0)
                                                  end                                                 end                                               else  # if one_file_fix_rate_diff > 0.009259259328246117
                                                 return 0.1 # (1.0 out of 10.0)
                                              end                                             else  # if same_day_duration_avg_diff > 24.349340438842773
                                              case when cur_count_x <= 1.5 then
                                                case when avg_coupling_code_size_cut_diff <= -0.3511904776096344 then
                                                   return 0.07142857142857142 # (1.0 out of 14.0)
                                                else  # if avg_coupling_code_size_cut_diff > -0.3511904776096344
                                                  case when one_file_fix_rate_diff <= -0.0416666679084301 then
                                                     return 0.45454545454545453 # (5.0 out of 11.0)
                                                  else  # if one_file_fix_rate_diff > -0.0416666679084301
                                                     return 0.25 # (4.0 out of 16.0)
                                                  end                                                 end                                               else  # if cur_count_x > 1.5
                                                 return 0.46153846153846156 # (6.0 out of 13.0)
                                              end                                             end                                           else  # if same_day_duration_avg_diff > 55.85763931274414
                                             return 0.7272727272727273 # (8.0 out of 11.0)
                                          end                                         else  # if refactor_mle_diff > 0.06844497099518776
                                          case when refactor_mle_diff <= 0.22173862904310226 then
                                            case when refactor_mle_diff <= 0.181062251329422 then
                                              case when avg_coupling_code_size_cut_diff <= -0.26153846830129623 then
                                                 return 0.16666666666666666 # (2.0 out of 12.0)
                                              else  # if avg_coupling_code_size_cut_diff > -0.26153846830129623
                                                 return 0.3 # (3.0 out of 10.0)
                                              end                                             else  # if refactor_mle_diff > 0.181062251329422
                                               return 0.0 # (0.0 out of 11.0)
                                            end                                           else  # if refactor_mle_diff > 0.22173862904310226
                                            case when avg_coupling_code_size_cut_diff <= -0.7075320482254028 then
                                               return 0.5833333333333334 # (7.0 out of 12.0)
                                            else  # if avg_coupling_code_size_cut_diff > -0.7075320482254028
                                               return 0.29411764705882354 # (5.0 out of 17.0)
                                            end                                           end                                         end                                       else  # if cur_count_x > 3.5
                                        case when same_day_duration_avg_diff <= 14.36868143081665 then
                                           return 0.0 # (0.0 out of 10.0)
                                        else  # if same_day_duration_avg_diff > 14.36868143081665
                                           return 0.2857142857142857 # (4.0 out of 14.0)
                                        end                                       end                                     else  # if same_day_duration_avg_diff > 63.5015869140625
                                      case when refactor_mle_diff <= 0.0006760784308426082 then
                                        case when avg_coupling_code_size_cut_diff <= -0.8253284096717834 then
                                           return 0.18181818181818182 # (2.0 out of 11.0)
                                        else  # if avg_coupling_code_size_cut_diff > -0.8253284096717834
                                           return 0.0 # (0.0 out of 21.0)
                                        end                                       else  # if refactor_mle_diff > 0.0006760784308426082
                                        case when superfluous-parens <= 0.5 then
                                           return 0.17647058823529413 # (3.0 out of 17.0)
                                        else  # if superfluous-parens > 0.5
                                           return 0.6 # (6.0 out of 10.0)
                                        end                                       end                                     end                                   else  # if same_day_duration_avg_diff > 139.0772705078125
                                    case when avg_coupling_code_size_cut_diff <= 0.01785714365541935 then
                                      case when same_day_duration_avg_diff <= 192.5952377319336 then
                                         return 0.7333333333333333 # (11.0 out of 15.0)
                                      else  # if same_day_duration_avg_diff > 192.5952377319336
                                        case when same_day_duration_avg_diff <= 247.22142791748047 then
                                           return 0.3 # (3.0 out of 10.0)
                                        else  # if same_day_duration_avg_diff > 247.22142791748047
                                           return 0.5833333333333334 # (7.0 out of 12.0)
                                        end                                       end                                     else  # if avg_coupling_code_size_cut_diff > 0.01785714365541935
                                       return 0.2727272727272727 # (3.0 out of 11.0)
                                    end                                   end                                 else  # if avg_coupling_code_size_cut_diff > 1.1547619104385376
                                  case when refactor_mle_diff <= 0.05365701764822006 then
                                    case when same_day_duration_avg_diff <= 5.983731985092163 then
                                       return 0.7 # (7.0 out of 10.0)
                                    else  # if same_day_duration_avg_diff > 5.983731985092163
                                      case when refactor_mle_diff <= -0.272966668009758 then
                                         return 0.6153846153846154 # (8.0 out of 13.0)
                                      else  # if refactor_mle_diff > -0.272966668009758
                                        case when same_day_duration_avg_diff <= 28.604629516601562 then
                                           return 0.0 # (0.0 out of 10.0)
                                        else  # if same_day_duration_avg_diff > 28.604629516601562
                                          case when same_day_duration_avg_diff <= 135.8011245727539 then
                                             return 0.5263157894736842 # (10.0 out of 19.0)
                                          else  # if same_day_duration_avg_diff > 135.8011245727539
                                             return 0.09090909090909091 # (1.0 out of 11.0)
                                          end                                         end                                       end                                     end                                   else  # if refactor_mle_diff > 0.05365701764822006
                                    case when refactor_mle_diff <= 0.22053766250610352 then
                                       return 0.9333333333333333 # (14.0 out of 15.0)
                                    else  # if refactor_mle_diff > 0.22053766250610352
                                       return 0.4117647058823529 # (7.0 out of 17.0)
                                    end                                   end                                 end                               else  # if too-many-boolean-expressions > 0.5
                                 return 0.0625 # (1.0 out of 16.0)
                              end                             else  # if one_file_fix_rate_diff > 0.1665591448545456
                              case when one_file_fix_rate_diff <= 0.1775210127234459 then
                                 return 0.9 # (9.0 out of 10.0)
                              else  # if one_file_fix_rate_diff > 0.1775210127234459
                                case when same_day_duration_avg_diff <= 38.82900333404541 then
                                   return 0.5833333333333334 # (7.0 out of 12.0)
                                else  # if same_day_duration_avg_diff > 38.82900333404541
                                   return 0.2 # (2.0 out of 10.0)
                                end                               end                             end                           else  # if prev_count_y > 0.5
                            case when McCabe_sum_after <= 19.0 then
                              case when avg_coupling_code_size_cut_diff <= -0.5166666805744171 then
                                 return 1.0 # (12.0 out of 12.0)
                              else  # if avg_coupling_code_size_cut_diff > -0.5166666805744171
                                 return 0.6666666666666666 # (12.0 out of 18.0)
                              end                             else  # if McCabe_sum_after > 19.0
                              case when McCabe_max_after <= 9.5 then
                                 return 0.1 # (1.0 out of 10.0)
                              else  # if McCabe_max_after > 9.5
                                 return 0.3888888888888889 # (7.0 out of 18.0)
                              end                             end                           end                         else  # if prev_count_x > 18.0
                           return 0.8571428571428571 # (12.0 out of 14.0)
                        end                       else  # if cur_count_x > 66.5
                         return 0.07692307692307693 # (1.0 out of 13.0)
                      end                     else  # if one_file_fix_rate_diff > 0.26713287830352783
                      case when same_day_duration_avg_diff <= 48.272727966308594 then
                        case when same_day_duration_avg_diff <= 21.48488998413086 then
                           return 0.2 # (3.0 out of 15.0)
                        else  # if same_day_duration_avg_diff > 21.48488998413086
                           return 0.6 # (6.0 out of 10.0)
                        end                       else  # if same_day_duration_avg_diff > 48.272727966308594
                        case when one_file_fix_rate_diff <= 0.561904788017273 then
                          case when one_file_fix_rate_diff <= 0.40963202714920044 then
                             return 0.0625 # (1.0 out of 16.0)
                          else  # if one_file_fix_rate_diff > 0.40963202714920044
                             return 0.5 # (5.0 out of 10.0)
                          end                         else  # if one_file_fix_rate_diff > 0.561904788017273
                           return 0.0 # (0.0 out of 10.0)
                        end                       end                     end                   else  # if Comments_before > 102.0
                     return 0.0 # (0.0 out of 11.0)
                  end                 else  # if McCabe_sum_after > 101.0
                  case when refactor_mle_diff <= -0.29168687760829926 then
                     return 0.2727272727272727 # (3.0 out of 11.0)
                  else  # if refactor_mle_diff > -0.29168687760829926
                    case when McCabe_sum_after <= 154.0 then
                       return 1.0 # (12.0 out of 12.0)
                    else  # if McCabe_sum_after > 154.0
                      case when refactor_mle_diff <= -0.00530461547896266 then
                         return 0.8461538461538461 # (11.0 out of 13.0)
                      else  # if refactor_mle_diff > -0.00530461547896266
                         return 0.3333333333333333 # (6.0 out of 18.0)
                      end                     end                   end                 end               else  # if McCabe_max_after > 34.0
                case when Blank_before <= 245.0 then
                   return 0.0 # (0.0 out of 12.0)
                else  # if Blank_before > 245.0
                   return 0.2 # (2.0 out of 10.0)
                end               end             end           else  # if McCabe_max_before > 51.0
             return 1.0 # (11.0 out of 11.0)
          end         end       end     else  # if hunks_num > 11.5
      case when Comments_after <= 213.0 then
        case when McCabe_max_before <= 15.5 then
           return 0.5384615384615384 # (7.0 out of 13.0)
        else  # if McCabe_max_before > 15.5
          case when LLOC_before <= 439.0 then
             return 0.26666666666666666 # (4.0 out of 15.0)
          else  # if LLOC_before > 439.0
            case when LOC_before <= 1637.0 then
               return 0.0 # (0.0 out of 54.0)
            else  # if LOC_before > 1637.0
               return 0.1 # (1.0 out of 10.0)
            end           end         end       else  # if Comments_after > 213.0
         return 0.7 # (7.0 out of 10.0)
      end     end   else  # if SLOC_diff > 38.0
    case when removed_lines <= 376.5 then
      case when length_diff <= 14.5 then
        case when LOC_diff <= 78.0 then
           return 1.0 # (23.0 out of 23.0)
        else  # if LOC_diff > 78.0
           return 0.9 # (9.0 out of 10.0)
        end       else  # if length_diff > 14.5
         return 0.625 # (10.0 out of 16.0)
      end     else  # if removed_lines > 376.5
       return 0.35714285714285715 # (5.0 out of 14.0)
    end   end )