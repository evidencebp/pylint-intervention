create or replace function RandomForest_2 (low_McCabe_max_before int64, LLOC_before int64, low_McCabe_sum_diff int64, modified_McCabe_max_diff int64, bugs_diff int64, McCabe_max_before int64, Single comments_before int64, prev_count_y int64, added_lines int64, LLOC_diff int64, N2_diff int64, added_functions int64, prev_count int64, too-many-boolean-expressions int64, SLOC_diff int64, mostly_delete int64, time_diff int64, calculated_length_diff int64, McCabe_max_after int64, Comments_diff int64, line-too-long int64, McCabe_sum_after int64, one_file_fix_rate_diff int64, h1_diff int64, high_McCabe_max_diff int64, too-many-branches int64, SLOC_before int64, cur_count_y int64, prev_count_x int64, McCabe_sum_before int64, Comments_after int64, wildcard-import int64, unnecessary-semicolon int64, same_day_duration_avg_diff int64, effort_diff int64, too-many-statements int64, broad-exception-caught int64, LOC_before int64, cur_count int64, Comments_before int64, using-constant-test int64, LOC_diff int64, high_McCabe_sum_diff int64, only_removal int64, superfluous-parens int64, try-except-raise int64, Blank_before int64, McCabe_max_diff int64, N1_diff int64, massive_change int64, refactor_mle_diff int64, pointless-statement int64, too-many-lines int64, simplifiable-if-statement int64, high_McCabe_sum_before int64, vocabulary_diff int64, removed_lines int64, difficulty_diff int64, Simplify-boolean-expression int64, avg_coupling_code_size_cut_diff int64, Single comments_after int64, low_ccp_group int64, Multi_diff int64, is_refactor int64, hunks_num int64, Single comments_diff int64, length_diff int64, unnecessary-pass int64, Blank_diff int64, h2_diff int64, changed_lines int64, cur_count_x int64, low_McCabe_max_diff int64, high_McCabe_max_before int64, high_ccp_group int64, too-many-nested-blocks int64, McCabe_sum_diff int64, volume_diff int64, comparison-of-constants int64, too-many-return-statements int64, simplifiable-condition int64, simplifiable-if-expression int64, low_McCabe_sum_before int64) as (
  case when low_ccp_group <= 0.5 then
    case when McCabe_max_before <= 18.5 then
      case when SLOC_before <= 106.0 then
         return 1.0 # (1.0 out of 1.0)
      else  # if SLOC_before > 106.0
        case when added_lines <= 53.0 then
          case when avg_coupling_code_size_cut_diff <= 0.40138889849185944 then
            case when low_McCabe_max_before <= 0.5 then
              case when hunks_num <= 3.5 then
                 return 0.9333333333333333 # (0.9333333333333333 out of 1.0)
              else  # if hunks_num > 3.5
                 return 0.5238095238095238 # (0.5238095238095238 out of 1.0)
              end             else  # if low_McCabe_max_before > 0.5
              case when SLOC_diff <= -0.5 then
                 return 0.7619047619047619 # (0.7619047619047619 out of 1.0)
              else  # if SLOC_diff > -0.5
                 return 0.08695652173913043 # (0.08695652173913043 out of 1.0)
              end             end           else  # if avg_coupling_code_size_cut_diff > 0.40138889849185944
            case when SLOC_before <= 545.0 then
               return 0.36 # (0.36 out of 1.0)
            else  # if SLOC_before > 545.0
               return 0.05555555555555555 # (0.05555555555555555 out of 1.0)
            end           end         else  # if added_lines > 53.0
          case when h1_diff <= -0.5 then
             return 0.7142857142857143 # (0.7142857142857143 out of 1.0)
          else  # if h1_diff > -0.5
            case when SLOC_before <= 309.5 then
               return 0.9230769230769231 # (0.9230769230769231 out of 1.0)
            else  # if SLOC_before > 309.5
               return 1.0 # (1.0 out of 1.0)
            end           end         end       end     else  # if McCabe_max_before > 18.5
      case when Blank_before <= 176.0 then
        case when Single comments_after <= 80.0 then
          case when Single comments_diff <= 0.5 then
            case when removed_lines <= 9.5 then
              case when McCabe_max_before <= 23.5 then
                 return 0.26666666666666666 # (0.26666666666666666 out of 1.0)
              else  # if McCabe_max_before > 23.5
                 return 0.48 # (0.48 out of 1.0)
              end             else  # if removed_lines > 9.5
              case when LLOC_before <= 436.0 then
                 return 0.8260869565217391 # (0.8260869565217391 out of 1.0)
              else  # if LLOC_before > 436.0
                 return 0.44 # (0.44 out of 1.0)
              end             end           else  # if Single comments_diff > 0.5
             return 0.1 # (0.1 out of 1.0)
          end         else  # if Single comments_after > 80.0
          case when N2_diff <= -7.0 then
             return 0.07692307692307693 # (0.07692307692307693 out of 1.0)
          else  # if N2_diff > -7.0
             return 0.0 # (0.0 out of 1.0)
          end         end       else  # if Blank_before > 176.0
        case when Single comments_before <= 368.0 then
          case when h2_diff <= 0.5 then
            case when SLOC_before <= 966.0 then
               return 0.5 # (0.5 out of 1.0)
            else  # if SLOC_before > 966.0
              case when LLOC_before <= 994.0 then
                 return 0.9333333333333333 # (0.9333333333333333 out of 1.0)
              else  # if LLOC_before > 994.0
                 return 0.625 # (0.625 out of 1.0)
              end             end           else  # if h2_diff > 0.5
             return 1.0 # (1.0 out of 1.0)
          end         else  # if Single comments_before > 368.0
           return 0.12 # (0.12 out of 1.0)
        end       end     end   else  # if low_ccp_group > 0.5
    case when added_functions <= 0.5 then
      case when N2_diff <= -24.5 then
         return 0.4375 # (0.4375 out of 1.0)
      else  # if N2_diff > -24.5
        case when LLOC_diff <= 1.0 then
          case when LLOC_diff <= -7.5 then
             return 0.0625 # (0.0625 out of 1.0)
          else  # if LLOC_diff > -7.5
             return 0.0 # (0.0 out of 1.0)
          end         else  # if LLOC_diff > 1.0
           return 0.2631578947368421 # (0.2631578947368421 out of 1.0)
        end       end     else  # if added_functions > 0.5
      case when mostly_delete <= 0.5 then
        case when Comments_after <= 79.5 then
           return 0.13333333333333333 # (0.13333333333333333 out of 1.0)
        else  # if Comments_after > 79.5
           return 0.45 # (0.45 out of 1.0)
        end       else  # if mostly_delete > 0.5
         return 0.7222222222222222 # (0.7222222222222222 out of 1.0)
      end     end   end )