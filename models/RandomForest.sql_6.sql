create or replace function RandomForest_6 (low_McCabe_max_before int64, LLOC_before int64, low_McCabe_sum_diff int64, modified_McCabe_max_diff int64, bugs_diff int64, McCabe_max_before int64, Single comments_before int64, prev_count_y int64, added_lines int64, LLOC_diff int64, N2_diff int64, added_functions int64, prev_count int64, too-many-boolean-expressions int64, SLOC_diff int64, mostly_delete int64, time_diff int64, calculated_length_diff int64, McCabe_max_after int64, Comments_diff int64, line-too-long int64, McCabe_sum_after int64, one_file_fix_rate_diff int64, h1_diff int64, high_McCabe_max_diff int64, too-many-branches int64, SLOC_before int64, cur_count_y int64, prev_count_x int64, McCabe_sum_before int64, Comments_after int64, wildcard-import int64, unnecessary-semicolon int64, same_day_duration_avg_diff int64, effort_diff int64, too-many-statements int64, broad-exception-caught int64, LOC_before int64, cur_count int64, Comments_before int64, using-constant-test int64, LOC_diff int64, high_McCabe_sum_diff int64, only_removal int64, superfluous-parens int64, try-except-raise int64, Blank_before int64, McCabe_max_diff int64, N1_diff int64, massive_change int64, refactor_mle_diff int64, pointless-statement int64, too-many-lines int64, simplifiable-if-statement int64, high_McCabe_sum_before int64, vocabulary_diff int64, removed_lines int64, difficulty_diff int64, Simplify-boolean-expression int64, avg_coupling_code_size_cut_diff int64, Single comments_after int64, low_ccp_group int64, Multi_diff int64, is_refactor int64, hunks_num int64, Single comments_diff int64, length_diff int64, unnecessary-pass int64, Blank_diff int64, h2_diff int64, changed_lines int64, cur_count_x int64, low_McCabe_max_diff int64, high_McCabe_max_before int64, high_ccp_group int64, too-many-nested-blocks int64, McCabe_sum_diff int64, volume_diff int64, comparison-of-constants int64, too-many-return-statements int64, simplifiable-condition int64, simplifiable-if-expression int64, low_McCabe_sum_before int64) as (
  case when LOC_diff <= 46.0 then
    case when high_ccp_group <= 0.5 then
      case when Comments_diff <= -4.5 then
        case when same_day_duration_avg_diff <= 9.772172689437866 then
          case when SLOC_diff <= -112.0 then
             return 0.4444444444444444 # (0.4444444444444444 out of 1.0)
          else  # if SLOC_diff > -112.0
             return 0.19230769230769232 # (0.19230769230769232 out of 1.0)
          end         else  # if same_day_duration_avg_diff > 9.772172689437866
          case when vocabulary_diff <= -46.0 then
             return 1.0 # (1.0 out of 1.0)
          else  # if vocabulary_diff > -46.0
             return 0.6842105263157895 # (0.6842105263157895 out of 1.0)
          end         end       else  # if Comments_diff > -4.5
        case when LOC_before <= 143.0 then
           return 0.6 # (0.6 out of 1.0)
        else  # if LOC_before > 143.0
          case when added_functions <= 2.5 then
            case when avg_coupling_code_size_cut_diff <= 1.8458558917045593 then
              case when broad-exception-caught <= 0.5 then
                case when one_file_fix_rate_diff <= 0.2361111119389534 then
                  case when superfluous-parens <= 0.5 then
                    case when LOC_diff <= 11.5 then
                      case when McCabe_sum_before <= 14.0 then
                         return 0.5 # (0.5 out of 1.0)
                      else  # if McCabe_sum_before > 14.0
                        case when McCabe_sum_after <= 198.0 then
                          case when avg_coupling_code_size_cut_diff <= 0.3166666775941849 then
                            case when LOC_before <= 761.5 then
                              case when SLOC_before <= 172.0 then
                                 return 0.1111111111111111 # (0.1111111111111111 out of 1.0)
                              else  # if SLOC_before > 172.0
                                 return 0.0 # (0.0 out of 1.0)
                              end                             else  # if LOC_before > 761.5
                              case when refactor_mle_diff <= 0.012770370580255985 then
                                 return 0.0 # (0.0 out of 1.0)
                              else  # if refactor_mle_diff > 0.012770370580255985
                                 return 0.5 # (0.5 out of 1.0)
                              end                             end                           else  # if avg_coupling_code_size_cut_diff > 0.3166666775941849
                             return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
                          end                         else  # if McCabe_sum_after > 198.0
                           return 0.0 # (0.0 out of 1.0)
                        end                       end                     else  # if LOC_diff > 11.5
                       return 0.391304347826087 # (0.391304347826087 out of 1.0)
                    end                   else  # if superfluous-parens > 0.5
                     return 0.4827586206896552 # (0.4827586206896552 out of 1.0)
                  end                 else  # if one_file_fix_rate_diff > 0.2361111119389534
                   return 0.6086956521739131 # (0.6086956521739131 out of 1.0)
                end               else  # if broad-exception-caught > 0.5
                 return 0.0 # (0.0 out of 1.0)
              end             else  # if avg_coupling_code_size_cut_diff > 1.8458558917045593
               return 0.6285714285714286 # (0.6285714285714286 out of 1.0)
            end           else  # if added_functions > 2.5
             return 0.08695652173913043 # (0.08695652173913043 out of 1.0)
          end         end       end     else  # if high_ccp_group > 0.5
      case when LLOC_before <= 364.0 then
        case when Single comments_before <= 21.5 then
           return 0.9 # (0.9 out of 1.0)
        else  # if Single comments_before > 21.5
           return 1.0 # (1.0 out of 1.0)
        end       else  # if LLOC_before > 364.0
        case when McCabe_max_before <= 17.0 then
           return 0.9473684210526315 # (0.9473684210526315 out of 1.0)
        else  # if McCabe_max_before > 17.0
          case when SLOC_diff <= -102.0 then
             return 0.14814814814814814 # (0.14814814814814814 out of 1.0)
          else  # if SLOC_diff > -102.0
            case when LOC_before <= 1158.0 then
               return 0.16129032258064516 # (0.16129032258064516 out of 1.0)
            else  # if LOC_before > 1158.0
              case when same_day_duration_avg_diff <= 11.75 then
                 return 0.7647058823529411 # (0.7647058823529411 out of 1.0)
              else  # if same_day_duration_avg_diff > 11.75
                 return 0.7692307692307693 # (0.7692307692307693 out of 1.0)
              end             end           end         end       end     end   else  # if LOC_diff > 46.0
    case when Blank_before <= 63.5 then
       return 1.0 # (1.0 out of 1.0)
    else  # if Blank_before > 63.5
      case when McCabe_sum_after <= 181.0 then
         return 0.7692307692307693 # (0.7692307692307693 out of 1.0)
      else  # if McCabe_sum_after > 181.0
         return 0.2 # (0.2 out of 1.0)
      end     end   end )