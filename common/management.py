import cache
import logger
from api import apost, report
import gc
from common import run_controlled
import hal
import sal

def system_management_task(chronos):
    
    updates=False
    
    # Call management API
    response = run_controlled(2,apost,api='/apps/management/')
    if response and 'content' in response: 
        content = response['content']
    else:
        logger.error('Error in receiving/parsing settings, skipping the rest of the management task!')
        return
    del response
    gc.collect()

    # Update settings, Pythings and App.
    try:
        if 'settings' in content and content['settings'] != cache.settings:
            updates='Settings'
            from updates_settings import update_settings
            update_settings(content)

        elif not cache.frozen and cache.settings['pythings_version'].upper() != 'FACTORY' and cache.settings['pythings_version'] != cache.pythings_version:
            updates='Pythings' 
            logger.debug('Downloading new Pythings (running version = "{}"; required version = "{}")'.format(cache.pythings_version, cache.settings['pythings_version']))
            from updates_pythings import update_pythings
            update_pythings(cache.settings['pythings_version'])

        else:
            if cache.settings['app_version'] != cache.app_version:
                updates='App' 
                logger.debug('Downloading new App (running version = "{}"; required version = "{}")'.format(cache.app_version, cache.settings['app_version']))
                from updates_app import update_app
                update_app(cache.settings['app_version'])

    except Exception as e:
        logger.error('Error in management task while updating {} ({}: {}), skipping the rest...'.format(updates, e.__class__.__name__, e))
        logger.debug(sal.get_traceback(e))
        run_controlled(2,report,what='management', status='KO', message='{} {} ({})'.format(e.__class__.__name__, e, sal.get_traceback(e)))
        return False

    gc.collect()

    # If updates, reboot.
    if updates:
        logger.info('Rebooting due to update')
        run_controlled(2,report,what='pythings', status='OK', message='Resetting due to {} update'.format(updates))
        hal.reboot()

    # Management Command (cmd), Command ID (cid) and Management Reply
    msg = content['msg'] if 'msg' in content else None
    mid = content['mid'] if 'mid' in content else None
    rep = None

    # Call App's management
    if cache.app_management_task:
        try:
            logger.debug('Mem free:', sal.get_mem_free())
            rep=cache.app_management_task.call(chronos, msg)
            if mid:
                run_controlled(2,report,what='management', status='OK', message={'mid':mid,'rep':rep})
            else:
                run_controlled(2,report,what='management', status='OK')
                
        except Exception as e:
            logger.error('Error in executing app\'s management task: {} {}'.format(e.__class__.__name__, e))
            logger.debug(sal.get_traceback(e))
            run_controlled(2,report,what='management', status='KO', message='{} {} ({})'.format(e.__class__.__name__, e, sal.get_traceback(e)))
