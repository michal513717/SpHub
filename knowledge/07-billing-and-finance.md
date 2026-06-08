# Rozliczenia i Finanse

## Proces fakturowania

### Cykl rozliczeniowy
1. **1. dzień miesiąca**: Automatyczne generowanie faktur za bieżący miesiąc
2. **Do 3. dnia**: Faktury wysyłane emailem (PDF) i dostępne w aplikacji
3. **Termin płatności**: 14 dni od wystawienia
4. **Przypomnienie**: automatyczny email 3 dni przed terminem
5. **Po terminie**: email + powiadomienie push w aplikacji

### Struktura faktury
- Abonament bazowy (hot desk / biuro / wirtualne)
- Dodatkowe usługi (parking, szafka, monitor, standing desk)
- Nadwyżki: drukowanie ponad limit, godziny sal konferencyjnych ponad limit
- Jednorazowe: wydanie karty, deep cleaning, opłata za event

### Metody płatności
- **Przelew bankowy**: SpaceHub Sp. z o.o., mBank, PL61 1140 2004 0000 3102 7456 8901
- **Karta kredytowa/debetowa**: przez Stripe (Visa, Mastercard, American Express)
- **Gotówka**: tylko w lokalizacjach z recepcją, do kwoty 5,000 PLN (limit ustawowy)
- **EUR**: akceptowane dla klientów zagranicznych, faktura w PLN, przeliczenie po kursie NBP z dnia wystawienia

### Windykacja

| Etap | Czas po terminie | Działanie |
|------|------------------|-----------|
| 1. Przypomnienie | +1 dzień | Email automatyczny |
| 2. Przypomnienie | +7 dni | Email + telefon od księgowości |
| 3. Wezwanie do zapłaty | +14 dni | Formalne wezwanie (email + list) |
| 4. Blokada dostępu | +21 dni | Dezaktywacja karty/kodu. Dostęp do biura dedykowanego zachowany (rzeczy osobiste). |
| 5. Wypowiedzenie umowy | +30 dni | Wypowiedzenie ze skutkiem natychmiastowym |
| 6. Windykacja zewnętrzna | +60 dni | Przekazanie do firmy windykacyjnej (Kruk S.A.) |

**WAŻNE**: Blokada dostępu (etap 4) NIE dotyczy biur dedykowanych — członek zachowuje dostęp do swojego biura, ale traci dostęp do przestrzeni wspólnych i sal konferencyjnych.

## Raporty finansowe

### Miesięczne KPI
- **MRR (Monthly Recurring Revenue)**: suma aktywnych abonamentów
- **ARR (Annual Recurring Revenue)**: MRR × 12
- **Churn rate**: % członków rezygnujących w danym miesiącu
- **Net Revenue Retention (NRR)**: uwzględnia upgrade/downgrade + churn
- **Average Revenue Per Member (ARPM)**: MRR / liczba aktywnych członków
- **Occupancy rate**: % zajętych biur dedykowanych
- **Hot desk utilization**: % zajętych hot desków (średnia dzienna)

### Aktualne wartości (marzec 2026)
- MRR: 487,000 PLN
- ARR: 5,844,000 PLN
- Churn rate: 4.2% (cel: <5%)
- NRR: 103% (netto wzrost — upgrade'y > churn)
- ARPM: 263 PLN
- Occupancy (biura): 94%
- Hot desk utilization: 67%

### Breakdown przychodów

| Źródło | Udział w MRR | Kwota/mies. |
|--------|-------------|-------------|
| Biura dedykowane | 62% | 301,940 PLN |
| Hot Desk (wszystkie plany) | 21% | 102,270 PLN |
| Wirtualne Biuro | 7% | 34,090 PLN |
| Sale konferencyjne (nadwyżki) | 4% | 19,480 PLN |
| Parking | 3% | 14,610 PLN |
| Pozostałe usługi | 2% | 9,740 PLN |
| Eventy | 1% | 4,870 PLN |

### Koszty operacyjne (miesięczne)

| Kategoria | Kwota/mies. | Udział |
|-----------|-------------|--------|
| Wynajem nieruchomości | 185,000 PLN | 42% |
| Wynagrodzenia (38 osób) | 142,000 PLN | 32% |
| Media (prąd, woda, gaz, internet) | 38,000 PLN | 9% |
| Sprzątanie (CleanPro) | 22,000 PLN | 5% |
| Marketing | 18,000 PLN | 4% |
| Utrzymanie i naprawy | 15,000 PLN | 3% |
| Ubezpieczenia | 8,000 PLN | 2% |
| Oprogramowanie (licencje) | 6,500 PLN | 1.5% |
| Pozostałe | 5,500 PLN | 1.5% |
| **SUMA** | **440,000 PLN** | **100%** |

**Marża operacyjna**: (487,000 - 440,000) / 487,000 = **9.7%**

### Sezonowość
- **Najlepsze miesiące**: wrzesień-listopad (powrót z wakacji, nowy rok akademicki)
- **Najgorsze miesiące**: lipiec-sierpień (spadek obłożenia hot desków o 25-30%)
- **Stabilne**: biura dedykowane — minimalna sezonowość (kontrakty roczne)

## Podatki i rachunkowość
- Biuro rachunkowe: Grantax Sp. z o.o.
- System księgowy: wFirma (integracja API ze SpaceHub App)
- Stawka VAT na usługi coworkingowe: 23%
- Stawka VAT na wirtualne biuro: 23%
- Stawka VAT na catering (eventy): 8%
- Rok obrotowy: styczeń-grudzień
- Audyt: brak obowiązku (przychód <50M PLN), ale planowany dobrowolny audyt w 2027
