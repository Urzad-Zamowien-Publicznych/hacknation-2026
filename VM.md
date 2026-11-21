# Hacknation — instrukcja dla zespołów: serwer do wdrożenia rozwiązania

Każdy zespół może dostać własną maszynę wirtualną w Azure. Zainstalujcie na niej swoje rozwiązanie do ekstrakcji
informacji z dokumentów tak, żeby oceniający mogli je uruchomić i przetestować **bez Waszej pomocy**.

## Jak dostać serwer

Aby otrzymać maszynę wirtualną, wypełnijcie formularz:
**[Odwołania2JSON | Zapotrzebowanie na VM](https://forms.cloud.microsoft/e/HRFJjEcqMF)**

Wystarczy jedno zgłoszenie na zespół.

## Dostęp

Login, hasło i adres IP dostaniecie od organizatorów po wypełnieniu formularza.

```bash
ssh <login>@<adres-ip>
```

Jeśli SSH zwraca `Too many authentication failures` (macie dużo kluczy SSH w agencie, np. w 1Password),
wymuście logowanie hasłem:

```bash
ssh -o PubkeyAuthentication=no <login>@<adres-ip>
```

> ⚠️ **Dostęp zespołów zostanie odcięty o: 22.11.2026 o 11:00.** Od tej chwili nie zalogujecie się na serwer,
> a rozwiązanie będzie oceniane w stanie, w jakim je zostawicie. Usługi i kontenery, które działają w tle, **nie
> zostaną zatrzymane**.

## Parametry serwera

| | |
|---|---|
| System | Ubuntu 24.04 LTS |
| CPU / RAM | 2 vCPU / 16 GB |
| Dysk | 64 GB |
| GPU | brak |
| Porty otwarte z internetu | 22 (SSH), **80, 443, 8000, 8080** |
| Internet z serwera | tak (apt, pip, Docker Hub, GitHub, zewnętrzne API) |

## Co jest już zainstalowane

- **Docker** + **Docker Compose v2** (`docker compose ...`). Wasze konto jest w grupie `docker`, więc `sudo` nie jest potrzebne.
- **git**
- **Python 3.12** z `venv` i `pip` (`python3 -m venv .venv`)
- **build-essential** (gcc, make), `unzip`, `jq`, `htop`, `tmux`

Macie uprawnienia administratora: `sudo` (z Waszym hasłem), np. `sudo apt install <pakiet>`.
Możecie doinstalować wszystko, czego potrzebujecie.

## Jak przebiega ocena

1. Po terminie odcinamy dostęp zespołu do serwera.
2. Logujemy się na serwer kontem oceniających.
3. Wgrywamy do **`/opt/solution/input`** nasz **tajny zbiór dokumentów** (nie znacie go wcześniej).
4. W katalogu **`/opt/solution`** uruchamiamy **komendę z pliku `RUN.md`**.
5. Zabieramy pliki z **`/opt/solution/output`** i na ich podstawie oceniamy rozwiązanie.

Nikt z Was nie będzie obecny przy ocenie — komenda z `RUN.md` musi zadziałać bez Waszej pomocy.

## Struktura katalogów

```
/opt/solution/          ← cały projekt (kod, konfiguracja, modele, docker-compose.yml, ...)
├── RUN.md              ← komenda uruchamiająca (wymagany)
├── input/              ← tu wgramy dokumenty do przetworzenia
└── output/             ← tu rozwiązanie zapisuje wyniki
```

Katalogi `input/` i `output/` są już utworzone — nie usuwajcie ich i nie zmieniajcie im nazw. Przed oceną możemy
je wyczyścić, więc nie trzymajcie w nich niczego, czego potrzebuje rozwiązanie.

Projekt umieśćcie bezpośrednio w `/opt/solution` (katalog należy do Waszego konta, `sudo` nie jest potrzebne), np.:

```bash
cd /opt/solution
git clone <adres-repozytorium> repo     # albo skopiujcie pliki bezpośrednio do /opt/solution
```

## Wymagania

1. **Cały projekt i jego konfiguracja są w `/opt/solution`.** Oceniający będą szukać rozwiązania wyłącznie tam.
2. **Rozwiązanie przetwarza wszystkie pliki z `/opt/solution/input`** i zapisuje wyniki do **`/opt/solution/output`**.
3. **Plik `/opt/solution/RUN.md`** zawiera komendę uruchamiającą przetwarzanie (szablon niżej). Komenda:
   - jest uruchamiana z katalogu `/opt/solution` z uprawnieniami administratora (`sudo`), więc może korzystać z Dockera,
   - nie wymaga żadnej interakcji (pytań, potwierdzeń, otwierania przeglądarki),
   - kończy się sama po przetworzeniu wszystkich plików.
4. **Przetestujcie to dokładnie tak, jak zrobimy to my:** wrzućcie kilka przykładowych dokumentów do `input/`,
   wyczyśćcie `output/`, uruchomcie komendę skopiowaną z `RUN.md` i sprawdźcie wyniki. Najlepiej zróbcie to także
   po restarcie serwera (`sudo reboot`, odczekajcie 1–2 minuty).
5. **Jeśli komenda korzysta z usługi działającej w tle** (np. kontenera z modelem), ta usługa musi startować sama
   po restarcie serwera (`restart: unless-stopped` w Docker Compose albo `sudo systemctl enable <usługa>`)
   albo komenda musi ją uruchomić sama.
6. **Modele, obrazy Dockera i zależności pobierzcie wcześniej na serwer.** Nie zakładajcie, że w czasie oceny
   pobranie kilku GB się uda.
7. **Klucze API zewnętrznych usług** (np. do modeli w chmurze) umieśćcie w `/opt/solution/.env` i opiszcie w `RUN.md`,
   z których usług korzystacie. Nie wpisujcie ich na sztywno w kod w publicznym repozytorium.