# DFIR Programuppdaterare

En Python GUI-applikation för att uppdatera programvara på offline Windows-arbetsstationer. Detta verktyg använder CustomTkinter för gränssnittet och PowerShell för att köra installationsprogram tyst.

## Funktioner

- Modern mörkt tema GUI med CustomTkinter
- Visar program med installationsstatus och versionsinformation
- Uppdaterar programvara med PowerShell-kommandon
- Förloppsindikator för uppdateringar
- Detaljerad loggning av uppdateringsaktiviteter
- Stöd för tyst installation
- Extern konfigurationsfil för enkel anpassning

## Krav

- Windows OS
- Python 3.7 eller högre (för att köra från källkod)
- CustomTkinter-bibliotek

## Katalogstruktur

```
DFIR_Updater/
├── assets/                 # Ikoner och andra resurser
├── dist/                   # Paketerade exekverbara filer (skapas under bygget)
├── build/                  # Byggartefakter (skapas under bygget)
├── src/                    # Källkod
├── scripts/                # Verktygsskript
├── programs.json           # Konfigurationsfil
├── programs_template.json  # Konfigurationsmall
├── requirements.txt        # Python-beroenden
├── README.md               # Denna fil
├── build.bat               # Byggskript
├── run_updater.bat         # Körskript för källversionen
├── run_packaged.bat        # Körskript för paketerad version
├── setup.bat               # Installationskript
└── config_helper.bat       # Konfigurationshjälpskript
```

## Installation

1. Installera Python från https://www.python.org/downloads/
2. Installera nödvändiga beroenden:
   ```
   pip install -r requirements.txt
   ```
   Eller kör `setup.bat` som gör detta automatiskt.

## Konfiguration

Programvaror konfigureras i filen `programs.json`. Redigera denna fil för att lägga till, ta bort eller ändra program:

```json
[
    {
        "name": "Programnamn",
        "install_path": "C:\\Program Files\\Program",
        "installer_path": "C:\\Installers\\program-installer.exe",
        "silent_args": "/S",
        "version_check": {
            "type": "exe_version",
            "path": "C:\\Program Files\\Program\\program.exe"
        },
        "new_version": "1.2.3"
    }
]
```

### Konfigurationsfält
- `name`: Visningsnamn för programvaran
- `install_path`: Sökväg där programvaran är installerad (används för att kontrollera om den redan är installerad)
- `installer_path`: Fullständig sökväg till installationsprogrammets exekverbara fil eller arkiv
- `silent_args`: Argument för tyst/obemannad installation
- `version_check`: Konfiguration för att kontrollera den aktuella versionen (se nedan)
- `new_version`: Den version som finns tillgänglig för uppdatering

### Versionskontroll
Objektet `version_check` stödjer flera metoder för att kontrollera den aktuella versionen:

1. **Exekverbar filversion**:
   ```json
   "version_check": {
       "type": "exe_version",
       "path": "C:\\Sökväg\\Till\\Exekverbar.exe"
   }
   ```

2. **Kommandoutdata**:
   ```json
   "version_check": {
       "type": "cmd_output",
       "command": "C:\\Sökväg\\Till\\exekverbar.exe --version",
       "regex": "Version ([0-9.]+)"
   }
   ```

3. **Filinnehåll**:
   ```json
   "version_check": {
       "type": "file_content",
       "path": "C:\\Sökväg\\Till\\version.txt",
       "regex": "([0-9.]+)"
   }
   ```

4. **Ingen versionskontroll**:
   ```json
   "version_check": {
       "type": "none"
   }
   ```

Om `programs.json` inte finns kommer applikationen att skapa den från `programs_template.json` vid första körningen.

### Resurskatalog

Katalogen `assets` innehåller ikoner och andra resurser för applikationen. För att använda en anpassad ikon:
1. Skapa en .ico-fil (rekommenderad storlek: 256x256 pixlar)
2. Placera den i katalogen `assets` som `icon.ico`

## Användning

### Köra från källkod

1. Se till att installationsprogram finns tillgängliga på de angivna sökvägarna
2. Kör applikationen med någon av dessa metoder:
   - Dubbelklicka på `run_updater.bat`
   - Kör från kommandoraden:
     ```
     python src/main.py
     ```

### Köra paketerad version

1. Kör `build.bat` för att skapa den exekverbara filen
2. Kör applikationen med någon av dessa metoder:
   - Dubbelklicka på `run_packaged.bat`
   - Navigera till `dist/DFIR_Software_Updater` och kör `DFIR_Software_Updater.exe`

## Paketering som exekverbar fil

För att paketera applikationen som en fristående exekverbar fil:

1. Kör `build.bat` för att skapa den exekverbara filen
2. Den exekverbara filen kommer att skapas i katalogen `dist/DFIR_Software_Updater`
3. Kör `run_packaged.bat` för att starta den paketerade applikationen

### Byggkrav

- Python 3.7 eller högre
- PyInstaller
- Pillow (för ikonhantering)

Dessa beroenden kommer att installeras automatiskt när du kör `build.bat`.

### Distribution

För att distribuera applikationen, kopiera hela katalogen `dist/DFIR_Software_Updater` till målsystemet. Katalogen innehåller:
- `DFIR_Software_Updater.exe` - Den huvudsakliga exekverbara filen
- `programs.json` - Konfigurationsfil (kan ändras efter paketering)
- `programs_template.json` - Mall för att skapa nya konfigurationer
- `assets/` - Ikon- och andra resursfiler

### Skapa en enskild exekverbar fil

För att skapa en enskild exekverbar fil istället för en katalog, använd alternativet `--onefile`:
```
pyinstaller --noconfirm --onefile --windowed --hidden-import=customtkinter --add-data "programs.json;." --add-data "programs_template.json;." --add-data "assets;assets" --icon "assets/icon.ico" --name "DFIR_Software_Updater" src/main.py
```

Obs: Enskilda exekverbara filer startar långsammare eftersom de behöver extrahera filer till en temporär katalog vid varje körning. När du använder alternativet för enskild fil kommer filen `programs.json` att skapas i samma katalog som den exekverbara filen när applikationen körs för första gången.

## Argument för tyst installation

Vanliga argument för tyst installation:
- `/S` - Tyst installation (NSIS-installationsprogram)
- `/quiet` - Tyst installation (MSI-installationsprogram)
- `/silent` - Tyst installation (Inno Setup)
- `/qn` - Inget användargränssnitt (Windows Installer)

## Hur det fungerar

1. Applikationen kontrollerar om programvaran är installerad genom att verifiera att installationskatalogen finns
2. När du klickar på "Uppdatera" kör den PowerShell för att exekvera installationsprogrammet med tysta argument
3. PowerShell väntar på att installationen ska slutföras innan den fortsätter
4. Förlopp och status uppdateras i GUI:t

## Felsökning

- Se till att sökvägarna till installationsprogrammen är korrekta och att filerna finns
- Kontrollera argumenten för tyst installation för varje installationstyp
- Granska loggutdata för felmeddelanden
- Vissa installationsprogram kan kräva administratörsbehörighet