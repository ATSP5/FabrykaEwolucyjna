Punkt wejścia: buduje dane, uruchamia ewolucję, sprawdza wynik i pokazuje raport. Main celowo nie ma markerów `#<blocks_def>` i `#<blocks_call>`. Generator emituje blok CUDA jako jednorazowe uruchomienie, a tu kernele działają tysiące razy w pętli na buforach GPU w `EvolutionEngine`. Dlatego ten kod jest zapisywany dosłownie i po zmianie połączeń trzeba go zaktualizować ręcznie. `CUDAKernelLoader` musi być importowany jako pierwszy, bo ustawia ścieżkę DLL CUDA. Tryb uruchomienia to Code Run, ponieważ uchwytów kerneli nie można przekazać między procesami Graph Run.

## result
Wejście: wyjście `show` raportu `FactoryDashboard`. Main wywołuje je na końcu przepływu.

## main
Funkcja bez argumentów wykonująca cały przepływ raz.
