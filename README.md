# Create README.md file
cat > README.md << 'EOF'
# Nepali Land Valuation System

A Django web application for property valuation with Nepali land measurement systems.

## Features
- Valuation reports with bank/borrower details
- Nepali land measurements (Ropani-Ana-Paisa-Dam, Bigha-Kattha-Dhur)
- Automatic area conversion and valuation calculations
- Property management with owners and plots
- Professional Bootstrap UI

## Installation
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 