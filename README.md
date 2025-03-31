# Schedule Project

Aplikacja CRUD służy do tworzenia dynamicznych harmonogramów pracy integralnych z dyspozycyjnością wysyłaną przez każdego z pracownków.



## Lista funkcjonalności

- **Zarządzanie pracownikami** (dodawanie, edytowanie, usuwanie, pobieranie danych)
- **Zarządzanie harmonogramem** (dodawanie, edytowanie, usuwanie)
- **Zarządzanie dyspozycyjnością** (dodawanie, edytowanie, usuwanie)
- **Filtrowanie według daty** (możliwość pobrania harmonogramu na dany dzień lub tydzień)
- **Filtracja według stanowiska** (pobieranie grafików według typu stanowiska)
- **Pobieranie statystyk



## Przebieg działania aplikacji

1. Pracownik zgłasza swoją dyspozycyjność
- **Pracownik określa swoją dostępność na przyszły tydzień.
- **Wybiera jeden z dostępnych przedziałów godzinowych dla każdego dnia (PRACA, OFF, Z1, Z2).
- **System zapisuje dyspozycyjność w bazie danych.

2. Kierownik pobiera dyspozycyjność pracowników
- **Kierownik ma dostęp do listy zgłoszonych dyspozycyjności.
- **Może sprawdzić, którzy pracownicy są dostępni w danym dniu i w jakich godzinach.

3. Kierownik układa harmonogram pracy
- **Kierownik przypisuje pracowników do zmian na podstawie ich dostępności.
- **System sprawdza, czy dany pracownik jest dostępny w wybranych godzinach:
    - ***Jeśli nie – zwraca błąd wraz z informacją o rzeczywistej dostępności.
    - ***Jeśli czas między kolejnymi zmianami wynosi poniżej 12h – system zwraca błąd o zbyt krótkim odstępie między zmianami.

4. Pracownik sprawdza swój harmonogram
- **Po zatwierdzeniu grafiku pracownik może podejrzeć swoje przydzielone zmiany.

5. Kierownik monitoruje pracę i analizuje statystyki
- **Liczba przepracowanych godzin, liczba godzin dyspozycyjności
- ** Filtrowanie według stanowiska/pracownika/zakresu dat



## Technologie

- Python 3.12.7 
- FastAPI
- PostgreSQL 17.0  
- Docker
