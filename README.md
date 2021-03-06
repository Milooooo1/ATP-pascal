
# Pascal

Interpreter and compiler for the Pascal language

[Reference Manual](https://public.support.unisys.com/aseries/docs/clearpath-mcp-17.0/pdf/86000080-103.pdf)

# Gebruik van het programma

Het programma vereist python versie 3.10. Het is ontwikkeld op Linux dus garantie dat eventuele onderdelen op Windows werken is er niet (het gaat hier met name over de uitvoering van shell commands die voorkomen in de compiler).

Om het programma aan te roepen moet je een aantal flags meegeven. Deze zijn:

* -f, --file voor het input bestand
* -c, --compile voor het compileren
* -i, --interpret voor het interpreteren

Een mogelijke aanroep ziet er dus als volgt uit

`python3.10 main.py -f example.pas -i` 

of

`python3.10 main.py -f example.pas -c` 

# Interpreter checklist

## Turing compleet

Mijn interpreter voor Pascal is turing compleet aangezien het de volgende functionaliteiten bevat:

* Conditional branching met behulp van if else statements, binnen deze statements kan je alle andere functionaliteiten gebruiken.
* While loops op basis van condities worden ondersteund.
* Je kan interacteren met het programma door in de main variabelen te declareren.
* De interpreter ondersteund meerdere functies per file recursieve functies worden ook ondersteund.

## Functionaliteiten

* Classes met inheritance: Er wordt op meerdere plekken binnen mijn interpreter gebruik gemaakt van inheritance, hieronder is een lijstje toegevoegd met plekken waar inheritance is gebruikt.
  * Alle classes in [ast_classes.py](https://github.com/Milooooo1/ATP-pascal/blob/main/ast_classes.py)
  * Het tokens object maakt gebruik van het interne type Enum [TokensEnum](https://github.com/Milooooo1/ATP-pascal/blob/main/tokens.py#L8)
  * Verder erfen alle overige objecten van het (object) type, dit kan in Python 3 ook weggelaten worden maar voor de old-schoolers onder ons vind ik dit wel netjes
* Object printing is geimplementeerd voor alle ast classed in [ast_classes.py](https://github.com/Milooooo1/ATP-pascal/blob/main/ast_classes.py)
* Een decorator die ervoor zorgt dat alle variabelen worden gecopieerd is gedefineerd in [lexer.py](https://github.com/Milooooo1/ATP-pascal/blob/main/lexer.py#L11)
  * Dit decorator object is gebruikt in [lexer.py](https://github.com/Milooooo1/ATP-pascal/blob/main/lexer.py#L163)
* Haskell type annotation in comments: ja
* Python type hinting in functie definities: ja
* Toepassingen van hogere order functies:
  * [Zip](https://github.com/Milooooo1/ATP-pascal/blob/main/interpreter.py#L61)
  * [Reduce (zelfgemaakt)](https://github.com/Milooooo1/ATP-pascal/blob/main/lexer.py#L142)
  * [Map](https://github.com/Milooooo1/ATP-pascal/blob/main/interpreter.py#L73) op basis van list comprehension
  * [Map](https://github.com/Milooooo1/ATP-pascal/blob/main/interpreter.py#L78) op basis van list comprehension
  * [Map](https://github.com/Milooooo1/ATP-pascal/blob/main/interpreter.py#L80) op basis van list comprehension
* Functie resultaten worden opgeslagen in het door Pascal gedefineerde 'result' variabel

Om de werking van het programma inzichtelijk te maken staan er een aantal print statements door het programma heen. De eerste is te vinden in de main.py (regel 27), deze print alle tokens die zijn gegenereed door de lexer.

Na het printen van de tokens word de tree node van de AST geprint, dit gebeurd ook in main.py (regel 32)

Om te laten zien dat de interpreter werkt word bij elke assignment de locale scope geprint. Dit gebeurd in de interpreter in de visit_Assign functie. Tot slot returned de visit_Program functie "done" wat door de Interpreter.interpret() wordt geprint. Deze print statements zijn allemaal niet nodig en puur hier om te laten zien dat het werkt.

# Compiler checklist

Om mijn compiler te testen maak ik gebruik van [Lennart Janssen](https://github.com/Lennart99/ASM-interpreter) zijn cortex-m0 assembly interpreter. Deze wordt automatisch aangeroepen wanneer je de compiler flag meegeeft aan het programma. Zorg ervoor dat je in de root van dit project zit wanneer je het programma aanroept om eventuele directory errors te voorkomen.

Voor de checklist refereer ik naar de checklist van de Interpreter aangezien hier alle benodigde items al zijn benoemd.