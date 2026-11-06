Otwiera trzy kernele ewolucji z plików PTX i udostępnia ich uchwyty, po jednej metodzie na kernel. Izoluje też konfigurację DLL CUDA pod Windows, dlatego Main musi importować ten blok jako pierwszy. Gdy brak PTX, kompiluje `.cu` przez nvcc w czasie uruchomienia. Wyjścia trafiają do `EvolutionEngine`. Wejścia z kerneli wyznaczają tylko kolejność w grafie i nie są argumentami konstruktora, bo kernele są uruchamiane w pętli, nie jednorazowo.

## ptx_dir
Dodatkowy folder szukania PTX, `str`, domyślnie pusty. Potem szukane są: bieżący folder, folder modułu i folder wyżej. Bez PTX i bez `.cu` zgłaszany jest `FileNotFoundError`. PTX w projekcie jest skompilowany dla `sm_61` (GTX 1050 Ti).

## cost
Wejście porządkujące z `EvaluateSchedules`; wartość nie jest czytana.

## children
Wejście porządkujące z `BreedGeneration`; wartość nie jest czytana.

## next_population
Wejście porządkujące z `ReplaceSurvivors`; wartość nie jest czytana.

## evaluate_schedules
Zwraca uchwyt kernela `EvaluateSchedules`. Uchwytu nie da się zapisać przez pickle, więc projekt musi działać w trybie Code Run, nie Graph Run.

## breed_generation
Zwraca uchwyt kernela `BreedGeneration`, z tym samym ograniczeniem.

## replace_survivors
Zwraca uchwyt kernela `ReplaceSurvivors`, z tym samym ograniczeniem.
