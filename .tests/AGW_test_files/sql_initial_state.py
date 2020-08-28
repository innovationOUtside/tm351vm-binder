import pandas as pd

import psycopg2 as pg
import psycopg2.extensions as pge

import os

THIS_PATH=os.path.dirname(os.path.realpath(__file__))


# A script to put the database into a default state at
# the start of each notebook

# First create a connection using the user name and
# password that were provided by the call

tm351_cleanup_conn = pg.connect(dbname=DB_NAME_CLEANUP,
                                user=DB_USER_CLEANUP,
                                password=DB_PWD_CLEANUP,
                                host='127.0.0.1',
                                port=5432)


# Next, want the list of tables created by the user

tables_df=pd.read_sql('''
                    SELECT tablename
                    FROM pg_catalog.pg_tables
                    WHERE tableowner=%(user)s
                    ''',
                      tm351_cleanup_conn,
                      params={'user':DB_USER_CLEANUP})


# And DROP those tables. Use CASCADE to get rid of any
# dependencies
c=tm351_cleanup_conn.cursor()

for t in list(tables_df['tablename'].values):
    print("DROPping table {}".format(t))
    c.execute("DROP TABLE IF EXISTS %(tablename)s CASCADE;",
              {'tablename':pge.AsIs(t)})

c.close()
tm351_cleanup_conn.commit()

# Now we need to populate the tables in the tm351_hospital schema

c=tm351_cleanup_conn.cursor()

# (Re-)create the schema:
print("Recreating the tm351_hospital schema")
c.execute("DROP SCHEMA IF EXISTS tm351_hospital CASCADE;")
c.execute("CREATE SCHEMA tm351_hospital;")


print("Populating the tm351_hospital schema")

c.execute('''
    CREATE TABLE tm351_hospital.patient (
        patient_id CHAR(4),
        patient_name VARCHAR(20),
        date_of_birth DATE,
        gender CHAR(6),
        height_cm DECIMAL(4,1),
        weight_kg DECIMAL(4,1),
        doctor_id CHAR(4))
    ''')

c.execute('''
    CREATE TABLE tm351_hospital.doctor (
        doctor_id CHAR(4),
        doctor_name VARCHAR(20))
    ''')

c.execute('''
    CREATE TABLE tm351_hospital.drug (
        drug_code CHAR(6),
        drug_name TEXT)
    ''')

c.execute('''
    CREATE TABLE tm351_hospital.prescription (
        patient_id CHAR(4),
        doctor_id VARCHAR(20),
        drug_code CHAR(6),
        date DATE,
        dosage TEXT,
        duration TEXT)
    ''')

# We'll populate the tables from the csv files in the
# sql_data directory

df=pd.read_csv(os.path.join(THIS_PATH, 'sql_data', 'doctor.csv'))

for it in df.itertuples():
    c.execute('''
        INSERT INTO tm351_hospital.doctor (doctor_id, doctor_name)
        VALUES (%s, %s)
        ''', (it.doctor_id, it.doctor_name))

df=pd.read_csv(os.path.join(THIS_PATH, 'sql_data', 'patient.csv'),
               parse_dates=['date_of_birth'])

for it in df.itertuples():
    c.execute('''
        INSERT INTO tm351_hospital.patient (patient_id, patient_name,
                             date_of_birth, gender, height_cm,
                             weight_kg, doctor_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (it.patient_id, it.patient_name, it.date_of_birth,
              it.gender, it.height_cm, it.weight_kg, it.doctor_id))

df=pd.read_csv(os.path.join(THIS_PATH, 'sql_data', 'drug.csv'))

for it in df.itertuples():
    c.execute('''
        INSERT INTO tm351_hospital.drug (drug_code, drug_name)
        VALUES (%s, %s)
        ''', (it.drug_code, it.drug_name))

df=pd.read_csv(os.path.join(THIS_PATH, 'sql_data', 'prescription.csv'),
               parse_dates=['date'])

for it in df.itertuples():
    c.execute('''
        INSERT INTO tm351_hospital.prescription (patient_id, date, doctor_id,
                                  drug_code, dosage, duration)
        VALUES (%s, %s, %s, %s, %s, %s)
        ''', (it.patient_id, it.date, it.doctor_id, it.drug_code,
             it.dosage, it.duration))


# Add primary key constraints

c.execute('''
    ALTER TABLE tm351_hospital.patient
    ADD CONSTRAINT patient_pk
        PRIMARY KEY (patient_id)
    ''')

c.execute('''
    ALTER TABLE tm351_hospital.doctor
    ADD CONSTRAINT doctor_pk
        PRIMARY KEY (doctor_id)
    ''')

c.execute('''
    ALTER TABLE tm351_hospital.drug
    ADD CONSTRAINT drug_pk
        PRIMARY KEY (drug_code)
    ''')

c.execute('''
    ALTER TABLE tm351_hospital.prescription
    ADD CONSTRAINT prescription_pk
        PRIMARY KEY (patient_id, doctor_id, drug_code, date)
    ''')

# Add foreign key constraints

c.execute('''
    ALTER TABLE tm351_hospital.patient
    ADD CONSTRAINT patient_doctor_fk
        FOREIGN KEY (doctor_id) REFERENCES tm351_hospital.doctor
        ''')

c.execute('''
    ALTER TABLE tm351_hospital.prescription
    ADD CONSTRAINT prescription_patient_fk
        FOREIGN KEY (patient_id) REFERENCES tm351_hospital.patient
        ''')

c.execute('''
    ALTER TABLE tm351_hospital.prescription
    ADD CONSTRAINT prescription_doctor_fk
        FOREIGN KEY (doctor_id) REFERENCES tm351_hospital.doctor
        ''')

c.execute('''
    ALTER TABLE tm351_hospital.prescription
    ADD CONSTRAINT prescription_drug_fk
        FOREIGN KEY (drug_code) REFERENCES tm351_hospital.drug
        ''')

c.close()

tm351_cleanup_conn.commit()
