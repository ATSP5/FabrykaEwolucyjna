Rekord danych: jedno zlecenie ze strumienia, np. „wytwórz X, deadline 2 h”. Tworzy je `OrderStreamGenerator`, a czytają `ProblemEncoder` i `AnalysisFileWriter`; jako czysty rekord nie ma połączeń.

## order_id
Identyfikator zlecenia, `str`, np. `"Z0001"`, kolejny numer w strumieniu. Służy tylko do opisu w raporcie i CSV.

## product
Produkt do wytworzenia, `str`. Musi mieć przepis w katalogu, inaczej `ProblemEncoder` zgłosi `KeyError`.

## arrival_minute
Minuta napływu od początku zmiany, `int`, od 0. Żaden krok zlecenia nie zacznie się wcześniej, co ogranicza harmonogram.

## deadline_minutes
Czas na realizację liczony od napływu, w minutach, `int`, większy od 0. Krótszy deadline zwiększa ryzyko spóźnienia i koszt.

## weight
Priorytet zlecenia, `int`, co najmniej 1 (mnożnik spóźnienia w funkcji kosztu). Większa waga sprawia, że ewolucja chętniej wykona to zlecenie na czas kosztem innych.

## due_minute
Właściwość tylko do odczytu: `arrival_minute + deadline_minutes`, czyli termin w minutach od początku zmiany. Od niego liczone jest spóźnienie.
