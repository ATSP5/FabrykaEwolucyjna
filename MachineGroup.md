Rekord danych: jeden typ maszyny i liczba identycznych sztuk w fabryce. Jest osobnym blokiem, bo używają go `FactoryCatalog`, `OrderStreamGenerator`, `ProblemEncoder` i `AnalysisFileWriter`; jako czysty rekord nie ma połączeń.

## name
Nazwa typu maszyny, `str`, np. `"A"`. Musi być unikalna w fabryce. Przepis z nieznaną nazwą kończy się `KeyError` w `ProblemEncoder`. Pierwsza litera nazwy służy też do grupowania w raporcie, więc nazwy powinny zaczynać się różnymi literami.

## count
Liczba identycznych maszyn tego typu, `int`, co najmniej 1. Suma po wszystkich typach może wynosić najwyżej 64 (limit kerneli; powyżej błąd `ValueError`). Więcej sztuk to większa przepustowość typu, zwykle mniej spóźnień i większy napływ zleceń przy tym samym obciążeniu.
