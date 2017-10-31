import codecs
import os
import mysql.connector

IWN_DATA_ENTRY_TOOL_DB, HWN_DB, MWN_DB, SWN_DB, IWN_DB, HWN_LINKING = 'iwn_data_entry_tool', 'iwn_web_unicode', 'mwn_web_unicode', 'swn_web_unicode', 'regional_wn', 'hwn_linking'
SYNSET_SEPARATOR = ','
HINDI, MARATHI, SANSKRIT = 'hindi', 'marathi', 'sanskrit'
FETCH_ONE_ROW = 'FETCH_ONE_ROW'
FETCH_ALL_ROWS = 'FETCH_ALL_ROWS'
DATABASE = {HINDI: HWN_DB, MARATHI: MWN_DB, SANSKRIT: SWN_DB}
SYNSET_DELIMITER = ','
GLOSS_EXAMPLE_DELIMITER = ':'
FILE_COLUMN_DELIMITER = '\t'


def read_file(filename):
    return codecs.open(filename, 'r', encoding='utf-8')


def clean_line(line):
    line = line.replace('\n', '').strip()
    return line


def convert_to_list(rows):
    l = []
    for row in rows:
        l.append(str(row[0]))
    return l


def post_process_row(row):
    postprocessed_row = []
    for item in row:
        if type(item) is bytes:
            postprocessed_row.append(item.decode('utf-8'))
        else:
            postprocessed_row.append(item)
    return postprocessed_row


def get_config():
    os.path.abspath(os.curdir)
    config_file_path = os.path.join(os.path.abspath(os.curdir), 'iwn-data-entry-tool.cfg')
    fo = read_file(config_file_path)
    host = None
    database_user = None
    database_password = None

    for line in fo:
        line = clean_line(line)
        sp = line.split('=')
        if sp[0] == 'host':
            host = sp[1]
        elif sp[0] == 'database_password':
            database_password = sp[1]
        elif sp[0] == 'database_user':
            database_user = sp[1]
    fo.close()
    return host, database_user, database_password


host, db_user, db_password = get_config()


def execute_query(query, db_name=None, n_rows=None, values=None):
    if db_name == None:
        cnx = mysql.connector.connect(host=host, user=db_user, password=db_password)
        cursor = cnx.cursor()
        if values == None:
            cursor.execute(query)
        else:
            cursor.execute(query, values)
        if "INSERT INTO" not in query and "DELETE FROM" not in query and "UPDATE" not in query:
            if n_rows == FETCH_ONE_ROW:
                row = cursor.fetchone()
                cursor.close()
                if row is not None:
                    row = post_process_row(row)
                return row
            elif n_rows == FETCH_ALL_ROWS:
                rows = cursor.fetchall()
                cursor.close()
                for i in range(0, len(rows)):
                    rows[i] = post_process_row(rows[i])
                return rows
        else:
            cnx.commit()
            cursor.close()
        cnx.close()
    else:
        for db in db_name:
            cnx = mysql.connector.connect(host=host, user=db_user, password=db_password, database=db)
            cursor = cnx.cursor()
            if values == None:
                cursor.execute(query)
            else:
                cursor.execute(query, values)
            if "INSERT INTO" not in query and "DELETE FROM" not in query and "UPDATE" not in query:
                if n_rows == FETCH_ONE_ROW:
                    row = cursor.fetchone()
                    cursor.close()
                    if row is not None:
                        row = post_process_row(row)
                    return row
                elif n_rows == FETCH_ALL_ROWS:
                    rows = cursor.fetchall()
                    cursor.close()
                    for i in range(0, len(rows)):
                        rows[i] = post_process_row(rows[i])
                    return rows
            else:
                cnx.commit()
                cursor.close()
            cnx.close()