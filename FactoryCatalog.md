Przykładowe stałe dane fabryki: park maszyn i przepis każdego z ośmiu produktów. Wydzielony jako jedyne miejsce definicji fabryki; jego wyjścia zasilają `OrderStreamGenerator`, `ProblemEncoder` i `AnalysisFileWriter`.

## MACHINES
Stała klasy: pary (typ, liczba sztuk): A 3, B 4, C 2, D 1, E 5, F 8, razem 23 maszyny. Dopuszczalne najwyżej 64 sztuki łącznie. Zmiana liczby sztuk przesuwa wąskie gardło i zmienia napływ zleceń wyliczany przez generator.

## RECIPES
Stała klasy: produkt i uporządkowane pary (maszyna, minuty). Przepisy mają od 8 do 16 kroków (średnio 11,5) i po 87–115 minut pracy. Trasy wielokrotnie wracają na te same typy maszyn, a czasy dobrano tak, by obciążenie na sztukę było podobne we wszystkich typach (3,9–4,4 min na zlecenie), bez jednego wąskiego gardła. To celowe: przy jednym wąskim gardle i krótkich przepisach zwykłe reguły kolejkowania wystarczały do zera spóźnień. Przepis X zaczyna się od kroków z zadania (A 30, B 10, A 4, D 8) i ma sześć dodanych kroków; pozostałe przepisy są przykładowe. Każdy produkt musi mieć co najmniej jeden krok, a kroki muszą wskazywać istniejące maszyny (inaczej `KeyError`). Dłuższe przepisy wydłużają chromosom, czyli powiększają przestrzeń poszukiwań i czas pokolenia, a przy tym samym obciążeniu zmniejszają liczbę zleceń.

## machines
Zwraca `list[MachineGroup]`. Wyjście trafia do `OrderStreamGenerator`, `ProblemEncoder` i `AnalysisFileWriter`.

## recipes
Zwraca `list[Recipe]`. Wyjście trafia do tych samych trzech bloków.
