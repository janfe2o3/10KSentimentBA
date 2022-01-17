# 10KSentimentBA
 Bachelorarbeit Skripte

Setup:
    Anforderungen:
        -Python 3.9.7
        -Installation aller benötigten Python-Bibliotheken (siehe requirements.txt)
        -Firefox
        -Geckodriver
        -Internetverbindung

    Die benötigte Python-Bibliotheken können gebündelt installiert werden. Dazu in diesem Ordner (10KsentimentBA) eine Eingabeaufforderung (command prompt) öffnen.
    Dort den Befehl "pip install -r requirements.txt" ausführen.

    Da in Skript 3 "3_get_token.py" Selenium verwendet wird, wird außerdem ein Browser benötigt. In diesem Fall wird Firefox benutz, dies kann aber auch entsprechend geändert werden.
    Wenn Firefox benutzt wird, sollte die aktuelle Version von geckdriver heruntergeladen werden (https://github.com/mozilla/geckodriver/releases).
    Damit die Datei verwendet werden kann, muss sie außerdem zum PATH in Windows hinzugefügt werden.
    Dies kann in folgenden Schritten eingrichtet werden:
        -Rechtklick auf "Dieser PC"
        -Eigenschaften auswählen
        -Rechts "Erweiterte Systemeinstellungen" auswählen
        -Auf "Umgebungsvaribalen" klicken.
        -Bei "System Variablen" PATH auswählen.
        -Auf "Bearbeiten..." Button klicken.
        -Auf "Neu" Button klicken
        -Den Dateipfad zum GeckoDriver file einfügen.

Anwendung:

Als erstes sollten in der Datei "settings.py" die Ordnerpfade geändert werden. Insgesamt sollten etwa 25 GB Speicherplatz auf dem Datenträger verfügbar sein sein. 
Bei externen Datenspeichern, muss beachtet werden, dass sich der Laufwerkbuchstabe bei Windows ändern kann.
Die restlichen Paramter können auch modifiziert werden. Diese sind aber standardmäßig auf die in der Arbeit verwendeten Werte eingestellt.
Nach jeder Änderung muss die Datei gespeichert werden.

Anschließend könnnen in chronologischer Reihenfolge alle Skripte ausgeführt werden.
Es ist zu beachten, dass zum Teil lange Wartezeiten eingeplant werden müssen. Das Parsing der 10-Ks in Skript 3 hat auf meinem 4 Jahre alten Laptop 50 Stunden gedauert.
In den zeitaufwändigen Abschnitten wird, falls das Programm unterbrochen wird, in der Regel beim erneuten Ausführen nicht von vorne angefangen werden.
Es ist darauf zu achen, dass keine Excel-Outputdateien geöffnet sind, wenn ein Skript ausgeführt wird.
Die Datei "MOD_Load_MasterDictionary_v2020.py" soll nicht direkt ausgeführt werden, muss aber im Ordner sein.
Außerdem muss sich zusätzlich zu den Python-Dateien, die CSV-Datei "LoughranMcDonald_MasterDictionary_2020.csv" im Verzeichnis befinden.


Eine Beschreibung, was der Zweck der einzelnen Python-Dateien ist, befindet sich am Anfang der jeweiligen Dateien.
Alle Tabellen sind im csv_path zu finden.

Von den 11 Dateien sind 8 klassischen Python-Dateien und 3 Jupyter Notebooks (Dateiendung ".ipynb").
am übersichtlichsten lässt sich das Projkt (meiner Meinung nach) mit "VS Code" (https://code.visualstudio.com/download) mit der Python und Jupyter Ereiterung öffnen und ausführen.




