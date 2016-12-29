import gc
import os
import sys

sys.path.append('/')
import hal
from utils import load_stg

try:
    pythings_version = load_stg()['pythings_version']
    if not pythings_version.upper() == 'FACTORY':
        print('Trying to load Pythings version {}'.format(pythings_version))
        path = '/'+pythings_version
        try:
            os.stat(path)
        except OSError:
            print('Proceeding with factory default version...')
            path='/'
        else:
            print('Updated version found, checking its consistency...')
            try:
                os.stat(path+'/version.py')
            except OSError:
                print('Error, proceeding with factory default version...')
                path='/'
            else:
                print('Valid updated version found.')
                sys.path.append(path)
                os.chdir(path)
    else:
        path='/'

except Exception as e:
    print (hal.get_traceback(e))
    print('Error, proceeding with factory defaults: ',type(e), str(e))
    path='/'

del load_stg

        
# Execute Pythings framework
try:
    import init
    gc.collect()
    init.start(path=path)

except Exception as e:
    import handle_main_error
    handle_main_error.handle(e) # Fallback on factory defaults?
finally:
    os.chdir('/')
    

