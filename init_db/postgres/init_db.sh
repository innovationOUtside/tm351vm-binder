#!/bin/bash
set -eux

THISDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#Demo PostgreSQL Database initialisation
psql postgres -c "CREATE USER testuser PASSWORD 'testpass'"

# Add users for compatibility with pre-20J notebooks
psql postgres -c "CREATE USER tm351 PASSWORD 'tm351'"
psql postgres -c "CREATE USER tm351_student PASSWORD 'tm351_pwd'"
psql postgres -c "CREATE USER tm351admin PASSWORD 'tm351admin' SUPERUSER"

#The -O flag below sets the user: createdb -O DBUSER DBNAME
createdb -O testuser testdb

# Add a database for compatibility with pre-20J notebooks
createdb -O tm351 tm351
createdb -O tm351_student tm351_clean
createdb -O tm351_student tm351_hospital

psql -d testdb -U testuser -f $THISDIR/seed_db.sql
