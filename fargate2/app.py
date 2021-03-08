from datetime import datetime
import configparser
import json
import boto3
import mysql.connector
import sentry_sdk


def init_s3(config):
    return boto3.client(
        's3',
        aws_access_key_id=config['AWS']['access_key'],
        aws_secret_access_key=config['AWS']['secret'])


def get_s3_data_as_a_json(config, s3, file_name):
    response = s3.get_object(
        Bucket=config['S3']['datalake'], Key=config['S3'][file_name])
    return json.loads(response['Body'].read())


def init_mysql_connection(config):
    return mysql.connector.connect(
        host=config['Datawarehouse']['host'],
        user=config['Datawarehouse']['user'],
        password=config['Datawarehouse']['password'],
        database=config['Datawarehouse']['db']
    )


def truncate_sql_table(sql, table):
    cursor = sql.cursor()
    cursor.execute('TRUNCATE TABLE `' + table + '`')
    cursor.close()


def store_users_in_datawarehouse(sql, users):
    """users

    user_id	varchar(255) NULL	
    name	varchar(255) NULL	
    email	varchar(255) NULL	
    """

    cursor = sql.cursor()
    for user in users:
        print('insert in users table:',
              user['id'], user['name'], user['email'])
        cursor.execute('INSERT INTO `users` (user_id, name, email) VALUES ("{}", "{}", "{}")'
                       .format(user['id'], user['name'], user['email']))
    cursor.close()


def store_conversations_in_datawarehouse(sql, conversations):
    """conversation

    conv_id	varchar(255) NULL	
    user_id	varchar(255) NULL	
    creation_date	datetime NULL	
    body	longtext NULL
    """

    cursor = sql.cursor()
    for conversation in conversations:
        date_time = datetime.fromtimestamp(conversation['created_at'])
        user_id = (0, conversation['contacts']['contacts'][0]['id'])[
            len(conversation['contacts']['contacts']) > 0]
        print('insert in conversations table:', conversation['id'], user_id,
              date_time, conversation['source']['body'])
        cursor.execute('INSERT INTO `conversation` (conv_id, user_id, creation_date, body) VALUES ("{}", "{}", "{}", "{}")'
                       .format(conversation['id'], user_id, date_time, conversation['source']['body']))
    cursor.close()


def etl_datalake_to_datawarehouse():
    print('etl_datalake_to_datawarehouse')
    config = configparser.ConfigParser()
    config.read('config.ini')

    sentry_sdk.init(config['Sentry']['url'], traces_sample_rate=1.0)

    s3 = init_s3(config)

    users = get_s3_data_as_a_json(config, s3, 'users')
    conversations = get_s3_data_as_a_json(config, s3, 'conversations')

    sql = init_mysql_connection(config)

    truncate_sql_table(sql, 'users')
    truncate_sql_table(sql, 'conversation')  # error in database (missing 's')

    store_users_in_datawarehouse(sql, users)
    store_conversations_in_datawarehouse(sql, conversations)

    sql.commit()
    sql.close()


if __name__ == '__main__':
    etl_datalake_to_datawarehouse()
