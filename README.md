Opgave 4

Det første du skal gøre, er at installere venv (virtuel environment).

Kør følgende kommando i terminalen – husk at være i din Opgave 4-mappe (eller hvad du har kaldt den):

python -m venv .venv

Når venv er oprettet, kør derefter denne kommando for at installere de nødvendige pakker:

pip install -r requirements.txt

Efter at pakkerne er installeret, kan du starte projektet ved at køre:

cd src
python start.py

Dette projekt opsætter en **MySQL-database** med tre relaterede tabeller: `customers`, `products` og `orders`. Scriptet gør automatisk følgende:

- Opretter databasen `ugedata`
- Opretter tabeller med fremmednøgler
- Indlæser data fra CSV-filer
- Indsætter data i databasen
- Sletter databasen til sidst (valgfrit)