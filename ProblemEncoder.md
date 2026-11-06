Zamienia maszyny, przepisy i zlecenia na płaskie tablice `int32` dla kerneli. To jedyne miejsce parsowania rekordów do postaci GPU. Wyjście `problem` zasila bloki Pythona, a pozostałe wyjścia to tablice wejściowe kernela `EvaluateSchedules`.

## machines
Wejście: `list[MachineGroup]`. Łącznie najwyżej 64 maszyny, inaczej `ValueError`.

## recipes
Wejście: `list[Recipe]`. Krok z nieznaną maszyną daje `KeyError`.

## orders
Wejście: `list[ProductionOrder]`, od 1 do 512 zleceń, inaczej `ValueError`. Zlecenie bez przepisu daje `KeyError`.

## tardiness_scale
Mnożnik ważonej spóźnialności w koszcie, `int`, co najmniej 1, domyślnie `100`; poniżej `ValueError`. Koszt to `tardiness_scale × Σ(waga × spóźnienie) + czas zakończenia`. Większa wartość mocniej przedkłada terminy nad wcześniejszy koniec pracy. Zbyt duża może przekroczyć zakres `int32` w kernelu.

## MAX_JOBS
Stała: 512. Musi równać się `MAX_JOBS` w `EvaluateSchedules`.

## MAX_MACHINES
Stała: 64. Musi równać się `MAX_MACHINES` w `EvaluateSchedules`.

## problem
Zwraca `FactoryProblem`. Wyjście trafia do `PriorityRuleSeeder`, `PopulationInitializer`, `EvolutionEngine`, `ScheduleDecoder` i `ScheduleAnalysis`.

## job_op_offset
Zwraca tablicę offsetów operacji, wejście `EvaluateSchedules`.

## op_machine_type
Zwraca typ maszyny każdej operacji, wejście `EvaluateSchedules`.

## op_minutes
Zwraca czas każdej operacji w minutach, wejście `EvaluateSchedules`.

## job_arrival
Zwraca minutę napływu każdego zlecenia, wejście `EvaluateSchedules`.

## job_due
Zwraca termin każdego zlecenia, wejście `EvaluateSchedules`.

## job_weight
Zwraca wagę każdego zlecenia, wejście `EvaluateSchedules`.

## type_machine_offset
Zwraca zakresy numerów maszyn każdego typu, wejście `EvaluateSchedules`.
