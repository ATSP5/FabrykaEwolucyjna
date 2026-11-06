Kernel CUDA, krok sukcesji: w każdej komórce dziecko zastępuje osobnika tylko wtedy, gdy nie jest od niego gorsze. Dzięki temu najlepszy harmonogram nigdy nie ginie, a równe dzieci pozwalają przechodzić przez plateau. Plik `replacesurvivors.ptx` otwiera `CUDAKernelLoader`, uruchamia `EvolutionEngine` raz na pokolenie. Nie używaj „Regenerate Code” bez ustawienia typu konektorów na Integer.

## population
Wejście: bieżące chromosomy `int32`, osobniki × geny.

## cost
Wejście: `int32[osobniki]`, koszty bieżącej populacji.

## children
Wejście: dzieci z `BreedGeneration`, ten sam układ co `population`.

## children_cost
Wejście: `int32[osobniki]`, koszty dzieci z `EvaluateSchedules`.

## params
Wejście: `int32[13]`, kernel czyta 0 osobniki i 1 geny.

## n
Liczba elementów pierwszego wejścia; kernel jej nie używa, a zakres wyznacza `params[0]`.

## next_population
Wyjście: chromosomy następnego pokolenia. Silnik zamienia wskaźniki buforów, dzięki czemu pokolenie niczego nie kopiuje na CPU.

## next_cost
Wyjście: koszty następnego pokolenia. Najlepszy koszt nie może rosnąć między pokoleniami.
