# /simplify

A `/simplify` párhuzamos review-agentjei alatt **csend**, a végén **egy** válasz.

- **Indításkor**: egy rövid üzenet a `⏳ Folyamatban` blokkal (melyik agent mit néz).
- **Köztes értesítés** (egy agent kész, a többi fut): nincs szöveg.
- **Ha mind kész**: dedup, majd a javítás **előtt** egy lista arról, mit fogsz javítani. Itt **megállsz**, és csak a *Fejlesztő* jóváhagyása után javítasz. Utána ellenőrzés (build/check), végül egyetlen záró válasz.
