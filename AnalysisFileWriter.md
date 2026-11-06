Przedstawia dane analizy jako tabele i zapisuje je do CSV, razem z najlepszym harmonogramem. Dzięki temu dane wejściowe i wynik można otworzyć poza CatNip. Wejścia pochodzą z `FactoryCatalog`, `OrderStreamGenerator` i `ScheduleAnalysis`, a oba wyjścia trafiają do `FactoryDashboard`.

## machines
Wejście: `list[MachineGroup]`.

## recipes
Wejście: `list[Recipe]`.

## orders
Wejście: `list[ProductionOrder]`.

## report
Wejście: słownik z `ScheduleAnalysis.report`.

## folder
Folder zapisu, `str`, domyślnie podfolder `data` obok modułu. Tworzony, gdy go brak; brak uprawnień kończy się `OSError`. Nie wpływa na obliczenia.

## input_tables
Zwraca słownik `DataFrame`: `machines`, `recipes`, `orders`.

## written_paths
Zapisuje `machines.csv`, `recipes.csv`, `orders.csv`, `best_schedule.csv` i `order_outcomes.csv` (UTF-8 z BOM), nadpisując poprzednie wersje, i zwraca listę ścieżek.
