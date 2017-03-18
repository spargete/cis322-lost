import sys
import json
import datetime

# URL lib parts
from urllib.request import Request, urlopen
from urllib.parse   import urlencode

roles = {'logofc' : 'Logistics Officer', 'facofc' : 'Facilities Officer'}

def main():
    # Check the CLI arguments
    if len(sys.argv)<5 :
        print("Usage: python3 %s <url> <username> <password> <role>"%sys.argv[0])
        return
    
    # Prep the arguments blob
    args = dict()
    #args['timestamp'] = datetime.datetime.utcnow().isoformat()
    args['username']  = sys.argv[2]
    args['password']  = sys.argv[3]
    args['role']      = roles[sys.argv[4]]

    # Print a message to let the user know what is being tried
    print("Activating user: %s"%args['username'])

    # Setup the data to send
    #sargs = dict()
    #sargs['arguments']=json.dumps(args)
    #sargs['signature']=''
    data = urlencode(args)
    #print("sending:\n%s"%data)
    
    # Make the resquest
    location = sys.argv[1] + 'activate_user'
    req = Request(location, data.encode('ascii'), method='POST')
    res = urlopen(req)
    
    # Parse the response
    resp = json.loads(res.read().decode('ascii'))
    
    # Print the result code
    print("Call to LOST returned: %s"%resp['result'])

if __name__=='__main__':
    main()