import sys
import json
import datetime

# URL lib parts
from urllib.request import Request, urlopen
from urllib.parse   import urlencode

def main():
    # Check the CLI arguments
    if len(sys.argv)<5 :
        print("Usage: python3 %s <url> <username> <password> <role>"%sys.argv[0])
        return
    
    # Prep the arguments blob
    args = dict()
    args['timestamp'] = datetime.datetime.utcnow().isoformat()
    args['username']  = sys.argv[2]
    args['password']  = sys.argv[3]
    args['role']      = sys.argv[4]

    # Print a message to let the user know what is being tried
    print("Activating user: %s"%args['username'])

    # Setup the data to send
    sargs = dict()
    sargs['arguments']=json.dumps(args)
    sargs['signature']=''
    data = urlencode(sargs)
    #print("sending:\n%s"%data)
    
    # Make the resquest
    req = Request(sys.argv[1] + 'activate_user',data.encode('ascii'),method='POST')
    res = urlopen(req)
    
    # Parse the response
    resp = res.read().decode('ascii')
    
    # Print the result code
    print("Call to LOST returned: %s"%resp)
    

if __name__=='__main__':
    main()