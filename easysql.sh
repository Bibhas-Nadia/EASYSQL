#!/bin/bash

BASE_DIR="$(dirname "$(realpath "$0")")"
CRED_FILE="$BASE_DIR/credentials/database_credentials.json"

# Optional: Activate virtual environment if needed
if [ -f "$BASE_DIR/venv/bin/activate" ]; then
    source "$BASE_DIR/venv/bin/activate"
fi

# Run saveCredential if the file doesn't exist
if [ ! -f "$CRED_FILE" ]; then
    echo "No credentials file found. Running setup..."
    python3 "$BASE_DIR/credentials/saveCredential.py"
else
    echo "Credentials found. Launching suggestion tool..."
    python3 "$BASE_DIR/app/give_Suggestion.py"
fi
