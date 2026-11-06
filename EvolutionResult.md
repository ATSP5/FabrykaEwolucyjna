Rekord danych: wynik ewolucji na GPU. Tworzy go `EvolutionEngine`, a czytają `ScheduleDecoder`, `ScheduleAnalysis` i `FactoryDashboard`; jako czysty rekord nie ma połączeń.

## best_chromosome
Najlepszy chromosom ostatniego pokolenia, tablica `int32` o długości `genes`. `ScheduleDecoder` odtwarza z niego harmonogram.

## best_cost
Koszt tego chromosomu policzony na GPU, `int`. Musi równać się kosztowi z dekodera Pythona; niezgodność przerywa przebieg.

## history
`DataFrame` z kolumnami `Pokolenie`, `Najlepszy koszt`, `Średni koszt`, po jednym wierszu co `log_every` pokoleń. Rysuje wykres przebiegu ewolucji.

## individuals
Liczba osobników, `int`: `grid_side` do kwadratu.

## generations
Liczba wykonanych pokoleń, `int`.

## seconds
Czas ewolucji w sekundach, `float`, razem z przesłaniem danych na GPU i odczytem telemetrii.

## device
Nazwa karty GPU, `str`, pokazywana w raporcie.
