# ~/.bash_profile

if [[ -z $DISPLAY ]] && [[ $(tty) = /dev/tty1 ]]; then
  exec dbus-run-session Hyprland
fi
