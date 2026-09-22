# inbox

Más projektek sessionjeiből érkező tanulságok gyűjtőhelye. Ide a `/capture`
parancs ír, innen a `/curate` emeli át őket a `rules/`-ba vagy a plugin-repóba.

Az itteni fájlok **nem hatnak semmire** — egyetlen session kontextusába sem
töltődnek be. Ez szándékos: a bővítés ne legyen azonos az azonnali, mindenhol
ható változtatással.

Append-only: egy fájl egy tanulság, a neve `<YYYY-MM-DD>-<slug>.md`. Két
párhuzamos session így soha nem ütközik ugyanazon a fájlon.

`deferred/` — halasztott bejegyzések: a `/curate` még nem tudott dönteni róluk.
Ugyanúgy nem hatnak semmire; a fájl elején a **Miért halasztva** bekezdés
mondja meg, mi hiányzik a döntéshez.
