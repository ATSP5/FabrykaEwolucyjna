Rekord danych: jeden krok przepisu, czyli typ maszyny i czas pracy. Składa się z niego `Recipe`; jako czysty rekord nie ma połączeń.

## machine
Nazwa typu maszyny, `str`. Musi istnieć w `FactoryCatalog.MACHINES`, inaczej `ProblemEncoder` zgłosi `KeyError`. Wybór maszyny decyduje, którą kolejkę obciąża krok, a tym samym, co jest wąskim gardłem.

## minutes
Czas kroku w całych minutach, `int`, większy od 0 (jednostka wszystkich obliczeń na GPU). Dłuższe kroki zwiększają obciążenie typu maszyny, a generator przy tym samym `bottleneck_load` zmniejszy wtedy częstość zleceń.
