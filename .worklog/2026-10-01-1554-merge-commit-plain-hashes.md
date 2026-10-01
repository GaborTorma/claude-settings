# Sima hash-sorok a merge commit worklog-listájában

A `/merge-pr` a merge commit leírásába másolt worklogok commitlistáját markdown-linkek
helyett `- <hash> · <subject>` formában írja.

A commit-üzenet nem markdown: a git log és a GitHub commit-nézete a linkeket nyers
szövegként mutatta, olvashatatlanul.

- [`[60a438cb]`](https://github.com/GaborTorma/claude-settings/commit/60a438cb0ac047b482630ebf79ffddfbedf28086) · fix(commands): use plain hash lines in the merge commit worklog list
