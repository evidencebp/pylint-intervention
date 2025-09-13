create or replace function RandomForest_9 (h1_diff int64, SLOC_before int64, avg_coupling_code_size_cut_diff int64, Multi_diff int64, using-constant-test int64, high_McCabe_sum_diff int64, difficulty_diff int64, LLOC_diff int64, length_diff int64, Comments_after int64, McCabe_max_before int64, low_McCabe_sum_before int64, cur_count int64, LOC_before int64, low_McCabe_max_before int64, massive_change int64, too-many-return-statements int64, Comments_diff int64, added_lines int64, broad-exception-caught int64, comparison-of-constants int64, Single comments_diff int64, refactor_mle_diff int64, prev_count_x int64, McCabe_sum_before int64, modified_McCabe_max_diff int64, Simplify-boolean-expression int64, Blank_diff int64, added_functions int64, LLOC_before int64, cur_count_x int64, high_McCabe_sum_before int64, volume_diff int64, low_McCabe_max_diff int64, LOC_diff int64, calculated_length_diff int64, changed_lines int64, N2_diff int64, h2_diff int64, too-many-lines int64, unnecessary-pass int64, simplifiable-if-statement int64, prev_count int64, too-many-nested-blocks int64, Comments_before int64, SLOC_diff int64, McCabe_sum_after int64, bugs_diff int64, cur_count_y int64, Single comments_after int64, McCabe_max_diff int64, N1_diff int64, wildcard-import int64, McCabe_sum_diff int64, prev_count_y int64, superfluous-parens int64, hunks_num int64, try-except-raise int64, simplifiable-if-expression int64, McCabe_max_after int64, high_McCabe_max_diff int64, too-many-statements int64, simplifiable-condition int64, only_removal int64, unnecessary-semicolon int64, effort_diff int64, is_refactor int64, same_day_duration_avg_diff int64, one_file_fix_rate_diff int64, high_McCabe_max_before int64, vocabulary_diff int64, too-many-branches int64, mostly_delete int64, high_ccp_group int64, low_ccp_group int64, removed_lines int64, Single comments_before int64, low_McCabe_sum_diff int64, time_diff int64, Blank_before int64, line-too-long int64, too-many-boolean-expressions int64, pointless-statement int64) as (
  case when SLOC_diff <= 38.0 then
    case when McCabe_max_after <= 7.5 then
      case when Comments_after <= 76.5 then
        case when Comments_diff <= -2.5 then
          case when Multi_diff <= -16.5 then
             return 0.7894736842105263 # (0.7894736842105263 out of 1.0)
          else  # if Multi_diff > -16.5
             return 1.0 # (1.0 out of 1.0)
          end         else  # if Comments_diff > -2.5
          case when McCabe_sum_after <= 1.0 then
             return 0.9 # (0.9 out of 1.0)
          else  # if McCabe_sum_after > 1.0
            case when SLOC_before <= 251.0 then
              case when added_lines <= 13.0 then
                 return 0.6470588235294118 # (0.6470588235294118 out of 1.0)
              else  # if added_lines > 13.0
                 return 0.16 # (0.16 out of 1.0)
              end             else  # if SLOC_before > 251.0
               return 0.7619047619047619 # (0.7619047619047619 out of 1.0)
            end           end         end       else  # if Comments_after > 76.5
         return 0.15384615384615385 # (0.15384615384615385 out of 1.0)
      end     else  # if McCabe_max_after > 7.5
      case when low_ccp_group <= 0.5 then
        case when high_ccp_group <= 0.5 then
          case when removed_lines <= 2.5 then
            case when SLOC_before <= 595.5 then
               return 0.42857142857142855 # (0.42857142857142855 out of 1.0)
            else  # if SLOC_before > 595.5
              case when vocabulary_diff <= -6.5 then
                 return 0.0 # (0.0 out of 1.0)
              else  # if vocabulary_diff > -6.5
                 return 0.1875 # (0.1875 out of 1.0)
              end             end           else  # if removed_lines > 2.5
            case when refactor_mle_diff <= 0.420738086104393 then
              case when LLOC_diff <= -92.5 then
                 return 0.8571428571428571 # (0.8571428571428571 out of 1.0)
              else  # if LLOC_diff > -92.5
                case when Single comments_after <= 100.5 then
                  case when McCabe_sum_diff <= 1.5 then
                    case when Blank_before <= 137.0 then
                      case when vocabulary_diff <= -0.5 then
                         return 0.8421052631578947 # (0.8421052631578947 out of 1.0)
                      else  # if vocabulary_diff > -0.5
                         return 0.52 # (0.52 out of 1.0)
                      end                     else  # if Blank_before > 137.0
                       return 0.4 # (0.4 out of 1.0)
                    end                   else  # if McCabe_sum_diff > 1.5
                     return 0.13333333333333333 # (0.13333333333333333 out of 1.0)
                  end                 else  # if Single comments_after > 100.5
                  case when Single comments_after <= 177.0 then
                     return 0.11764705882352941 # (0.11764705882352941 out of 1.0)
                  else  # if Single comments_after > 177.0
                     return 0.4375 # (0.4375 out of 1.0)
                  end                 end               end             else  # if refactor_mle_diff > 0.420738086104393
               return 0.0 # (0.0 out of 1.0)
            end           end         else  # if high_ccp_group > 0.5
          case when Single comments_after <= 20.0 then
             return 0.2631578947368421 # (0.2631578947368421 out of 1.0)
          else  # if Single comments_after > 20.0
            case when refactor_mle_diff <= -0.08266359195113182 then
              case when refactor_mle_diff <= -0.1550946906208992 then
                 return 0.5555555555555556 # (0.5555555555555556 out of 1.0)
              else  # if refactor_mle_diff > -0.1550946906208992
                 return 0.2 # (0.2 out of 1.0)
              end             else  # if refactor_mle_diff > -0.08266359195113182
              case when added_lines <= 21.0 then
                 return 0.9615384615384616 # (0.9615384615384616 out of 1.0)
              else  # if added_lines > 21.0
                 return 0.5882352941176471 # (0.5882352941176471 out of 1.0)
              end             end           end         end       else  # if low_ccp_group > 0.5
        case when LLOC_diff <= -41.0 then
           return 0.4375 # (0.4375 out of 1.0)
        else  # if LLOC_diff > -41.0
          case when McCabe_sum_after <= 220.5 then
            case when LLOC_before <= 318.0 then
               return 0.047619047619047616 # (0.047619047619047616 out of 1.0)
            else  # if LLOC_before > 318.0
               return 0.0 # (0.0 out of 1.0)
            end           else  # if McCabe_sum_after > 220.5
             return 0.25 # (0.25 out of 1.0)
          end         end       end     end   else  # if SLOC_diff > 38.0
    case when LLOC_before <= 685.5 then
      case when Single comments_before <= 31.0 then
         return 0.8421052631578947 # (0.8421052631578947 out of 1.0)
      else  # if Single comments_before > 31.0
         return 1.0 # (1.0 out of 1.0)
      end     else  # if LLOC_before > 685.5
       return 0.45 # (0.45 out of 1.0)
    end   end )