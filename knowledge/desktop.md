# Hermes Desktop Knowledge

## General
- The desktop app renders Markdown with full GitHub flavor.
- Plugins: desktop renderer in `desktop/plugin.js`, Python backend optional.
- Floating panes: `data: { placement: 'floating', anchor, width, height }` in a
  `ctx.register` contribution. The core pane shell renders it as a fixed,
  draggable card (header = drag handle, corner = resize grip); position and
  size are persisted per pane id. No drag code needed in the plugin.
- Plugin commands dispatch through `command.dispatch` without a session:
  `session_id: ''` routes to the Python handler and returns a plain string.
  No chat session is created, no tab opens.

## Tabs & Sessions
- **Reopen a closed tab:** `Ctrl+Shift+T` (`Cmd+Shift+T` on macOS) — the last
  closed tab reopens where it was.
- **Toggle the tab strip (if it vanished):** `Ctrl+Alt+T` (`Cmd+Alt+T`). The tab
  bar can be hidden via the session action menu ("Hide tab bar"); this keybind is
  the way back.
- **Switch tabs:** `Ctrl+Tab` / `Ctrl+Shift+Tab` (also `Ctrl+PageUp`/`PageDown`).
- **Bots vs sessions:** each bot is a *profile* with its own persistent chat
  ("Bot Chat"). Selecting a bot reuses its canonical chat rather than opening a
  new tab; a bot's chat is hidden from the Sessions sidebar by design — the bot
  row is the only door back into it. If a session "vanished" after switching
  bots, it is almost always a bot chat that is now reachable only through the
  bot row, not a deleted session.

## Error Patterns
- **Empty preview pane:** write the widget file as HTML and use `::preview{file="..."}`.
- **A chat tab opened but stayed empty:** a slash command went through the
  composer path, which creates a backend session before dispatching. Ask from
  the floating pane instead — it renders the answer inline.
