# Systemy IT i Integracje

## SpaceHub App

### Architektura
- **Frontend**: React Native (iOS + Android)
- **Backend**: Node.js + Express, baza PostgreSQL
- **Hosting**: AWS (eu-central-1, Frankfurt)
- **CDN**: CloudFront
- **Auth**: Auth0 (SSO dla firm)

### Funkcje aplikacji
| Funkcja | Opis | Dostępność |
|---------|------|-----------|
| Dashboard | Podsumowanie: abonament, godziny sal, faktury | Wszyscy |
| Rezerwacja sal | Kalendarz sal, rezerwacja, anulowanie | Wszyscy (z limitem) |
| Rezerwacja hot desku | Wybór lokalizacji i biurka na dany dzień | Hot Desk Flex/Global |
| WiFi | Aktualne hasło do WiFi | Wszyscy |
| Faktury | Przeglądanie i pobieranie faktur PDF | Wszyscy |
| Zgłoszenia | Usterki, prośby, bezpieczeństwo | Wszyscy |
| Kod dostępu | QR kod mobilny do skanowania | Wszyscy |
| Perki | Kody rabatowe od partnerów | Wszyscy |
| Profil | Dane osobowe, firma, preferencje | Wszyscy |
| Zespół | Zarządzanie członkami zespołu | Admin biura ded. |
| Statystyki | Wykorzystanie sal, hot desków, koszty | Admin biura ded. |

### Wersje i aktualizacje
- Obecna wersja: 3.2.1 (wydana 2026-02-15)
- Cykl wydawniczy: co 2-4 tygodnie
- Auto-update: tak (App Store / Google Play)
- Minimalna wersja iOS: 15.0
- Minimalna wersja Android: 10.0

### Znane problemy (v3.2.1)
- Powiadomienia push czasami nie dochodzą na Androidzie 14 (fix w v3.3)
- Rezerwacja hot desku: nie odświeża się automatycznie po anulowaniu (workaround: pull-to-refresh)
- Ciemny motyw: nieprawidłowe kolory w sekcji "Faktury" (fix w v3.3)

## System kontroli dostępu

### Keri Systems NXT
- **Czytniki**: Keri NXT reader przy każdych drzwiach wejściowych + biurach dedykowanych
- **Karty**: Keri RFID 13.56 MHz (MIFARE DESFire EV2)
- **Integracja**: API → SpaceHub App (kod mobilny generuje wirtualną kartę BLE)
- **Backup**: Kod PIN na klawiaturze przy głównym wejściu

### Zarządzanie dostępem
- Nowy członek → FM lub recepcja tworzy profil w Keri → przypisuje strefy → wydaje kartę
- Zmiana planu → automatyczna aktualizacja stref (via webhook SpaceHub App → Keri API)
- Koniec umowy → automatyczna dezaktywacja karty (via webhook)
- Zgubiona karta → natychmiastowa dezaktywacja przez recepcję lub FM

### Logi dostępu
- Każde skanowanie karty/kodu zapisywane: data, godzina, lokalizacja, strefa, członek
- Logi przechowywane 12 miesięcy
- Dostęp do logów: FM + COO + IT
- Na żądanie: członek może poprosić o swoje logi (RODO)
- Wykorzystanie: monitorowanie obłożenia, bezpieczeństwo, rozliczanie hot desków

## CRM — HubSpot

### Pipeline sprzedażowy
Etapy: Lead → Kwalifikacja → Tour → Negocjacja → Umowa → Aktywacja

**Automatyzacje:**
- Nowy lead z formularza www → automatycznie do HubSpot → przypisanie do konsultanta (round-robin)
- Lead bez kontaktu >3 dni → automatyczny reminder do konsultanta
- Tour zrealizowany → automatyczny email follow-up (po 24h)
- Umowa podpisana → trigger do SpaceHub App (tworzenie konta członka)

### Raporty HubSpot
- Leady/miesiąc per źródło
- Konwersja per etap
- Czas w pipeline per etap
- Revenue per konsultant
- Lost reasons breakdown

## Integracje

### SpaceHub App ↔ Keri Systems
- Webhook: tworzenie/usuwanie/modyfikacja dostępu
- Kierunek: SpaceHub App → Keri API
- Częstotliwość: real-time (event-driven)

### SpaceHub App ↔ HubSpot
- Webhook: nowy członek → update deal status
- API: sync danych kontaktowych
- Kierunek: dwukierunkowy
- Częstotliwość: real-time

### SpaceHub App ↔ Stripe
- API: tworzenie subskrypcji, fakturowanie, płatności
- Webhook: potwierdzenie płatności → aktualizacja statusu w App
- Kierunek: dwukierunkowy

### SpaceHub App ↔ wFirma
- API: generowanie faktur VAT, korekty
- Kierunek: SpaceHub App → wFirma
- Częstotliwość: batch (1. dzień miesiąca)

### SpaceHub App ↔ Mailchimp
- API: sync listy członków (email, imię, lokalizacja, plan)
- Kierunek: SpaceHub App → Mailchimp
- Częstotliwość: codzienny sync (3:00 AM)

### SpaceHub App ↔ Slack
- Bot: powiadomienia o nowych członkach, eventach, awariach
- Kierunek: SpaceHub App → Slack
- Kanały: #general, #lokalizacja-specific
