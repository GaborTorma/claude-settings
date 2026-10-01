# A commandok átnézése a plugin-dev szempontjai szerint

A 26 slash commandot átnéztük a `plugin-dev` plugin `command-development` skillje
alapján, és a rendszerszintű hibákat javítottuk. A Kontextus-sorok mostantól nem
nyelik le a hibát: ahol a hiány a várt állapot (nincs parkoló, remote, tag, commit),
ott `NINCS` jelzőt adnak, ahol a hiba oka számít, ott `HIBA`-t; a PR-lekérdezés
`gh pr list`-tel megy, ami PR híján `[]`-t ad hiba helyett. Az `allowed-tools` lefedi
a lépések helyi és olvasó parancsait és a láncolt commandokat (`Skill(...)`), az
argumentum pedig `$ARGUMENTS`-ként érkezik a szövegbe.

Eddig egy nem-nulla exitű Kontextus-sor az egész commandot leállította (pl. a
`/commit` üres repóban), a szöveg pedig a git hibaüzenetére ágazott el, ami
verziónként és nyelvenként változhat. A lépések parancsai minden futásnál engedélyt kértek.

Döntések: a remote-ra író és visszafordíthatatlan parancsok (push, tag, `gh release`,
`gh pr merge`/`create`, `branch -D`, deploy) szándékosan kérdeznek tovább. A lassú vagy
módosítás után elavuló lekérdezések kikerültek a Kontextusból: a `/commit` diffje a
`/check` után, a `/worktree-open` foglaltsága a slug ismeretében kérdeződik le, a
`/worklog` repó-URL-je a remote-ból jön.

Nyitva maradt: a régi remote-író engedélyek (`capture`/`curate` push, `issue`), a
shell-változók a bash-blokkokban, a `disable-model-invocation`, és a review logikai
hibái (`merge-dev` CI-kapu, `worklog` diff-hatókör, `park` duplikátum, `release` `git add`).

- [`[9b17d1a4]`](https://github.com/GaborTorma/claude-settings/commit/9b17d1a492adde0cfd74ec023e4d529f7d433e02) · fix(commands): keep expected-failure context lines from aborting capture, curate and commit
- [`[95dfa051]`](https://github.com/GaborTorma/claude-settings/commit/95dfa051ccb9332ec96f20cfc3ca0159b1769de5) · fix(commands): pre-approve the non-destructive steps and chained commands in allowed-tools
- [`[a4057e68]`](https://github.com/GaborTorma/claude-settings/commit/a4057e68422ae2b8faee1f285c5e32a143430c5f) · refactor(commands): pass the arguments through $ARGUMENTS instead of prose references
- [`[9b2dae59]`](https://github.com/GaborTorma/claude-settings/commit/9b2dae59e4895e53e6283ef828abc42ab313bc29) · refactor(commands): branch on an explicit NINCS marker instead of swallowed git errors in context lines
- [`[eedd28ed]`](https://github.com/GaborTorma/claude-settings/commit/eedd28ed079fde795f25ac60e5061c8698eb7bd5) · fix(commands): look up the branch PR with gh pr list so a missing PR is not an error
- [`[9adb350a]`](https://github.com/GaborTorma/claude-settings/commit/9adb350ac2774feb284b4d82be8fa7612e054e78) · refactor(commands): move slow and stale-prone lookups out of the context sections
