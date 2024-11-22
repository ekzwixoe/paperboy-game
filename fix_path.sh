#!/bin/bash

# Add Homebrew to PATH
export PATH="/opt/homebrew/bin:$PATH"

# Check if Homebrew is accessible
if command -v brew >/dev/null 2>&1; then
    echo "Homebrew is properly configured"
else
    echo "Error: Homebrew not found in PATH"
    exit 1
fi

# Check if gh is installed
if ! command -v gh >/dev/null 2>&1; then
    echo "Installing GitHub CLI..."
    brew install gh
fi

# Verify gh installation
if command -v gh >/dev/null 2>&1; then
    echo "GitHub CLI is properly installed"
    gh --version
else
    echo "Error: GitHub CLI installation failed"
    exit 1
fi

# Add this to your shell configuration
echo "Add these lines to your shell configuration file (~/.zshrc or ~/.bash_profile):"
echo 'export PATH="/opt/homebrew/bin:$PATH"'
