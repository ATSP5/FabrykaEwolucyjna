Buduje pokolenie zerowe na toroidalnej siatce oraz wektor parametrów czytany przez kernele. Oddziela wszystkie nastawy algorytmu genetycznego od pętli. `population` i `params` zasilają `EvolutionEngine` oraz kernele. Domyślna siatka 64×64 przy około 440 genach zajmuje około 7 MB na populację; `EvolutionEngine` trzyma trzy takie bufory, co dobrze mieści się w 4 GB VRAM karty GTX 1050 Ti.

## problem
Wejście: `FactoryProblem` z `ProblemEncoder`.

## seeds
Wejście: chromosomy reguł z `PriorityRuleSeeder`. Niezmienione kopie trafiają do komórek rozłożonych po siatce, a sukcesja ich nie pogarsza, więc ewolucja nie może skończyć gorzej niż najlepsza reguła.

## grid_side
Bok siatki, `int`, zakres 4–512, domyślnie `64` (4 096 osobników); poza zakresem `ValueError`. Więcej osobników to szersze przeszukiwanie, ale wolniejsze pokolenie i większe zużycie VRAM (rośnie z kwadratem boku).

## random_seed
Ziarno, `int`, domyślnie `7`. Steruje populacją startową, a przez `params[6]` także generatorem liczb losowych kerneli. Inne ziarno daje inny przebieg ewolucji na tych samych danych.

## seeded_share
Udział komórek startujących z zaburzonej reguły, `float`, 0–1, domyślnie `0,5`; poza zakresem `ValueError`. Reszta to kolejność zbliżona do napływu z szumem. Większy udział to szybszy start, ale mniejsza różnorodność.

## arrival_noise_minutes
Odchylenie szumu kolejności w minutach, `float`, co najmniej 0, domyślnie `60`; poniżej `ValueError`. Większe daje bardziej losowe osobniki startowe i słabszy koszt początkowy.

## neighbourhood_radius
Promień sąsiedztwa, w którym komórka szuka partnera, `int`, od 1 do `grid_side / 2`, domyślnie `2`; poza zakresem `ValueError`. Większy przyspiesza rozchodzenie się dobrych rozwiązań, ale szybciej traci różnorodność.

## crossover_permille
Szansa krzyżowania na dziecko w promilach, `int`, 0–1000, domyślnie `900`; poza zakresem `ValueError`. Bez krzyżowania dziecko jest kopią rodzica, więc wynik zależy wtedy wyłącznie od mutacji.

## mutation_permille
Szansa mutacji na dziecko w promilach, `int`, 0–1000, domyślnie `600`; poza zakresem `ValueError`. Większa wartość daje silniejszą eksplorację, ale częściej psuje dziecko (sukcesja i tak chroni rodzica).

## mutation_max_swaps
Największa liczba zamian genów na dziecko, `int`, co najmniej 1, domyślnie `4`; poniżej `ValueError`. Większa to grubsze zmiany harmonogramu.

## mutation_window
Największa odległość zamienianych genów, `int`, co najmniej 1, domyślnie `30`; poniżej `ValueError`. Małe okno to lokalne poprawki kolejności, duże to skoki po całej zmianie.

## population
Zwraca płaską tablicę `int32` o długości osobniki × geny, wiersz na komórkę siatki.

## params
Zwraca `int32[13]`: 0 osobniki, 1 geny, 2 joby, 3 maszyny, 4 bok siatki, 5 pokolenie (ustawia je `EvolutionEngine`), 6 ziarno, 7 promień, 8 mutacja, 9 zamiany, 10 okno, 11 skala spóźnienia, 12 krzyżowanie. Kolejność musi zgadzać się z kernelami.
