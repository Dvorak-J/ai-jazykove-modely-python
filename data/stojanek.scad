// Stojánek na mobilní telefon (všechny rozměry v mm)
sirka = 80;          // šířka stojánku
hloubka = 75;        // hloubka podstavy
tloustka = 6;        // tloušťka podstavy a opěrky
uhel = 65;           // sklon opěrky od vodorovné roviny (ve stupních)
delka_operky = 90;   // délka opěrky
drazka = 11;         // šířka drážky pro telefon (tloušťka telefonu + vůle)
vyska_okraje = 8;    // o kolik přední okraj přečnívá nad podstavu
zaobleni = 1.5;      // poloměr zaoblení hran profilu
kabel = 12;          // šířka otvoru pro kabel
napis = "3.A";       // text vyrytý na předním okraji
$fn = 64;

module profil() {
    zacatek = tloustka + drazka;
    sirka_paty = tloustka / sin(uhel);
    dx = delka_operky * cos(uhel);
    dy = delka_operky * sin(uhel);
    offset(r = zaobleni) offset(delta = -zaobleni) {             // zaoblení rohů
        square([hloubka, tloustka]);
        square([tloustka, tloustka + vyska_okraje]);
        polygon([[zacatek, 0], [zacatek + sirka_paty, 0],
                 [zacatek + sirka_paty + dx, dy], [zacatek + dx, dy]]);
        polygon([[zacatek + sirka_paty, tloustka], [hloubka, tloustka],
                 [hloubka, tloustka + 4], [zacatek + sirka_paty + dx * 0.55, dy * 0.55]]);
    }
}

difference() {
    rotate([90, 0, 90]) linear_extrude(height = sirka) profil();
    // otvor pro kabel ve dně drážky a kanálek pod podstavou směrem dozadu
    translate([(sirka - kabel) / 2, tloustka, -1]) cube([kabel, drazka, tloustka + 2]);
    translate([(sirka - 8) / 2, tloustka, -1]) cube([8, hloubka, 4.5]);
    // vyrytý nápis na přední straně okraje (hloubka 0,8 mm)
    translate([sirka / 2, 0.8, (tloustka + vyska_okraje) / 2])
        rotate([90, 0, 0]) linear_extrude(height = 2)
            text(napis, size = 7, halign = "center", valign = "center",
                 font = "Liberation Sans:style=Bold");
}
