# Hermes Core Knowledge

## Core Commands
- `/new` — start a new session
- `/stop` — abort a running turn
- `/loop` — repeated execution (see below)
- `/dash <question>` — this helpdesk

## Plugins (install / enable / disable / remove)

All via the `hermes plugins` CLI (there is no `/plugins install` slash command):

- `hermes plugins search <term>` / `hermes plugins browse` — find plugins in the
  curated catalog.
- `hermes plugins install <name|git-url|owner/repo>` — install from the catalog,
  a Git URL, or `owner/repo`. Portable packages install **disabled** by default.
- `hermes plugins enable <name>` — enable a disabled plugin.
- `hermes plugins disable <name>` — disable without removing (state is kept).
- `hermes plugins remove <name>` (aliases `rm`, `uninstall`) — fully remove.
- `hermes plugins list` / `hermes plugins show <name>` — list installed, or show
  one plugin's details (including its `emits`/`listens`).
- `hermes plugins update <name>` — pull latest changes for an installed plugin.

## Common tasks → command (non-obvious mappings)

- Move a session to another platform (Telegram, Discord, …) → `/handoff <platform>`
- Compress the conversation context → `/compress` (alias `/compact`)
- Undo the last N turns and re-prompt → `/undo [N]`
- Set a title for the current session → `/title [name]`
- Branch the session to explore another path → `/branch [name]` (alias `/fork`)
- List/restore filesystem checkpoints → `/rollback [number]`
- Show session/model/token/context info → `/status`
- Detailed context window + compression stats → `/context` (alias `/ctx`)

## Keyboard Shortcuts
- `Ctrl+Shift+P` (also `Cmd+Shift+P` on macOS) is NOT bound — nothing happens.
  The Command Palette is `Ctrl+K` or `Ctrl+P` (`Cmd+K` / `Cmd+P`).
- Other defaults: `Ctrl+N` new session, `Ctrl+T` new tab, `Ctrl+,` settings,
  `Ctrl+.` command center, `Ctrl+/` shortcuts panel, `Ctrl+B` sidebar,
  `Ctrl+J` right sidebar, `Ctrl+G` review, `Ctrl+W` close tab,
  `Ctrl+Shift+T` reopen tab, `Ctrl+F` find in page, `Ctrl+Shift+M` model
  picker, `Ctrl+Shift+S` status bar, `Ctrl+Shift+L` browser, `Ctrl+Shift+H` HUD.

## Steering & Background Commands (not in the official docs)

These all manage work *around* the current turn. They are easy to confuse because
their names blur together; the differentiator is **when** the message lands and
**how long** it lives. The official docs do not document them, so this is the
reference.

**Inject without interrupting the current turn:**
- `/btw <question>` — ask a side question about this conversation; the answer
  comes back but the running turn is not touched.
- `/steer <prompt>` — inject a course-correction after the *next* tool call,
  mid-turn. Use when you see the agent heading the wrong way and don't want to
  stop it.
- `/queue <prompt>` (alias `/q`) — queue a prompt for the *next* turn; it runs
  after the current turn finishes. Subcommands: `list`, `edit N`, `rm N`,
  `move A B`, `clear`, `add`.

**Standing or recurring work:**
- `/goal <text>` — set a standing goal Hermes works toward across turns until
  achieved. Subcommands: `draft <text>`, `show`, `status`, `pause`, `resume`,
  `clear`, `gate add <cmd>`, `wait <pid>`, `unwait`.
- `/subgoal` — add or manage extra criteria on the active goal
  (`remove N` / `clear`).
- `/loop [interval] <prompt>` (alias `/proactive`) — re-run a prompt on a
  recurring interval *in this session* (`--times N`, `--until <cond>`,
  `status` / `pause` / `resume` / `stop`).
- `/heartbeat [every <interval> <prompt>]` (alias `/hb`) — a recurring prompt
  that re-enters the session *when idle* (unlike `/loop`, which is timer-driven).

**Offload / meta:**
- `/bg <prompt>` — run a prompt in a separate background session.
- `/plan [task]` — write a markdown plan to `.hermes/plans/` without executing.
- `/refine [focus]` — review this conversation now and save lessons to
  memory/skills.
- `/review [instructions]` — spawn an independent subagent to review the work
  just discussed.
- `/handoff <platform>` — hand this session off to a messaging platform
  (Telegram, Discord, …).

**Quick discriminator:** one-off side answer → `/btw`; mid-turn correction →
`/steer`; next-turn prompt → `/queue`; cross-turn objective → `/goal`;
timer re-run → `/loop`; idle re-entry → `/heartbeat`; fire-and-forget →
`/bg`.

## Error Patterns
- **Cron not delivering:** execute_code is blocked in cron — write to /tmp and use terminal instead.
- **Gateway won't start:** see the `gateway-troubleshooting` skill.
- **Plugin won't load:** check `plugin.yaml` + `__init__.py` with `register(ctx)`.
