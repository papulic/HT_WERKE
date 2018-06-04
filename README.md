# HT_WERKE
pocetak projekta 15.05


spisak:
fasader-moler
keramicar
zidar
armirac
tesar
gipsar
elektricar
vodoinstalater

prestanak radnog odnosa

__________________________________________________________________________________________________________


da li se pogadja posao na sat za sve radnike na projektu isti, onda automatska satnica ima smisla

def delete posao, pravi se log fajl sa svim detaljima i finansijama o poslu u media dir i odmah se skida (download)

pregledati titlove



----------------------------------------------------



- delete posao create log  AKO JE STARIJI OD DVE GODINE prvo ucitati te poslove pa redirect na default index page
- brisati i akontacije starije od ?  radnike koji nisu u radnom odnosu duze od ? dane koji su ostali u bazi  (nedelje...)
mozda sve objekte starije od tri godine?
- test test test provera svega sto moze ostati u bazi


- na listi vozila izbaciti kilometre i potrosnju  --  ok
- filter radnika na mesecnom izvodu po poslu.  --  ok (testirati odakle krece autoincrement)
- pregled ukupnog rada od pocetka radnog odnosa za svaki mesec koliko danaa radnih, bolovanja, odmora i nedozvoljenog odstustva,
 kad se udje u detalje radnika na dnu stranice  -- ok
- Izbaciti da mora upisati opis posla -- ok
- ako su dogovoreni radni sati 0kn rashod da ide u minus. --  ok
- dan polje ishrana - automatski rashod na trenutnom projektu.  --  ok
- ne unositi svaki dan na kom je poslu radnik, nego racunati rashod na trenutnom poslu!!!  --  ok
- posao dodati polje pocetak posla, kraja. Racunati broj dana..  ukupan broj radnih sati na projektu svih radnika. --  ok
- mesecni pregled radnika akontacija + ishrana, neto ld.  --  ok
- mozda model akontacija: polja: radnik, mesec, godina.  --  ok
- ukupna kolicina troskova za vozilo -- ok
- finansije -> sve poslove koji trenutno imaju radnike (izabrati mesec kao kod radnika) svaki prihod i rashod mora imati polje datum. i na automatsku satnicu dodati datum   --  ok
- dogovoreno po kvadratu  --  ok  (automatsi racunanje prihoda)
- potrebni komentari za posao ili polje u bazi ili word dokument u file field.  --  ok
- posebno obrisi, posebno napravi pdf izvestaj -- ok


- onemoguceno dodavanje na posao kroz objekat radnih, dakle MOOORA kroz posao...!!!!!!
- Ako je datum veci od kraja projekta, radnici se ne mogu dodati vise!
- Posao se ne moze obrisati ako nije postavljen datum na kraj projekta
- Brisanjem projekta se brisu svi dani, prihodi, rashodi vezani za taj projekat!!
- Kad se obrise posao, nece se vise precizno videti taj mesec za radnike..