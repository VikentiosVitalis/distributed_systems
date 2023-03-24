## [ECE @NTUA](https://www.ece.ntua.gr/en/undergraduate/info) [Distributed Systems](https://www.ece.ntua.gr/en/undergraduate/courses/3377)

<p align="center">
  <img src="noobcash/static/blockchain-logo.png" alt="DS's Custom Image" width="380" height="300" />
</p>

## Description: 
Blockchain is the technology used by most cryptocurrencies and in reality it's a distributed database which enables its users to make transactions with security, without the need of a central authority (i.e. Bank).

Task of this a project is to create the "Noobcash", a simple blockchain system in which transactions
between users are registered and consensus (agreement on any subject by a group of participants) is certified with Proof-of-Work (a decentralized consensus mechanism that requires network members to expend effort in solving an encrypted hexadecimal number).

## Deliverables:
* REST API that implements the functionality of Noobcash and it is placed in the new_src directory.

* CLI client placed in the cli.py file.

* Web page placed in the frontend directory.

## Built with:
The REST API is written in [Python 3.8](https://www.python.org/) using the following libraries:
* [Flask 8.1.1](https://flask-cors.readthedocs.io/en/latest/)
* [Flask-Cors 3.0.10](https://flask-cors.readthedocs.io/en/latest/)
* [pycryptodome 3.17](https://pycryptodome.readthedocs.io/en/latest/)
* [requests 2.27.1](https://requests.readthedocs.io/en/latest/)
* [urllib3 1.26.15](https://urllib3.readthedocs.io/en/stable/)

The webapp is developed using [Django 4.1.7](https://docs.djangoproject.com/en/4.1/) and:
* [Python 3.8](https://www.python.org/)
* [HTML 5](https://developer.mozilla.org/en-US/docs/Web/HTML)
* [CSS 3](https://developer.mozilla.org/en-US/docs/Web/CSS)

## Usage:
Inside the folder 'noobcash' install the necessary requirements:

 ``pip install -r requirements.txt``

 ``npm install``

## Execution:
Bootstrap node:
``python3.8 distributed_systems-main/noobcash/app.py <PORT> <IP> <Number of Children in the System> true``

Simple node: 
``python3.8 distributed_systems-main/noobcash/app.py <PORT> <IP> <Number of Children in the System> no``

Web Interface: ``http://<IP>:<PORT>/``

Run CLI: 

``cli.py <PORT> <IP>``

If you want to run the tests inside the folders 5nodes and 10nodes the last input of every node add 5 or 10 accordingly.


## Evaluation of the system:
We evaluate the performance and the scalability of Noobcash by running the system in [Okeanos](https://okeanos.grnet.gr/home/) and perform from each node 100 transcations to the system. The transactions are placed in /test/transactions path and the script for executing them in stored in the /test directory.

## Contributors:

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
