create or replace function RandomForest_3 (effort_diff int64, too-many-nested-blocks int64, Single comments_diff int64, N1_diff int64, avg_coupling_code_size_cut_diff int64, Simplify-boolean-expression int64, try-except-raise int64, h1_diff int64, added_functions int64, too-many-boolean-expressions int64, LLOC_diff int64, cur_count_x int64, wildcard-import int64, mostly_delete int64, LOC_diff int64, difficulty_diff int64, Comments_before int64, prev_count_y int64, time_diff int64, pointless-statement int64, vocabulary_diff int64, modified_McCabe_max_diff int64, prev_count int64, McCabe_sum_before int64, McCabe_max_after int64, Blank_diff int64, using-constant-test int64, McCabe_max_before int64, is_refactor int64, Comments_after int64, SLOC_before int64, superfluous-parens int64, too-many-branches int64, massive_change int64, comparison-of-constants int64, broad-exception-caught int64, Blank_before int64, N2_diff int64, McCabe_sum_after int64, too-many-statements int64, refactor_mle_diff int64, LOC_before int64, simplifiable-if-statement int64, only_removal int64, h2_diff int64, unnecessary-semicolon int64, too-many-lines int64, LLOC_before int64, volume_diff int64, too-many-return-statements int64, high_ccp_group int64, Single comments_before int64, simplifiable-if-expression int64, changed_lines int64, Multi_diff int64, one_file_fix_rate_diff int64, prev_count_x int64, simplifiable-condition int64, cur_count_y int64, calculated_length_diff int64, SLOC_diff int64, line-too-long int64, McCabe_max_diff int64, Comments_diff int64, cur_count int64, Single comments_after int64, removed_lines int64, added_lines int64, length_diff int64, unnecessary-pass int64, hunks_num int64, bugs_diff int64, same_day_duration_avg_diff int64, McCabe_sum_diff int64) as (
  case when prev_count_y <= 3.5 then
    case when SLOC_diff <= 38.0 then
      case when McCabe_max_before <= 15.5 then
        case when Single comments_diff <= 2.5 then
          case when Comments_after <= 84.5 then
            case when Single comments_before <= 60.5 then
              case when added_lines <= 36.5 then
                case when McCabe_max_before <= 7.5 then
                   return 0.6785714285714286 # (19.0 out of 28.0)
                else  # if McCabe_max_before > 7.5
                  case when SLOC_diff <= 0.5 then
                     return 0.14285714285714285 # (2.0 out of 14.0)
                  else  # if SLOC_diff > 0.5
                     return 0.5 # (9.0 out of 18.0)
                  end                 end               else  # if added_lines > 36.5
                case when changed_lines <= 175.0 then
                  case when LLOC_before <= 205.5 then
                     return 0.782608695652174 # (18.0 out of 23.0)
                  else  # if LLOC_before > 205.5
                     return 0.95 # (19.0 out of 20.0)
                  end                 else  # if changed_lines > 175.0
                   return 0.5833333333333334 # (14.0 out of 24.0)
                end               end             else  # if Single comments_before > 60.5
               return 0.8846153846153846 # (23.0 out of 26.0)
            end           else  # if Comments_after > 84.5
             return 0.19047619047619047 # (4.0 out of 21.0)
          end         else  # if Single comments_diff > 2.5
           return 0.0 # (0.0 out of 16.0)
        end       else  # if McCabe_max_before > 15.5
        case when added_lines <= 3.5 then
          case when refactor_mle_diff <= -0.13169444352388382 then
             return 0.47058823529411764 # (8.0 out of 17.0)
          else  # if refactor_mle_diff > -0.13169444352388382
             return 0.7741935483870968 # (24.0 out of 31.0)
          end         else  # if added_lines > 3.5
          case when McCabe_sum_after <= 381.0 then
            case when Blank_diff <= -1.5 then
              case when McCabe_sum_before <= 374.5 then
                case when N2_diff <= -131.5 then
                   return 0.8461538461538461 # (11.0 out of 13.0)
                else  # if N2_diff > -131.5
                  case when one_file_fix_rate_diff <= -0.3541666716337204 then
                     return 0.6153846153846154 # (8.0 out of 13.0)
                  else  # if one_file_fix_rate_diff > -0.3541666716337204
                    case when Blank_diff <= -7.0 then
                      case when N2_diff <= -44.5 then
                         return 0.10714285714285714 # (3.0 out of 28.0)
                      else  # if N2_diff > -44.5
                         return 0.391304347826087 # (9.0 out of 23.0)
                      end                     else  # if Blank_diff > -7.0
                       return 0.6296296296296297 # (17.0 out of 27.0)
                    end                   end                 end               else  # if McCabe_sum_before > 374.5
                 return 0.05263157894736842 # (1.0 out of 19.0)
              end             else  # if Blank_diff > -1.5
              case when Single comments_after <= 23.0 then
                 return 0.6 # (15.0 out of 25.0)
              else  # if Single comments_after > 23.0
                case when McCabe_max_after <= 27.5 then
                  case when SLOC_diff <= 0.5 then
                     return 0.22727272727272727 # (5.0 out of 22.0)
                  else  # if SLOC_diff > 0.5
                    case when Blank_before <= 91.5 then
                       return 0.05555555555555555 # (1.0 out of 18.0)
                    else  # if Blank_before > 91.5
                       return 0.0 # (0.0 out of 38.0)
                    end                   end                 else  # if McCabe_max_after > 27.5
                   return 0.3333333333333333 # (5.0 out of 15.0)
                end               end             end           else  # if McCabe_sum_after > 381.0
            case when refactor_mle_diff <= -0.021281367167830467 then
               return 0.8 # (16.0 out of 20.0)
            else  # if refactor_mle_diff > -0.021281367167830467
               return 0.1875 # (3.0 out of 16.0)
            end           end         end       end     else  # if SLOC_diff > 38.0
      case when Single comments_diff <= 22.5 then
        case when N1_diff <= 0.5 then
           return 0.9166666666666666 # (22.0 out of 24.0)
        else  # if N1_diff > 0.5
           return 0.43478260869565216 # (10.0 out of 23.0)
        end       else  # if Single comments_diff > 22.5
         return 1.0 # (20.0 out of 20.0)
      end     end   else  # if prev_count_y > 3.5
     return 0.05555555555555555 # (1.0 out of 18.0)
  end )