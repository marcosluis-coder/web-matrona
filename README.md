# Web Matrona

Aplicació web desenvolupada amb Flask orientada a la gestió de cites i serveis per a comares i pacients.

## Descripció

Aquest projecte permet gestionar cites mèdiques de manera senzilla i intuïtiva, diferenciant entre dos tipus d’usuaris: comare i pacient.

Les pacients poden registrar-se, reservar cites i consultar les seves cites programades.  
La comare pot gestionar totes les cites, confirmar-les, cancel·lar-les i visualitzar estadístiques mitjançant un dashboard interactiu.

A més, l’aplicació incorpora eines útils relacionades amb l’embaràs i el cicle menstrual.

---

# Funcionalitats principals

## Gestió d’usuaris
- Registre d’usuaris
- Inici i tancament de sessió
- Diferenciació de rols:
  - Pacient
  - Comare

---

## Gestió de cites
- Reserva de cites online
- Validació d’hores disponibles
- Restricció de cites en:
  - dates passades
  - caps de setmana
  - hores ocupades
- Visualització de cites personals
- Cancel·lació de cites

---

## Gestió per la comare
- Visualització de totes les cites
- Confirmació i cancel·lació de cites
- Dashboard amb estadístiques
- Gràfics interactius amb Chart.js

---

## Calculadores
- Càlcul de data probable de part
- Càlcul de propera regla

---

# Tecnologies utilitzades

## Backend
- Python
- Flask
- SQLAlchemy
- Flask-Login

## Frontend
- HTML
- CSS
- Bootstrap
- Chart.js

## Base de dades
- SQLite

## Altres eines
- Git
- GitHub
- Render (desplegament cloud)

---

# Instal·lació local

## 1. Clonar repositori

git clone https://github.com/marcosluis-coder/web-matrona.git

## 2. Entrar al projecte

cd web-matrona

## 3. Crear entorn virtual

python -m venv venv

## 4. Activar entorn virtual

Windows:
venv\Scripts\activate

Linux / Mac:
source venv/bin/activate

## 5. Instal·lar dependències

pip install -r requirements.txt

## 6. Executar aplicació

python run.py

## Desplegament

Aplicació desplegada a Render:

👉 https://web-matrona.onrender.com/

## Estructura del projecte

- web_matrona/ requirements.txt, config.py, run.py, Procfile,app/==
- ==> app/ __init__.py, models.py, routes.py, templates/

## Possibles millores futures

- Calendari visual interactiu
- Notificacions automàtiques
- Sistema de missatgeria
- Seguiment complet de l’embaràs
- Personalització del cicle menstrual
- Migració a MySQL/PostgreSQL

## Autor
- Marcos Luis 
- CIFP Pau Casesnoves
- Projecte Intermodular, Desplegament d'aplicacions Web