#!/bin/bash
YELLOW='\033[0;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'
source .env

if [[ "$DEBUG" =~ ^("true"|"True")$ ]]; then
    VENV_TYPE="development"
    REQUIREMENTS_FILE_PATH="requirements/development.txt";
else
    VENV_TYPE="production"
    REQUIREMENTS_FILE_PATH="requirements/production.txt";
fi

# Activate virtual environment (if exists - run, else create and run)
echo -e "${YELLOW}1. Start virtual environment stage.${NC}"
if [ -d "venv/${VENV_TYPE}" ]; then
    # Start an existing virtual environment
    echo -e "   - Starting venv/${VENV_TYPE}/bin/activate..."
    source venv/${VENV_TYPE}/bin/activate
    echo -e "${GREEN}   - Successfully!${NC}";
elif [ -d "venv/${VENV_TYPE}" ]; then
    # Start an existing virtual environment
    echo -e "   - Starting .venv/${VENV_TYPE}/bin/activate..."
    source .venv/${VENV_TYPE}/bin/activate
    echo -e "${GREEN}   - Successfully!${NC}";
else
    # Create a virtual environment (venv/<type_of_server>)
    echo -e "   - Creating virtual environment (venv/${VENV_TYPE}).."
    python3 -m venv venv/${VENV_TYPE}
    echo -e "${GREEN}   - Successfully!${NC}";
    # Start the created virtual environment
    echo -e "   - Starting venv/${VENV_TYPE}/bin/activate..."
    source venv/${VENV_TYPE}/bin/activate
    echo -e "${GREEN}   - Successfully!${NC}";
fi

# Load environment variables from .env file
echo -e "${YELLOW}2. Load environment variables from .env file stage.${NC}"
if [ -f .env ]; then
    echo -e "   - Exporting .env variables.."
    set -o allexport
    source .env
    set +o allexport
    echo -e "${GREEN}   - Successfully!${NC}";
else
    echo -e "${RED}   - File .env not found${NC}"
    exit 0
fi

# Install requirements from requirements.txt file
echo -e "${YELLOW}3. Install requirements stage.${NC}"
if [ -f requirements/base.txt ]; then
    echo -e "   - Installing base packages.."
    pip install -q -r requirements/base.txt
    echo -e "${GREEN}   - Successfully!${NC}";

    echo -e "   - Installing ${REQUIREMENTS_FILE_PATH} packages.."
    if [ -f ${REQUIREMENTS_FILE_PATH} ]; then
        pip install -q -r ${REQUIREMENTS_FILE_PATH}
        echo -e "${GREEN}   - Successfully!${NC}";
    else
        echo -e "${RED}   - File ${REQUIREMENTS_FILE_PATH} not found${NC}"
        exit 0
fi
else
    echo -e "${RED}   - File requirements/base.txt not found${NC}"
    exit 0
fi

# Make db model migrations
echo -e "${YELLOW}4. Migrate database migrations stage.${NC}"
echo -e "   - Starting migrate.."
python manage.py migrate
echo -e "${GREEN}   - Successfully!${NC}";


# Starting server, if DEBUG set to False, then development, else 
# collect statics and start production server
echo -e "${YELLOW}5. Start server stage.${NC}"
if [[ "$DEBUG" =~ ^("true"|"True")$ ]]; then
    echo -e "   - Starting development server.."
    export DJANGO_SETTINGS_MODULE="app.settings.development"
    python manage.py runserver $HOST:$PORT;
    exit 0
else
    echo -e "   - Starting production server.."
    export DJANGO_SETTINGS_MODULE="app.settings.production"
    python manage.py collectstatic --no-input
    gunicorn app.wsgi:application --bind $HOST:$PORT;
    exit 0
fi