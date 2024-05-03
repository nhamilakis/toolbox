#!/bin/bash
########
# Usage: ./$(basename "$0") [--] file1.ln file2.ln dir1.ln ....
########
# Script allowing to replace symlink with a copy of the target file (works with folders as well)
########


# Help message
LW="$(echo "$*" | tr '[:upper:]' '[:lower:]')"
if [[ "$LW" == *"help"* ]]
then
    cat <<EOT
Usage: ./$(basename "$0") [--] file1.ln file2.ln dir1.ln ....

Script allowing to replace symlink with a copy of the target file (works with folders as well)
EOT
exit 1
fi


# Loop over args & copy files to symlink location
for link in "$@"
do
    test -h "$link" || continue

    dir=$(dirname "$link")
    reltarget=$(readlink "$link")
    case $reltarget in
        /*) abstarget=$reltarget;;
        *)  abstarget=$dir/$reltarget;;
    esac
  rm -fv "$link"
  cp -afv "$abstarget" "$link" || {
    # on failure, restore the symlink
    rm -rfv "$link"
    ln -sfv "$reltarget" "$link"
  }
done