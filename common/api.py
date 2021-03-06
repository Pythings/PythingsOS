
import env
import logger
import json
try:
    from http_extended import post
except ImportError:
    from http import post
import gc

apiver='v1'

# Utility
def check_response(response):
    if response['status'] not in [b'200', 200]:
        try:
            msg=response['content']
            if not msg: msg=response 
        except Exception:
            msg=response
        raise Exception(msg)

# Apis
def apost(api, data={}):
    url = '{}/api/{}{}'.format(env.backend,apiver,api)
    logger.debug('Calling API {} with data'.format(url),data)
    response = post(url, data=data)
    gc.collect()
    logger.info('Got response:',response)
    check_response(response)
    if response['content'] and response['content'] != '\n':
        response['content'] = json.loads(response['content']) 
    return response

def download(file_name, version, dest, what, platform):
    logger.info('Downloading {} in'.format(file_name),dest) 
    response = post(env.backend+'/api/'+apiver+'/'+what+'/get/', {'file_name':file_name, 'version':version, 'token':env.token, 'platform':platform}, dest=dest)
    check_response(response)

# Report
def report(what, status, message=None):
    message_for_logger = message['msg'] if isinstance(message,dict) and 'msg' in message else message
    message_for_logger = message_for_logger[0:30]+'...' if message_for_logger and len(message_for_logger) >30 else message_for_logger
    logger.info('Reporting "{}" as "{}" with message "{}"'.format(what,status,message_for_logger))
    response = apost('/things/report/', {'what':what,'status': status,'msg': message})
    logger.debug('Response:',response)
