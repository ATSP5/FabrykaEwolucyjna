Tworzy losowy, powtarzalny strumień zleceń, np. „wytwórz X, deadline 2 h”. Odstępy są wykładnicze (proces Poissona), a częstość wynika z żądanego obciążenia najbardziej zajętego typu maszyny. Dzięki temu poziom trudności danych da się ustawić jedną nastawą, także po zmianie parku maszyn lub przepisów. Blok oddziela dane losowe od stałego katalogu; wyjście trafia do `ProblemEncoder` i `AnalysisFileWriter`.

Przy nastawach domyślnych i ziarnie 2026 powstaje 199 zleceń i 2 286 operacji, czyli przeciążona zmiana z napływem średnio co 3,6 minuty. Kolejność obsługi ma tu duże znaczenie: reguły różnią się niemal dwukrotnie (ważona spóźnialność EDD 8 696, FIFO 15 854), a około połowa zleceń jest spóźniona.

## machines
Wejście: `list[MachineGroup]` z `FactoryCatalog`. Liczba sztuk wyznacza przepustowość każdego typu.

## recipes
Wejście: `list[Recipe]` z `FactoryCatalog`. Produkt losowany jest z równym prawdopodobieństwem.

## seed
Ziarno generatora, `int`, domyślnie `2026`. To samo ziarno daje ten sam strumień; inne daje inny zestaw danych do analizy.

## shift_minutes
Czas napływu zleceń w minutach, `int`, domyślnie `720` (12 h), wartość dodatnia; inaczej `ValueError`. Dłuższy czas to więcej zleceń i dłuższe chromosomy, więc wolniejsze pokolenia. Strumień powyżej 512 zleceń odrzuci `ProblemEncoder`.

## bottleneck_load
Docelowe obciążenie najbardziej zajętego typu maszyny, `float`, zakres `(0; 3]`, domyślnie `1,4`; poza zakresem `ValueError`. Wyznacza napływ zleceń: przy obecnych przepisach `1,4` to około 0,28 zlecenia na minutę. Powyżej 1 fabryka nie nadąża, kolejka rośnie i spóźnienia są nieuniknione, a algorytm decyduje, które zlecenia poświęcić. Przy `1,1` reguła LST osiąga już zero spóźnień, więc ewolucja może skrócić tylko czas zakończenia pracy. Bardzo wysokie wartości (około `1,7` przy 8 h) sprawiają, że spóźnia się większość zleceń, a wynik zależy głównie od przeciążenia.

## deadline_minutes
Możliwe czasy na realizację w minutach, krotka wartości dodatnich, domyślnie 120, 150, 180, 240 i 300; inaczej `ValueError`. Krótsze deadline'y dają więcej spóźnień i większą wagę dobrego harmonogramu.

## weights
Możliwe priorytety zleceń, krotka wartości dodatnich, domyślnie `(1, 1, 1, 2, 3, 5)` (powtórzenia to większe prawdopodobieństwo); inaczej `ValueError`. Reguły FIFO, EDD, SPT i LST nie znają priorytetów, więc większa rozpiętość zwiększa możliwą przewagę algorytmu ewolucyjnego.

## min_slack_ratio
Najmniejszy stosunek deadline'u do łącznego czasu przepisu, `float`, co najmniej 1, domyślnie `1,2`; poniżej `ValueError`. Gdy żaden deadline nie spełnia warunku, generator bierze czas zaokrąglony w górę do 30 minut. Większa wartość łagodzi terminy.

## orders
Zwraca `list[ProductionOrder]` posortowaną rosnąco po napływie. Pusty wynik (bardzo mały napływ) odrzuci `ProblemEncoder`.
