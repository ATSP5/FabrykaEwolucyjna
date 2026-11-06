Kernel CUDA, krok tworzenia potomstwa: każdy wątek to komórka siatki, która wybiera partnera turniejem dwóch sąsiadów, krzyżuje się z nim operatorem POX i mutuje dziecko zamianami genów. POX zawsze daje poprawną permutację z powtórzeniami i nie potrzebuje pamięci roboczej, co pasuje do GPU. Generator liczb losowych jest bezstanowy (hash PCG z ziarna, pokolenia i komórki), więc przebieg jest powtarzalny. Plik `breedgeneration.ptx` otwiera `CUDAKernelLoader`, uruchamia `EvolutionEngine` raz na pokolenie. Nie używaj „Regenerate Code” bez ustawienia typu konektorów na Integer.

## population
Wejście: bieżące chromosomy `int32`, osobniki × geny.

## cost
Wejście: `int32[osobniki]`, koszty bieżącej populacji, używane w turnieju. Lepszy sąsiad zostaje partnerem.

## params
Wejście: `int32[13]`, kernel czyta 0 osobniki, 1 geny, 4 bok siatki, 5 pokolenie, 6 ziarno, 7 promień, 8 szansę mutacji, 9 liczbę zamian, 10 okno, 12 szansę krzyżowania. Wartości i ich wpływ opisuje `PopulationInitializer`.

## n
Liczba elementów pierwszego wejścia; kernel jej nie używa, a zakres wyznacza `params[0]`.

## children
Wyjście: `int32`, osobniki × geny, jedno dziecko na komórkę. Dziecko ocenia następnie `EvaluateSchedules`.
