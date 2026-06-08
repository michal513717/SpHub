# Utrzymanie i Zarządzanie Obiektem

## Zgłoszenia serwisowe

### Proces zgłaszania usterek

**Kanały zgłoszeń:**
1. Aplikacja SpaceHub App → "Zgłoś usterkę" (preferowany)
2. Recepcja (w godzinach pracy)
3. Email: maintenance@spacehub.pl
4. Telefon awaryjny (po godzinach): +48 12 345 67 88

**Kategorie zgłoszeń:**
- **Elektryka**: awaria oświetlenia, gniazdek, bezpieczników
- **Hydraulika**: zalanie, cieknący kran, zatkana toaleta
- **Klimatyzacja/Ogrzewanie**: zbyt zimno, zbyt gorąco, hałas z klimatyzacji
- **Meble**: zepsute krzesło, biurko, szafka
- **IT**: awaria WiFi, drukarki, monitora, systemu rezerwacji
- **Czystość**: prośba o dodatkowe sprzątanie, brudna kuchnia
- **Inne**: wszystko co nie pasuje do powyższych

### SLA czasów reakcji

| Priorytet | Czas reakcji | Czas rozwiązania | Przykłady |
|-----------|-------------|-------------------|-----------|
| Krytyczny | 30 min | 4h | Brak prądu, zalanie, awaria alarmu, brak internetu w całej lokalizacji |
| Wysoki | 2h | 24h | Klimatyzacja nie działa (temperatura >28°C lub <16°C), drukarka główna |
| Średni | 8h | 72h | Zepsute krzesło, oświetlenie w jednym pokoju |
| Niski | 24h | 5 dni roboczych | Kosmetyczne naprawy, wymiana żarówki w rzadko używanej sali |

**WAŻNE**: Czas reakcji = potwierdzenie przyjęcia zgłoszenia. Czas rozwiązania = usterka naprawiona lub tymczasowe obejście zapewnione.

### Eskalacja

Jeśli SLA nie jest dotrzymane:
1. **Automatyczny alert** do facility managera lokalizacji
2. **Po 2x przekroczeniu SLA** → alert do dyrektora operacyjnego
3. **Po 3x przekroczeniu SLA** → spotkanie z klientem, plan naprawczy

Członkowie mogą eskalować ręcznie:
- Przez aplikację: przycisk "Eskaluj" na zgłoszeniu
- Email do: operations@spacehub.pl

## Sprzątanie

### Harmonogram

| Strefa | Częstotliwość | Godziny |
|--------|---------------|---------|
| Open space | Codziennie | 6:00-7:30 (przed otwarciem) |
| Biura prywatne | 3x w tygodniu (pon, śr, pt) | 6:00-7:30 |
| Toalety | 3x dziennie | 8:00, 12:00, 16:00 |
| Kuchnia | 2x dziennie | 10:00, 15:00 |
| Sale konferencyjne | Po każdym spotkaniu (bufor 15 min) | Na bieżąco |
| Prysznice | Codziennie | 6:00-7:30 |
| Parking | 1x w tygodniu (sobota) | 6:00-8:00 |

**Firma sprzątająca**: CleanPro Sp. z o.o. (umowa do końca 2026, odnowienie automatyczne)

### Dodatkowe sprzątanie
- Przez aplikację: "Zamów sprzątanie" → czas realizacji: 2h w godzinach pracy
- Po eventach: wliczone w cenę wynajmu eventowego
- Deep cleaning biura: na żądanie, 200 PLN (do 10 m2), 350 PLN (10-30 m2)

## Infrastruktura techniczna

### Internet
- **Łącze główne**: Fiber 1 Gbps symetryczne (dostawca: Netia Business)
- **Łącze zapasowe**: Fiber 500 Mbps (dostawca: Orange)
- **Failover**: automatyczny, czas przełączenia <30 sekund
- **WiFi**: Ubiquiti UniFi, osobna sieć dla każdej lokalizacji
- **Gwarantowana prędkość per użytkownik**: 50 Mbps download / 50 Mbps upload
- **SLA dostępności**: 99.9% miesięcznie (max 43 min przestoju)

**Sieci WiFi:**
- `SpaceHub-Main` — główna sieć dla członków (hasło zmieniane co miesiąc, dostępne w aplikacji)
- `SpaceHub-Guest` — sieć gościnna (hasło na recepcji, limit: 10 Mbps, max 4h sesji)
- `SpaceHub-Event` — dedykowana sieć na eventy (konfiguracja na żądanie)

### Drukowanie
- **Drukarki**: HP LaserJet Enterprise (1 na lokalizację Standard/Budget, 2 na Premium)
- **Drukowanie mobilne**: przez aplikację lub email na print@spacehub.pl
- **Skanowanie**: bezpłatne, bez limitu
- **Formaty**: A4, A3 (tylko Premium)
- **Rozliczanie**: automatyczne, naliczane do miesięcznej faktury po przekroczeniu limitu

### Klimatyzacja i ogrzewanie
- **System**: VRF (Variable Refrigerant Flow) w lokalizacjach Premium i Standard
- **Sterowanie**: centralne, temperatura ustawiana przez facility managera
- **Zakres**: 20-24°C (biura), 18-22°C (open space)
- **Indywidualne sterowanie**: tylko biura dedykowane 6+ osób (termostat w biurze)
- **Zgłoszenia dotyczące temperatury**: przez aplikację, kategoria "Klimatyzacja/Ogrzewanie"

**Sezon grzewczy (październik-kwiecień):**
- Lokalizacje Nowa Huta i Prądnik: stare instalacje, czas nagrzewania do 2h rano
- Znany problem: w Prądniku biura od strony północnej mają o 2-3°C mniej niż południowe
