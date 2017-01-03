def handle(e):
    # Do not move the following import on top or code will fail (why?!)
    import sal
    print(sal.get_traceback(e))
    print('Error in executing Pythings framework: ',type(e), str(e))
    try:
        from api import report
        report(what='pythings', status='KO', message='{} {} ({})'.format(e.__class__.__name__, e, sal.get_traceback(e)))
    except Exception as e2:
        print('Error in reporting error to Pythings framework: ',type(e2), str(e2))
        print(sal.get_traceback(e2))
    print('\n{}: I will reboot in 5 seconds. CTRL-C now to stop the reboot.'.format(e.__class__.__name__)) 
    import time
    time.sleep(5)
    import hal
    hal.reboot()
