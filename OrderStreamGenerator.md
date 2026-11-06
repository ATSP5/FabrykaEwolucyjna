Tworzy losowy, powtarzalny strumień zleceń, np. „wytwórz X, deadline 2 h”. Odstępy są wykładnicze (proces Poissona), a częstość wynika z żądanego obciążenia najbardziej zajętego typu maszyny. Dzięki temu dane są trudne, ale nie beznadziejne, także po zmianie parku maszyn lub przepisów. Blok oddziela dane losowe od stałego katalogu; wyjście trafia do `ProblemEncoder` i `AnalysisFileWriter`.

## machines
Wejście: `list[MachineGroup]` z `FactoryCatalog`. Liczba sztuk wyznacza przepustowość każdego typu.

## recipes
Wejście: `list[Recipe]` z `FactoryCatalog`. Produkt losowany jest z równym prawdopodobieństwem.

## seed
Ziarno generatora, `int`, domyślnie `2026`. To samo ziarno daje ten sam strumień; inne daje inny zestaw danych do analizy.

## shift_minutes
Czas napływu zleceń w minutach, `int`, domyślnie `480` (8 h), wartość dodatnia; inaczej `ValueError`. Dłuższa zmiana to więcej zleceń i dłuższe chromosomy. Strumień powyżej 512 zleceń odrzuci `ProblemEncoder`.

## bottleneck_load
Docelowe obciążenie najbardziej zajętego typu maszyny, `float`, zakres `(0; 1,5]`, domyślnie `0,9`; poza zakresem `ValueError`. Przy tych danych daje średnio około 120 zleceń. Powyżej 1 fabryka nie nadąża i spóźnienia są nieuniknione.

## deadline_minutes
Możliwe czasy na realizację w minutach, krotka wartości dodatnich, domyślnie 60, 90, 120, 180 i 240; inaczej `ValueError`. Krótsze deadline'y dają więcej spóźnień i większą przewagę dobrego harmonogramu.

## weights
Możliwe priorytety zleceń, krotka wartości dodatnich, domyślnie `(1, 1, 1, 2, 3)` (powtórzenia to większe prawdopodobieństwo); inaczej `ValueError`. Większe rozpiętości silniej premiują ważne zlecenia.

## min_slack_ratio
Najmniejszy stosunek deadline'u do łącznego czasu przepisu, `float`, co najmniej 1, domyślnie `1,2`; poniżej `ValueError`. Gdy żaden deadline nie spełnia warunku, generator bierze czas zaokrąglony w górę do 30 minut. Większa wartość łagodzi terminy.

## orders
Zwraca `list[ProductionOrder]` posortowaną rosnąco po napływie. Pusty wynik (bardzo mały napływ) odrzuci `ProblemEncoder`.
