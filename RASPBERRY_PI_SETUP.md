# Raspberry Pi Einrichtungsanleitung für Memegen Bot

Diese Anleitung erklärt, wie du den Meme-Generator-Bot dauerhaft auf deinem Raspberry Pi einrichtest und im Hintergrund laufen lässt.

## 1. Dateien auf den Raspberry Pi übertragen

Kopiere die Projektdateien per `scp` auf den Pi:

```bash
# Auf deinem Mac im Ordner TelegramBots ausführen
scp -r memegen pi@raspberrypi.local:/home/pi/memegen
```
*(Pfade und IP/Hostname ggf. anpassen)*

## 2. Einrichtung auf dem Raspberry Pi

SSH-Verbindung herstellen:
```bash
ssh pi@raspberrypi.local
cd memegen
```

### Python & Virtuelle Umgebung

```bash
# 1. Virtuelle Umgebung erstellen
python3 -m venv venv

# 2. Aktivieren
source venv/bin/activate

# 3. Abhängigkeiten installieren (kann bei moviepy/numpy einen Moment dauern)
pip install -r requirements.txt

# 4. Systempakete installieren (WICHTIG für Bild- und Videobearbeitung)
sudo apt update
sudo apt install imagemagick ffmpeg
```

### 3. ImageMagick Security Policy anpassen (SEHR WICHTIG!)

ImageMagick blockiert standardmäßig die Texterstellung für Videos. Du musst dies erlauben:

1. Öffne die Policy-Datei:
   ```bash
   sudo nano /etc/ImageMagick-6/policy.xml
   ```
   *(Falls nicht vorhanden, versuche `/etc/ImageMagick-7/policy.xml` oder `/etc/ImageMagick/policy.xml`)*

2. Suche ganz unten die Zeile:
   ```xml
   <policy domain="path" rights="none" pattern="@*" />
   ```

3. Kommentiere sie aus (mit `<!--` und `-->` umschließen):
   ```xml
   <!-- <policy domain="path" rights="none" pattern="@*" /> -->
   ```

4. Speichern: `Ctrl+O`, `Enter`, `Ctrl+X`.

### 4. Token eintragen
Erstelle oder bearbeite die `.env` Datei und trage deinen echten Bot-Token ein:
```bash
nano .env
```
Füge ein:
```ini
TELEGRAM_BOT_TOKEN=dein_bot_token_hier
```
Speichern: `Ctrl+O`, `Enter`, `Ctrl+X`.

## 5. Dauerhafter Betrieb (Systemd Service)

Wir nutzen Systemd, damit der Bot im Hintergrund läuft und bei Neustarts automatisch startet.

1. Erstelle eine Service-Datei `/etc/systemd/system/memegen.service`:
   ```bash
   sudo nano /etc/systemd/system/memegen.service
   ```

2. Füge folgenden Inhalt ein (Pfade ggf. anpassen):
   ```ini
   [Unit]
   Description=Telegram Memegen Bot Service
   After=network.target

   [Service]
   Type=simple
   User=pi
   WorkingDirectory=/home/pi/memegen
   ExecStart=/home/pi/memegen/venv/bin/python bot.py
   Restart=on-failure

   [Install]
   WantedBy=multi-user.target
   ```

3. Service aktivieren und starten:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable memegen
   sudo systemctl start memegen
   ```

### Status & Logs prüfen:
- **Status abfragen**: `sudo systemctl status memegen`
- **Logs live verfolgen**: `journalctl -u memegen -f`
- **Bot neustarten**: `sudo systemctl restart memegen`
- **Bot stoppen**: `sudo systemctl stop memegen`
