test1 = '''% Det här är en kommentar
% Nu ritar vi en kvadrat
DOWN.
FORW 1. LEFT 90.
FORW 1. LEFT 90.
FORW 1. LEFT 90.
FORW 1. LEFT 90.'''


test2 = '''% Space runt punkt valfritt.
DOWN . UP.DOWN. DOWN.
% Rader kan vara tomma
% radbrytning/space/tabb för
% att göra koden mer läslig.
REP 3 "COLOR #FF0000.
FORW 1. LEFT 10.
COLOR #000000.
FORW 2. LEFT 20."
% Eller oläslig
COLOR
% färgval på gång
#111111.
REP 1 BACK 1.'''

test3 = '''% Syntaxfel: felaktig färgsyntax
COLOR 05AB34.
FORW 1.'''


test4 = '''% Oavslutad loop
REP 5 "DOWN. FORW 1. LEFT 10.'''

test5 = '''% Syntaxfel: ej heltal
FORW 2,3.'''

test6 = '''%&(CDH*(
FORW
# 123456.
&C(*N&(*#NRC
'''

test7 = '''% Måste vara whitespace mellan
% kommando och parameter
DOWN. COLOR#000000.'''

test8 = '''% Syntaxfel: saknas punkt.
DOWN
% Om filen tar slut mitt i ett kommando
% så anses felet ligga på sista raden
% i filen där det förekom någon kod'''

test9 = '''% Måste vara space mellan argument
REP 5"FORW 1."
% Detta inte OK heller
REP 5FORW 1.'''


test10 = '''% Ta 8 steg framåt
REP 2 REP 4 FORW 1.
REP% Repetition på gång
2% Två gånger
"%Snart kommer kommandon
DOWN% Kommentera mera
.% Avsluta down-kommando
FORW 1
LEFT 1. % Oj, glömde punkt efter FORW-kommando
"'''

test11 = '''% Nästlad loop 1
REP 2 "UP. FORW 10. DOWN. REP 3 "LEFT 120. FORW 1.""
% Nästlad loop 2
REP 3 "REP 2 "RIGHT 2. FORW 1."
COLOR #FF0000. FORW 10. COLOR #0000FF."
% COLOR #000000. % Bortkommenterat färgbyte
BACK 10.
% Upper/lower case ignoreras
% Detta gäller även hex-tecknen A-F i färgerna i utdata,
% det spelar ingen roll om du använder stora eller små
% bokstäver eller en blandning.
color #AbcdEF. left 70. foRW 10.'''


test12 = '''DOWN .
% OBS! Denna fil har ett
% tabb-tecken (’\t’) i första
% REP-satsen. Om du kör den
% genom att göra copy-paste
% kommer tabb-tecknet inte
% testas korrekt.
REP\t2 REP % raaadbryyyt
1 "REP 2 REP 2 "FORW 1."
LEFT 45."'''
