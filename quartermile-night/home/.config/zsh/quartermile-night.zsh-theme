# ~/.config/zsh/quartermile-night.zsh-theme
# Quarter Mile night prompt: agnoster's segment chain, standalone (no oh-my-zsh). The
# plates are plain rectangles and every join is a chequer, not the powerline
# arrow: the quadrant glyph U+259A printed twice in the plate's colour over the
# next plate's colour, and twice more over the terminal ground after the last
# plate, so the chain ends in a small chequered flag. Nothing is cut on a slant.
#   status  tree red, only on failure / root / background jobs
#   context raised + text, only over SSH or as another user
#   dir     deep body blue + light text
#   git     the stripe colour when clean (staged), tree amber with ± when dirty
# U+259A is a block element, not a private-use glyph: foot draws it itself and
# Source Code Pro carries it, so no Nerd Font is needed. It is written as a
# $'\u....' escape, so this file is plain ASCII apart from its comments.
# Hex colours need zsh 5.7+ and a true-colour terminal.

setopt prompt_subst

QM_DEFAULT_USER=${QM_DEFAULT_USER:-$USER}   # hide context on your own box

Q_SEL='#21242A'  Q_DEEP='#145A9C'  Q_ONDEEP='#F3F1EA' Q_AMBER='#FFB02E' Q_ONAMBER='#101113'
Q_TEXT='#F3F1EA' Q_RED='#E5342B'   Q_ONRED='#0A0B0C'   Q_PLATE='#F3F1EA' Q_ONPLATE='#101113' Q_DIM='#7A828C'

QM_SEP=$'\u259a\u259a'   # the chequer: the plate's colour over what follows
typeset -g QM_BG=NONE

qm_segment() {
  local bg="%K{$1}" fg="%F{$2}"
  if [[ $QM_BG == NONE ]]; then
    print -n "%{$bg$fg%} "
  elif [[ $1 != $QM_BG ]]; then
    print -n " %{$bg%F{$QM_BG}%}$QM_SEP%{$fg%} "
  else
    print -n " %{$bg$fg%} "
  fi
  QM_BG=$1
  [[ -n $3 ]] && print -n -- "$3"
}

qm_end() {
  if [[ $QM_BG != NONE ]]; then
    print -n " %{%k%F{$QM_BG}%}$QM_SEP"
  else
    print -n "%{%k%}"
  fi
  print -n "%{%f%}"
  QM_BG=NONE
}

# ~/dotfiles/hypr -> ~/d/hypr
qm_short_pwd() {
  local p=${(%):-%~}
  local -a parts=("${(@s:/:)p}")
  local i
  for (( i = 1; i < ${#parts}; i++ )); do
    [[ -z ${parts[i]} || ${parts[i]} == '~' ]] && continue
    if [[ ${parts[i]} == .* ]]; then
      parts[i]=${parts[i][1,2]}
    else
      parts[i]=${parts[i][1]}
    fi
  done
  print -rn -- "${(j:/:)parts//\%/%%}"
}

qm_status() {
  local -a s
  (( QM_RETVAL != 0 )) && s+=$'\u2718'" $QM_RETVAL"
  (( UID == 0 )) && s+=$'\u26a1'
  [[ -n ${jobstates} ]] && s+=$'\u2699'
  (( ${#s} )) && qm_segment $Q_RED $Q_ONRED "${(j: :)s}"
}

qm_context() {
  [[ $USER != $QM_DEFAULT_USER || -n $SSH_CONNECTION ]] &&
    qm_segment $Q_SEL $Q_TEXT '%n@%m'
}

qm_dir() {
  qm_segment $Q_DEEP $Q_ONDEEP "$(qm_short_pwd)"
}

qm_git() {
  command git rev-parse --is-inside-work-tree &>/dev/null || return
  local ref
  ref=$(command git symbolic-ref --short HEAD 2>/dev/null) ||
    ref=$'\u27a6'" $(command git rev-parse --short HEAD 2>/dev/null)"
  ref=${ref//\%/%%}
  if [[ -n $(command git status --porcelain --ignore-submodules=dirty 2>/dev/null | head -n1) ]]; then
    qm_segment $Q_AMBER $Q_ONAMBER "$ref "$'\u00b1'
  else
    qm_segment $Q_PLATE $Q_ONPLATE "$ref"
  fi
}

qm_build_prompt() {
  qm_status
  qm_context
  qm_dir
  qm_git
  qm_end
}

qm_precmd() { QM_RETVAL=$? }
autoload -Uz add-zsh-hook
add-zsh-hook precmd qm_precmd

PROMPT='%{%f%b%k%}$(qm_build_prompt) '
RPROMPT="%F{$Q_DIM}%*%f"

# ---- completion ------------------------------------------------------
autoload -Uz compinit && compinit
zstyle ':completion:*' menu select
zstyle ':completion:*' list-colors 'ma=48;2;20;90;156;38;2;243;241;234'

# ---- plugins ---------------------------------------------------------
ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE="fg=$Q_DIM"
[[ -r /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh ]] &&
  source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh

# zsh-syntax-highlighting must be sourced last, then styled.
if [[ -r /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ]]; then
  source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
  ZSH_HIGHLIGHT_STYLES[command]='fg=#F3F1EA'
  ZSH_HIGHLIGHT_STYLES[builtin]='fg=#F3F1EA'
  ZSH_HIGHLIGHT_STYLES[alias]='fg=#F3F1EA'
  ZSH_HIGHLIGHT_STYLES[function]='fg=#F3F1EA'
  ZSH_HIGHLIGHT_STYLES[precommand]='fg=#F3F1EA,underline'
  ZSH_HIGHLIGHT_STYLES[path]='fg=#F3F1EA'
  ZSH_HIGHLIGHT_STYLES[single-hyphen-option]='fg=#5AA9F0'
  ZSH_HIGHLIGHT_STYLES[double-hyphen-option]='fg=#5AA9F0'
  ZSH_HIGHLIGHT_STYLES[single-quoted-argument]='fg=#9AA0A8'
  ZSH_HIGHLIGHT_STYLES[double-quoted-argument]='fg=#9AA0A8'
  ZSH_HIGHLIGHT_STYLES[unknown-token]='fg=#FF5348,underline'
fi

export FZF_DEFAULT_OPTS="--color=bg+:#21242A,fg:#9AA0A8,fg+:#F3F1EA,hl:#5AA9F0,hl+:#F3F1EA,pointer:#F3F1EA,prompt:#9AA0A8,info:#9AA0A8,border:#B9BEC6 --pointer='‖' --border=sharp"
