#!/bin/bash
set -e

echo "Starting multi-database initialization..."

PGUSER="${POSTGRES_USER}"
PGPASSWORD="${POSTGRES_PASSWORD}"
export PGPASSWORD
PGHOST="localhost"
PGPORT="${POSTGRES_DB_PORT}"

# function for creating a user and grant permissions
create_user_and_grants() {
    local DB_NAME=$1
    local DB_USER=$2
    local DB_PASS=$3

    echo "Creating user '$DB_USER' for database '$DB_NAME'..."

    # Create user if missing
    psql -U "$PGUSER" -d "$DB_NAME" -tc \
        "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'" | grep -q 1 \
        || psql -U "$PGUSER" -d "$DB_NAME" -c \
            "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';"

    echo "Granting permissions..."
    psql -U "$PGUSER" -d "$DB_NAME" -c "GRANT USAGE ON SCHEMA public TO $DB_USER;"
    psql -U "$PGUSER" -d "$DB_NAME" -c \
        "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO $DB_USER;"
    psql -U "$PGUSER" -d "$DB_NAME" -c \
        "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO $DB_USER;"
    psql -U "$PGUSER" -d "$DB_NAME" -c \
        "GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO $DB_USER;"
    psql -U "$PGUSER" -d "$DB_NAME" -c \
        "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO $DB_USER;"
}


# Bookstore
echo "Initializing bookstore..."
psql -U "$PGUSER" -d "$POSTGRES_DB" -c "CREATE DATABASE ${BOOKSTORE_DB_NAME};" || true
psql -U "$PGUSER" -d "${BOOKSTORE_DB_NAME}" -f /docker-entrypoint-initdb.d/scripts/bookstore_db.sql

create_user_and_grants \
    "$BOOKSTORE_DB_NAME" \
    "$BOOKSTORE_DB_USER" \
    "$BOOKSTORE_DB_PASSWORD"


# Coffee Shop
echo "Initializing coffee_shop..."
psql -U "$PGUSER" -d "$POSTGRES_DB" -c "CREATE DATABASE ${COFFEE_SHOP_DB_NAME};" || true
psql -U "$PGUSER" -d "${COFFEE_SHOP_DB_NAME}" -f /docker-entrypoint-initdb.d/scripts/coffee_shop_db.sql

create_user_and_grants \
    "$COFFEE_SHOP_DB_NAME" \
    "$COFFEE_SHOP_DB_USER" \
    "$COFFEE_SHOP_DB_PASSWORD"

echo "All databases initialized successfully!"
