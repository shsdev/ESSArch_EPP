# Install ESSArch EPP on debian based linux for development

## Requirements

### Debian packages

    sudo apt-get install libxslt1.1 python-libxslt1 libxml2 libxml2-python

### Install and configure MySQL Server

    sudo apt-get install mysql-server

Login and create database 'eark':

    mysql -u root -p<password>
    create database eark;

### Install RabbitMQ

Add the following line to your /etc/apt/sources.list:

    deb http://www.rabbitmq.com/debian/ testing main

Install 

    wget https://www.rabbitmq.com/rabbitmq-signing-key-public.asc

    sudo apt-key add rabbitmq-signing-key-public.asc

    sudo apt-get update
    sudo apt-get install rabbitmq-server

Enable management

    sudo rabbitmq-plugins enable rabbitmq_management

Check availability at

    http://localhost:15672

### Virtual environment 
 
Create a virtual environment (e.g. named earkweb) to install additional python packages separately from the default python installation.

    sudo pip install virtualenv
    sudo pip install virtualenvwrapper
    mkvirtualenv  epp
    workon epp

If the virtual environment is active, this is shown by a prefix in the console:

    (epp)user@machine:~

If it is not active, it can be activated as follows:

    user@machine:~/ESSArch_EPP1$ workon epp

And it can be deactivated again by typing:

    deactivate

## Installation

### Checkout ESSArch_EPP

    git clone https://github.com/shsdev/ESSArch_EPP.git
    
As a result ESSArch_EPP is cloned into the current working directory:

    ESSArch_EPP/

In the following variable `$EPPROOT` refers to the absolute path to the root directory of ESSArch_EPP. 

The ESSArch_EPP modules are available in a sub-directory which is also named "ESSArch_EPP".

    ESSArch_EPP/ESSArch_EPP

In the following variable `$EPPMOD` refers to the absolute path to the sub-directory containing the modules of ESSArch_EPP.

### Install required python packages

Make sure the virtual environment is active, the following list of packages can be installed using the command:

    pip install -r $EPPROOT/requirements.txt

#### Install additional python dependencies

    cd ESSArch_EPP/dependencies/
    tar -xzvf logfileviewer-0.6.2.tar.gz
    cd logfileviewer-0.6.2/
    python setup.py install

### Adapt environment variables

Adapt environment variables in the following file 

    $EPPROOT/.env

and make sure the environment variables are initialised according to your execution environment.

### Create log directory
    
    sudo mkdir -p /var/log/ESSArch/log
    sudo chown -R <user>:<user> /var/log/ESSArch

### Configure database

Adapt MySQL database settings in the following files:

    $EPPMOD/config/settings_dev.py (DATABASES)
    $EPPMOD/workers/ESSDB.py (DATABASES_dict)

Set user=”root”/password=”<password>” and the database name “eark”.

### Prepare database

Create database from Django models

    cd $EPPMOD
    python manage.py syncdb 
    python manage.py migrate 

and initialise database values

    python extra/install_config.py

### Verify if the Django setup is correct

You should be able to run 

    python manage.py runserver

If the basic settings are correct, the message should be similar to the following:

    (epp)<user>@<machine>:$EPPMOD$ python manage.py runserver
    Django version 1.7, using settings 'config.settings_dev'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

### Backend

#### Compile workers

    python -m compileall workers/
    
#### Celery configuration

Adapt the configuration and celery start script:

    $EPPMOD/config/celeryd
    $EPPMOD/extra/celeryd
    
#### Start celery

Start celery daemon:

    cd $EPPMOD/extra
    sudo ./celeryd start

which should give the following result:

    celery init v10.0.
    Using config script: $EPPMOD/config/celeryd
    celery multi v3.1.18 (Cipater)
    > Starting nodes...
	> worker1@<machine>: OK
	
#### Start ESSArch_EPP workers

Start the workers

    cd $EPPMOD/extra
    sudo ./ESSArch.sh start

which should give the following result:

    Start process:  ESSlogging 
    Process ESSlogging now running
    Start process:  SIPReceiver
    Process SIPReceiver now running
    Start process:  SIPValidateAIS
    Process SIPValidateAIS now running
    Start process:  SIPValidateApproval
    Process SIPValidateApproval now running
    Start process:  SIPValidateFormat
    Process SIPValidateFormat now running
    Start process:  AIPCreator
    Process AIPCreator now running
    Start process:  AIPChecksum
    Process AIPChecksum now running
    Start process:  AIPValidate
    Process AIPValidate now running
    Start process:  SIPRemove
    Process SIPRemove now running
    Start process:  TLD
    Process TLD now running
    Start process:  IOEngine
    Process IOEngine now running
    Start process:  AIPWriter
    Process AIPWriter now running
    Start process:  AIPPurge
    Process AIPPurge now running
    Start process:  AccessEngine
    Process AccessEngine now running
    Start process: db_sync_ais
    Process db_sync_ais now running
    Start process: FTPServer
    Process FTPServer now running
