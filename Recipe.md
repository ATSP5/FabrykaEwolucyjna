Rekord danych: uporządkowany przepis na jeden produkt. Tworzy go `FactoryCatalog`, a czytają `OrderStreamGenerator`, `ProblemEncoder` i `AnalysisFileWriter`; jako czysty rekord nie ma połączeń.

## product
Nazwa produktu, `str`, np. `"X"`. Unikalna w katalogu; duplikat zastąpiłby wcześniejszy przepis w `ProblemEncoder`. Produkt wskazują zlecenia.

## steps
Kroki w kolejności wykonania, `tuple[RecipeStep, ...]`, co najmniej jeden. Ta sama maszyna może wystąpić kilka razy (X używa A dwa razy). Kolejność jest wiążąca: dekoder nie zacznie kroku przed końcem poprzedniego.

## total_minutes
Właściwość tylko do odczytu: suma czasów kroków w minutach, `int`, czyli najkrótszy możliwy czas produkcji. Na jej podstawie generator wybiera osiągalny deadline, a raport pokazuje długość przepisu.
