# Zadanie 3

Celem zadania jest skonstruowanie prymitywnego mechanizmu autokorekty w wybranym przez siebie języku programowania (preferowanie Python). Rozwiązaniem powininen być skrypt, który na wejściu przyjmuje zmienną **word** typu string będącą słowem, które chcemy sprawdzić i **k** będące liczbą proponowanych wyrazów, które wskaże mechanizm autokorekty. Na wyjściu powinniśmy dostać **k** wyrazów, które wskazała autokorekta.

### Przykład

#### wejście

granot 2

#### wyjście

[granit, granat]

wykonanie poniższej komendy, powinno zwrócić wynik jak wyżej

```
$ zadanie3.py granot 2
```

# Jak rozwiązać zadanie
- Wczytaj zmienne z linii komend
- Wczytaj zbiór wyrazów w języku polskim. W internecie dostępne są słowniki, które takie zbiory zawierają. Należy samemu znaleźć jak je wczytać i z nich korzystać.
- Posortuj zbiór wyrazów według wybranej odległości między **word**, a każdym słowem ze zbioru (*Podpowiedź* poczytaj czym jest odległość Levenshteina)
- Zwróć **k** pierwszych elementów z posortowanego zbioru

