
1) https://github.com/fr1sk/boban-bot

2) Da bi se projekat buildovao potrebno je imati docker sve ostalo ce docker sam odraditi za vas. 

3) pokrenutni 'docker build -t boban-bot .' iz root direktorijuma projekta
kada docker izbilduje sliku, nju pokrecete sa 'docker run -it -p 8081:8081 boban-bot' i time pokrecete app na 0.0.0.0:8081

4) Boban-Bot je chat bot koji ima namenu da pomogne Bobanu, kao i studentima u efikasnijem obavljanju posla studentske sluzbe. Skeniranjem QR koda koji se nalazi kod Bobana, dobija se informacija o tome koliko ljudi je pre tebe koji cekaju u redu i za koliko minuta bi trebalo da dodjem na red. U slucaju da je puno ljudi u redu, mogu da posaljem lokaciju mesta gde cu da cekam(neki kafic, ili stan, ako zivim blizu) i da mi aplikacija kaze koliko vremena odatle mi treba do Bobana. Takodje, aplikacija moze da salje podsetnik kada da krenem, da bih na vreme stigao do Bobana

5) Docker slika je zasnovana na UBUNTU operativnom sistemu ali je nezavisna od operativnog sistema na kome se pokrece jer je pokrece docker

6) Marko Jovanovic - 062/2014 fr1sk@live.com
   Stevan Djokic - 373/2014 stevandjokic94@live.com

7) Da bi ste testirali app (messenger bota) potrebno je da nam posaljete vase facebook id-jeve ili username-ove.