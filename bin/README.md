# bin — PATH-ra kerülő parancsok

Ide a **saját CLI-eszközök** jönnek, nem a repó karbantartó scriptjei (azok a
`scripts/` alatt vannak). A `scripts/install.sh` mindent, ami itt van,
szimlinkel a `~/.local/bin`-be, tehát a fájlnév = a parancs neve, és
futtathatónak kell lennie (`chmod +x`, shebanggel).

| Parancs | Mit csinál |
| --- | --- |
| `gitgraph` | Git Graph-szerű commit-gráf bármelyik repóból, egyetlen önálló HTML-be (`--open` rögtön meg is nyitja). |
