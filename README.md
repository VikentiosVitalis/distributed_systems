## [ECE @NTUA](https://www.ece.ntua.gr/en/undergraduate/info) [Distributed Systems](https://www.ece.ntua.gr/en/undergraduate/courses/3377)

<p align="center">
  <img src="noobcash/etc/logo.png" alt="DS's Custom Image" width="200" height="250" />
</p>

## Description: 
Blockchain is the technology used by most cryptocurrencies and in reality it's a distributed database which enables its users to make transactions with security, without the need of a central authority (i.e. Bank).

Task of this a project is to create the "Noobcash", a simple blockchain system in which transactions
between users are registered and consensus (agreement on any subject by a group of participants) is certified with Proof-of-Work (a decentralized consensus mechanism that requires network members to expend effort in solving an encrypted hexadecimal number).

## Built With:
* Python 3.8
* Flask
* HTML/CSS
* JQuery

## Set Up:
Inside the folder noobcash:
* pip install -r requirements.txt
* npm install

## Run Application:
* bootstrap node: ``python <PORT> <IP> <Number of Children in the System> true``
 example: ``python 5000 127.0.0.1 2 true``
* simple node: ``python <PORT> <IP> <Number of Children in the System> no``
 example: ``python 5001 127.0.0.1 2 false``
* Open Web Interface: Open at your browser the IP and PORT the node is registered.
* Run CLI: ``cli.py <PORT> <IP>``

If you want to run the tests inside the folders 5nodes and 10nodes replace app.py with app_auto.py.

## About us:
This project was created by our team consisting of the members below:
- [Mark Ramos](https://github.com/MarkRamosS)
- [Vikentios Vitalis](https://github.com/VikentiosVitalis)
- [Ioannis Lyras](https://github.com/ioannislyras98)