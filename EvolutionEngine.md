Prowadzi ewolucję: trzyma populację i dane na GPU, a w każdym pokoleniu uruchamia kolejno `BreedGeneration`, `EvaluateSchedules` i `ReplaceSurvivors`. Python tylko ustala kolejność i co `log_every` pokoleń czyta koszty; same kroki ewolucji liczą kernele. Wejścia to uchwyty z `CUDAKernelLoader` oraz dane z `ProblemEncoder` i `PopulationInitializer`, a wyjście trafia do `ScheduleDecoder`, `ScheduleAnalysis` i `FactoryDashboard`.

## evaluate_schedules
Wejście: uchwyt kernela oceny.

## breed_generation
Wejście: uchwyt kernela tworzenia potomstwa.

## replace_survivors
Wejście: uchwyt kernela sukcesji.

## problem
Wejście: `FactoryProblem`, którego tablice są raz wysyłane na GPU.

## population
Wejście: populacja startowa `int32`, osobniki × geny.

## params
Wejście: `int32[13]`. Silnik przed każdym krokiem wpisuje numer pokolenia.

## formatter
Wejście: `PolishNumberFormat` do komunikatów o postępie w konsoli.

## generations
Liczba pokoleń, `int`, co najmniej 1, domyślnie `3000`; poniżej `ValueError`. Więcej pokoleń to dłuższy przebieg i koszt nie gorszy, zwykle z coraz mniejszym zyskiem.

## log_every
Co ile pokoleń odczytać koszty, `int`, co najmniej 1, domyślnie `25`; poniżej `ValueError`. Mniejsza wartość daje gęstszy wykres i kosztuje więcej transferów z GPU. Nie wpływa na wynik.

## block_size
Wątki w bloku CUDA, `int`, 32–1024, domyślnie `256`; poza zakresem `ValueError`. Wpływa tylko na wydajność, nie na wynik.

## GENERATION_SLOT
Stała: indeks numeru pokolenia w `params` (5). Musi zgadzać się z kernelem `BreedGeneration`.

## individuals
Atrybut: liczba osobników z `params[0]`.

## grid
Atrybut: siatka bloków CUDA pokrywająca wszystkich osobników.

## result
Uruchamia ewolucję i zwraca `EvolutionResult`. Każde wywołanie liczy od nowa, więc Main wywołuje ją raz.
