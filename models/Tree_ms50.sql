create or replace function Tree_ms50 (prev_count int64, prev_count_x int64, prev_count_y int64, using-constant-test int64, Comments_diff int64, massive_change int64, McCabe_max_after int64, Comments_before int64, too-many-statements int64, cur_count_x int64, h1_diff int64, McCabe_sum_diff int64, LLOC_before int64, McCabe_sum_before int64, high_McCabe_max_before int64, avg_coupling_code_size_cut_diff int64, is_refactor int64, N2_diff int64, too-many-branches int64, SLOC_before int64, too-many-nested-blocks int64, too-many-lines int64, bugs_diff int64, time_diff int64, Single comments_after int64, simplifiable-condition int64, Multi_diff int64, high_McCabe_sum_before int64, low_ccp_group int64, refactor_mle_diff int64, low_McCabe_max_diff int64, SLOC_diff int64, changed_lines int64, hunks_num int64, McCabe_sum_after int64, cur_count_y int64, one_file_fix_rate_diff int64, low_McCabe_sum_before int64, modified_McCabe_max_diff int64, superfluous-parens int64, mostly_delete int64, added_functions int64, Comments_after int64, N1_diff int64, McCabe_max_diff int64, simplifiable-if-statement int64, LOC_before int64, low_McCabe_max_before int64, McCabe_max_before int64, try-except-raise int64, line-too-long int64, unnecessary-semicolon int64, wildcard-import int64, difficulty_diff int64, Simplify-boolean-expression int64, cur_count int64, low_McCabe_sum_diff int64, pointless-statement int64, length_diff int64, broad-exception-caught int64, h2_diff int64, high_McCabe_sum_diff int64, only_removal int64, comparison-of-constants int64, Single comments_diff int64, too-many-boolean-expressions int64, Blank_before int64, calculated_length_diff int64, Single comments_before int64, removed_lines int64, simplifiable-if-expression int64, LOC_diff int64, volume_diff int64, high_McCabe_max_diff int64, high_ccp_group int64, same_day_duration_avg_diff int64, Blank_diff int64, effort_diff int64, too-many-return-statements int64, added_lines int64, unnecessary-pass int64, vocabulary_diff int64, LLOC_diff int64) as (
  case when high_ccp_group <= 0.5 then
    case when h1_diff <= -4.5 then
      case when avg_coupling_code_size_cut_diff <= 0.27243589982390404 then
        case when h1_diff <= -5.5 then
           return 1.0 # (1.0 out of 1.0)
        else  # if h1_diff > -5.5
           return 0.75 # (0.75 out of 1.0)
        end       else  # if avg_coupling_code_size_cut_diff > 0.27243589982390404
         return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
      end     else  # if h1_diff > -4.5
      case when low_ccp_group <= 0.5 then
        case when Comments_before <= 23.5 then
          case when one_file_fix_rate_diff <= 0.08472222462296486 then
            case when McCabe_max_after <= 10.5 then
              case when McCabe_max_after <= 5.5 then
                 return 0.7857142857142857 # (0.7857142857142857 out of 1.0)
              else  # if McCabe_max_after > 5.5
                case when LOC_diff <= -0.5 then
                   return 0.25 # (0.25 out of 1.0)
                else  # if LOC_diff > -0.5
                   return 0.47058823529411764 # (0.47058823529411764 out of 1.0)
                end               end             else  # if McCabe_max_after > 10.5
               return 1.0 # (1.0 out of 1.0)
            end           else  # if one_file_fix_rate_diff > 0.08472222462296486
             return 0.14285714285714285 # (0.14285714285714285 out of 1.0)
          end         else  # if Comments_before > 23.5
          case when McCabe_max_after <= 47.5 then
            case when Blank_diff <= 6.5 then
              case when same_day_duration_avg_diff <= -128.49257278442383 then
                 return 0.3793103448275862 # (0.3793103448275862 out of 1.0)
              else  # if same_day_duration_avg_diff > -128.49257278442383
                case when superfluous-parens <= 0.5 then
                  case when McCabe_sum_after <= 56.5 then
                    case when McCabe_sum_before <= 41.0 then
                       return 0.09090909090909091 # (0.09090909090909091 out of 1.0)
                    else  # if McCabe_sum_before > 41.0
                       return 0.625 # (0.625 out of 1.0)
                    end                   else  # if McCabe_sum_after > 56.5
                    case when Single comments_after <= 69.5 then
                      case when modified_McCabe_max_diff <= -1.5 then
                         return 0.14285714285714285 # (0.14285714285714285 out of 1.0)
                      else  # if modified_McCabe_max_diff > -1.5
                        case when LOC_before <= 1052.0 then
                          case when Comments_before <= 29.5 then
                             return 0.03571428571428571 # (0.03571428571428571 out of 1.0)
                          else  # if Comments_before > 29.5
                             return 0.0 # (0.0 out of 1.0)
                          end                         else  # if LOC_before > 1052.0
                           return 0.09090909090909091 # (0.09090909090909091 out of 1.0)
                        end                       end                     else  # if Single comments_after > 69.5
                      case when Single comments_before <= 95.5 then
                         return 0.5714285714285714 # (0.5714285714285714 out of 1.0)
                      else  # if Single comments_before > 95.5
                        case when LOC_before <= 1830.5 then
                           return 0.019230769230769232 # (0.019230769230769232 out of 1.0)
                        else  # if LOC_before > 1830.5
                           return 0.14285714285714285 # (0.14285714285714285 out of 1.0)
                        end                       end                     end                   end                 else  # if superfluous-parens > 0.5
                  case when McCabe_sum_after <= 273.0 then
                     return 0.1 # (0.1 out of 1.0)
                  else  # if McCabe_sum_after > 273.0
                     return 0.6 # (0.6 out of 1.0)
                  end                 end               end             else  # if Blank_diff > 6.5
              case when same_day_duration_avg_diff <= -29.55000114440918 then
                 return 1.0 # (1.0 out of 1.0)
              else  # if same_day_duration_avg_diff > -29.55000114440918
                 return 0.18181818181818182 # (0.18181818181818182 out of 1.0)
              end             end           else  # if McCabe_max_after > 47.5
             return 0.52 # (0.52 out of 1.0)
          end         end       else  # if low_ccp_group > 0.5
        case when Single comments_diff <= 21.0 then
          case when added_lines <= 147.5 then
            case when LLOC_diff <= 2.5 then
              case when too-many-statements <= 0.5 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if too-many-statements > 0.5
                 return 0.05714285714285714 # (0.05714285714285714 out of 1.0)
              end             else  # if LLOC_diff > 2.5
              case when LOC_diff <= 14.0 then
                 return 0.25 # (0.25 out of 1.0)
              else  # if LOC_diff > 14.0
                 return 0.0 # (0.0 out of 1.0)
              end             end           else  # if added_lines > 147.5
            case when avg_coupling_code_size_cut_diff <= 0.03750000149011612 then
               return 0.3333333333333333 # (0.3333333333333333 out of 1.0)
            else  # if avg_coupling_code_size_cut_diff > 0.03750000149011612
               return 0.03225806451612903 # (0.03225806451612903 out of 1.0)
            end           end         else  # if Single comments_diff > 21.0
           return 0.6666666666666666 # (0.6666666666666666 out of 1.0)
        end       end     end   else  # if high_ccp_group > 0.5
    case when McCabe_sum_before <= 135.5 then
      case when refactor_mle_diff <= -0.02819955162703991 then
         return 0.4827586206896552 # (0.4827586206896552 out of 1.0)
      else  # if refactor_mle_diff > -0.02819955162703991
        case when vocabulary_diff <= -2.5 then
           return 0.75 # (0.75 out of 1.0)
        else  # if vocabulary_diff > -2.5
           return 1.0 # (1.0 out of 1.0)
        end       end     else  # if McCabe_sum_before > 135.5
      case when McCabe_sum_after <= 195.5 then
        case when Comments_before <= 82.5 then
          case when McCabe_sum_before <= 155.5 then
             return 0.12903225806451613 # (0.12903225806451613 out of 1.0)
          else  # if McCabe_sum_before > 155.5
             return 0.5714285714285714 # (0.5714285714285714 out of 1.0)
          end         else  # if Comments_before > 82.5
           return 0.021739130434782608 # (0.021739130434782608 out of 1.0)
        end       else  # if McCabe_sum_after > 195.5
        case when McCabe_sum_after <= 242.0 then
           return 1.0 # (1.0 out of 1.0)
        else  # if McCabe_sum_after > 242.0
          case when SLOC_before <= 1436.0 then
             return 0.18181818181818182 # (0.18181818181818182 out of 1.0)
          else  # if SLOC_before > 1436.0
             return 0.8125 # (0.8125 out of 1.0)
          end         end       end     end   end )