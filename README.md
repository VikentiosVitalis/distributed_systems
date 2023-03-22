## [ECE @NTUA](https://www.ece.ntua.gr/en/undergraduate/info) [Distributed Systems](https://www.ece.ntua.gr/en/undergraduate/courses/3377)

<p align="center">
  <img src="noobcash/etc/logo.png" alt="DS's Custom Image" width="380" height="300" />
</p>

## Description: 
Blockchain is the technology used by most cryptocurrencies and in reality it's a distributed database which enables its users to make transactions with security, without the need of a central authority (i.e. Bank).

Task of this a project is to create the "Noobcash", a simple blockchain system in which transactions
between users are registered and consensus (agreement on any subject by a group of participants) is certified with Proof-of-Work (a decentralized consensus mechanism that requires network members to expend effort in solving an encrypted hexadecimal number).

## Deliverables:
A REST API that implements the functionality of Noobcash and is placed in the new_src directory.
A CLI client placed in the cli.py file.
A Web page plac in the frontend directory.

## Built with:
The rest api is written in Python 3.8 using the following libraries:
* Flask 8.1.1
* Flask-Cors 3.0.10
* pycryptodome 3.17
* requests 2.27.1
* urllib3 1.26.15

The webapp is developed using Django 4.1.7 and:
* Python 3.8
* HTML5
* CSS3

## Set-up/usage:
Inside the folder 'noobcash; install the necessary requirements:

 `pip install -r requirements.txt`

 `npm install`

## Run application:
Bootstrap node:

``python <PORT> <IP> <Number of Children in the System> true``

Simple node: 

``python <PORT> <IP> <Number of Children in the System> no``

Open Web Interface: Open at your browser the IP and PORT the node is registered.

Run CLI: 

``cli.py <PORT> <IP>``

If you want to run the tests inside the folders 5nodes and 10nodes replace app.py with app_auto.py.

## Evaluation of the system
We evaluate the performance and the scalability of Noobcash by running the system in Okeanos and perform from each node 100 transcations to the system. The transactions are placed in /test/transactions path and the script for executing them in stored in the /test directory.

## About us:
This project was created by our team consisting of the members below:

<p align="center">
    <a href="https://github.com/MarkRamosS">
      <!--  Mark Ramos  -->
      <img src="/noobcash/static/mark.png" width="10%">
    </a>  

   <a href="https://github.com/VikentiosVitalis">
      <!--  Vikentios Vitalis -->
      <img src="/noobcash/static/vikentios.png" width="10%">
    </a>  

   <a href="https://github.com/ioannislyras98">
      <!--  Giannis Lyras -->
      <img src="/noobcash/static/giannis.png" width="10%">
    </a>  
<p>