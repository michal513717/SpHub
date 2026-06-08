# Proces Onboardingu Nowego Członka

## Pipeline sprzedażowy

### Etap 1: Lead (pozyskanie zainteresowania)
Potencjalny klient kontaktuje się z SpaceHub lub zostawia dane.

**Źródła leadów:**
- **Strona www** (38%) — formularz kontaktowy, rezerwacja tour
- **Google Ads** (22%) — kampanie na frazy "coworking Kraków", "biuro do wynajęcia"
- **Polecenia** (18%) — istniejący członkowie polecają znajomych
- **Social media** (12%) — Instagram, LinkedIn, Facebook
- **Eventy** (6%) — targi pracy, meetupy tech, konferencje
- **Walk-in** (4%) — osoby wchodzące z ulicy

**Rejestracja leada:**
- Imię, nazwisko, email, telefon
- Źródło pozyskania
- Preferowany typ przestrzeni (hot desk / biuro / wirtualne)
- Wielkość zespołu
- Preferowana lokalizacja
- Budżet miesięczny
- Priorytet: niski / średni / wysoki / krytyczny

### Etap 2: Kwalifikacja
Konsultant kontaktuje leada w ciągu 24h (SLA).

**Checklist kwalifikacji:**
- [ ] Potwierdzenie potrzeb (typ, wielkość, lokalizacja)
- [ ] Sprawdzenie dostępności
- [ ] Weryfikacja budżetu
- [ ] Zaproponowanie planu
- [ ] Umówienie wizyty (tour)

**Statusy kwalifikacji:**
- `qualified` — potwierdzone zainteresowanie, umówiony tour
- `unqualified` — brak budżetu, niedopasowanie oferty
- `no_contact` — brak odpowiedzi po 3 próbach (telefon + email)
- `postponed` — zainteresowany, ale nie teraz (follow-up za X miesięcy)

### Etap 3: Tour (wizyta w lokalizacji)
Konsultant oprowadza potencjalnego klienta po lokalizacji.

**Tour obejmuje:**
- Prezentacja dostępnych przestrzeni
- Demo systemu rezerwacji sal
- Pokazanie udogodnień (kuchnia, prysznice, strefa relaksu)
- Omówienie warunków i cennika
- Próbny dzień pracy (opcjonalnie — 1 dzień gratis)

**Po tour:**
- `interested` — chce podpisać umowę
- `considering` — potrzebuje czasu, follow-up za 3-7 dni
- `declined` — nie zainteresowany (powód zapisywany)
- `competitor` — wybrał konkurencję (który? zapisywane)

**Najczęstsze powody odmowy:**
1. Za drogo (34%)
2. Za daleko od domu/biura (21%)
3. Brak wolnych biur w preferowanej wielkości (18%)
4. Wybrał konkurencję — Business Link (11%), Regus (8%), O4 (5%)
5. Zdecydował się na własne biuro (3%)

### Etap 4: Negocjacja i umowa
Ustalenie warunków i podpisanie umowy.

**Proces:**
1. Konsultant przygotowuje ofertę w systemie
2. Klient akceptuje lub negocjuje
3. Podpisanie umowy (elektronicznie przez Autenti lub fizycznie)
4. Wpłata kaucji (biura dedykowane)
5. Wystawienie pierwszej faktury

**Uprawnienia do rabatów:**
- Konsultant: do 10% rabatu bez akceptacji
- Team Leader: do 20% rabatu
- Dyrektor sprzedaży: powyżej 20% (wymaga uzasadnienia)

### Etap 5: Aktywacja
Nowy członek otrzymuje dostęp do przestrzeni.

**Checklist aktywacji:**
- [ ] Karta dostępu wydana (lub kod mobilny aktywowany)
- [ ] Konto w aplikacji SpaceHub App aktywowane
- [ ] WiFi: login i hasło przekazane
- [ ] Regulamin podpisany
- [ ] Tour po lokalizacji (jeśli nie był wcześniej)
- [ ] Przedstawienie community managerowi
- [ ] Biuro przygotowane (dedykowane): meble, klucze, tabliczka z nazwą firmy
- [ ] Dodanie do kanału Slack lokalizacji

**Czas aktywacji:**
- Hot Desk: ten sam dzień
- Biuro Dedykowane: 1-3 dni robocze (przygotowanie biura)
- Wirtualne Biuro: 1 dzień roboczy

### Etap 6: Okres próbny
Przez pierwsze 14 dni nowy członek może zrezygnować bez konsekwencji.

**Warunki:**
- Dotyczy tylko umów miesięcznych
- Zwrot 100% opłaty za pierwszy miesiąc
- Kaucja zwracana w ciągu 7 dni
- Karta dostępu do zwrotu

**Statystyki rezygnacji w okresie próbnym:**
- Hot Desk: 8% rezygnacji
- Biuro Dedykowane: 3% rezygnacji
- Wirtualne Biuro: 12% rezygnacji
