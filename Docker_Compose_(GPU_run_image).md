Plik `docker-compose.yml` projektu, z którego CatNip buduje obraz na GPU, gdy środowisko *Docker: Python + CUDA 12.2 (GPU)* ma **Docker source = Build Docker**. Blok nie jest wykonywany ani połączony; bez niego `docker compose build` kończy się błędem `no configuration file provided`.

## services.fabrykaewolucyjna
Jedyna usługa, czyli przepis na obraz projektu. Nazwa nie wpływa na wynik.

## build.context
`.` oznacza folder projektu. Dockerfile niczego z niego nie kopiuje, więc jego rozmiar wydłuża tylko wysyłanie kontekstu.

## build.dockerfile
`Dockerfile`, plik zapisany z bloku *Dockerfile (GPU run image)*. Po zmianie tego bloku potrzebne jest *Generate Source*.

## image
`fabrykaewolucyjna-cuda:12.2`, nazwa obrazu używanego przez CatNip. Nowa nazwa tworzy nowy obraz, a stary zostaje na dysku do ręcznego usunięcia.

## working_dir / volumes
`/app` i `.:/app`: folder projektu w kontenerze. Potrzebne przy ręcznym `docker compose run`; CatNip montuje projekt sam.

## deploy.resources.reservations.devices
Dostęp do wszystkich kart NVIDIA (`count: all`) przy ręcznym uruchomieniu. Wymaga NVIDIA Container Toolkit. W CatNip GPU włącza opcja środowiska *Enable GPU (--gpus all)*. Bez GPU kernele CUDA się nie załadują i przebieg zakończy się błędem.
