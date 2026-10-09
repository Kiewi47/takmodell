# 3D-takmodellen (Taklagret)

En kärna som används i fem kanaler via **läge** i adressen:

| Läge | Adress | Används i | Skillnad |
|---|---|---|---|
| skarm | `https://3d.taklagret.se/` | Butiksskärmar | Demoläge, viloläge, full kvalitet |
| skola | `?lage=skola` | Takskolan (eget fönster) | Stäng-knapp |
| kalkyl | `?lage=kalkyl` | Takkalkylen (eget fönster) | Stäng-knapp |
| portal | `?lage=portal` | Takportalen | Stäng-knapp, startar på mobilkvalitet |
| shop | `?lage=shop` | taklagret.se | Knappar till produktsidor, taksäkerhet → kalkylator/paket |

Regel: varje ändring görs i kärnan och slår igenom i alla kanaler. Skillnader styrs bara av `LC` (lägeskonfigurationen) i `src/takmodell.html`.

## Kontrakt mot värdappen
- **In (URL):** `lage` (skarm|skola|kalkyl|portal|shop). Planerat: `taktyp`, `hus`, `del`.
- **Ut (postMessage när modellen är inbäddad):** `{tak:'stang'}`, `{tak:'produkt',nr,url}`, `{tak:'kalkylator'}`, `{tak:'paket'}`.
- Produktlänkar öppnas med `target="_top"`, så att hela sidan går till produkten och varukorgen fungerar som vanligt.

## E-handelns produktkoppling
I läget shop hämtas artikelnummer → produktsida live från e-handelns databas (bara aktiva produkter, publik läsnyckel). En ögonblicksbild i koden används om hämtningen misslyckas.

## Bygge och publicering
`python3 build/build.py src/takmodell.html dist <three-paket>` lägger bilderna som egna WebP-filer i `img/` och Three.js i `vendor/`.
Push till `beta` publiceras på `/beta/`, push till `main` publiceras skarpt. GitHub-hemligheter: `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD` (FTP-konto som bara når 3d.taklagret.se).
