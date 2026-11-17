// Smyšlená data pro výukový web. Žádné z ubytování neexistuje.
const UBYTOVANI = [
  {id: 1, nazev: "Penzion Modrý hrozen", misto: "Mikulov", cena: 1450, hodnoceni: 4.7, centrum: 0.4, osob: 4,
   popis: "Rodinný penzion se sklepem a snídaní. Pokoje s výhledem na zámek, parkování ve dvoře."},
  {id: 2, nazev: "Apartmány Na Vyhlídce", misto: "Mikulov", cena: 1890, hodnoceni: 4.8, centrum: 1.2, osob: 4,
   popis: "Moderní apartmány s kuchyňkou a terasou. Klidná část města pod kopcem."},
  {id: 3, nazev: "Penzion U Rybníka", misto: "Mikulov", cena: 1150, hodnoceni: 4.5, centrum: 2.5, osob: 3,
   popis: "Jednoduché pokoje u rybníka, ideální pro cyklisty. Úschovna kol, snídaně za příplatek."},
  {id: 4, nazev: "Royal Suite Residence", misto: "Mikulov", cena: 6900, hodnoceni: 4.2, centrum: 0.8, osob: 2,
   popis: "Luxusní apartmá s vířivkou."},
  {id: 5, nazev: "Hotel Zámecký park", misto: "Lednice", cena: 2300, hodnoceni: 4.6, centrum: 0.3, osob: 4,
   popis: "Hotel pár kroků od zámeckého parku. Snídaně v ceně, půjčovna kol."},
  {id: 6, nazev: "Chata U Lesa", misto: "Lednice", cena: 990, hodnoceni: 4.1, centrum: 3.0, osob: 5,
   popis: "Dřevěná chata na okraji lesa, vlastní kuchyně, ohniště."},
  {id: 7, nazev: "Penzion Na Náměstí", misto: "Telč", cena: 1600, hodnoceni: 4.9, centrum: 0.1, osob: 4,
   popis: "Historický dům přímo na náměstí. Pokoje s trámovými stropy."},
  {id: 8, nazev: "Apartmán Rybník Štěpnický", misto: "Telč", cena: 1350, hodnoceni: 4.4, centrum: 1.5, osob: 4,
   popis: "Apartmán u rybníka s půjčovnou loděk."},
];
function parametr(nazev) { return new URLSearchParams(location.search).get(nazev); }
