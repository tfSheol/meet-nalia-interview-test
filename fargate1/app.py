import configparser
import json
import boto3
import requests
import sentry_sdk


def query_data(config, path, result, lambda_filter, lambda_pages, json_key='data', starting_after=''):
    """Execute api query to Intercom api

    :config: configuration values from 'config.ini'
    :path: Intercom api endpoint path (contacts / conversations / ...)
    :result: result array
    :lambda_filter: filter result type
    :lambda_pages: follow next page
    :json_key='data': default data key
    :starting_after='': next valyue for the next page
    """

    response = requests.get(
        '{}/{}'.format(config['Intercom']['api_endpoint'], path),
        params={
            'starting_after': starting_after,
            'per_page': 50  # tmp fix ...
        },
        headers={
            'Authorization': 'Bearer ' + config['Intercom']['access_token'],
            'Accept': 'application/json;charset=UTF-8'
        },
    )
    if response.status_code == 200:
        result.extend(lambda_filter(response.json().get(json_key)))
        print(response.json()['pages'])
        if lambda_pages(response.json()['pages'].get('next')):
            query_data(config, path, result, lambda_filter, lambda_pages, json_key,
                       response.json()['pages']['next'].get('starting_after'))
    return result


def get_contacts(config):
    return query_data(config, 'contacts', [],
                      lambda json_value: [
                          x for x in json_value if x['role'] == 'user'],
                      lambda pages: pages is not None)


def get_conversations(config):
    return query_data(config, 'conversations', [],
                      lambda json_value: json_value,
                      lambda pages: None,  # need fix: get only contacts type conversations
                      'conversations')


def init_s3(config):
    return boto3.client(
        's3',
        aws_access_key_id=config['AWS']['access_key'],
        aws_secret_access_key=config['AWS']['secret'])


def store_in_s3(config, s3, file_name, data):
    print('store', file_name, 'in S3')
    s3.put_object(
        Body=(bytes(json.dumps(data).encode('UTF-8'))),
        Bucket=config['S3']['datalake'],
        Key=config['S3'][file_name])


def import_intercom():
    print('import_intercom')
    config = configparser.ConfigParser()
    config.read('config.ini')

    sentry_sdk.init(config['Sentry']['url'], traces_sample_rate=1.0)

    users = get_contacts(config)
    conversations = get_conversations(config)

    print(len(users), 'users')
    print(len(conversations), 'conversations')

    s3 = init_s3(config)

    store_in_s3(config, s3, 'users', users)
    store_in_s3(config, s3, 'conversations', conversations)


if __name__ == '__main__':
    import_intercom()
