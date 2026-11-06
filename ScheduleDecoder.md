Odtwarza pełne harmonogramy z chromosomów, niezależnie od GPU. Ewolucja zwraca tylko chromosom i koszt, a do wykresu Gantta potrzebne są czasy i maszyny każdego kroku. Wejścia pochodzą z `ProblemEncoder`, `EvolutionEngine` i `PriorityRuleSeeder`; wyjście trafia do `ScheduleAnalysis`.

## problem
Wejście: `FactoryProblem`.

## result
Wejście: `EvolutionResult`, z którego dekodowany jest najlepszy chromosom.

## seeds
Wejście: chromosomy reguł, dekodowane jako punkty odniesienia.

## EVOLUTION_NAME
Stała: nazwa wyniku ewolucji w raporcie, `"Algorytm ewolucyjny"`. Musi równać się `ScheduleAnalysis.evolution_name`, inaczej powstanie `KeyError`.

## schedules
Zwraca słownik nazwa → `list[ScheduledOperation]`: najpierw ewolucja, potem reguły.
