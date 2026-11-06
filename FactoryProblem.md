Rekord danych: cały problem harmonogramowania jako płaskie tablice `int32`, w układzie czytanym przez kernele CUDA. Tworzy go `ProblemEncoder`, a używają `PriorityRuleSeeder`, `PopulationInitializer`, `EvolutionEngine`, `ScheduleDecoder` i `ScheduleAnalysis`. Metoda `pick_machine` jest tu celowo, aby wszystkie dekodery Pythona miały jedną regułę wyboru maszyny, identyczną z kernelem. Blok nie ma połączeń, bo to rekord importowany przez używające go klasy.

## machine_types
Nazwy typów maszyn, `tuple[str, ...]`, w kolejności numeracji typów.

## machine_labels
Nazwy konkretnych maszyn, `tuple[str, ...]`, np. `"A1"`, `"A2"`; najwyżej 64 pozycje. Oś pionowa wykresu Gantta.

## order_ids
Identyfikator zlecenia dla każdego numeru joba, `tuple[str, ...]`; od 1 do 512 pozycji.

## products
Produkt dla każdego joba, `tuple[str, ...]`.

## job_op_offset
Tablica `int32` o długości `jobs + 1`: operacje joba `j` to indeksy od `job_op_offset[j]` do `job_op_offset[j+1]-1`.

## op_machine_type
Numer typu maszyny dla każdej operacji, `int32`, od 0 do liczby typów minus 1.

## op_minutes
Czas każdej operacji w minutach, `int32`, większy od 0.

## job_arrival
Minuta napływu każdego joba, `int32`, od 0. Żaden krok nie zacznie się wcześniej.

## job_due
Termin każdego joba w minutach od początku zmiany, `int32`.

## job_weight
Waga spóźnienia każdego joba, `int32`, co najmniej 1.

## type_machine_offset
Tablica `int32` o długości liczby typów + 1: maszyny typu `t` mają numery od `type_machine_offset[t]` do `type_machine_offset[t+1]-1`.

## tardiness_scale
Mnożnik ważonej spóźnialności w koszcie, `int`, co najmniej 1. Patrz `ProblemEncoder.tardiness_scale`.

## jobs
Właściwość: liczba zleceń, `int`.

## genes
Właściwość: liczba operacji, czyli długość chromosomu, `int`.

## machines
Właściwość: liczba wszystkich maszyn, `int`.

## base_chromosome
Zwraca tablicę `int32` z numerem każdego joba powtórzonym tyle razy, ile ma kroków. Każdy osobnik jest permutacją tych genów.

## pick_machine
`pick_machine(machine_free, machine_type, ready)` zwraca `(machine, start_minute)`. Wybiera maszynę danego typu, która zacznie krok najwcześniej, a przy remisie tę zwolnioną najpóźniej (najkrótszy przestój). Musi działać identycznie jak kernel `EvaluateSchedules`, bo inaczej `ScheduleAnalysis` przerwie przebieg błędem niezgodności kosztów.
