import json
import requests
from flask import Flask, jsonify, request, session, render_template
import sys
from new_src.node import Node, minings, bcLock
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.debug = True

KEY_ID = '-'

if len(sys.argv) != 5:
    print("Usage")
    print("python app.py Port IP number_of_nodes  is_bootstrap_node(true/false)")
    sys.exit(0)

start = Node(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), sys.argv[4])

# Bootstrap node registers child in the blockchain
@app.route('/bootstrap_register', methods=['POST'])
def register():
    pub_key = request.json['pub_key']
    addr = request.json['addrr']
    start.addNode(addr,pub_key)
    response = { 'message': 'Node registered.' }
    return jsonify(response),200

# Send all children info about the id, ring, public keys, genesis block
@app.route('/child_inform', methods=['POST'])
def info():
    res = request.get_json()
    start.setIPList(res['ipList'])
    start.setGenesis(res['genBlock'])
    response = {'message': 'Node Informed'}
    return jsonify(response), 200

@app.route('/broadcast', methods=['POST'])
def broadcast():
    res = request.get_json()
    start.buffer.append([res['sender'], res['receiver'], res['amount'], res['inputs'], res['amtLeft'], res['tid'], res['signature']])
    #print(f'Buffered transaction from {start.getID(res["sender"])} to {start.getID(res["receiver"])}')
    response = {'message': 'Broadcast finished'}
    return jsonify(response), 200


@app.route('/mine', methods=['POST'])
def mining():
    res = request.get_json()
    if start.validateBlock(res['lb'], res['mt']):
        minings.set()
        response = { 'message': 'Current block successfully inserted.' }
        return jsonify(response), 201
    else:
        minings.set()
        response = {'message': 'Current block was not inserted.' }
        return jsonify(response), 400


@app.route('/consensus', methods=['POST'])
def consensus():
    # Consensus begin
    res = request.get_json()
    addrr = res['address'] ## , 'trans_dict': start.transactions_dictionary, 'utxos': start.unspent_coins
    bcLock.acquire()
    msg = {'pub_key': start.getAddr(start.id), 'chain': start.blockchain.convert_chain()}
    bcLock.release()
    requests.post(addrr + '/all_nodes_consensus', json=msg,headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
    response = {'message': 'Consensus done'}
    return jsonify(response), 200


@app.route('/all_nodes_consensus', methods=['POST'])
def cons_data():
    res = request.get_json()
    start.allBlockchains[res['pub_key']] = res['chain']
    tmp = json.loads(res['chain'][-1])
    if tmp['current_hash'] == start.currentBlock.previous_hash:
        start.allBlockchains[res['pub_key']].append(start.currentBlock.convert_block())
    print('Received blockchain from: ', start.getID(res['pub_key']), 'of length:', len(res['chain']))
    response = {'message': 'Consensus Done'}
    return jsonify(response), 200

@app.route('/alltrans', methods=['POST'])
def cons():
    # Consensus done, begin transactions from files
    # start.file_runs.set()
    response = {'message': 'File Transactions Completed'}
    print("COMPLETED ALL TRANSACTIONS")
    return jsonify(response), 200


# Only for Command-Line Interface (CLI)
@app.route('/create_transaction', methods=['POST'])
def newtrans():
    res = request.get_json()
    sender = res['sender']
    receiver = res['address']
    coins = res['coins']

    if sender == receiver:
        response = { 'message': 'You are not allowed to send coins to yourself! Try again.' }
        print(response['message'])
        return jsonify(response), 400
    if not receiver.isnumeric() or int(receiver) < 0 or int(receiver) > len(start.ipList):
        response = {'message' : 'Invalid receiver'}
        print(response['message'])
        return jsonify(response), 400
    if not sender.isnumeric() or int(sender) < 0 or int(sender) > len(start.ipList):
        response = {'message' : 'Invalid sender'}
        print(response['message'])
        return jsonify(response), 400
    if not coins.isnumeric() or int(coins) <= 0 or int(coins) > start.getBalanceOf(sender):
        response = { 'message': "Invalid Amount Given." }
        print(response['message'])    
        return jsonify(response), 400
    
    
    print("COINS = ", coins)

    print('Creating Transaction ', end="")
    #if not start.mining.isSet():
    #    start.mining.wait()
    print('now.')
    start.createTransaction(int(receiver), int(coins))


    response = { 'message': "Transaction Completed" }
    return jsonify(response), 200


@app.route('/view_transactions', methods=['GET'])
def get_trans():
    print(len(start.chain.blocks_list))
    last_transactions = start.chain.blocks_list[-1].transactions
    response = { 'Transactions of the last block (verified)': last_transactions }
    return jsonify(response), 200


@app.route('/show_balance', methods=['GET'])
def get_bal():
    bal = start.getBalance()
    x = len(start.chain.blocks_list)
    y = len(start.buffer)
    print('The balance is: ',x,y)
    response = {
        'Current Balance': bal
    }
    return jsonify(response), 200

# ============ FRONTEND ============= #
 
# Home page
@app.route('/', methods=['GET'])
def home():
    # Keep track of current page
    # session['viewing'] = 'home'
    bal = start.getBalance()

    data = {
        'ADDRESS': start.getFullAddr(),
        'NO_OF_NODES':  len(set(start.ipList)),
        'ID': start.id,
        'SENDER': start.getAddr(start.id),
        'OTHERSK': start.getSK(),
        'KEY_ID': KEY_ID,
        'bal': start.getBalance(),

    }
    return render_template('homepage.html', data=data)

# View latest transaction
@app.route('/view', methods=['GET'])
def viewpage():

    coins = []
    inputs = []
    outputs = []
    receiv = []
    sender = []
    bal = start.getBalance()
    #res1 = start.chain.blocks_list[-1].transactions
    tmp = start.blockchain.blockchain[-1].transactions
    return render_template('viewpage.html', data=tmp)

@app.route('/balance', methods=['GET'])
def balancepage():
    bal = start.getBalance()
    data = {
        'bal': bal,
        'id': str(start.id)
    }
    return render_template('balancepage.html', data=data)

@app.route('/about', methods=['GET'])
def aboutpage():
    return render_template('about.html')

@app.route('/help', methods=['GET'])
def helppage():
    return render_template('help.html')

@app.route('/create_transaction_webapp', methods=['POST'])
def webapp_transaction():
    print("FRONTEND TRANSACTION")
    res = request.get_json()
    print(res)

    sender = res['sender']
    receiver = res['receiver']
    coins = res['amount']

    if not coins.isnumeric():
        response = 'You should provide a number for the coins.'
        return jsonify(response), 400
    elif sender == receiver:
        response = 'You can not send money to yourself.'
        return jsonify(response), 400

    elif start.id != int(sender):
        response = 'This is not your ID.'
        return jsonify(response), 400

    elif int(sender) != start.ID:
        response = 'Your ID is not valid.'
        return jsonify(response), 400
    else:
        payload = {'address': receiver, 'coins': coins}
        payload = json.dumps(payload)
        print(payload)
        URL = 'http://' + str(start.ip) + ':' + str(start.port) + "/"
        response = requests.post(URL + "create_transaction", data=payload, headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
        if response.status_code == 200:
            print('Transaction Done!')
        else:
            print(f'Error: {response.text}')
    response = {'message': 'OKEIII'}
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host=sys.argv[2], port=int(sys.argv[1]), use_reloader=False)
