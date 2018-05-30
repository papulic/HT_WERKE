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




- potrebni komentari za posao ili polje u bazi ili word dokument u file field.  (ok, ali mozda posebno model komentar pa vezan za posao, tako bi bilo vise mogucnosti!)
- mesecni pregled radnika akontacija + ishrana, neto ld.
- finansije -> sve poslove koji su trenutno imaju radnike (izabrati mesec kao kod radnika) svaki prihod i rashod mora imati polje datum. i na automatsku satnicu dodati datum
- mozda model akontacija: polja: radnik, mesec, godina.
- ukupna kolicina troskova za vozilo  ( mozda i datum za prihod i rashod, automatski)


- na listi vozila izbaciti kilometre i potrosnju  --  ok
- filter radnika na mesecnom izvodu po zanimanju i poslu.  --  ok samo poslu receno da je dovoljno  (testirati odakle krece autoincrement)
- pregled ukupnog rada od pocetka radnog odnosa za svaki mesec koliko danaa radnih, bolovanja, odmora i nedozvoljenog odstustva,
 kad se udje u detalje radnika na dnu stranice  -- ok
- Izbaciti da mora upisati opis posla -- ok
- ako su dogovoreni radni sati 0kn rashod da ide u minus. --  ok
- dan polje ishrana - automatski rashod na trenutnom projektu.  --  ok
- ne unositi svaki dan na kom je poslu radnik, nego racunati rashod na trenutnom poslu!!!  --  ok
- posao dodati polje pocetak posla, kraja. Racunati broj dana..  ukupan broj radnih sati na projektu svih radnika. --  ok


- onemoguceno dodavanje na posao kroz objekat radnih, dakle MOOORA kroz posao...!!!!!!