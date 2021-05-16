# Krótki opis aplikacji 'Planthood'

Aplikacja, która umożliwia wymianę roślin między użytkownikami w bliskiej
okolicy. Dodatkowo aplikacja ma przypominać użytkownikowi mailem o zaplanowanej
pielęgnacji posiadanych przez niego roślin. Aplikacja gromadzi też statystyki
wymian z ostatnich dni/tygodni/miesięcy.

Zbudowana przy wykorzystaniu: Python 3.9, Django 3.0.14, Bootstrap4,
PostgreSQL/PostGIS, DRF 3.11.2, APScheduler 3.7.0

# Wymagania

## Wymiana

Aplikacja powinna umożliwić:

MUST HAVE

* tworzenie wymian
* przegląd wymian

COULD HAVE

* usuwanie wymian

Wymiana (Transaction):

* roślina (plant)
* od użytkownika (from_user)
* do użytkownika (to_user)
* ukończona (finished)
* wiadomość (message)

## Kwiaty

Aplikacja powinna umożliwić:

MUST HAVE

* tworzenie rośliny
* modyfikowanie rośliny
* przegląd roślin

COULD HAVE

* usuwanie roślin

Roślina (Plant):

* nazwa (name)
* zdjęcie (photo) ** opcjonalne
* opis (description)
* data dodania (added)
* właściciel (owner)

## Wiadomości

Aplikacja powinna umożliwiać:

MUST HAVE

* wysłanie (tworzenie) wiadomości

WON'T HAVE

* usunięcie wiadomości

Wiadomość (Message):

* nadawca (sender)
* odbiorca (recipient)
* roślina (plant)
* data utworzenia (created_at)
* treść (content)


## Użytkownik

Aplikacja powinna umożliwiać:

MUST HAVE

* utworzenie konta użytkownika
* modyfikację konta użytkownika
* przegląd konta użytkownika

WON'T HAVE

* usunięcie użytkownika

Użytkownik (User):

* imię (first_name)
* nazwisko (last_name)
* email (email)
* ulica (street)
* numer budynku (building number)


## Przypomnienie

Aplikacja powinna umożliwiać:

MUST HAVE

* utworzenie przypomnienia
* modyfikowanie przypomnienia
* przegląd przypomnień

SHOULD HAVE

* usunięcie przypomnienia

Przypomnienie (Reminder):

* typ (care_type choice)
* roślina (plan, FK Plant)
* dzień ostatniej pielęgnacji (previous_care_day)
* cykl (cycle)
* dzień kolejnej pielęgnacji (next_care_day)

## Statystyki

System umożliwia generowanie agregatów transakcji oraz roślin:

* dziennie
* tygodniowo

SHOULD HAVE

* dodane transakcje i rośliny

COULD HAVE

* zakończone transakcje

## TBD

* RestAPI
