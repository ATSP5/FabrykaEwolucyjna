Polski zapis liczb, np. `1 321 690 982,53`, wszędzie, gdzie widzi je człowiek. Jedno miejsce notacji używane przez `EvolutionEngine` (konsola) i `FactoryDashboard` (raport). Wyjście `formatter` zwraca cały obiekt, bo odbiorcy formatują wartości znane dopiero u nich, wiele razy w trakcie pracy.

## decimals
Domyślna liczba miejsc po przecinku, `int`, domyślnie `2`; ujemna daje `ValueError`.

## thousands
Separator tysięcy, `str`, domyślnie spacja. Musi być niepusty i różny od `decimal`, inaczej `ValueError`.

## decimal
Separator dziesiętny, `str`, domyślnie przecinek, z tym samym warunkiem.

## number
`number(value, decimals=None, signed=False)` zwraca tekst liczby; dla `None` i NaN pusty tekst.

## percent
`percent(value, decimals=2, signed=False)` zwraca tekst liczby ze znakiem `%`.

## frame
`frame(frame, decimals=None)` zwraca kopię `DataFrame` z kolumnami liczbowymi jako tekst. Stąd tabele raportu mają wyłączone sortowanie, bo sortowałyby tekst.

## plotly_layout
`plotly_layout(y_title, x_title, y_decimals=0)` zwraca klucze układu Plotly z tym samym zapisem na osiach.

## hover
`hover(unit="", decimals=0, axis="y")` zwraca szablon podpowiedzi Plotly w tym samym zapisie.

## formatter
Zwraca ten obiekt. Wyjście trafia do `EvolutionEngine` i `FactoryDashboard`.
