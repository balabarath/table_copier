#!/usr/bin/env python
import yaml
import subprocess

def get_connection_string(db_config):
    return 'postgresql://{}:{}@{}:{}/{}'.format(db_config['user_name'], db_config['password'], \
    db_config['host'], db_config['port'], db_config['name'])

def get_copy_query(source_conn, destination_conn, table):
    table_name = table['name']
    filter = table['filter']
    return 'psql -d {} -c "COPY (SELECT * FROM {} WHERE {}) TO stdout" | psql -d {} -c "COPY {} FROM stdin"'.format(source_conn, \
    table_name, filter, destination_conn, table_name)

def execute_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    exit_code = process.wait()
    if process.stdout:
        for line in process.stdout.readlines():
            print line
    if process.stderr:
        for line in process.stderr.readlines():
            print line
    if not exit_code:
        return True
    return False

def delete_records(connection_string, table_name):
    delete_command = 'psql -d {} -c "DELETE FROM {}"'.format(connection_string, table_name)
    is_delete_success = execute_command(delete_command)
    if not is_delete_success:
        print "DELETE OPERATION FAILED."

def copy_records(source_conn, destination_conn, table_name):
    copy_command = get_copy_query(source_conn, destination_conn, table)
    is_copy_success = execute_command(copy_command)
    if not is_copy_success:
        print "COPY OPERATION FAILED."

def test_connection(conn_string):
    return execute_command('pg_isready -d ' + conn_string)

with open("config.yaml", 'r') as stream:
    try:
        copy_config = yaml.load(stream)['copy_config']
        source_db = copy_config['source_db']
        destination_db = copy_config['destination_db']
        source_conn = get_connection_string(source_db)
        destination_conn = get_connection_string(destination_db)

        print "---------- CHECKING DATABASES CONNECTION -------------- "
        is_source_db_alive = test_connection(source_conn)
        if not is_source_db_alive:
            print "Please check the {} connection".format(source_db['name'])
            exit(1)

        is_destination_db_alive = test_connection(destination_conn)
        if not is_destination_db_alive:
            print "Please check the {} connection".format(destination_db['name'])
            exit(1)
        print "---------- DATABASES CONNECTION CHECK SUCCESS -------------- "

        for table in copy_config['tables']:
            table_name = table['name']
            if copy_config['delete_destination_db_tables_record_before_copy']:
                print '---------- DELETING all the records in {} table --------------'.format(table_name)
                delete_records(destination_conn, table_name)
            print '"---------- COPYING all the records in from {} database to {} for {} table "----------'.format(source_db['name'], \
            destination_db['name'], table['name'])
            copy_records(source_conn, destination_conn, table)

    except yaml.YAMLError as err:
        print(err)
