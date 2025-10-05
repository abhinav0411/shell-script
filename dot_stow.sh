#!/bin/bash

echo "Write the name of the directory where you have your config files"

read file_name

mkdir -p "$HOME/dotfiles/$file_name/.config/$file_name"

cp -r "$HOME/.config/$file_name/"* "$HOME/dotfiles/$file_name/.config/$file_name"

if [ -d "$HOME/.config/$file_name.bak" ]; then
    echo "Backup already exists: $HOME/.config/$file_name.bak"
    exit 1
fi

mv "$HOME/.config/$file_name" "$HOME/.config/$file_name.bak"

cd $HOME/dotfiles/

stow "$file_name"
