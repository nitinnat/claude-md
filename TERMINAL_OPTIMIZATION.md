# Terminal Optimization Plan

**Scope:** All recommendations
**Theme:** Catppuccin Mocha

---

## Current Status

**Already Installed:**
- ripgrep (rg) - grep replacement
- jq - JSON processor
- trash - safe delete

**Need Installation:**
- All other tools listed below

---

## Step 1: Install CLI Tools via Homebrew

```bash
# Core CLI tools
brew install fd fzf bat eza btop lazygit git-delta tldr starship zoxide

# Mac apps (casks) - exclude Maccy since Raycast has clipboard
brew install --cask raycast stats iina alt-tab font-jetbrains-mono
```

### Tool Evaluation

| Tool | Purpose | Value |
|------|---------|-------|
| **fd** | Fast `find` replacement, respects .gitignore | High - pairs with fzf |
| **fzf** | Fuzzy finder for history, files, everything | High - essential |
| **bat** | `cat` with syntax highlighting, git integration | High - daily use |
| **eza** | Modern `ls` with colors, icons, git status | Medium - nice to have |
| **btop** | Beautiful system monitor TUI | Medium - replaces htop |
| **lazygit** | Full git TUI for staging, commits, branches | High - faster than CLI |
| **delta** | Pretty git diffs with line numbers, syntax | High - much better diffs |
| **tldr** | Community-maintained simplified man pages | Medium - quick reference |
| **starship** | Fast, customizable prompt | High - essential |
| **zoxide** | Smart `cd` that learns your habits | High - huge time saver |

### Mac App Evaluation

| App | Purpose | Value |
|-----|---------|-------|
| **Raycast** | Spotlight replacement with extensions, clipboard, snippets | High - replaces multiple apps |
| **Stats** | Menu bar system monitor (CPU, memory, network, battery) | Medium - at-a-glance monitoring |
| **IINA** | Modern video player (better than VLC for Mac) | Medium - if you watch video |
| **AltTab** | Windows-style alt-tab with window previews | High - better app switching |

**Note:** Skipping Maccy since Raycast includes clipboard history.

---

## Step 2: Update ~/.zshrc

Replace current content with:

```zsh
. "$HOME/.local/bin/env"
export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"

# History
HISTSIZE=10000
SAVEHIST=10000
HISTFILE=~/.zsh_history
setopt SHARE_HISTORY HIST_IGNORE_DUPS HIST_IGNORE_SPACE

# Completions
autoload -Uz compinit && compinit
[[ -d /opt/homebrew/share/zsh/site-functions ]] && fpath+=(/opt/homebrew/share/zsh/site-functions)

# Tool initializations
eval "$(starship init zsh)"
eval "$(fzf --zsh)"
eval "$(zoxide init zsh)"

# fzf configuration - use fd for file finding
export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
export FZF_ALT_C_COMMAND='fd --type d --hidden --follow --exclude .git'

# File/directory aliases
alias ls='eza'
alias ll='eza -lah --git'
alias la='eza -a'
alias lt='eza --tree --level=2'
alias cat='bat --paging=never'
alias rm='trash'
alias ..='cd ..'
alias ...='cd ../..'

# Git aliases
alias gs='git status'
alias gd='git diff'
alias gc='git commit'
alias gp='git push'
alias gpl='git pull'
alias gl='git log --oneline -15'
alias lg='lazygit'

# Quick edit
alias zshrc='${EDITOR:-code} ~/.zshrc'
```

---

## Step 3: Create ~/.config/starship.toml

```toml
format = "$directory$git_branch$git_status$python$nodejs$cmd_duration$line_break$character"

[directory]
style = "blue bold"
truncation_length = 3

[git_branch]
style = "green"
format = "[$branch]($style) "

[git_status]
style = "red"
format = "[$all_status$ahead_behind]($style) "

[python]
format = "[py $version]($style) "
style = "yellow"

[cmd_duration]
min_time = 2000
format = "[$duration]($style) "
style = "dimmed white"

[character]
success_symbol = "[❯](green)"
error_symbol = "[❯](red)"
```

---

## Step 4: Update ~/.config/ghostty/config

```
right-click-action = "paste"

# Font
font-family = "JetBrains Mono"
font-size = 14

# Catppuccin Mocha
background = 1e1e2e
foreground = cdd6f4
selection-background = 45475a
selection-foreground = cdd6f4
cursor-color = f5e0dc

palette = 0=#45475a
palette = 1=#f38ba8
palette = 2=#a6e3a1
palette = 3=#f9e2af
palette = 4=#89b4fa
palette = 5=#f5c2e7
palette = 6=#94e2d5
palette = 7=#bac2de
palette = 8=#585b70
palette = 9=#f38ba8
palette = 10=#a6e3a1
palette = 11=#f9e2af
palette = 12=#89b4fa
palette = 13=#f5c2e7
palette = 14=#94e2d5
palette = 15=#a6adc8

# Window
window-padding-x = 10
window-padding-y = 10
```

---

## Step 5: Update ~/.gitconfig

Add to existing config:

```gitconfig
[core]
    pager = delta
[interactive]
    diffFilter = delta --color-only
[delta]
    navigate = true
    line-numbers = true
    syntax-theme = Catppuccin Mocha
[alias]
    lg = log --oneline --graph --decorate -20
    st = status -sb
    unstage = reset HEAD --
```

---

## Step 6: Create ~/.config/bat/config

```
--theme="Catppuccin Mocha"
--style="numbers,changes"
```

---

## Files Modified

| File | Action |
|------|--------|
| `~/.zshrc` | Expand with history, completions, tool inits, aliases |
| `~/.config/starship.toml` | Create (new file) |
| `~/.config/ghostty/config` | Expand with font, Catppuccin theme, padding |
| `~/.config/bat/config` | Create (new file) |
| `~/.gitconfig` | Add delta config, aliases |

---

## Post-Install

1. Restart terminal or `source ~/.zshrc`
2. Run `tldr --update` to download pages
3. Navigate around to train zoxide
4. Configure Raycast hotkey (recommend Cmd+Space to replace Spotlight)
5. Configure AltTab preferences (enable window previews)

---

## Key Shortcuts After Setup

| Shortcut | Action |
|----------|--------|
| `Ctrl+R` | Fuzzy search command history (fzf) |
| `Ctrl+T` | Fuzzy find files (fzf+fd) |
| `Alt+C` | Fuzzy cd to directory (fzf+fd) |
| `z <partial>` | Smart cd (zoxide) |
| `lg` | Open lazygit |
| `ll` | List files with git status |
| `lt` | Tree view of current dir |
