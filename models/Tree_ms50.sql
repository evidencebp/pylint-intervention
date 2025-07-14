create or replace function Tree_ms50 (simplifiable-if-expression int64, too-many-branches int64, too-many-statements int64, superfluous-parens int64, too-many-return-statements int64, too-many-nested-blocks int64, too-many-boolean-expressions int64, simplifiable-condition int64, Simplify-boolean-expression int64, comparison-of-constants int64, unnecessary-semicolon int64, using-constant-test int64, simplifiable-if-statement int64, try-except-raise int64, broad-exception-caught int64, wildcard-import int64, unnecessary-pass int64, pointless-statement int64, too-many-lines int64, line-too-long int64, is_refactor int64, McCabe_sum_reduced int64, McCabe_max_reduced int64, only_removal int64, mostly_delete int64, massive_change int64, high_ccp_group int64) as (
  case when high_ccp_group <= 0.5 then
    case when superfluous-parens <= 0.5 then
      case when line-too-long <= 0.5 then
        case when mostly_delete <= 0.5 then
          case when massive_change <= 0.5 then
            case when is_refactor <= 0.5 then
              case when McCabe_max_reduced <= 0.5 then
                case when too-many-branches <= 0.5 then
                  case when broad-exception-caught <= 0.5 then
                    case when too-many-return-statements <= 0.5 then
                      case when McCabe_sum_reduced <= 0.5 then
                        case when only_removal <= 0.5 then
                          case when too-many-statements <= 0.5 then
                            case when too-many-lines <= 0.5 then
                               return 0.16666666666666666 # (9.0 out of 54.0)
                            else  # if too-many-lines > 0.5
                               return 0.18181818181818182 # (4.0 out of 22.0)
                            end                           else  # if too-many-statements > 0.5
                             return 0.09090909090909091 # (3.0 out of 33.0)
                          end                         else  # if only_removal > 0.5
                           return 0.21739130434782608 # (5.0 out of 23.0)
                        end                       else  # if McCabe_sum_reduced > 0.5
                        case when too-many-lines <= 0.5 then
                           return 0.0847457627118644 # (5.0 out of 59.0)
                        else  # if too-many-lines > 0.5
                           return 0.1206896551724138 # (7.0 out of 58.0)
                        end                       end                     else  # if too-many-return-statements > 0.5
                       return 0.03571428571428571 # (1.0 out of 28.0)
                    end                   else  # if broad-exception-caught > 0.5
                     return 0.025 # (1.0 out of 40.0)
                  end                 else  # if too-many-branches > 0.5
                   return 0.2857142857142857 # (6.0 out of 21.0)
                end               else  # if McCabe_max_reduced > 0.5
                case when too-many-statements <= 0.5 then
                  case when too-many-branches <= 0.5 then
                     return 0.06557377049180328 # (4.0 out of 61.0)
                  else  # if too-many-branches > 0.5
                     return 0.058823529411764705 # (3.0 out of 51.0)
                  end                 else  # if too-many-statements > 0.5
                   return 0.09302325581395349 # (4.0 out of 43.0)
                end               end             else  # if is_refactor > 0.5
              case when McCabe_sum_reduced <= 0.5 then
                case when McCabe_max_reduced <= 0.5 then
                   return 0.18181818181818182 # (4.0 out of 22.0)
                else  # if McCabe_max_reduced > 0.5
                   return 0.023255813953488372 # (1.0 out of 43.0)
                end               else  # if McCabe_sum_reduced > 0.5
                case when too-many-branches <= 0.5 then
                   return 0.34782608695652173 # (8.0 out of 23.0)
                else  # if too-many-branches > 0.5
                   return 0.5714285714285714 # (8.0 out of 14.0)
                end               end             end           else  # if massive_change > 0.5
            case when McCabe_max_reduced <= 0.5 then
              case when too-many-lines <= 0.5 then
                 return 0.11764705882352941 # (4.0 out of 34.0)
              else  # if too-many-lines > 0.5
                 return 0.125 # (3.0 out of 24.0)
              end             else  # if McCabe_max_reduced > 0.5
              case when is_refactor <= 0.5 then
                 return 0.45454545454545453 # (15.0 out of 33.0)
              else  # if is_refactor > 0.5
                 return 0.12903225806451613 # (4.0 out of 31.0)
              end             end           end         else  # if mostly_delete > 0.5
          case when too-many-statements <= 0.5 then
             return 0.22580645161290322 # (7.0 out of 31.0)
          else  # if too-many-statements > 0.5
             return 0.3684210526315789 # (7.0 out of 19.0)
          end         end       else  # if line-too-long > 0.5
        case when McCabe_sum_reduced <= 0.5 then
           return 0.2682926829268293 # (22.0 out of 82.0)
        else  # if McCabe_sum_reduced > 0.5
           return 0.16 # (4.0 out of 25.0)
        end       end     else  # if superfluous-parens > 0.5
      case when McCabe_sum_reduced <= 0.5 then
        case when mostly_delete <= 0.5 then
           return 0.1935483870967742 # (18.0 out of 93.0)
        else  # if mostly_delete > 0.5
           return 0.3684210526315789 # (7.0 out of 19.0)
        end       else  # if McCabe_sum_reduced > 0.5
        case when massive_change <= 0.5 then
           return 0.25 # (7.0 out of 28.0)
        else  # if massive_change > 0.5
           return 0.8 # (12.0 out of 15.0)
        end       end     end   else  # if high_ccp_group > 0.5
    case when massive_change <= 0.5 then
      case when is_refactor <= 0.5 then
        case when too-many-statements <= 0.5 then
          case when only_removal <= 0.5 then
            case when superfluous-parens <= 0.5 then
              case when McCabe_sum_reduced <= 0.5 then
                 return 0.375 # (18.0 out of 48.0)
              else  # if McCabe_sum_reduced > 0.5
                case when McCabe_max_reduced <= 0.5 then
                   return 0.55 # (11.0 out of 20.0)
                else  # if McCabe_max_reduced > 0.5
                   return 0.42857142857142855 # (9.0 out of 21.0)
                end               end             else  # if superfluous-parens > 0.5
               return 0.6470588235294118 # (11.0 out of 17.0)
            end           else  # if only_removal > 0.5
             return 0.7692307692307693 # (10.0 out of 13.0)
          end         else  # if too-many-statements > 0.5
           return 0.2894736842105263 # (11.0 out of 38.0)
        end       else  # if is_refactor > 0.5
         return 0.7857142857142857 # (11.0 out of 14.0)
      end     else  # if massive_change > 0.5
      case when McCabe_max_reduced <= 0.5 then
         return 0.08333333333333333 # (3.0 out of 36.0)
      else  # if McCabe_max_reduced > 0.5
         return 0.3333333333333333 # (6.0 out of 18.0)
      end     end   end )