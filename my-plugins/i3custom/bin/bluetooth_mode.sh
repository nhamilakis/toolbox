#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

notify() {
    local msg
    local is_error

    msg=${1?BUG: no message}
    is_error=${2:-0}

    if command -v notify-send >/dev/null 2>&1; then
        notify-send "btmenu" "$msg"  # TODO: escaping
    fi

    if (( is_error )); then
        printf 'ERROR: %s\n' "$msg" >&2
    else
        printf '%s\n' "$msg"
    fi
}



option0="Status"
option1="Enable"
option2="Disable"
option3="Connect"
option4="Disconnect"


options="$option0\n$option1\n$option2\n$option3\n$option4"
chosen="$(echo -e "$options" | rofi -lines 5 -dmenu -p "Bluetooth")"
device="$(bluetoothctl info | grep -A1 Device)"

case $chosen in
    $option0)        
        echo "Status" && rofi -e "$device";;
    $option1)
        echo "Enable" && rfkill unblock bluetooth && notify "Bluetooth Enabled";;
    $option2)
        echo "Disable" && rfkill block bluetooth && notify "Bluetooth Disabled";;
    $option3)
        echo "Connect" && $SCRIPT_DIR/bt_connect;;
    $option4)
        echo "Disconnect" && $SCRIPT_DIR/bt_connect -d;;
esac
