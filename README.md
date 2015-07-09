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
    
If installing python packages fails, additional debian packages might be required. 
They can be installed using `sudo apt-get install <package>`:

* `libssl-dev`
* `libxslt1-dev` 
* `libmysqlclient-dev` 
* `libffi-dev`
* `unixodbc-dev` 

#### Install additional python dependencies

    cd ESSArch_EPP/dependencies/
    tar -xzvf logfileviewer-0.6.2.tar.gz
    cd logfileviewer-0.6.2/
    python setup.py install

### Adapt environment variables

Adapt environment variables in the following file 

    $EPPROOT/.env

and make sure the environment variables are initialised according to your execution environment.

### Additional linux user/group settings

Create user `arch` (needed for `Celery` background processes) and group `epp`, then add both, your 
development user (or the wsgi user in server for server deployment) and the background process user, to this group:

    sudo useradd arch
    sudo groupadd epp
    sudo usermod -g epp arch
    sudo usermod -a -G epp <user>

### Create directories

Note that group `epp` is assigned and that both, the development user (or the wsgi user in server for server deployment) 
and the background process user `arch`, must have the right to write to the log directory.
    
#### Log directories

    sudo mkdir -p /var/log/ESSArch/log
    sudo chown -R <user>:epp /var/log/ESSArch
    sudo chmod -R g+w /var/log/ESSArch
    
#### Data directories
    
    mkdir -p /var/data/ESSArch/ /var/data/ESSArch/Tools /var/data/ESSArch/Tools/env /var/data/ESSArch/Tools/env/data 
    mkdir -p /var/data/ESSArch/reception /var/data/ESSArch/work /var/data/ESSArch/exchange /var/data/ESSArch/control /var/data/ESSArch/ingest
    sudo chown -R <user>:epp /var/data/ESSArch
    sudo chmod -R g+w /var/data/ESSArch

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

## Deployment

### Configure as WSGI app

Edit `/etc/apache2/sites-enabled/000-default` and add the variable `WSGIScriptAlias` which marks the file 
path to the WSGI script, that should be processed by mod_wsgi's wsgi-script handler.:

    WSGIScriptAlias $EPPMOD/wsgi.py

A request for http://earkdev.ait.ac.at/earkweb in this case would cause the server to run the WSGI application defined in /path/to/wsgi-scripts/earkweb.

Additionally create variable `WSGIPythonPath` which defines a directory where to search for Python modules. 

    WSGIScriptAlias /epp $EPPMOD/config/wsgi.py

And create a directory entry:

    <Directory $EPPROOT>
        Options Indexes FollowSymLinks MultiViews
        <Files wsgi.py>
            Order allow,deny
            allow from all
        </Files>
    </Directory>
    
Further information on using Django with Apache and mod_wsgi:

    https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/modwsgi/

### Update demo server deployment

The deployed version is a copy from this Github repository, update is done by sending a pull request on the master branch:

    cd $EPPROOT
    sudo -u www-data git pull origin master
    
## Testing

### Check parameters

Check configuration of parameters.

Configure parameters at MANAGEMENT > Configuration

#### Paths

* path_control - Control filearea
* path_gate - Exchange filearea (This directory contains another directory called "lobby")
* path_ingest - Ingest filearea
* path_mimetypesdefinition - only used for ET (ESSArch Tools) to find the mimetypesdefinition file
* path_reception - Lobby ingest filearea (This directory contains two other direcotorys "cd" and "usb")
* path_work - Work filearea - user workarea in EPP before preservation of IP, example virus control, submit more metadata ...

#### Parameter (core)s

* MD_FTP_ROOT_PATH - filearea to store extra copy metadata files for access purpose
* verifydir - temporary fileare used to verify tapes
* OS - parameter for EPP to how to handle tape robotic devices. Values permitted is "SUSE" och "FEDORA".

#### Parameters

* content_descriptionfile    - sip.xml
* ip_logfile - log.xml
* package_descriptionfile    - info.xml
* preservation_descriptionfile - metadata/premis.xml
* site_profile - SE
* templatefile_log - log.xml
* templatefile_specification - sip.xml
* zone - zone3

#### Archive policys

Select `ProjectX`

Temp work directory - worker process temporary work area
Ingest directory - worker process SIPRecieiver checks this filearea for new IPs (this filearea should be configured to the same value as the previous Paths/path_ingest)

Click on Storage method 1 (Show)

Target (path or barcodeprefix) - filearea for longterm AIP storage (`/var/data/ESSArch/store/disk1`)

### Test run

Test data is available in the directory `$EPPROOT/testdata/`.

Extract the tarfile `test_ip1_path_reception.tar` to the directory configured by parameter "path_reception" (e.g. `/var/data/ESSArch/reception`)".

Extract the second tarfile `test_ip1_path_gate.tar` to the directory configured by parameter "path_gate" (e.g. `/var/data/ESSArch/exchange`).

After you extracted the `test_ip1` run the following steps:

#### Step 1.

CONTROL AREA / CheckIn from Reception

+ Click on media row with test IP
+ Fill in ReqPurpose: test
    - Click on Submit
    - Verifiy if Status = success

#### Step 2.

CONTROL AREA>Preserve Information Package
*  Click on Generation row with test IP
* Fill in ReqPurpose: test
** Click on Submit
** Verifiy if Status = success

Check worker processes logfiles.

If every process step now in workflow ended with "success" the AIP for test IP is now preserved in storage filearea 
"Target" that was configured in storage method 1 of the archive policy.