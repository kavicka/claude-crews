# Cenová ponuka: Kvások & syn — online objednávky s vyzdvihnutím v predajni

Dátum: 2026-11-04 · Platná do: 2026-12-04 · Stav: návrh · Fiktívne príkladové údaje

**Pre:** Kvások & syn, Bratislava–Ružinov, pani Jana Kováčová
**Od:** Lucia Horváthová, lucia-dev.example

## Zhrnutie

- Na váš súčasný web (SK + EN), ktorý som robila v roku 2024, doplním objednávkový formulár s výberom času vyzdvihnutia. Nový web nestaviame.
- Objednávky budú chodiť e-mailom do predajne. Platí sa pri vyzdvihnutí, ako doteraz.
- **Fáza 1 (spustenie): pevná cena 3 500 € bez DPH.** Toto je hlavná ponuka.
- **Fáza 2 (tlačiteľný zoznam objednávok pre rannú zmenu): 500 € bez DPH.** Je voliteľná a objednáva sa samostatne.
- **Cieľový termín spustenia je utorok 1. 12. 2026.** Záväzne ho potvrdím po doručení textov a fotiek. Pravidlá pre prípad omeškania sú v časti Harmonogram.

Všetky ceny sú bez DPH. DPH pripočítam podľa platnej sadzby v deň fakturácie, som platiteľka DPH.

## Prečo sa to oplatí

- **Menej telefonátov počas ranného náporu:** dnes vám medzi 7:00 a 9:00 ujde 5–10 hovorov denne. Nevieme, koľko z nich je stratená objednávka. Ak by formulár zachytil čo i len jednu objednávku denne navyše (priemerne 14 €), je to okolo 84 € tržieb týždenne. Cena fázy 1 by sa tak vrátila v tržbách asi za 10 mesiacov, pričom počítam tržby, nie zisk.
- **Čo formulár nevyrieši:** uzávierka je o 14:00 deň vopred. Kto chce niečo v to isté ráno, bude naďalej volať. Formulár odbremení telefón od objednávok na ďalšie dni, nie od všetkých hovorov.
- **Porovnateľný projekt:** pre Kvetinárstvo Ruža som telefonické objednávky nahradila formulárom s časovými oknami a dnes tam online príde okolo 140 objednávok mesačne.
- **Vaše obavy:**
  - *Poplatky:* pri spustení nebudú žiadne, zákazník platí pri vyzdvihnutí ako dnes.
  - *Vrátenie peňazí:* online sa nič nevracia, lebo sa online ani neplatí.
  - *Personál:* nový systém sa učiť nemusí. Objednávky prídu e-mailom do schránky predajne. Zaškolenie trvá 30 minút a personál dostane návod na jednu stranu. Ak si objednáte fázu 2, ranná zmena dostane aj tlačiteľný zoznam na ďalší deň.

## Torty

- Online sa dajú objednať **len produkty z vášho menu na webe, vrátane medovníka (38 €)**.
- Oslavové torty, torty na objednávku a každá torta nad 50 € sa **naďalej objednávajú telefonicky alebo v predajni s 30 % zálohou, ako dnes**. Formulár ich neponúka, a preto pri spustení nie je potrebné žiadne pravidlo pre torty nad 50 €.
- Torty vo veľkostiach a na objednávku môžeme online doplniť neskôr ako samostatnú zmenu s písomným odhadom.

## Rozsah

### Fáza 1: spustenie (cieľový termín 1. 12. 2026)

- **Objednávkový formulár** na existujúcej stránke v jej súčasnom vzhľade: zákazník vyberie produkty zo 7 položiek menu a ich počet a vyplní meno, telefón, e-mail a poznámku. Formulár skontroluje vyplnenie a pri chybe zrozumiteľne povie, čo opraviť.
- **Časové okná na vyzdvihnutie:**
  - Zákazník vyberie deň a okno, plné okná sa nedajú vybrať.
  - Okná sa riadia otváracími hodinami, zatvoreným pondelkom, uzávierkou na ďalší deň a predstihom pre medovník.
  - Sviatky a vianočné hodiny (napr. 24. 12., 31. 12.) nastavím podľa vášho zoznamu.
- **Ukladanie objednávok:** jednoduchá databáza, teda jeden súbor na serveri, do ktorého sa objednávky zapisujú. Systém z nej vie, koľko miest v okne ešte ostáva. Súčasťou je nastavenie denných záloh.
- **E-maily:**
  - Zapojím ostré odosielanie cez poštový server (SMTP). V kóde webu je dnes iba skúšobné odosielanie.
  - Nastavím doménu (záznamy SPF a DKIM, ktoré potvrdzujú, že e-mail naozaj posiela vaša doména), aby e-maily nekončili v spame.
  - Každá objednávka príde do predajne a zákazník dostane potvrdenie v slovenčine alebo angličtine.
- **Ochrana proti spamu:**
  - Skryté pole, ktoré vyplní iba robot.
  - Obmedzenie počtu odoslaní z jednej adresy za krátky čas.
- **Informácia o spracúvaní osobných údajov:** krátky text pri formulári podľa GDPR (meno, telefón, e-mail, na aký účel a ako dlho ich uchovávate). Pripravím ho podľa vzoru a vy ho ako prevádzkovateľ potvrdíte. Nejde o právne poradenstvo.
- **Angličtina:** preložím nové texty, formulár, chybové hlášky a e-maily. Názvy produktov v menu už v angličtine sú.
- **Vaše texty:** vložím ich na stránku.
- **Testovanie a odovzdanie:**
  - Web otestujem na mobiloch a s personálom vyskúšame jednu ostrú objednávku.
  - Spustenie nasadím v pondelok 30. 11., keď máte zatvorené.
  - Zaškolenie trvá 30 minút a personál dostane návod na jednu stranu.

### Fáza 2 (voliteľná): tlačiteľný zoznam objednávok

- Stránka chránená heslom so zoznamom objednávok na nasledujúci deň, zoradených podľa času vyzdvihnutia.
- Tlač na A4 pre rannú zmenu.
- Súčty podľa produktov pre pekárov, napr. „kváskový chlieb: 23 ks“.
- Prepínač „zrušené“: zrušená objednávka zmizne z ranného zoznamu a uvoľní miesto v okne.
- Bez exportu a bez úprav objednávok.
- Termín: do 11. 12. 2026, ak ju objednáte do spustenia fázy 1.

### Čo ponuka nezahŕňa

- Online platby a online zálohy (záloha je voliteľný doplnok, pozri nižšie).
- Oslavové torty a torty na objednávku cez formulár (pozri časť Torty).
- Fotky produktov v menu, pretože menu je dnes textový zoznam bez obrázkov. Ponúkam ich ako doplnok, pozri nižšie.
- Export objednávok, štatistiky a napojenie na eKasu alebo účtovníctvo.
- Administráciu, v ktorej by ste sami menili produkty, ceny, okná alebo kapacity. Takéto zmeny urobím ja v rámci údržby alebo za 50 €/h.
- Zrušenie objednávky zákazníkom online. Zákazník zavolá alebo odpovie na potvrdzovací e-mail. Miesto v okne uvoľní až prepínač z fázy 2.
- Rozvoz, zákaznícke účty, SMS notifikácie, sledovanie zásob.
- Písanie slovenských textov, fotografovanie a nový dizajn webu.
- Poplatky za hosting a doménu.

## Cena

### Fáza 1: pevná cena (hlavná ponuka)

| Položka | Hodiny | Cena |
|---|---|---|
| Spresnenie zadania a pravidiel (okná, kapacity, uzávierka, produkty) | 2 | 100 € |
| Ukladanie objednávok (databáza, denné zálohy) | 4 | 200 € |
| Objednávkový formulár (7 produktov z menu, kontakt, poznámka, kontrola údajov) | 7 | 350 € |
| Časové okná s kapacitou, uzávierka, predstih pre medovník, sviatky | 22 | 1 100 € |
| E-maily: ostré odosielanie (SMTP), SPF/DKIM, potvrdenie zákazníkovi SK/EN | 7 | 350 € |
| Ochrana proti spamu (skryté pole, obmedzenie odoslaní) | 2 | 100 € |
| Informácia o spracúvaní osobných údajov (GDPR) | 2 | 100 € |
| Angličtina: preklad nových textov, formulára a e-mailov | 4 | 200 € |
| Vloženie vašich textov | 2 | 100 € |
| Testovanie na mobiloch, skúšobná objednávka, opravy | 8 | 400 € |
| Nasadenie, zaškolenie personálu, návod | 4 | 200 € |
| Rezerva (približne 10 %) | 6 | 300 € |
| **Spolu fáza 1 bez DPH** | **70** | **3 500 €** |

V cene sú 2 kolá pripomienok. DPH pripočítam podľa platnej sadzby.

**Známe riziko: pravidlá kapacity.** Pri Kvetinárstve Ruža zabrali pravidlá kapacity o 6 hodín viac, než som odhadla. Preto počítam s 22 h, čo je skutočný čas z toho projektu, hoci tu sú pravidlá podobné alebo jednoduchšie.

### Fáza 2 (voliteľná): tlačiteľný zoznam

| Položka | Hodiny | Cena |
|---|---|---|
| Prihlásenie heslom | 3 | 150 € |
| Zoznam na ďalší deň podľa času vyzdvihnutia | 2 | 100 € |
| Úprava pre tlač na A4 | 1 | 50 € |
| Súčty podľa produktov pre pekárov | 2 | 100 € |
| Prepínač „zrušené“ (vyradí zo zoznamu, uvoľní miesto v okne) | 2 | 100 € |
| **Spolu fáza 2 bez DPH** | **10** | **500 €** |

### Hodinový variant

50 €/h. Odhad pre fázu 1 je 64–78 h (3 200–3 900 € bez DPH), pre fázu 2 je 8–12 h (400–600 € bez DPH). Fakturujem podľa skutočne odpracovaných hodín s výkazom. **Hornú hranicu odhadu prekročím len s vaším písomným súhlasom.**

### Čo sa do 3 500 € nezmestilo

Pri poctivom prepočte hodín vyšiel celý rozsah nad váš strop 3 500 €. Namiesto zľavy som preto rozsah viditeľne zmenšila:

| Časť | Cena bez DPH | Stav |
|---|---|---|
| Menu s fotkami produktov (nové rozloženie, úprava fotiek), 5 h | 250 € | Mimo fázy 1, voliteľný doplnok |
| Tlačiteľný zoznam pre rannú zmenu (fáza 2), 10 h | 500 € | Voliteľné, objednáva sa samostatne |
| Torty na objednávku a nad 50 € cez formulár | odhad na požiadanie | Zatiaľ telefonicky alebo v predajni |

Celý rozsah vrátane fotiek v menu a fázy 2 je 4 250 € bez DPH. Ak by ste chceli ísť pod 3 500 €, ďalej sa dá vynechať len angličtina pri spustení (−200 €). To neodporúčam, lebo v nedeľu chodia z trhu turisti.

## Platobné podmienky

**Fáza 1 (3 500 € bez DPH):**

| Splátka | Kedy | Bez DPH |
|---|---|---|
| 40 % | pri podpise ponuky | 1 400 € |
| 40 % | pri kontrole fázy 1 na skúšobnej verzii webu (kópia webu, ktorú vidíte len vy) | 1 400 € |
| 20 % | pri odovzdaní fázy 1 | 700 € |

**Fáza 2 (500 € bez DPH):** fakturujem samostatne, po jej odovzdaní.

**Spoločné podmienky:**

- DPH pripočítam podľa platnej sadzby. Faktúry sú splatné do 14 dní.
- Skúšobnú verziu považujem za schválenú, ak mi do 2 pracovných dní od oznámenia nepošlete pripomienky.
- Zmeny nad rámec ponuky účtujem 50 €/h a vopred vám ich písomne odhadnem.

## Harmonogram

| Týždeň | Termín | Čo sa deje |
|---|---|---|
| 1 | 5. – 11. 11. | Do 9. 11. podpis a prvá platba, do 11. 11. vaše rozhodnutia o oknách, kapacite, uzávierke a produktoch. Ukladanie objednávok a formulár. |
| 2 | 12. – 18. 11. | Časové okná, e-maily, ochrana proti spamu, text o osobných údajoch. |
| 3 | 19. – 25. 11. | **Pi 20. 11. vaše texty** (a fotky, ak si objednáte menu s fotkami). Vloženie textov, angličtina, 1. kolo pripomienok. **Do st 25. 11. stabilná skúšobná verzia** na stretnutie s personálom. |
| 4 | 26. – 30. 11. | Stretnutie s personálom (skúšobná objednávka, zaškolenie), 2. kolo pripomienok, testy na mobiloch. V pondelok 30. 11. nasadenie. |
| | **ut 1. 12.** | **Cieľové spustenie fázy 1** |
| 5–6 | do 11. 12. | Fáza 2, ak ju objednáte. |

**Cieľový termín je 1. 12. Záväzne ho potvrdím po doručení textov a fotiek.** Pre prípad omeškania platia tieto pravidlá:

- Ak texty prídu po 20. 11., najviac však o 3 pracovné dni (do 25. 11.), spustenie sa posúva o rovnaký počet dní.
- Ak meškajú viac ako 3 pracovné dni, spustenie sa posúva za začiatok predvianočných objednávok. Druhá možnosť je spustiť 1. 12. so súčasnými textmi webu a nové texty doplniť po spustení.
- Termín sa posúva aj vtedy, ak sa podpis posunie za 9. 11.

## Predvolené nastavenia a zmeny

Kým sa nerozhodnete inak, platia tieto nastavenia:

- Okná trvajú 30 minút počas otváracích hodín a do jedného okna sa zmestí 8 objednávok.
- Uzávierka je o 14:00 deň pred vyzdvihnutím, aby pekári stihli naplánovať cesto.
- Medovník treba objednať aspoň 2 dni vopred.
- Objednávať sa dá najviac 14 dní dopredu.
- Online sa dá objednať všetkých 7 produktov zo súčasného menu, bez variantov (veľkostí).

Nastavenia potrebujem odsúhlasiť do 11. 11. 2026. **Zmena okien, kapacít, uzávierky alebo produktov po 11. 11. je zmena rozsahu:** účtujem ju 50 €/h a vopred vám ju písomne odhadnem. Formulár bude v súčasnom vzhľade webu, bez redizajnu. Po spustení meníte produkty, ceny a kapacity cez mňa (údržba alebo 50 €/h).

## Čo potrebujem od vás

**Do 9. 11. 2026**

- Podpísanú ponuku a prvú platbu.

**Do 11. 11. 2026**

- Rozhodnutia o oknách, kapacite, uzávierke (aj pre utorok po zatvorenom pondelku) a produktoch.
- Zoznam sviatkov a vianočných otváracích hodín (24. 12. – 6. 1.).
- Prístup k hostingu, k nastaveniam domény a k e-mailovej schránke predajne.

**Do 20. 11. 2026** (písomne potvrdené)

- Slovenské texty: krátky úvod k objednávaniu a pravidlá vyzdvihnutia, pri tortách upozornenie, že sa objednávajú telefonicky.
- Aktuálne ceny.

**Počas projektu**

- Jedna kontaktná osoba na schvaľovanie.
- 30 minút s personálom v týždni od 26. 11. na zaškolenie a skúšobnú objednávku.

**Pred podpisom si ešte overím** (nemusíte nič robiť):

- Či súčasný hosting vie spustiť aplikáciu v Node.js (prostredie, v ktorom web beží) a natrvalo ukladať súbory na disk.
- Ako dnes v ostrej prevádzke odosiela e-maily kontaktný formulár.

Ak jedna z odpovedí zmení cenu, ozvem sa vám pred podpisom.

## Voliteľné doplnky

| Doplnok | Cena bez DPH | Poznámka |
|---|---|---|
| Fáza 2: tlačiteľný zoznam pre rannú zmenu | 500 € (10 h), nová cena | Popis je vyššie v časti Rozsah. |
| Menu s fotkami produktov | 250 € (5 h), nová cena | Nové rozloženie menu, úprava vašich fotiek pre web. Fotky dodáte vy. |
| Online záloha na torty (Stripe alebo GoPay, čo sú služby na platby kartou cez internet) | od 700 € (asi 14 h) | Najskôr v januári 2027, keď váš účtovník posúdi, ako sa online zálohy evidujú v eKase. Predpokladá, že torty sa už dajú objednať online (samostatná zmena). Ak účtovník bude vyžadovať ďalšie kroky, cenu prepočítam. Poplatky platobnej brány idú mimo tejto ceny, pri Stripe približne 1,5 % + 0,25 € za platbu (overíme pri zriadení). |
| Mesačná údržba: aktualizácie, zálohy, 1 h zmien mesačne (napr. kapacity okien, nové produkty) | 60 € / mesiac | 720 € za rok. Odporúčam aspoň na december a január. |
| Nastavenie hostingu a domény | 120 € | Pravdepodobne potrebné, ak súčasný hosting nevie natrvalo ukladať objednávky. |

## Platnosť ponuky

Ponuka platí 30 dní, do 4. 12. 2026. Cieľový termín 1. 12. platí, ak ponuku podpíšete do 9. 11. 2026 a texty dostanem do 20. 11. 2026.

S pozdravom,

```
Lucia Horváthová
lucia-dev.example
lucia@lucia-dev.example
```

**Súhlas s ponukou:**

- [ ] Fáza 1, pevná cena 3 500 € bez DPH
- [ ] Fáza 1, hodinová sadzba (odhad 3 200–3 900 € bez DPH)
- [ ] Fáza 2, tlačiteľný zoznam, 500 € bez DPH
- [ ] Menu s fotkami produktov, 250 € bez DPH

Meno: ______________________ Podpis: ______________________ Dátum: ____________
