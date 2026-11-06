Sprawdza każdy harmonogram, a potem go mierzy. Kontrola wykrywa niezgodność między GPU a niezależnym dekoderem, zanim wynik trafi do raportu. Pomiary dotyczą spóźnień, końca pracy i wykorzystania maszyn. Wejścia pochodzą z `ProblemEncoder`, `EvolutionEngine` i `ScheduleDecoder`; wyjście trafia do `AnalysisFileWriter` i `FactoryDashboard`.

## problem
Wejście: `FactoryProblem`.

## result
Wejście: `EvolutionResult`, którego `best_cost` musi równać się kosztowi z dekodera; inaczej `RuntimeError`.

## schedules
Wejście z `ScheduleDecoder`, przechowywane jako `all_schedules`.

## all_schedules
Atrybut: słownik nazwa → operacje. Kontrola sprawdza liczbę operacji, brak nakładania się prac na maszynie, kolejność kroków i napływ; naruszenie daje `RuntimeError`.

## evolution_name
Nazwa wyniku ewolucji, `str`, domyślnie `"Algorytm ewolucyjny"`. Musi być kluczem w `schedules`, inaczej `KeyError`.

## report
Zwraca słownik: `evolution_name`, `names`, `comparison` (porównanie harmonogramów), oraz dla każdej nazwy `outcomes` (wynik zleceń), `operations` (operacje na maszynach) i `utilization` (wykorzystanie typów maszyn względem czasu zakończenia).
