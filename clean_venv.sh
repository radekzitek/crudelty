# 1. Deactivate the virtual environment (if it's active)
deactivate

# 2. Delete the virtual environment directory
rm -rf .venv  # Linux/macOS (be very careful with rm -rf)

# 3. Recreate the virtual environment
python3 -m venv .venv

# 4. Activate the new virtual environment
source .venv/bin/activate # Linux/macOS
