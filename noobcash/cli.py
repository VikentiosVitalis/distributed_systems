import time
import sys
import requests
import json
import new_src.node as node

help_message = '''
Usage:
$ python app.py HOST PORT NUMBER_OF_CHILDREN_NODES IP     Run as child node, N children nodes, IP
$ python app.py HOST PORT N IP                            Run as bootstrap node, for N children nodes, IP of bootstrap
Available commands:
* `t [recepient_address] [amount]`                        Send `amount` NBC to `recepient` node
* `view`                                                  View transactions of the latest block
* `balance`                                               View balance of each wallet (as of last validated block)
* `help`                                                  Print this help message
* `exit`                                                  Exit client (will not stop server)
'''
def signal_handler(sig, frame):
    print("Forced Termination")
    sys.exit(0)

PORT = int(sys.argv[1])
IP = str(sys.argv[2])
URL = 'http://' + str(IP) + ':' + str(PORT) + "/"


ipList = [
    'http://192.168.0.3:5000',
    'http://192.168.0.1:5002',
    'http://192.168.0.5:5003',
    'http://192.168.0.4:5004',
    'http://192.168.0.2:5005'
]


if len(sys.argv) < 3 or len(sys.argv) > 3:
    print("Invalid inputs! Please Type the command as: python cli.py <PORT> <IP>")
    sys.exit(0)

print("\n\n\n Welcome to Noobcash!\n\n\n")

while (1):
    print("Enter a desired action! Type help if want to know the available actions!")
    choice = input()
    # Transaction
    if choice.startswith('t'):
        params = choice.split()

        sender = params[1]
        receiver = params[2]
        coins = params[3]

        payload = {'address': receiver, 'coins': coins}
        payload = json.dumps(payload)

        response = requests.post(ipList[int(sender)] + "/create_transaction", data=payload, headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
        if response.status_code == 200:
            print('Transaction Done!')
        else:
            print(f'Error: {response.text}')

    # view last transaction
    elif choice == 'view':
        response = requests.get(URL + "view_transactions")
        print(response.json())
    # balance
    elif choice == 'balance':
        response = requests.get(URL + "show_balance")
        print(response.json())

    # help
    elif choice == 'help':
        print(help_message)

    elif choice == 'exit':
        sys.exit(0)

    else:
        print("Invalid action. Try again!")
