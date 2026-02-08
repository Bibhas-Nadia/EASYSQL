#!/bin/bash

INSTALL_DIR="/opt/easysql"
VENV_DIR="$INSTALL_DIR/venv"
REQUIREMENTS_FILE="./requirements.txt"  # local path inside install folder

echo "🔧 Installing EasySQL to $INSTALL_DIR..."


# Step 1: Create install directory and subfolders
sudo mkdir -p "$INSTALL_DIR"
sudo mkdir -p "$INSTALL_DIR/credentials"

# Step 6: Change ownership so current user can write credentials and use venv
sudo chown -R "$USER:$USER" "$INSTALL_DIR"


# Step 2: Copy app, queries, and scripts
 cp -r ./../app "$INSTALL_DIR/"
 cp -r ./../Query_files "$INSTALL_DIR/"
 cp ./saveCredential.py "$INSTALL_DIR/credentials/saveCredential.py"
 cp ./../easysql.sh "$INSTALL_DIR/easysql.sh"
 cp ./requirements.txt "$INSTALL_DIR/requirements.txt"

# Step 3: Make main script executable
 chmod +x "$INSTALL_DIR/easysql.sh"

# Step 4: Create virtual environment (as current user to avoid permission issues)
python3 -m venv "$VENV_DIR"

# Step 5: Activate venv and install requirements
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r "$INSTALL_DIR/requirements.txt"
deactivate



# Step 7: Run saveCredential.py using venv
source "$VENV_DIR/bin/activate"
python "$INSTALL_DIR/credentials/saveCredential.py"
deactivate

# Step 8: Add /opt/easysql to PATH in user's shell profile

# Detect the correct shell RC file
SHELL_NAME=$(basename "$SHELL")
RC_FILE=""

case "$SHELL_NAME" in
    bash) RC_FILE="$HOME/.bashrc" ;;
    zsh)  RC_FILE="$HOME/.zshrc"  ;;
    fish) RC_FILE="$HOME/.config/fish/config.fish" ;;  # Fish shell
    *)    echo "Unsupported shell ($SHELL_NAME). Please add /opt/easysql to your PATH manually." ;;
esac

if [ -n "$RC_FILE" ] && [ -f "$RC_FILE" ]; then
    # Only append if not already present
    if ! grep -q 'export PATH=/opt/easysql:$PATH' "$RC_FILE"; then
        echo 'export PATH=/opt/easysql:$PATH' >> "$RC_FILE"
        echo "Added /opt/easysql to PATH in $RC_FILE"
        echo "Run 'source $RC_FILE' or restart your terminal to apply changes."
    else
        echo "ℹ️ /opt/easysql is already in PATH in $RC_FILE"
    fi
fi

echo "EasySQL installed successfully!"
echo "To run it: bash $INSTALL_DIR/easysql.sh"
# echo "▶ Or just type 'easysql' (after symlink added)"
