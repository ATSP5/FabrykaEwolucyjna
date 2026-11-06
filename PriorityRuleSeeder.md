Układa harmonogram czterema klasycznymi regułami i zapisuje każdy jako chromosom. Te same chromosomy są punktem odniesienia w raporcie i ziarnem populacji startowej. Zasila `PopulationInitializer` i `ScheduleDecoder`. Blok działa na CPU, bo to deterministyczna symulacja jednego przebiegu, wykonywana raz na początku.

## problem
Wejście: `FactoryProblem` z `ProblemEncoder`.

## RULES
Stała: `FIFO` (najwcześniejszy napływ), `EDD` (najwcześniejszy termin), `SPT` (najkrótsza operacja), `LST` (najmniejszy zapas czasu). Spośród operacji mogących zacząć się najwcześniej reguła wybiera tę o najlepszym priorytecie. Inna nazwa wymaga nowej gałęzi w `_priority`, inaczej liczona jest jak `LST`.

## seeds
Zwraca słownik reguła → chromosom `int32`. Wyjście trafia do `PopulationInitializer` i `ScheduleDecoder`.
