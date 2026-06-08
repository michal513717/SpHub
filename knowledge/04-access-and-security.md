# System Dostępu i Bezpieczeństwo

## Kontrola dostępu

### Karty i kody dostępu
Każdy członek otrzymuje kartę RFID lub kod mobilny w aplikacji SpaceHub App.

**Typy dostępu:**
- **Karta RFID**: Fizyczna karta, działa przy czytniku na drzwiach. Koszt wydania: 20 PLN (jednorazowo). Koszt wymiany przy zgubieniu: 50 PLN.
- **Kod mobilny**: QR kod w aplikacji, skanowany przy wejściu. Bezpłatny, wymaga smartfona z Bluetooth LE.
- **Kod PIN**: Awaryjny dostęp numeryczny. Wydawany tylko na żądanie, zmiana co 90 dni.

### Strefy dostępu

| Strefa | Hot Desk Basic | Hot Desk Flex/Global | Biuro Dedykowane | Wirtualne Biuro |
|--------|---------------|---------------------|------------------|-----------------|
| Recepcja | Tak | Tak | Tak | Tak (w godzinach pracy) |
| Open space | Tak (8-18) | Tak (24/7) | Tak (24/7) | Nie |
| Kuchnia | Tak | Tak | Tak | Nie |
| Sale konferencyjne | Rezerwacja | Rezerwacja | Rezerwacja | Rezerwacja (Virtual Plus+) |
| Biura prywatne | Nie | Nie | Tylko swoje | Nie |
| Prysznice | Nie | Tak | Tak | Nie |
| Strefa relaksu | Tak | Tak | Tak | Nie |
| Parking | Osobny abonament | Osobny abonament | Osobny abonament | Nie |
| Serwerownia | Nie | Nie | Na żądanie (IT admin) | Nie |

### Godziny dostępu
- **Lokalizacje Premium**: 24/7 dla Flex/Global/Biuro
- **Lokalizacje Standard**: 6:00-23:00 (Flex/Global/Biuro), 8:00-18:00 (Basic)
- **Lokalizacje Budget**: 7:00-22:00 (Flex/Global/Biuro), 8:00-18:00 (Basic)
- **Lokalizacja Boutique**: 7:00-21:00 dla wszystkich (budynek zabytkowy — regulamin wspólnoty)

## Bezpieczeństwo

### Monitoring
- Kamery CCTV we wszystkich przestrzeniach wspólnych (open space, korytarze, recepcja, parking)
- **Brak kamer** w biurach prywatnych, toaletach, prysznicach
- Nagrania przechowywane 30 dni (RODO)
- Dostęp do nagrań: tylko management + policja (na wniosek)

### System alarmowy
- Alarm włączany automatycznie po zamknięciu lokalizacji (lub po 23:00 w Standard)
- Czujniki ruchu w strefach zamkniętych
- Czujniki dymu i CO2 we wszystkich pomieszczeniach
- Monitoring 24/7 przez firmę ochroniarską SecureNet

### Procedura zgubienia karty
1. Członek zgłasza zgubienie przez aplikację lub na recepcji
2. Stara karta jest natychmiast dezaktywowana
3. Nowa karta wydawana w ciągu 1 dnia roboczego (koszt: 50 PLN)
4. Tymczasowy dostęp przez kod PIN (ważny 48h)

### Procedura ewakuacji
1. Alarm pożarowy → automatyczne odblokowanie wszystkich drzwi
2. Community manager kieruje ewakuację do punktu zbiórki
3. Sprawdzenie listy obecności (system dostępu = kto jest w budynku)
4. Kontakt z służbami: 112
5. Punkty zbiórki oznaczone zielonymi tablicami przy wejściu

### Zgłaszanie incydentów bezpieczeństwa
- Przez aplikację: sekcja "Zgłoś problem" → kategoria "Bezpieczeństwo"
- Na recepcji (godziny pracy)
- Email: security@spacehub.pl
- Telefon alarmowy (po godzinach): +48 12 345 67 99

**Kategorie incydentów:**
- Kradzież lub próba kradzieży
- Uszkodzenie mienia
- Nieautoryzowany dostęp
- Pożar / zalanie / awaria
- Zachowanie zagrażające bezpieczeństwu
- Inne

**SLA rozpatrywania:**
- Krytyczne (kradzież, pożar): natychmiast
- Wysokie (uszkodzenie mienia): 4h
- Średnie (nieautoryzowany dostęp): 24h
- Niskie (inne): 72h
