import os
import psutil
import time
from datetime import datetime
import email_notifications

# Load environment variables from .env file
import dotenv
dotenv.load_dotenv()

# Diese Funktion ruft eine Liste aller aktuell angemeldeten Benutzer ab.
# Sie verwendet die psutil-Bibliothek, um Informationen über laufende Prozesse und Systemauslastung zu erhalten.
def get_logged_in_users():
    users = psutil.users()
    # Extrahieren Sie die Benutzernamen jedes Benutzerobjekts mithilfe einer List Comprehension
    # um eine neue Liste von Strings zu erstellen, die nur den Benutzernamen enthält.
    logged_in_users = [user.name for user in users]
    return logged_in_users

# Diese Funktion überwacht die Systemleistung für eine bestimmte Zeitdauer und speichert das Ergebnis in der Protokolldatei: system_log.txt.
# Sie akzeptiert auch optional Grenzwerte für CPU, RAM und Festplattenauslastung.
def monitor_system(duration, cpu_limit=None, ram_limit=None, disk_limit=None):
    log_file = 'system_log.txt'  # Name of the log file
    first_run = True             # Diese Variable wird verwendet, um festzustellen, ob dies der erste Durchlauf des Codes ist.
    start_time = time.time()     # Die Startzeit wird auf den aktuellen Zeitpunkt gesetzt, um die Gesamtdauer der Überwachung zu messen.

    # Solange die Gesamtzeit der Überwachungsdauer noch nicht abgelaufen ist, arbeitet diese Schleife weiter.
    while time.time() - start_time < duration:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")
        if first_run:
            first_run = False
            datestamp = datetime.now().strftime("%Y-%m-%d") # Das aktuelle Datum wird im datestamp-Format gespeichert.
            with open(log_file, 'a') as file:               # Öffne das Protokoll in Anhangsmodus und schreibe das Datum in die Datei.
                file.write(f"Date: {datestamp}\n")

        with open(log_file, 'a') as file:           # Öffne das angegebene Protokoll im Anhangsmodus und schreibe die folgenden Informationen hinein.
            file.write(f"Timestamp: {timestamp}\n")

            # Logged-in users
            logged_in_users = get_logged_in_users()                         # Rufe eine Funktion auf, um die Benutzerinformationen abzurufen.
            users_log = f"Logged-in Users: {', '.join(logged_in_users)}"    # Formatieren der Benutzerinformationen in einen lesbaren String.
            file.write(users_log + '\n')                                    # Schreibe die Benutzerinformationen in das Protokoll.
            print(f"{timestamp} - {users_log}")                             # Gib die Benutzerinformationen auf der Konsole aus.

            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)    # Rufe die aktuelle CPU-Auslastung ab.
            cpu_log = f"CPU Usage: {cpu_percent}%"          # Formatiere die CPU-Auslastung in einen lesbaren String.
            file.write(cpu_log + '\n')                      # Schreibe die CPU-Informationen in das Protokoll.
            print(f"{timestamp} - {cpu_log}")               # Gib die CPU-Informationen auf der Konsole aus.

            # RAM usage
            mem = psutil.virtual_memory()                                                   # Rufe Informationen zur Speichernutzung ab.
            mem_percent = mem.percent                                                       # Speicherprozentual wird gespeichert.
            mem_used = mem.used / 1024 / 1024                                               # Konvertiere die Speichernutzung in MB.
            mem_total = mem.total / 1024 / 1024                                             # Konvertiere die Gesamtspeichergröße in MB.
            mem_log = f"RAM Usage: {mem_used:.2f}MB / {mem_total:.2f}MB ({mem_percent}%)"   # Formatiere die Speicherinformationen in einen lesbaren String.
            file.write(mem_log + '\n')                                                      # Schreibe die RAM-Informationen in das Protokoll.
            print(f"{timestamp} - {mem_log}")                                               # Gib die RAM-Informationen auf der Konsole aus.

            # Disk usage
            partitions = psutil.disk_partitions()                                                                           # Ruft Informationen zu den Laufwerken ab, die aktuell angeschlossen sind.
            for partition in partitions:
                disk_usage = psutil.disk_usage(partition.mountpoint)                                                        # Ruft die Nutzungs-/Kapazitätsinformationen des Laufwerks ab.
                disk_percent = disk_usage.percent                                                                           # Prozentualer Anteil des verwendetem Speichers.
                disk_used = disk_usage.used / 1024 / 1024 / 1024                                                            # Konvertiere die Speichernutzung in GB.
                disk_total = disk_usage.total / 1024 / 1024 / 1024                                                          # Konvertiere die Gesamtkapazität des Laufwerks in GB.
                disk_log = f"Disk Usage ({partition.mountpoint}): {disk_used:.2f}GB / {disk_total:.2f}GB ({disk_percent}%)" # Formatiere die Informationen zur Laufwerksauslastung in einen lesbaren String.
                file.write(disk_log + '\n')                                                                                 # Schreibe die Laufwerksinformationen in das Protokoll.
                print(f"{timestamp} - {disk_log}")                                                                          # Gib die Laufwerksinformationen auf der Konsole aus.

        # Check limits
        if cpu_limit is not None and cpu_percent > cpu_limit:                           # Wenn ein Grenzwert festgelegt ist und die aktuelle CPU-Auslastung den Grenzwert überschreitet.
            cpu_message = f"CPU usage exceeded the limit of {cpu_limit}%"               # Formatiere eine Benachrichtigungsmeldung in einen lesbaren String.
            print(cpu_message)                                                          # Gib die Meldung auf der Konsole aus.
            email_notifications.send_email("CPU Usage Limit Exceeded", cpu_message)     # Versende eine E-Mail-Benachrichtigung, mit der Meldung, dass der vorgegebene Grenzwert überschritten wurde.
            with open(log_file, 'a') as file:                                           # Öffne das Protokoll im Anhangsmodus und schreibe eine Grenzwertüberschreitungs-Meldung hinein.
                file.write(f"Limit Exceeded: {cpu_message}\n")
            break                                                                       # Beende die Schleife. 

        if ram_limit is not None and mem_percent > ram_limit:                           # Wenn ein RAM-Grenzwert festgelegt ist und die aktuelle RAM-Auslastung den Grenzwert überschreitet.
            ram_message = f"RAM usage exceeded the limit of {ram_limit}%"               # Formatiere eine Benachrichtigungsmeldung in einen lesbaren String.
            print(ram_message)                                                          # Gib die RAM-Meldung auf der Konsole aus.
            email_notifications.send_email("RAM Usage Limit Exceeded", ram_message)     # Versende eine E-Mail-Benachrichtigung, mit der Meldung, dass der vorgegebene RAM-Grenzwert überschritten wurde.
            with open(log_file, 'a') as file:                                           # Öffne das Protokoll im Anhangsmodus und schreibe eine Grenzwertüberschreitungs-Meldung hinein.
                file.write(f"Limit Exceeded: {ram_message}\n")
            break                                                                       # Beende die Schleife.

        if disk_limit is not None:                                                                                  # Wenn ein Festplatten-Grenzwert definiert wurde.
            for partition in partitions:                                                                            # Iteriere über die vorhandenen Partitionen im System.
                disk_usage = psutil.disk_usage(partition.mountpoint)                                                # Erhalte den Festplattenverbrauch für eine bestimmte Partition.
                disk_percent = disk_usage.percent                                                                   # Berechne den prozentualen Festplattennutzungsgrad.
                if disk_percent > disk_limit:                                                                       # Wenn der aktuelle Festplattennutzungsgrad den Grenzwert überschreitet.
                    disk_message = f"Disk usage on {partition.mountpoint} exceeded the limit of {disk_limit}%"      # Formatiere eine Benachrichtigungsmeldung in einen lesbaren String.
                    print(disk_message)                                                                             # Gib die Festplatten-Benachrichtigung auf der Konsole aus.
                    email_notifications.send_email("Disk Usage Limit Exceeded", disk_message)                       # Versende eine E-Mail-Benachrichtigung, dass der vorgegebene Festplattengrenzwert überschritten wurde.
                    with open(log_file, 'a') as file:                                                               # Öffne das Protokoll im Anhangsmodus und schreibe eine Grenzwertüberschreitungs-Meldung hinein.
                        file.write(f"Limit Exceeded: {disk_message}\n")
                    break                                                                                           # Beende die Schleife.

        time.sleep(5)

# Rufe die Funktion 'monitor_system()' auf und übergebe die zu überwachenden Parameter. Die Überwachungsdauer beträgt 60 Sekunden, der CPU-Auslastungs-Grenzwert beträgt 80%, der RAM-Nutzungs-Grenzwert beträgt 70% und der Festplatten-Nutzungs-Grenzwert beträgt 90%. 
monitor_system(duration=60, cpu_limit=80, ram_limit=10, disk_limit=90)