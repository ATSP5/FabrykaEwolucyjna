Przykładowe stałe dane fabryki: park maszyn i przepis każdego z ośmiu produktów. Wydzielony jako jedyne miejsce definicji fabryki; jego wyjścia zasilają `OrderStreamGenerator`, `ProblemEncoder` i `AnalysisFileWriter`.

## MACHINES
Stała klasy: pary (typ, liczba sztuk): A 3, B 4, C 2, D 1, E 5, F 8, razem 23 maszyny. Dopuszczalne najwyżej 64 sztuki łącznie. Zmiana liczby sztuk przesuwa wąskie gardło i zmienia napływ zleceń wyliczany przez generator.

## RECIPES
Stała klasy: produkt i uporządkowane pary (maszyna, minuty). Przepis X to A 30, B 10, A 4, D 8, jak w zadaniu; pozostałe (Y, Z, V, W, Q, R, S) są przykładowe. Każdy produkt musi mieć co najmniej jeden krok, a kroki muszą wskazywać istniejące maszyny (inaczej `KeyError`). Przy tych danych wąskim gardłem jest typ C. Dłuższe przepisy zmniejszają liczbę zleceń przy tym samym obciążeniu.

## machines
Zwraca `list[MachineGroup]`. Wyjście trafia do `OrderStreamGenerator`, `ProblemEncoder` i `AnalysisFileWriter`.

## recipes
Zwraca `list[Recipe]`. Wyjście trafia do tych samych trzech bloków.
