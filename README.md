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

    Da in Skript 3 Selenium verwendet wird, wird außerdem ein Browser benötigt. In diesem Fall wird Firefox benutz, dies kann aber auch entsprechend geändert werden.
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

Als erstes sollten in der Datei "settings.py" die Ordnerpfade geändert werden. Insgesamt sollten etwa 25 GB Speicherplatz frei sein. Bei externen Datenspeichern, sollte beachtet werden, dass sich der Laufwerkbuchstabe bei Windows ändern kann.
die restlichen Paramter können auch modifiziert werden, sind aber standardmäßig auf die in der Arbeit verwendeten Werte eingestellt.
Nach jeder Änderung muss die datei gespeichert werden.

Anschließend könnnen in chronologischer Reihenfolge alle Skripte ausgeführt werden.
Es ist zu beachten, dass zum Teil lange Wartezeiten eingeplant werden müssen. Das Parsing der 10-Ks in Skript 3 hat auf meinem 4 Jahre alten Laptop 50 Stunden gedauert.
In den zeitaufwändigen Abschnitten muss, falls das Programm unterbrochen wird, in der Regel beim erneuten Ausführen nicht von vorne angefangen werden.
Es ist darauf zu achen, dass keine Excel-Outputdateien geöffnet sind, wenn ein Skript ausgeführt wird.
Die Datei "MOD_Load_MasterDictionary_v2020.py" soll nicht direkt ausgeführt werden, muss aber im Ordner sein.


Alle Tabellen sind im csv_path zu finden.





