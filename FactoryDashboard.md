Raport interaktywny: porównuje wynik ewolucji z regułami, pokazuje przebieg ewolucji, wykres Gantta, wykorzystanie maszyn, wyniki zleceń i dane wejściowe. To jedyne miejsce prezentacji; kontrolki zmieniają tylko widok, a nie uruchamiają ewolucji ponownie. Wejścia pochodzą z `AnalysisFileWriter`, `EvolutionEngine`, `ScheduleAnalysis` i `PolishNumberFormat`; wyjście `show` trafia do Maina.

## input_tables
Wejście: tabele `machines`, `recipes`, `orders`.

## result
Wejście: `EvolutionResult`, skąd pochodzi przebieg ewolucji i czas.

## report
Wejście: słownik z `ScheduleAnalysis.report`.

## written_paths
Wejście: ścieżki plików CSV, wypisywane w stopce.

## formatter
Wejście: `PolishNumberFormat`. Tabele dostają gotowy tekst, stąd wyłączone sortowanie, a wykresy układ z polskimi separatorami.

## schedule_name
Kontrolka lista, stan `schedule_name`; wartości to `Algorytm ewolucyjny`, `FIFO`, `EDD`, `SPT`, `LST`, domyślnie ewolucja. Wybiera harmonogram na wykresie Gantta, wykresie wykorzystania i w tabeli zleceń. Nie zmienia obliczeń.

## machine_type
Kontrolka lista, stan `machine_type`; wartości to `Wszystkie` oraz typy A–F, domyślnie `Wszystkie`. Filtruje tylko wykres Gantta.

## late_only
Pole wyboru, stan `late_only`, `True` lub `False`, domyślnie `False`. Gdy zaznaczone, tabela zleceń pokazuje tylko spóźnione.

## ALL_MACHINES
Stała: etykieta opcji bez filtra, `"Wszystkie"`.

## setup
Ustawia stan początkowy i wypisuje porównanie oraz ścieżki CSV w konsoli.

## prepare
Przed każdym rysowaniem przelicza wskaźniki, tabele i wykresy z bieżącego stanu kontrolek.

## show
Wyjście: wysyła stronę do zakładki Output. Strona pozostaje aktywna po końcu przepływu.
