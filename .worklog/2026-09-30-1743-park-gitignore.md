# A parkoló a projekt .gitignore-jába kerül

A `/park` mostantól maga gondoskodik róla, hogy a `.parked.md` ignorálva legyen: ha
a projekt `.gitignore`-jában nincs benne, a parkoló létrehozásakor felveszi (és ha kell,
a `.gitignore`-t is létrehozza), majd csak ezt a fájlt, külön commitban viszi fel. A
command a Kontextusban egy `grep`-pel előre megkapja, benne van-e már, így nem kell
külön megnyitnia a fájlt.

Eddig az ignorálás a globális git ignore-ban élt, amit kézzel kellett felvenni —
másik gépen a `.parked.md` ignorálatlan maradt, és bekerülhetett egy commitba.

A projektszintű `.gitignore` mellett döntöttünk a telepítő-script helyett. A külön
commit azért kell, hogy a `.gitignore` változása ne keveredjen a folyamatban lévő
munkával; a `-- .gitignore` pathspec a már stage-elt egyéb változásokat kihagyja.

Nyitva maradt: a sor csak a `.parked.md` létrehozásakor kerül be, így ahol a parkoló
már létezik (pl. ebben a repóban), ott továbbra is csak a globális ignore védi — kérdés,
hogy minden `/park` pótolja-e, ha hiányzik.

- [`[faff46b7]`](https://github.com/GaborTorma/claude-settings/commit/faff46b71773812c0e2d1f36b27d31ef77aeadda) · fix(commands): add the parked list to the project gitignore on park
