Kernel CUDA, krok oceny: każdy wątek dekoduje chromosom jednego osobnika na harmonogram i liczy koszt. To osobny kernel, bo uruchamiany jest raz dla populacji startowej i raz na pokolenie dla dzieci. Skompilowany plik to `evaluateschedules.ptx`, otwiera go `CUDAKernelLoader`, a uruchamia `EvolutionEngine` na buforach trzymanych na GPU. Limity: 512 zleceń i 64 maszyny (tablice na stosie wątku), pilnowane w `ProblemEncoder`. Nie używaj „Regenerate Code” bez ustawienia typu konektorów na Integer, bo sygnatura zmieni się na `float*`.

## population
Wejście: chromosomy `int32`, osobniki × geny. Silnik podaje tu populację startową albo dzieci.

## job_op_offset
Wejście: `int32[jobs+1]`, początek operacji każdego joba.

## op_machine_type
Wejście: `int32[genes]`, typ maszyny operacji.

## op_minutes
Wejście: `int32[genes]`, czas operacji w minutach.

## job_arrival
Wejście: `int32[jobs]`, minuta napływu. Wcześniej żaden krok joba nie zacznie się.

## job_due
Wejście: `int32[jobs]`, termin w minutach od początku zmiany.

## job_weight
Wejście: `int32[jobs]`, waga spóźnienia.

## type_machine_offset
Wejście: `int32[typy+1]`, zakres numerów maszyn każdego typu.

## params
Wejście: `int32[13]`, kernel czyta 0 osobniki, 1 geny, 2 joby, 3 maszyny, 11 skalę spóźnienia.

## n
Liczba elementów pierwszego wejścia; kernel jej nie używa, a zakres wyznacza `params[0]`. Siatka wątków musi pokrywać `params[0]`, a blok ma domyślnie 256 wątków.

## cost
Wyjście: `int32[osobniki]`, koszt = skala × Σ(waga × spóźnienie) + czas zakończenia pracy, mniej znaczy lepiej. To kryterium selekcji i sukcesji. Zależy tylko od chromosomu, więc taki sam wynik musi dać dekoder Pythona.
