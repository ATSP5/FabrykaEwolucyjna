Rekord danych: jeden krok zlecenia umieszczony na konkretnej maszynie i w konkretnym czasie. Tworzy go `ScheduleDecoder`, a czyta `ScheduleAnalysis`; jako czysty rekord nie ma połączeń.

## job
Numer zlecenia, `int`, od 0 do `jobs - 1`.

## step
Numer kroku w przepisie, `int`, liczony od 0.

## machine
Numer maszyny, `int`, od 0 do `machines - 1`; nazwa jest w `FactoryProblem.machine_labels`.

## start_minute
Początek pracy w minutach od początku zmiany, `int`.

## end_minute
Koniec pracy w minutach od początku zmiany, `int`. Koniec ostatniego kroku porównywany jest z terminem zlecenia.
