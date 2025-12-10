# Praxisprojekt_04A_Buchhandlung_mit_Cafe

Ein API- und Datenbankprojekt für einen Buchladen mit Café.

## Projektbeschreibung

Dieses Projekt stellt eine RESTful API für einen Buchladen mit integriertem Café bereit. Es dient als Test- und Lernprojekt zur Entwicklung von APIs und Datenbankanwendungen.

## Technologien

- **Python**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**

## Projektstruktur

- `main.py`: Einstiegspunkt der Anwendung
- `auth.py`: Authentifizierungslogik
- `database.py`: Datenbankverbindung und -initialisierung
- `models/`: Datenbankmodelle
- `schemas/`: Pydantic-Schemas für Datenvalidierung
- `routers/`: API-Routen
- `sql/data/`: Beispieldaten
- `sql/data/secret`: Umgebungsvariablen, Token, Zertifikate
- `docker/`: Docker Script
- `sql/`: Shell Script für die Datenbankinitialisierung

## Installation und Ausführung

1. Repository klonen:
   ```bash
   git clone https://github.com/Pydatrick/Praxisprojekt_04A_Buchhandlung_mit_Cafe.git
   ```

2. Virtuelle Umgebung erstellen und aktivieren:
   ```bash
   python -m venv venv
   python venv\Scripts\activate
   ```

3. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```

4. Datenbank einrichten:

   - Im Ordner /sql/data/secret 
   - Umgebungsvariablen anpassen und in .env umbennenen
   - Token anpassen und in token.env umbenennen
   - Mit Docker : Im Ordner /docker/
   - ```bash
   docker-compose --env-file ../sql/data/secret/.env up -d
   ´´´ 

5. Anwendung starten:
   ```bash
   uvicorn main:app --reload
   ```

6. API-Dokumentation aufrufen:
   - Swagger UI: [http://localhost:58723/docs](http://localhost:58723/docs)
   - ReDoc: [http://localhost:58723/redoc](http://localhost:58723/redoc)

