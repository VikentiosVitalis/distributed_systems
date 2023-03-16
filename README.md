## [ECE @NTUA](https://www.ece.ntua.gr/en/undergraduate/info) [Distributed Systems](https://www.ece.ntua.gr/en/undergraduate/courses/3377)

<p align="center">
  <img src="https://user-images.githubusercontent.com/62433719/209676755-2f18ca15-2743-4383-920f-a25d3b962c3f.png"
alt="DS's Custom Image" width="250" height="130" />
</p>

## Description 
The task of this project is to create a Blockchain System. The user can interact with the system by using a simple CLI or the Webapp Interface. In Noobcash App you will register nodes and simulate a blockchain system, through processes of sending and receiving money (NBC Coins), consensus, proof of work, mining etc. At the start of the system the first node to register should be the bootstrap node who will create the genesis block. After all the "children" nodes have registered the bootstrap node will transfer to each one of them 100 NBC. Let the transactions begin!

## Built With:
* Python 3.8
* Flask
* HTML/CSS
* JQuery

## Set Up
Inside the folder noobcash:
* pip install -r requirements.txt
* npm install

## Run Application
* bootstrap node: ``python <PORT> <IP> <Number of Children in the System> true``
 example: ``python 5000 127.0.0.1 2 true``
* simple node: ``python <PORT> <IP> <Number of Children in the System> no``
 example: ``python 5001 127.0.0.1 2 false``
* Open Web Interface: Open at your browser the IP and PORT the node is registered.
* Run CLI: ``cli.py <PORT> <IP>``

If you want to run the tests inside the folders 5nodes and 10nodes replace app.py with app_auto.py.

## About us
This project was created by our team consisting of the members below:
- [Mark Ramos](https://github.com/MarkRamosS)
- [Vikentios Vitalis](https://github.com/VikentiosVitalis)
- [Ioannis Lyras](https://github.com/ioannislyras98)