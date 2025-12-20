source /usr/share/cachyos-fish-config/cachyos-config.fish

# overwrite greeting
# potentially disabling fastfetch
#function fish_greeting
#    # smth smth
#end

# History Settings (converted from bashrc)
set -x fish_history_size 5000

# Environment Variables
set -x EDITOR nano
set -x VISUAL nano
set -x PAGER less
set -x DALAMUD_HOME /home/nostrathomas/.xlcore/dalamud/Hooks/dev

# Aliases
alias back='prevd'
alias ..='cd ..'
alias ...='cd ../../../'
alias ....='cd ../../../../'
alias .....='cd ../../../../'
alias rm='rm -I --preserve-root'
alias mv='mv -i'
alias cp='cp -i'
alias ln='ln -i'
alias mkdir='mkdir -pv'
alias grep='grep --color=auto'
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'
if type -q colordiff
    alias diff='colordiff'
end
alias now='date +"%F-%T; %V week"'
alias my_ip='curl -s ifconfig.co/json | python3 -m json.tool'
