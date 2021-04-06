# Krótki opis aplikacji 'Planthood'

Aplikacja, która umożliwia wymianę roślin między użytkownikami w bliskiej
okolicy. Dodatkowo aplikacja ma przypominać użytkownikowi mailem o 
zaplanowanej pielęgnacji posiadanych przez niego roślin. Aplikacja gromadzi też statystyki wymian z
ostatnich dni/tygodni/miesięcy.

# Wymagania

## Wymiana

Aplikacja powinna umożliwić:

* tworzenie wymian
* modyfikowanie wymian
* przegląd wymian

CRUD dla modelu Wymiana

Wymiana (Transaction):

* nazwa (name)
* opis (description)
* zdjęcie (image) // lub roślina (plant, FK Plant)  
* status (status)
* użytkownik (creator, FK User)

## Kwiaty

Aplikacja powinna umożliwić:

* tworzenie rośliny
* modyfikowanie kwiatów
* przegląd kwiatów

CRUD dla modelu Roślina

Roślina (Plant):

* nazwa (name)
* zdjęcie (image) ** opcjonalne  
* opis (description) ** opcjonalne
* ziemia (ground) ** opcjonalne
* podlewanie (water) ** opcjonalne
* właściciel (owner, FK User)

## Wiadomości

Aplikacja powinna umożliwiać:

* wysłanie (tworzenie) wiadomości

Wiadomość (Message):

* nadawca (sender, FK User)
* odbiorca (receiver, FK User)
* wymiana (transaction, FK Transaction)  
* data utworzenia (created_at)

## Użytkownik

Aplikacja powinna umożliwiać:

* utworzenie konta użytkownika
* modyfikację konta użytkownika
* przegląd konta użytkownika

CRUD do modelu Użytkownik

Użytkownik (User):

* imię (first_name)
* nazwisko (last_name)
* email (email)
* ulica (street)

## Przypomnienie

Aplikacja powinna umożliwiać:

* utworzenie przypomnienia
* modyfikowanie przypomnienia
* usunięcie przypomnienia
* przegląd przypomnień

CRUD do modelu Przypomnienie

Przypomnienie (Reminder):

* typ (type, choice)
* roślina (plan, FK Plant)
* dzień ostatniej pielęgnacji (last_completed)
* cykl (cycle)

## Statystyki

???

## TBD

* logowanie, autoryzacja
* obsługa powiadomień
* obsługa wysyłania wiadomości między użytkownikami
* obliczanie odległości między użytkownikami
