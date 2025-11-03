# Generated with bashrc generator: https://alexbaranowski.github.io/bash-rc-generator/
# History Settings

export HISTFILESIZE=5000
export HISTSIZE=5000
export HISTIGNORE="cd*:false:history:htop:ls*:ll*:la:l:popd:pushd*:reset:top:true"
export HISTCONTROL="ignoreboth"
export HISTTIMEFORMAT="%Y-%m-%d %T "
export HISTFILE=~/.bash_history
shopt -s histappend

# Aliases
alias cd="pushd"
alias back="popd"
popd()
{
  builtin popd > /dev/null
}
pushd()
{
  if [ $# -eq 0 ]; then
    builtin pushd "${HOME}" > /dev/null
  elif [ $1 == "-" ]; then
      builtin popd > /dev/null
  else
    builtin pushd "$1" > /dev/null
  fi
}
alias ..="cd .."
alias ...="cd ../../../"
alias ....="cd ../../../../"
alias .....="cd ../../../../"
alias .....="cd ../../../../"
alias rm='rm -I --preserve-root'
alias mv='mv -i'
alias cp='cp -i'
alias ln='ln -i'
alias sudo='sudo '
alias mkdir="mkdir -pv"
alias grep='grep --color=auto'
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'
hash colordiff &> /dev/null && alias diff='colordiff'
alias now='date +"%F-%T; %V week"'
alias my_ip='curl -s ifconfig.co/json | python3 -m json.tool'
# Extra options

export EDITOR="nano"
export VISUAL="nano"
export PAGER="less"
export DALAMUD_HOME="/home/nostrathomas/.xlcore/dalamud/Hooks/dev"
export OLLAMA_HOST="normandy-sr2:11434"
export OLLAMA_CONTEXT_LENGTH=64000
