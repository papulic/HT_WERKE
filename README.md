# HT_WERKE
pocetak projekta 15.05

- Ask for implementation of reset/forgot password  ne treba
- Only authenticated users can change "Project" or "people" details?  ne treba
- worker groups choose field or char field  moze

spisak:
fasader-moler
keramicar
zidar
armirac
tesar
gipsar
elektricar
vodoinstalater


da moze sam uneti zanimanje i jedan radnik da ima vise zanimanja

 oib, br tel, br radnog odela, broj cipela

 prestanak radnog odnosa

da moze update radnik..
__________________________________________________________________________________________________________



kad se radniku dodaju isplaceni dani !! MORA !! biti na nekom projektu kako bi se prihod povecao, moramo imati polje
dogovoreni sati za posao  !! projekat polje. dogovoreni sati, ako ga ima.. !!   ako ne, ne racunaj sate automatski.


Automatski KADA SE DODA RADNIK NA PROJEKAT POCETI RACUNANJE DANA NA PROJEKTU


svaki radnik da ima jos po polje: broj radnih sati za tekuci mesec, broj slobodnih dana, i broj dana bolovanja,


dodati fiksne prihode na sate radnika + fiksni rashod na sate radnika koje vuce iz tabele kad se unese broj radnih sati
 za taj dan

 razmisliti o many to many posao - radnik, zbog cuvanja istorije
 ili mozda svaki posao da ima svaki dan i svaki radnik svaki dan..??

Radnik details !!!!!!

 ____________________

 Pitati Saleta da li ipak da se rucno unose prihodi da se ne pogubi da li ima na sate ili ne u projektu,
 ili ovaj projekat je dogovoren na sate radnika i samostalno racuna neke prihode!!



ne moze ovako mesec zbog dodavanja novih radnika u pola meseca

mesecni pregled  --> td color zavisi od dan.bolovanje ili dan.odsustvo




dan treba da ima polje sati a ne koliko je isplaceno, to mnozi sa cenom sata
sume svih isplata za mesec

problem je ako se menja satnica menja se i ukupni rashod za radnika, a samim tim i rashod na projektu,
trebao bi svaki dan imati posebnu isplacenu sumu. Videti da li moze uneto da se ne menja tipa:
dan.novac = current satnica * sati. mada bi to trebalo da radi i ovako ako se posle ne menja!!!

rashod mora imati pokazivac na dan kad se automatski unosi