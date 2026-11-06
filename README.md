# FabrykaEwolucyjna

Harmonogramowanie losowego strumienia zleceń w fabryce algorytmem ewolucyjnym, którego kolejne kroki wykonują kernele CUDA. Projekt jest przeznaczony dla osób analizujących przepustowość produkcji i terminowość zleceń.

Fabryka ma maszyny A×3, B×4, C×2, D×1, E×5 i F×8. Każdy z ośmiu produktów ma przepis, np. X: A 30 min, B 10 min, A 4 min, D 8 min. Celem jest kolejność operacji minimalizująca ważone spóźnienia.

## Metoda

Komórkowy algorytm genetyczny na toroidalnej siatce (domyślnie 64×64, czyli 4 096 osobników):

| Krok pokolenia | Kernel CUDA | Działanie |
|---|---|---|
| Potomstwo | `BreedGeneration` | turniej sąsiadów, krzyżowanie POX, mutacja zamianami |
| Ocena | `EvaluateSchedules` | dekodowanie chromosomu na harmonogram i koszt |
| Sukcesja | `ReplaceSurvivors` | dziecko zastępuje rodzica, gdy nie jest gorsze |

Chromosom to permutacja z powtórzeniami numerów zleceń: k-te wystąpienie zlecenia to jego k-ty krok. Koszt = 100 × Σ(priorytet × spóźnienie) + czas zakończenia pracy. Niezależny dekoder Pythona sprawdza wynik GPU, a reguły FIFO, EDD, SPT i LST stanowią punkt odniesienia oraz ziarno populacji.

## Wymagania

- NVIDIA GPU ze sterownikiem CUDA (PTX w projekcie: `sm_61`, GTX 1050 Ti; inna karta może wymagać ponownej kompilacji przez **Compile CUDA Kernels**)
- Python 3.10 lub nowszy
- `numpy`, `pandas`, `pycuda`

## Instalacja

```bash
pip install numpy pandas pycuda
```

## Uruchomienie

```bash
python main_1.py
```

W CatNip uruchamiaj w trybie **Code Run**. Graph Run nie zadziała, bo uchwytów kerneli nie można przekazać między procesami.

Docker na GPU (obraz z bloku Dockerfile, wymaga NVIDIA Container Toolkit):

```bash
docker build -t fabrykaewolucyjna-cuda:12.2 .
docker run --rm --gpus all -v "$PWD:/app" -w /app fabrykaewolucyjna-cuda:12.2 python main_1.py
```

## Struktura

| Blok | Rola |
|---|---|
| `MachineGroup`, `RecipeStep`, `Recipe`, `ProductionOrder`, `FactoryProblem`, `EvolutionResult`, `ScheduledOperation` | rekordy danych |
| `FactoryCatalog` | maszyny i przepisy |
| `OrderStreamGenerator` | losowy strumień zleceń |
| `ProblemEncoder` | tablice `int32` dla GPU |
| `PriorityRuleSeeder` | harmonogramy reguł FIFO, EDD, SPT, LST |
| `PopulationInitializer` | pokolenie zerowe i parametry algorytmu |
| `EvaluateSchedules`, `BreedGeneration`, `ReplaceSurvivors` | kernele CUDA |
| `CUDAKernelLoader` | ładowanie kerneli |
| `EvolutionEngine` | pętla pokoleń na GPU |
| `ScheduleDecoder`, `ScheduleAnalysis` | odtworzenie, kontrola i pomiar harmonogramów |
| `AnalysisFileWriter` | tabele i pliki CSV |
| `PolishNumberFormat` | polski zapis liczb |
| `FactoryDashboard` | raport interaktywny |
| `Main` | punkt wejścia |
| `Dockerfile (GPU run image)`, `Docker Compose (GPU run image)` | obraz Dockera do uruchomień na GPU |

## Konfiguracja

Nastawy to argumenty konstruktorów z wartościami domyślnymi: `OrderStreamGenerator` (ziarno, obciążenie, deadline'y), `PopulationInitializer` (rozmiar siatki, krzyżowanie, mutacja) i `EvolutionEngine` (liczba pokoleń). Pliki CSV powstają w `data/`.

## Licencja

Nie określono licencji.
