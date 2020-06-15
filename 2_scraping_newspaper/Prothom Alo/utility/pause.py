import requests
import socket
import time

def is_connected():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False
 
def get_resource(url = 'www.google.com'):
    connection_message_positive = 'Connention Established...'
    connection_message_negative = 'Connention Checking...'
    pause_time = 5
    
    while True:
        try:
            if(is_connected()):
                print(connection_message_positive)
                time.sleep(2)
            else:
                print(connection_message_negative + 'TRY')
                time.sleep(2)
        except OSError:
            pass
                
get_resource()
