# Krótki opis aplikacji 'Planthood'

Aplikacja, która umożliwia wymianę roślin między użytkownikami w bliskiej
okolicy. Dodatkowo aplikacja ma przypominać użytkownikowi mailem o zaplanowanej
pielęgnacji posiadanych przez niego roślin. Aplikacja gromadzi też statystyki
wymian z ostatnich dni/tygodni/miesięcy.

# Wymagania

## Wymiana

Aplikacja powinna umożliwić:

MUST HAVE

* tworzenie wymian
* modyfikowanie wymian
* przegląd wymian

COULD HAVE

* usuwanie wymian

Wymiana (Transaction):

* nazwa (name)
* opis (description)
* zdjęcie (image) // lub roślina (plant, FK Plant)
* status (status)
* użytkownik (creator, FK User)

## Kwiaty

Aplikacja powinna umożliwić:

MUST HAVE

* tworzenie rośliny
* modyfikowanie kwiatów
* przegląd kwiatów

COULD HAVE

* usuwanie roślin

Roślina (Plant):

* nazwa (name)
* zdjęcie (image) ** opcjonalne
* opis (description) ** opcjonalne
* ziemia (ground) ** opcjonalne
* podlewanie (water) ** opcjonalne
* właściciel (owner, FK User)

## Wiadomości

Aplikacja powinna umożliwiać:

MUST HAVE

* wysłanie (tworzenie) wiadomości

WON'T HAVE

* usunięcie wiadomości

Wiadomość (Message):

* nadawca (sender, FK User)
* odbiorca (receiver, FK User)
* wymiana (transaction, FK Transaction)
* data utworzenia (created_at)


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


## Przypomnienie

Aplikacja powinna umożliwiać:

MUST HAVE

* utworzenie przypomnienia
* modyfikowanie przypomnienia
* przegląd przypomnień

SHOULD HAVE

* usunięcie przypomnienia

Przypomnienie (Reminder):

* typ (type, choice)
* roślina (plan, FK Plant)
* dzień ostatniej pielęgnacji (last_completed)
* cykl (cycle)

## Statystyki

System umożliwia generowanie agregatów transakcji oraz roślin:

* dziennie
* tygodniowo

SHOULD HAVE

* dodane transakcje i rośliny

COULD HAVE

* zakończone transakcje

## TBD

* logowanie, autoryzacja
* obsługa powiadomień
* obsługa wysyłania wiadomości między użytkownikami
* obliczanie odległości między użytkownikami
