create or replace function Tree_default (simplifiable-if-expression int64, too-many-branches int64, too-many-statements int64, superfluous-parens int64, too-many-return-statements int64, too-many-nested-blocks int64, too-many-boolean-expressions int64, simplifiable-condition int64, Simplify-boolean-expression int64, comparison-of-constants int64, unnecessary-semicolon int64, using-constant-test int64, simplifiable-if-statement int64, try-except-raise int64, broad-exception-caught int64, wildcard-import int64, unnecessary-pass int64, pointless-statement int64, too-many-lines int64, line-too-long int64, is_refactor int64, McCabe_sum_reduced int64, McCabe_max_reduced int64, only_removal int64, mostly_delete int64, massive_change int64, high_ccp_group int64) as (
  case when high_ccp_group <= 0.5 then
    case when superfluous-parens <= 0.5 then
      case when line-too-long <= 0.5 then
        case when mostly_delete <= 0.5 then
          case when massive_change <= 0.5 then
            case when too-many-boolean-expressions <= 0.5 then
              case when is_refactor <= 0.5 then
                case when pointless-statement <= 0.5 then
                  case when too-many-lines <= 0.5 then
                    case when too-many-branches <= 0.5 then
                      case when unnecessary-semicolon <= 0.5 then
                        case when only_removal <= 0.5 then
                          case when unnecessary-pass <= 0.5 then
                            case when too-many-statements <= 0.5 then
                              case when McCabe_sum_reduced <= 0.5 then
                                case when using-constant-test <= 0.5 then
                                   return 0.0 # (0.0 out of 60.0)
                                else  # if using-constant-test > 0.5
                                   return 0.25 # (1.0 out of 4.0)
                                end                               else  # if McCabe_sum_reduced > 0.5
                                case when simplifiable-if-statement <= 0.5 then
                                  case when try-except-raise <= 0.5 then
                                    case when using-constant-test <= 0.5 then
                                      case when simplifiable-if-expression <= 0.5 then
                                        case when wildcard-import <= 0.5 then
                                          case when too-many-return-statements <= 0.5 then
                                            case when McCabe_max_reduced <= 0.5 then
                                              case when too-many-nested-blocks <= 0.5 then
                                                 return 0.04 # (1.0 out of 25.0)
                                              else  # if too-many-nested-blocks > 0.5
                                                 return 0.14285714285714285 # (1.0 out of 7.0)
                                              end                                             else  # if McCabe_max_reduced > 0.5
                                              case when broad-exception-caught <= 0.5 then
                                                 return 0.0 # (0.0 out of 9.0)
                                              else  # if broad-exception-caught > 0.5
                                                 return 0.1 # (1.0 out of 10.0)
                                              end                                             end                                           else  # if too-many-return-statements > 0.5
                                            case when McCabe_max_reduced <= 0.5 then
                                               return 0.0625 # (1.0 out of 16.0)
                                            else  # if McCabe_max_reduced > 0.5
                                               return 0.07692307692307693 # (1.0 out of 13.0)
                                            end                                           end                                         else  # if wildcard-import > 0.5
                                           return 0.0 # (0.0 out of 3.0)
                                        end                                       else  # if simplifiable-if-expression > 0.5
                                         return 0.0 # (0.0 out of 9.0)
                                      end                                     else  # if using-constant-test > 0.5
                                       return 0.0 # (0.0 out of 9.0)
                                    end                                   else  # if try-except-raise > 0.5
                                     return 0.25 # (1.0 out of 4.0)
                                  end                                 else  # if simplifiable-if-statement > 0.5
                                   return 1.0 # (1.0 out of 1.0)
                                end                               end                             else  # if too-many-statements > 0.5
                              case when McCabe_max_reduced <= 0.5 then
                                case when McCabe_sum_reduced <= 0.5 then
                                   return 0.09090909090909091 # (3.0 out of 33.0)
                                else  # if McCabe_sum_reduced > 0.5
                                   return 0.0 # (0.0 out of 9.0)
                                end                               else  # if McCabe_max_reduced > 0.5
                                 return 0.09302325581395349 # (4.0 out of 43.0)
                              end                             end                           else  # if unnecessary-pass > 0.5
                            case when McCabe_sum_reduced <= 0.5 then
                               return 0.3333333333333333 # (3.0 out of 9.0)
                            else  # if McCabe_sum_reduced > 0.5
                               return 0.0 # (0.0 out of 15.0)
                            end                           end                         else  # if only_removal > 0.5
                          case when too-many-statements <= 0.5 then
                            case when too-many-nested-blocks <= 0.5 then
                               return 0.0 # (0.0 out of 9.0)
                            else  # if too-many-nested-blocks > 0.5
                               return 0.14285714285714285 # (1.0 out of 7.0)
                            end                           else  # if too-many-statements > 0.5
                             return 0.4 # (2.0 out of 5.0)
                          end                         end                       else  # if unnecessary-semicolon > 0.5
                        case when only_removal <= 0.5 then
                          case when McCabe_sum_reduced <= 0.5 then
                             return 0.4 # (2.0 out of 5.0)
                          else  # if McCabe_sum_reduced > 0.5
                             return 0.0 # (0.0 out of 3.0)
                          end                         else  # if only_removal > 0.5
                           return 0.0 # (0.0 out of 3.0)
                        end                       end                     else  # if too-many-branches > 0.5
                      case when McCabe_max_reduced <= 0.5 then
                        case when only_removal <= 0.5 then
                          case when McCabe_sum_reduced <= 0.5 then
                             return 1.0 # (2.0 out of 2.0)
                          else  # if McCabe_sum_reduced > 0.5
                             return 0.5 # (3.0 out of 6.0)
                          end                         else  # if only_removal > 0.5
                           return 0.07692307692307693 # (1.0 out of 13.0)
                        end                       else  # if McCabe_max_reduced > 0.5
                        case when McCabe_sum_reduced <= 0.5 then
                           return 0.0 # (0.0 out of 3.0)
                        else  # if McCabe_sum_reduced > 0.5
                           return 0.0625 # (3.0 out of 48.0)
                        end                       end                     end                   else  # if too-many-lines > 0.5
                    case when only_removal <= 0.5 then
                      case when McCabe_sum_reduced <= 0.5 then
                         return 0.18181818181818182 # (4.0 out of 22.0)
                      else  # if McCabe_sum_reduced > 0.5
                        case when McCabe_max_reduced <= 0.5 then
                           return 0.1206896551724138 # (7.0 out of 58.0)
                        else  # if McCabe_max_reduced > 0.5
                           return 0.07692307692307693 # (1.0 out of 13.0)
                        end                       end                     else  # if only_removal > 0.5
                       return 1.0 # (1.0 out of 1.0)
                    end                   end                 else  # if pointless-statement > 0.5
                  case when McCabe_sum_reduced <= 0.5 then
                     return 1.0 # (2.0 out of 2.0)
                  else  # if McCabe_sum_reduced > 0.5
                     return 0.25 # (2.0 out of 8.0)
                  end                 end               else  # if is_refactor > 0.5
                case when McCabe_sum_reduced <= 0.5 then
                  case when McCabe_max_reduced <= 0.5 then
                    case when too-many-statements <= 0.5 then
                       return 0.25 # (1.0 out of 4.0)
                    else  # if too-many-statements > 0.5
                       return 0.16666666666666666 # (3.0 out of 18.0)
                    end                   else  # if McCabe_max_reduced > 0.5
                    case when too-many-branches <= 0.5 then
                       return 0.0 # (0.0 out of 27.0)
                    else  # if too-many-branches > 0.5
                       return 0.0625 # (1.0 out of 16.0)
                    end                   end                 else  # if McCabe_sum_reduced > 0.5
                  case when too-many-nested-blocks <= 0.5 then
                    case when too-many-branches <= 0.5 then
                      case when too-many-statements <= 0.5 then
                         return 0.0 # (0.0 out of 3.0)
                      else  # if too-many-statements > 0.5
                        case when McCabe_max_reduced <= 0.5 then
                           return 0.4 # (2.0 out of 5.0)
                        else  # if McCabe_max_reduced > 0.5
                           return 0.25 # (3.0 out of 12.0)
                        end                       end                     else  # if too-many-branches > 0.5
                      case when McCabe_max_reduced <= 0.5 then
                         return 0.0 # (0.0 out of 3.0)
                      else  # if McCabe_max_reduced > 0.5
                         return 0.7272727272727273 # (8.0 out of 11.0)
                      end                     end                   else  # if too-many-nested-blocks > 0.5
                     return 1.0 # (3.0 out of 3.0)
                  end                 end               end             else  # if too-many-boolean-expressions > 0.5
              case when McCabe_sum_reduced <= 0.5 then
                 return 1.0 # (2.0 out of 2.0)
              else  # if McCabe_sum_reduced > 0.5
                 return 0.25 # (1.0 out of 4.0)
              end             end           else  # if massive_change > 0.5
            case when McCabe_max_reduced <= 0.5 then
              case when using-constant-test <= 0.5 then
                case when unnecessary-semicolon <= 0.5 then
                  case when broad-exception-caught <= 0.5 then
                    case when too-many-lines <= 0.5 then
                       return 0.0 # (0.0 out of 24.0)
                    else  # if too-many-lines > 0.5
                      case when McCabe_sum_reduced <= 0.5 then
                         return 0.25 # (1.0 out of 4.0)
                      else  # if McCabe_sum_reduced > 0.5
                         return 0.1 # (2.0 out of 20.0)
                      end                     end                   else  # if broad-exception-caught > 0.5
                    case when McCabe_sum_reduced <= 0.5 then
                       return 1.0 # (1.0 out of 1.0)
                    else  # if McCabe_sum_reduced > 0.5
                       return 0.0 # (0.0 out of 3.0)
                    end                   end                 else  # if unnecessary-semicolon > 0.5
                  case when McCabe_sum_reduced <= 0.5 then
                     return 0.25 # (1.0 out of 4.0)
                  else  # if McCabe_sum_reduced > 0.5
                     return 1.0 # (1.0 out of 1.0)
                  end                 end               else  # if using-constant-test > 0.5
                 return 1.0 # (1.0 out of 1.0)
              end             else  # if McCabe_max_reduced > 0.5
              case when is_refactor <= 0.5 then
                case when too-many-statements <= 0.5 then
                  case when too-many-lines <= 0.5 then
                    case when McCabe_sum_reduced <= 0.5 then
                       return 1.0 # (1.0 out of 1.0)
                    else  # if McCabe_sum_reduced > 0.5
                      case when too-many-branches <= 0.5 then
                        case when broad-exception-caught <= 0.5 then
                           return 0.0 # (0.0 out of 9.0)
                        else  # if broad-exception-caught > 0.5
                           return 0.25 # (1.0 out of 4.0)
                        end                       else  # if too-many-branches > 0.5
                         return 0.4 # (2.0 out of 5.0)
                      end                     end                   else  # if too-many-lines > 0.5
                     return 1.0 # (3.0 out of 3.0)
                  end                 else  # if too-many-statements > 0.5
                   return 0.7272727272727273 # (8.0 out of 11.0)
                end               else  # if is_refactor > 0.5
                case when too-many-nested-blocks <= 0.5 then
                  case when too-many-statements <= 0.5 then
                     return 0.0 # (0.0 out of 9.0)
                  else  # if too-many-statements > 0.5
                    case when McCabe_sum_reduced <= 0.5 then
                       return 0.0 # (0.0 out of 6.0)
                    else  # if McCabe_sum_reduced > 0.5
                       return 0.14285714285714285 # (2.0 out of 14.0)
                    end                   end                 else  # if too-many-nested-blocks > 0.5
                   return 1.0 # (2.0 out of 2.0)
                end               end             end           end         else  # if mostly_delete > 0.5
          case when too-many-lines <= 0.5 then
            case when is_refactor <= 0.5 then
              case when unnecessary-pass <= 0.5 then
                case when unnecessary-semicolon <= 0.5 then
                  case when only_removal <= 0.5 then
                     return 0.0 # (0.0 out of 21.0)
                  else  # if only_removal > 0.5
                     return 0.14285714285714285 # (1.0 out of 7.0)
                  end                 else  # if unnecessary-semicolon > 0.5
                   return 0.25 # (1.0 out of 4.0)
                end               else  # if unnecessary-pass > 0.5
                 return 0.4 # (2.0 out of 5.0)
              end             else  # if is_refactor > 0.5
              case when massive_change <= 0.5 then
                 return 1.0 # (5.0 out of 5.0)
              else  # if massive_change > 0.5
                 return 0.25 # (1.0 out of 4.0)
              end             end           else  # if too-many-lines > 0.5
             return 1.0 # (4.0 out of 4.0)
          end         end       else  # if line-too-long > 0.5
        case when McCabe_max_reduced <= 0.5 then
          case when mostly_delete <= 0.5 then
            case when McCabe_sum_reduced <= 0.5 then
              case when massive_change <= 0.5 then
                case when only_removal <= 0.5 then
                   return 0.32075471698113206 # (17.0 out of 53.0)
                else  # if only_removal > 0.5
                   return 0.25 # (1.0 out of 4.0)
                end               else  # if massive_change > 0.5
                 return 0.18181818181818182 # (2.0 out of 11.0)
              end             else  # if McCabe_sum_reduced > 0.5
              case when massive_change <= 0.5 then
                 return 0.14285714285714285 # (2.0 out of 14.0)
              else  # if massive_change > 0.5
                 return 1.0 # (1.0 out of 1.0)
              end             end           else  # if mostly_delete > 0.5
            case when only_removal <= 0.5 then
               return 0.1 # (1.0 out of 10.0)
            else  # if only_removal > 0.5
               return 0.25 # (1.0 out of 4.0)
            end           end         else  # if McCabe_max_reduced > 0.5
          case when massive_change <= 0.5 then
             return 0.14285714285714285 # (1.0 out of 7.0)
          else  # if massive_change > 0.5
             return 0.0 # (0.0 out of 3.0)
          end         end       end     else  # if superfluous-parens > 0.5
      case when McCabe_sum_reduced <= 0.5 then
        case when only_removal <= 0.5 then
          case when mostly_delete <= 0.5 then
            case when McCabe_max_reduced <= 0.5 then
              case when massive_change <= 0.5 then
                 return 0.1780821917808219 # (13.0 out of 73.0)
              else  # if massive_change > 0.5
                 return 0.25 # (4.0 out of 16.0)
              end             else  # if McCabe_max_reduced > 0.5
               return 0.0 # (0.0 out of 3.0)
            end           else  # if mostly_delete > 0.5
            case when massive_change <= 0.5 then
               return 0.4375 # (7.0 out of 16.0)
            else  # if massive_change > 0.5
               return 0.0 # (0.0 out of 3.0)
            end           end         else  # if only_removal > 0.5
           return 1.0 # (1.0 out of 1.0)
        end       else  # if McCabe_sum_reduced > 0.5
        case when massive_change <= 0.5 then
          case when McCabe_max_reduced <= 0.5 then
             return 0.25 # (6.0 out of 24.0)
          else  # if McCabe_max_reduced > 0.5
             return 0.25 # (1.0 out of 4.0)
          end         else  # if massive_change > 0.5
          case when McCabe_max_reduced <= 0.5 then
             return 0.625 # (5.0 out of 8.0)
          else  # if McCabe_max_reduced > 0.5
             return 1.0 # (7.0 out of 7.0)
          end         end       end     end   else  # if high_ccp_group > 0.5
    case when massive_change <= 0.5 then
      case when broad-exception-caught <= 0.5 then
        case when too-many-return-statements <= 0.5 then
          case when is_refactor <= 0.5 then
            case when too-many-statements <= 0.5 then
              case when pointless-statement <= 0.5 then
                case when only_removal <= 0.5 then
                  case when using-constant-test <= 0.5 then
                    case when superfluous-parens <= 0.5 then
                      case when simplifiable-if-expression <= 0.5 then
                        case when line-too-long <= 0.5 then
                          case when McCabe_sum_reduced <= 0.5 then
                            case when unnecessary-pass <= 0.5 then
                              case when too-many-lines <= 0.5 then
                                 return 0.0 # (0.0 out of 12.0)
                              else  # if too-many-lines > 0.5
                                case when mostly_delete <= 0.5 then
                                   return 0.14285714285714285 # (1.0 out of 7.0)
                                else  # if mostly_delete > 0.5
                                   return 0.0 # (0.0 out of 3.0)
                                end                               end                             else  # if unnecessary-pass > 0.5
                               return 1.0 # (3.0 out of 3.0)
                            end                           else  # if McCabe_sum_reduced > 0.5
                            case when wildcard-import <= 0.5 then
                              case when unnecessary-pass <= 0.5 then
                                case when simplifiable-if-statement <= 0.5 then
                                  case when too-many-branches <= 0.5 then
                                     return 1.0 # (4.0 out of 4.0)
                                  else  # if too-many-branches > 0.5
                                     return 0.5714285714285714 # (4.0 out of 7.0)
                                  end                                 else  # if simplifiable-if-statement > 0.5
                                   return 0.4 # (2.0 out of 5.0)
                                end                               else  # if unnecessary-pass > 0.5
                                case when McCabe_max_reduced <= 0.5 then
                                   return 0.0 # (0.0 out of 3.0)
                                else  # if McCabe_max_reduced > 0.5
                                   return 1.0 # (1.0 out of 1.0)
                                end                               end                             else  # if wildcard-import > 0.5
                               return 0.0 # (0.0 out of 3.0)
                            end                           end                         else  # if line-too-long > 0.5
                          case when McCabe_sum_reduced <= 0.5 then
                             return 1.0 # (6.0 out of 6.0)
                          else  # if McCabe_sum_reduced > 0.5
                            case when McCabe_max_reduced <= 0.5 then
                               return 0.25 # (1.0 out of 4.0)
                            else  # if McCabe_max_reduced > 0.5
                               return 0.0 # (0.0 out of 3.0)
                            end                           end                         end                       else  # if simplifiable-if-expression > 0.5
                         return 1.0 # (2.0 out of 2.0)
                      end                     else  # if superfluous-parens > 0.5
                      case when McCabe_sum_reduced <= 0.5 then
                        case when mostly_delete <= 0.5 then
                          case when McCabe_max_reduced <= 0.5 then
                             return 0.7 # (7.0 out of 10.0)
                          else  # if McCabe_max_reduced > 0.5
                             return 1.0 # (1.0 out of 1.0)
                          end                         else  # if mostly_delete > 0.5
                           return 1.0 # (2.0 out of 2.0)
                        end                       else  # if McCabe_sum_reduced > 0.5
                        case when McCabe_max_reduced <= 0.5 then
                           return 0.0 # (0.0 out of 3.0)
                        else  # if McCabe_max_reduced > 0.5
                           return 1.0 # (1.0 out of 1.0)
                        end                       end                     end                   else  # if using-constant-test > 0.5
                     return 1.0 # (3.0 out of 3.0)
                  end                 else  # if only_removal > 0.5
                  case when superfluous-parens <= 0.5 then
                     return 1.0 # (4.0 out of 4.0)
                  else  # if superfluous-parens > 0.5
                    case when mostly_delete <= 0.5 then
                       return 0.5714285714285714 # (4.0 out of 7.0)
                    else  # if mostly_delete > 0.5
                       return 1.0 # (1.0 out of 1.0)
                    end                   end                 end               else  # if pointless-statement > 0.5
                 return 1.0 # (4.0 out of 4.0)
              end             else  # if too-many-statements > 0.5
              case when McCabe_sum_reduced <= 0.5 then
                case when only_removal <= 0.5 then
                   return 0.1 # (1.0 out of 10.0)
                else  # if only_removal > 0.5
                   return 0.2 # (3.0 out of 15.0)
                end               else  # if McCabe_sum_reduced > 0.5
                case when McCabe_max_reduced <= 0.5 then
                   return 1.0 # (1.0 out of 1.0)
                else  # if McCabe_max_reduced > 0.5
                   return 0.5 # (6.0 out of 12.0)
                end               end             end           else  # if is_refactor > 0.5
            case when McCabe_max_reduced <= 0.5 then
              case when too-many-statements <= 0.5 then
                 return 1.0 # (2.0 out of 2.0)
              else  # if too-many-statements > 0.5
                case when McCabe_sum_reduced <= 0.5 then
                   return 0.25 # (1.0 out of 4.0)
                else  # if McCabe_sum_reduced > 0.5
                   return 1.0 # (1.0 out of 1.0)
                end               end             else  # if McCabe_max_reduced > 0.5
               return 1.0 # (6.0 out of 6.0)
            end           end         else  # if too-many-return-statements > 0.5
          case when is_refactor <= 0.5 then
             return 0.0 # (0.0 out of 12.0)
          else  # if is_refactor > 0.5
             return 1.0 # (1.0 out of 1.0)
          end         end       else  # if broad-exception-caught > 0.5
         return 1.0 # (8.0 out of 8.0)
      end     else  # if massive_change > 0.5
      case when too-many-branches <= 0.5 then
        case when line-too-long <= 0.5 then
          case when too-many-lines <= 0.5 then
            case when McCabe_max_reduced <= 0.5 then
              case when superfluous-parens <= 0.5 then
                 return 0.0 # (0.0 out of 12.0)
              else  # if superfluous-parens > 0.5
                case when McCabe_sum_reduced <= 0.5 then
                   return 0.1 # (1.0 out of 10.0)
                else  # if McCabe_sum_reduced > 0.5
                   return 0.0 # (0.0 out of 6.0)
                end               end             else  # if McCabe_max_reduced > 0.5
              case when is_refactor <= 0.5 then
                 return 0.4 # (2.0 out of 5.0)
              else  # if is_refactor > 0.5
                case when too-many-statements <= 0.5 then
                  case when McCabe_sum_reduced <= 0.5 then
                     return 1.0 # (1.0 out of 1.0)
                  else  # if McCabe_sum_reduced > 0.5
                     return 0.0 # (0.0 out of 3.0)
                  end                 else  # if too-many-statements > 0.5
                   return 0.0 # (0.0 out of 6.0)
                end               end             end           else  # if too-many-lines > 0.5
            case when McCabe_sum_reduced <= 0.5 then
               return 0.0 # (0.0 out of 6.0)
            else  # if McCabe_sum_reduced > 0.5
               return 1.0 # (2.0 out of 2.0)
            end           end         else  # if line-too-long > 0.5
           return 1.0 # (1.0 out of 1.0)
        end       else  # if too-many-branches > 0.5
         return 1.0 # (2.0 out of 2.0)
      end     end   end )