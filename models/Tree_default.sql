create or replace function Tree_default (too-many-branches int64, too-many-statements int64, too-many-return-statements int64, too-many-nested-blocks int64, is_refactor int64, McCabe_sum_reduced int64, McCabe_max_reduced int64, only_removal int64, mostly_delete int64, massive_change int64, high_ccp_group int64) as (
  case when high_ccp_group <= 0.5 then
    case when mostly_delete <= 0.5 then
      case when massive_change <= 0.5 then
        case when is_refactor <= 0.5 then
          case when McCabe_max_reduced <= 0.5 then
            case when McCabe_sum_reduced <= 0.5 then
              case when too-many-statements <= 0.5 then
                case when too-many-nested-blocks <= 0.5 then
                   return 0.0 # (0.0 out of 15.0)
                else  # if too-many-nested-blocks > 0.5
                  case when only_removal <= 0.5 then
                     return 0.0 # (0.0 out of 3.0)
                  else  # if only_removal > 0.5
                     return 0.1 # (1.0 out of 10.0)
                  end                 end               else  # if too-many-statements > 0.5
                case when only_removal <= 0.5 then
                   return 0.07692307692307693 # (3.0 out of 39.0)
                else  # if only_removal > 0.5
                   return 1.0 # (1.0 out of 1.0)
                end               end             else  # if McCabe_sum_reduced > 0.5
              case when too-many-branches <= 0.5 then
                case when too-many-return-statements <= 0.5 then
                  case when too-many-nested-blocks <= 0.5 then
                     return 0.11764705882352941 # (2.0 out of 17.0)
                  else  # if too-many-nested-blocks > 0.5
                     return 0.1 # (1.0 out of 10.0)
                  end                 else  # if too-many-return-statements > 0.5
                   return 0.14285714285714285 # (2.0 out of 14.0)
                end               else  # if too-many-branches > 0.5
                 return 0.25 # (1.0 out of 4.0)
              end             end           else  # if McCabe_max_reduced > 0.5
            case when too-many-nested-blocks <= 0.5 then
              case when too-many-statements <= 0.5 then
                case when McCabe_sum_reduced <= 0.5 then
                   return 0.0 # (0.0 out of 6.0)
                else  # if McCabe_sum_reduced > 0.5
                  case when too-many-branches <= 0.5 then
                     return 0.1 # (1.0 out of 10.0)
                  else  # if too-many-branches > 0.5
                     return 0.1 # (4.0 out of 40.0)
                  end                 end               else  # if too-many-statements > 0.5
                 return 0.04 # (1.0 out of 25.0)
              end             else  # if too-many-nested-blocks > 0.5
               return 0.0 # (0.0 out of 12.0)
            end           end         else  # if is_refactor > 0.5
          case when McCabe_sum_reduced <= 0.5 then
            case when too-many-nested-blocks <= 0.5 then
              case when too-many-return-statements <= 0.5 then
                case when too-many-branches <= 0.5 then
                  case when McCabe_max_reduced <= 0.5 then
                     return 0.1 # (2.0 out of 20.0)
                  else  # if McCabe_max_reduced > 0.5
                     return 0.0625 # (1.0 out of 16.0)
                  end                 else  # if too-many-branches > 0.5
                   return 0.1 # (2.0 out of 20.0)
                end               else  # if too-many-return-statements > 0.5
                 return 0.14285714285714285 # (1.0 out of 7.0)
              end             else  # if too-many-nested-blocks > 0.5
               return 0.0 # (0.0 out of 6.0)
            end           else  # if McCabe_sum_reduced > 0.5
            case when too-many-nested-blocks <= 0.5 then
              case when too-many-branches <= 0.5 then
                case when McCabe_max_reduced <= 0.5 then
                   return 0.4 # (2.0 out of 5.0)
                else  # if McCabe_max_reduced > 0.5
                  case when too-many-statements <= 0.5 then
                     return 0.0 # (0.0 out of 3.0)
                  else  # if too-many-statements > 0.5
                     return 0.2 # (3.0 out of 15.0)
                  end                 end               else  # if too-many-branches > 0.5
                case when McCabe_max_reduced <= 0.5 then
                   return 0.0 # (0.0 out of 3.0)
                else  # if McCabe_max_reduced > 0.5
                   return 0.5 # (6.0 out of 12.0)
                end               end             else  # if too-many-nested-blocks > 0.5
               return 1.0 # (2.0 out of 2.0)
            end           end         end       else  # if massive_change > 0.5
        case when is_refactor <= 0.5 then
          case when McCabe_max_reduced <= 0.5 then
             return 0.0 # (0.0 out of 9.0)
          else  # if McCabe_max_reduced > 0.5
            case when too-many-statements <= 0.5 then
               return 1.0 # (3.0 out of 3.0)
            else  # if too-many-statements > 0.5
               return 0.75 # (9.0 out of 12.0)
            end           end         else  # if is_refactor > 0.5
          case when too-many-nested-blocks <= 0.5 then
            case when McCabe_sum_reduced <= 0.5 then
               return 0.0 # (0.0 out of 9.0)
            else  # if McCabe_sum_reduced > 0.5
              case when too-many-statements <= 0.5 then
                 return 0.0 # (0.0 out of 6.0)
              else  # if too-many-statements > 0.5
                 return 0.18181818181818182 # (2.0 out of 11.0)
              end             end           else  # if too-many-nested-blocks > 0.5
             return 1.0 # (2.0 out of 2.0)
          end         end       end     else  # if mostly_delete > 0.5
      case when is_refactor <= 0.5 then
         return 0.14285714285714285 # (1.0 out of 7.0)
      else  # if is_refactor > 0.5
        case when massive_change <= 0.5 then
           return 1.0 # (7.0 out of 7.0)
        else  # if massive_change > 0.5
           return 0.25 # (1.0 out of 4.0)
        end       end     end   else  # if high_ccp_group > 0.5
    case when too-many-return-statements <= 0.5 then
      case when McCabe_sum_reduced <= 0.5 then
        case when is_refactor <= 0.5 then
          case when only_removal <= 0.5 then
             return 0.0 # (0.0 out of 12.0)
          else  # if only_removal > 0.5
            case when too-many-branches <= 0.5 then
               return 0.25 # (3.0 out of 12.0)
            else  # if too-many-branches > 0.5
               return 1.0 # (2.0 out of 2.0)
            end           end         else  # if is_refactor > 0.5
          case when too-many-statements <= 0.5 then
             return 1.0 # (4.0 out of 4.0)
          else  # if too-many-statements > 0.5
            case when massive_change <= 0.5 then
              case when McCabe_max_reduced <= 0.5 then
                 return 0.25 # (2.0 out of 8.0)
              else  # if McCabe_max_reduced > 0.5
                 return 1.0 # (4.0 out of 4.0)
              end             else  # if massive_change > 0.5
               return 0.0 # (0.0 out of 3.0)
            end           end         end       else  # if McCabe_sum_reduced > 0.5
        case when McCabe_max_reduced <= 0.5 then
           return 1.0 # (4.0 out of 4.0)
        else  # if McCabe_max_reduced > 0.5
          case when is_refactor <= 0.5 then
            case when massive_change <= 0.5 then
              case when too-many-branches <= 0.5 then
                 return 0.5714285714285714 # (8.0 out of 14.0)
              else  # if too-many-branches > 0.5
                 return 0.5 # (3.0 out of 6.0)
              end             else  # if massive_change > 0.5
               return 1.0 # (3.0 out of 3.0)
            end           else  # if is_refactor > 0.5
            case when too-many-statements <= 0.5 then
               return 1.0 # (1.0 out of 1.0)
            else  # if too-many-statements > 0.5
               return 0.14285714285714285 # (1.0 out of 7.0)
            end           end         end       end     else  # if too-many-return-statements > 0.5
      case when McCabe_sum_reduced <= 0.5 then
         return 0.0 # (0.0 out of 18.0)
      else  # if McCabe_sum_reduced > 0.5
        case when McCabe_max_reduced <= 0.5 then
           return 1.0 # (2.0 out of 2.0)
        else  # if McCabe_max_reduced > 0.5
           return 0.0 # (0.0 out of 6.0)
        end       end     end   end )