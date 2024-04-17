# AccFuse: Platforma integrująca dane wszystkich kont bankowych w jednym miejscu generując raporty, a także zapewniając bezpieczeństwo danych.

## Idea

Głównym założeniem projektu jest stworzenie aplikacji webowej, która za pomocą API wielu banków będzie pozwalała
użytkownikowi na łączenie swoich danych finansowych z różnych banków, a także będzie dawała możliwość generowania
raportów finansowych według wybranych przez użytkownika filtrów.

## Teoretyczna realizacja (perspektywa użytkownika)

Strona umożliwi użytkownikowi zalogowanie się lub utworzenie konta za pomocą danych logowania albo autoryzacji przez google.

Po zalogowaniu użytkownik będzie miał możliwość dodania swoich kont bankowych należących do uwzględnionych banków.

Po dodaniu kont bankowych użytkownik będzie miał dostęp do historii transakcji każdego ze swoich kont, a także będzie miał możliwość zaaplikowania na nie filtrów, takich jak:

- Wybór kont z których wyświetlane będą dane
- Wybór rodzaju transakcji uznania/obciążenia
- Kwoty większe/mniejsze niż
- Zakres czasu
- itp

Poza tym użytkownik będzie miał możliwość generowania raportów swoich wydatków, np z podsumowaniem swoich przychodów i wydatków

## Teoretyczna realizacja (perspektywa serwera)

Po zalogowaniu dane użytkownika zostaną zapisane w zabezpieczonej bazie danych, a aktualna sesja będzie nadzorowana za pomocą tokena JWT.

Po wyborze kont bankowych użytkownik zostanie przekierowany na strony banku w celu autoryzacji, w przypadku sukcesu dane zostaną przekazane na serwer w celu ułatwienia dostępu do nich kiedy tokeny dostępu do kont bankowych już wygasną (przy ikonie statusu dla każdego banku będzie informacja o tym czy dane są aktualne)

Filtry będą wykonywać zapytania na bazie danych wybierając tylko interesujące rekordy.

Raporty, będą generowane za pomocą skryptu w serwerze, który będzie przetwarzał dane w odpowiedni sposób, a następnie przekazywał je do użytkownika w czytelnym formacie, np pdf.
