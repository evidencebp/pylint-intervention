create or replace function RandomForest_6 (LOC_diff int64, Comments_after int64, volume_diff int64, LOC_before int64, McCabe_max_diff int64, Blank_diff int64, unnecessary-pass int64, McCabe_max_before int64, prev_count_x int64, prev_count_y int64, N2_diff int64, LLOC_before int64, prev_count int64, too-many-branches int64, added_functions int64, length_diff int64, h2_diff int64, removed_lines int64, too-many-nested-blocks int64, comparison-of-constants int64, bugs_diff int64, N1_diff int64, Comments_diff int64, line-too-long int64, McCabe_sum_diff int64, superfluous-parens int64, Multi_diff int64, changed_lines int64, McCabe_sum_before int64, calculated_length_diff int64, Single comments_after int64, time_diff int64, Single comments_diff int64, Comments_before int64, added_lines int64, effort_diff int64, refactor_mle_diff int64, Blank_before int64, too-many-return-statements int64, pointless-statement int64, too-many-statements int64, cur_count_y int64, unnecessary-semicolon int64, cur_count_x int64, using-constant-test int64, McCabe_sum_after int64, McCabe_max_after int64, too-many-lines int64, LLOC_diff int64, difficulty_diff int64, simplifiable-if-statement int64, vocabulary_diff int64, SLOC_before int64, modified_McCabe_max_diff int64, wildcard-import int64, one_file_fix_rate_diff int64, simplifiable-condition int64, SLOC_diff int64, h1_diff int64, same_day_duration_avg_diff int64, Single comments_before int64, cur_count int64, try-except-raise int64, Simplify-boolean-expression int64, simplifiable-if-expression int64, broad-exception-caught int64, hunks_num int64, too-many-boolean-expressions int64, avg_coupling_code_size_cut_diff int64) as (
  case when same_day_duration_avg_diff <= 15.797003269195557 then
    case when vocabulary_diff <= 1.5 then
      case when Comments_after <= 82.0 then
        case when McCabe_max_after <= 45.0 then
          case when too-many-return-statements <= 0.5 then
            case when refactor_mle_diff <= -0.29726889729499817 then
              case when too-many-statements <= 0.5 then
                case when hunks_num <= 0.5 then
                  case when line-too-long <= 0.5 then
                    case when same_day_duration_avg_diff <= -53.02083396911621 then
                       return 0.28 # (7.0 out of 25.0)
                    else  # if same_day_duration_avg_diff > -53.02083396911621
                       return 0.6363636363636364 # (14.0 out of 22.0)
                    end                   else  # if line-too-long > 0.5
                     return 0.5769230769230769 # (15.0 out of 26.0)
                  end                 else  # if hunks_num > 0.5
                   return 0.3157894736842105 # (6.0 out of 19.0)
                end               else  # if too-many-statements > 0.5
                 return 0.19047619047619047 # (4.0 out of 21.0)
              end             else  # if refactor_mle_diff > -0.29726889729499817
              case when LLOC_before <= 226.0 then
                case when same_day_duration_avg_diff <= -37.46688461303711 then
                  case when line-too-long <= 0.5 then
                    case when refactor_mle_diff <= -0.03147832956165075 then
                      case when cur_count_x <= 1.5 then
                        case when prev_count_x <= 0.5 then
                           return 0.5396825396825397 # (34.0 out of 63.0)
                        else  # if prev_count_x > 0.5
                           return 0.6296296296296297 # (17.0 out of 27.0)
                        end                       else  # if cur_count_x > 1.5
                         return 0.4583333333333333 # (11.0 out of 24.0)
                      end                     else  # if refactor_mle_diff > -0.03147832956165075
                      case when too-many-branches <= 0.5 then
                         return 0.3577981651376147 # (39.0 out of 109.0)
                      else  # if too-many-branches > 0.5
                         return 0.65 # (13.0 out of 20.0)
                      end                     end                   else  # if line-too-long > 0.5
                    case when one_file_fix_rate_diff <= 0.01785714365541935 then
                       return 0.42592592592592593 # (23.0 out of 54.0)
                    else  # if one_file_fix_rate_diff > 0.01785714365541935
                       return 0.21052631578947367 # (4.0 out of 19.0)
                    end                   end                 else  # if same_day_duration_avg_diff > -37.46688461303711
                  case when cur_count_x <= 3.5 then
                    case when Comments_before <= 12.0 then
                       return 0.6418918918918919 # (190.0 out of 296.0)
                    else  # if Comments_before > 12.0
                       return 0.13333333333333333 # (2.0 out of 15.0)
                    end                   else  # if cur_count_x > 3.5
                     return 0.4423076923076923 # (23.0 out of 52.0)
                  end                 end               else  # if LLOC_before > 226.0
                case when LOC_before <= 750.5 then
                  case when h2_diff <= -0.5 then
                     return 0.7368421052631579 # (14.0 out of 19.0)
                  else  # if h2_diff > -0.5
                     return 0.9444444444444444 # (17.0 out of 18.0)
                  end                 else  # if LOC_before > 750.5
                  case when Single comments_before <= 77.0 then
                    case when SLOC_diff <= -19.0 then
                       return 0.7727272727272727 # (17.0 out of 22.0)
                    else  # if SLOC_diff > -19.0
                       return 0.35 # (7.0 out of 20.0)
                    end                   else  # if Single comments_before > 77.0
                     return 0.75 # (15.0 out of 20.0)
                  end                 end               end             end           else  # if too-many-return-statements > 0.5
            case when same_day_duration_avg_diff <= -33.11794853210449 then
               return 0.13333333333333333 # (2.0 out of 15.0)
            else  # if same_day_duration_avg_diff > -33.11794853210449
               return 0.4666666666666667 # (7.0 out of 15.0)
            end           end         else  # if McCabe_max_after > 45.0
           return 0.15 # (3.0 out of 20.0)
        end       else  # if Comments_after > 82.0
        case when McCabe_max_diff <= -3.0 then
           return 0.6666666666666666 # (14.0 out of 21.0)
        else  # if McCabe_max_diff > -3.0
          case when McCabe_sum_before <= 222.0 then
            case when one_file_fix_rate_diff <= 0.02380952425301075 then
              case when LLOC_before <= 499.0 then
                 return 0.25 # (4.0 out of 16.0)
              else  # if LLOC_before > 499.0
                 return 0.0 # (0.0 out of 19.0)
              end             else  # if one_file_fix_rate_diff > 0.02380952425301075
               return 0.0 # (0.0 out of 23.0)
            end           else  # if McCabe_sum_before > 222.0
             return 0.4838709677419355 # (15.0 out of 31.0)
          end         end       end     else  # if vocabulary_diff > 1.5
      case when length_diff <= 19.5 then
        case when SLOC_diff <= 36.0 then
          case when SLOC_diff <= 7.5 then
             return 0.84 # (21.0 out of 25.0)
          else  # if SLOC_diff > 7.5
             return 0.5263157894736842 # (10.0 out of 19.0)
          end         else  # if SLOC_diff > 36.0
           return 1.0 # (26.0 out of 26.0)
        end       else  # if length_diff > 19.5
         return 0.4375 # (7.0 out of 16.0)
      end     end   else  # if same_day_duration_avg_diff > 15.797003269195557
    case when changed_lines <= 184.0 then
      case when added_lines <= 55.0 then
        case when McCabe_sum_after <= 361.5 then
          case when cur_count_x <= 0.5 then
            case when McCabe_max_before <= 13.5 then
              case when added_lines <= 7.5 then
                case when LLOC_before <= 3.0 then
                  case when same_day_duration_avg_diff <= 73.66666793823242 then
                     return 0.55 # (11.0 out of 20.0)
                  else  # if same_day_duration_avg_diff > 73.66666793823242
                     return 0.4 # (8.0 out of 20.0)
                  end                 else  # if LLOC_before > 3.0
                   return 0.75 # (21.0 out of 28.0)
                end               else  # if added_lines > 7.5
                 return 0.8 # (12.0 out of 15.0)
              end             else  # if McCabe_max_before > 13.5
              case when Comments_before <= 48.0 then
                 return 0.47368421052631576 # (9.0 out of 19.0)
              else  # if Comments_before > 48.0
                case when McCabe_max_after <= 26.5 then
                   return 0.0 # (0.0 out of 15.0)
                else  # if McCabe_max_after > 26.5
                   return 0.3125 # (5.0 out of 16.0)
                end               end             end           else  # if cur_count_x > 0.5
            case when unnecessary-pass <= 0.5 then
               return 0.33147632311977715 # (119.0 out of 359.0)
            else  # if unnecessary-pass > 0.5
              case when cur_count_x <= 35.0 then
                 return 0.5 # (11.0 out of 22.0)
              else  # if cur_count_x > 35.0
                 return 0.25 # (5.0 out of 20.0)
              end             end           end         else  # if McCabe_sum_after > 361.5
           return 0.5925925925925926 # (16.0 out of 27.0)
        end       else  # if added_lines > 55.0
        case when McCabe_max_before <= 24.0 then
           return 0.0 # (0.0 out of 20.0)
        else  # if McCabe_max_before > 24.0
           return 0.15384615384615385 # (2.0 out of 13.0)
        end       end     else  # if changed_lines > 184.0
      case when hunks_num <= 12.5 then
        case when h1_diff <= -0.5 then
          case when refactor_mle_diff <= -0.2756720781326294 then
             return 0.9523809523809523 # (20.0 out of 21.0)
          else  # if refactor_mle_diff > -0.2756720781326294
             return 1.0 # (21.0 out of 21.0)
          end         else  # if h1_diff > -0.5
           return 0.23076923076923078 # (3.0 out of 13.0)
        end       else  # if hunks_num > 12.5
        case when SLOC_diff <= -54.5 then
           return 0.0 # (0.0 out of 19.0)
        else  # if SLOC_diff > -54.5
           return 0.4 # (6.0 out of 15.0)
        end       end     end   end )