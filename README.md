# fcsim

## Einführung
Dieses Projekt stellt verschiedene Funktionen zur Analyse von Annuitätendarlehen zur Verfügung wie sie beispielsweise bei [Funding Circle](https://www.fundingcircle.com/de/ "externer Link") für Investitionen zur Verfügung stehen. Neben der Service-Gebühr kann auch die deutsche Kapitalertragssteuer berücksichtigt werden.

Basierend auf den Eckdaten eines Darlehens (Zins, Laufzeit, Ausfallwahrscheinlichkeit etc.) und Parametern (z.B. Steuersatz) werden die Renditen der möglichen Zahlungsströme bestimmt, womit sich sowohl die mittlere erwartete Rendite eines Darlehens als auch die Verlustwahrscheinlichkeit ergeben. Die Informationen können in einem weiteren Schritt auch genutzt werden, um ein Portfolio aus mehreren Darlehen zu simulieren.

## Einstieg
Das Projekt benötigt neben den normalen python-Bibliotheken scipy und numpy, welche für die Renditeberechnung und andere numerische Funktionen verwendet werden. Die Dateien `beispiele.py` und `unittests.py` enthalten ein paar Beispiele für den Aufruf der zentralen Funktionen.

## Anmerkungen
* Die zentralen Funktionen sind in Englisch gehalten, sodass sie leicher wiederverwendet werden können.
* Die Funktionen werden in der Hoffnung weiterverbreitet, daß sie nützlich sein werden, jedoch OHNE IRGENDEINE GARANTIE, auch ohne die implizierte Garantie der MARKTREIFE oder der VERWENDBARKEIT FÜR EINEN BESTIMMTEN ZWECK. Mehr Details finden sich in der GNU Lesser General Public License (`LICENSE`)
