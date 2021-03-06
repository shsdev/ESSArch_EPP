#!/usr/bin/env /ESSArch/python27/bin/python
# -*- coding: UTF-8 -*-
'''
    ESSArch - ESSArch is an Electronic Archive system
    Copyright (C) 2010-2013  ES Solutions AB

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Contact information:
    Web - http://www.essolutions.se
    Email - essarch@essolutions.se
'''
__majorversion__ = "2.5"
__revision__ = "$Revision$"
__date__ = "$Date$"
__author__ = "$Author$"
import re
__version__ = '%s.%s' % (__majorversion__,re.sub('[\D]', '',__revision__))

# own models etc
from configuration.models import Parameter, LogEvent, SchemaProfile, IPParameter, Path, ESSConfig, ESSArchPolicy, ESSProc
from essarch.models import eventType_codes, robotdrives, storageMedium
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

import sys,datetime


def createdefaultusers(): # default users, groups and permissions
    
    admingroup, created = Group.objects.get_or_create(name='Admin')
    admingroup.permissions.clear()
    usergroup, created = Group.objects.get_or_create(name='User')
    usergroup.permissions.clear()
    sysgroup, created = Group.objects.get_or_create(name='SysAdmin')
    sysgroup.permissions.clear()


    ct_controlarea_permission = ContentType.objects.get(app_label='controlarea', model='permission') 
    permission_list = ['add_permission','change_permission','delete_permission',
                       'CheckinFromReception','CheckoutToWork','CheckinFromWork',
                       'CheckoutToGate','CheckinFromGate','DiffCheck','PreserveIP']
    permission_obj_list = Permission.objects.filter(codename__in=permission_list, content_type=ct_controlarea_permission).all()
    for permission_obj in permission_obj_list:
        admingroup.permissions.add(permission_obj)
        usergroup.permissions.add(permission_obj)

    ct_essarch_permission = ContentType.objects.get(app_label='essarch', model='permission')
    permission_list = ['essadministrate','ESSArch_RA-OSLO',
                       'list_accessqueue','list_ingestqueue','list_robot','list_storage','list_storageMedium',
                       'infoclass_0','infoclass_1','infoclass_2','infoclass_3','infoclass_4']
    exclude_for_user = ['essadministrate']
    permission_obj_list = Permission.objects.filter(codename__in=permission_list, content_type=ct_essarch_permission)
    for permission_obj in permission_obj_list:
        admingroup.permissions.add(permission_obj)
    for permission_obj in permission_obj_list.exclude(codename__in=exclude_for_user):
        usergroup.permissions.add(permission_obj)

    ct_essarch_robot = ContentType.objects.get(app_label='essarch', model='robot')
    permission_list = ['list_robot']
    permission_obj_list = Permission.objects.filter(codename__in=permission_list, content_type=ct_essarch_robot).all()
    for permission_obj in permission_obj_list:
        admingroup.permissions.add(permission_obj)
        usergroup.permissions.add(permission_obj)

    ct_essarch_storage = ContentType.objects.get(app_label='essarch', model='storage')
    permission_list = ['list_storage']
    permission_obj_list = Permission.objects.filter(codename__in=permission_list, content_type=ct_essarch_storage).all()
    for permission_obj in permission_obj_list:
        admingroup.permissions.add(permission_obj)
        usergroup.permissions.add(permission_obj)

    ct_essarch_storageMedium = ContentType.objects.get(app_label='essarch', model='storageMedium')
    permission_list = ['list_storageMedium']
    permission_obj_list = Permission.objects.filter(codename__in=permission_list, content_type=ct_essarch_storageMedium).all()
    for permission_obj in permission_obj_list:
        admingroup.permissions.add(permission_obj)
        usergroup.permissions.add(permission_obj)

    ct_essarch_accessqueue = ContentType.objects.get(app_label='essarch', model='accessqueue')
    permission_list = ['list_accessqueue','add_accessqueue','change_accessqueue','delete_accessqueue']
    #permission_list = ['add_accessqueue','change_accessqueue','delete_accessqueue']
    permission_obj_list = Permission.objects.filter(codename__in=permission_list, content_type=ct_essarch_accessqueue).all()
    for permission_obj in permission_obj_list:
        admingroup.permissions.add(permission_obj)
        usergroup.permissions.add(permission_obj)

    ct_essarch_ingestqueue = ContentType.objects.get(app_label='essarch', model='ingestqueue')
    permission_list = ['list_ingestqueue','add_ingestqueue','change_ingestqueue','delete_ingestqueue']
    #permission_list = ['add_ingestqueue','change_ingestqueue','delete_ingestqueue']
    permission_obj_list = Permission.objects.filter(codename__in=permission_list, content_type=ct_essarch_ingestqueue).all()
    for permission_obj in permission_obj_list:
        admingroup.permissions.add(permission_obj)
        usergroup.permissions.add(permission_obj)

    ct_storagelogistics_permission = ContentType.objects.get(app_label='storagelogistics', model='permission')
    permission_list = ['StorageLogistics']
    permission_obj_list = Permission.objects.filter(codename__in=permission_list, content_type=ct_storagelogistics_permission).all()
    for permission_obj in permission_obj_list:
        admingroup.permissions.add(permission_obj)
        usergroup.permissions.add(permission_obj)

    ct_auth_permission = ContentType.objects.get(app_label='auth', model='permission')
    permission_list = ['add_permission','change_permission','delete_permission']
    permission_obj_list = Permission.objects.filter(codename__in=permission_list, content_type=ct_auth_permission).all()
    for permission_obj in permission_obj_list:
        sysgroup.permissions.add(permission_obj)

    ct_auth_group = ContentType.objects.get(app_label='auth', model='group')
    permission_list = ['add_group','change_group','delete_group']
    permission_obj_list = Permission.objects.filter(codename__in=permission_list, content_type=ct_auth_group).all()
    for permission_obj in permission_obj_list:
        sysgroup.permissions.add(permission_obj)

    ct_auth_user = ContentType.objects.get(app_label='auth', model='user')
    permission_list = ['add_user','change_user','delete_user']
    permission_obj_list = Permission.objects.filter(codename__in=permission_list, content_type=ct_auth_user).all()
    for permission_obj in permission_obj_list:
        sysgroup.permissions.add(permission_obj)

    ct_configuration_logevent = ContentType.objects.get(app_label='configuration', model='logevent')
    permission_list = ['add_logevent','change_logevent','delete_logevent']
    permission_obj_list = Permission.objects.filter(codename__in=permission_list, content_type=ct_configuration_logevent).all()
    for permission_obj in permission_obj_list:
        sysgroup.permissions.add(permission_obj)

    ct_configuration_parameter = ContentType.objects.get(app_label='configuration', model='parameter')
    permission_list = ['add_parameter','change_parameter','delete_parameter']
    permission_obj_list = Permission.objects.filter(codename__in=permission_list, content_type=ct_configuration_parameter).all()
    for permission_obj in permission_obj_list:
        sysgroup.permissions.add(permission_obj)

    ct_configuration_path = ContentType.objects.get(app_label='configuration', model='path')
    permission_list = ['add_path','change_path','delete_path']
    permission_obj_list = Permission.objects.filter(codename__in=permission_list, content_type=ct_configuration_path).all()
    for permission_obj in permission_obj_list:
        sysgroup.permissions.add(permission_obj)

    ct_configuration_schemaprofile = ContentType.objects.get(app_label='configuration', model='schemaprofile')
    permission_list = ['add_schemaprofile','change_schemaprofile','delete_schemaprofile']
    permission_obj_list = Permission.objects.filter(codename__in=permission_list, content_type=ct_configuration_schemaprofile).all()
    for permission_obj in permission_obj_list:
        sysgroup.permissions.add(permission_obj)

    ct_configuration_ipparameter = ContentType.objects.get(app_label='configuration', model='ipparameter')
    permission_list = ['add_ipparameter','change_ipparameter','delete_ipparameter']
    permission_obj_list = Permission.objects.filter(codename__in=permission_list, content_type=ct_configuration_ipparameter).all()
    for permission_obj in permission_obj_list:
        sysgroup.permissions.add(permission_obj)

    ct_configuration_essarchpolicy = ContentType.objects.get(app_label='configuration', model='essarchpolicy')
    permission_list = ['add_essarchpolicy','change_essarchpolicy','delete_essarchpolicy']
    permission_obj_list = Permission.objects.filter(codename__in=permission_list, content_type=ct_configuration_essarchpolicy).all()
    for permission_obj in permission_obj_list:
        sysgroup.permissions.add(permission_obj)

    ct_configuration_essconfig = ContentType.objects.get(app_label='configuration', model='essconfig')
    permission_list = ['add_essconfig','change_essconfig','delete_essconfig']
    permission_obj_list = Permission.objects.filter(codename__in=permission_list, content_type=ct_configuration_essconfig).all()
    for permission_obj in permission_obj_list:
        sysgroup.permissions.add(permission_obj)

    ct_configuration_essproc = ContentType.objects.get(app_label='configuration', model='essproc')
    permission_list = ['add_essproc','change_essproc','delete_essproc']
    permission_obj_list = Permission.objects.filter(codename__in=permission_list, content_type=ct_configuration_essproc).all()
    for permission_obj in permission_obj_list:
        sysgroup.permissions.add(permission_obj)

    try:
        myuser = User.objects.get(username='admin')
    except User.DoesNotExist:
        myuser = User.objects.create_user('admin', '', 'admin')
        myuser.groups.add(admingroup)
        myuser.is_staff = 1
        myuser.save()

    try:
        myuser = User.objects.get(username='sysadmin')
    except User.DoesNotExist:
        myuser = User.objects.create_user('sysadmin', '', 'sysadmin')
        myuser.groups.add(sysgroup)
        myuser.is_staff = 1
        myuser.save()

    try:
        myuser = User.objects.get(username='essadmin')
    except User.DoesNotExist:
        myuser = User.objects.create_user('essadmin', '', 'essadmin')
        myuser.groups.add(admingroup)
        myuser.is_staff = 1
        myuser.is_superuser = 1
        myuser.save()

    try:
        myuser = User.objects.get(username='user')
    except User.DoesNotExist:
        myuser = User.objects.create_user('user', '', 'user')
        myuser.groups.add(usergroup)
        myuser.is_staff = 1
        myuser.save()

    try:
        myuser = User.objects.get(username='meta')
    except User.DoesNotExist:
        myuser = User.objects.create_user('meta', '', 'meta123')
        myuser.groups.add(usergroup)
        myuser.is_staff = 1
        myuser.save()

    return 0
    

def installdefaultpaths(): # default paths
    
    # First remove all existing data 
    Path.objects.all().delete()

    # create dictionaries for zone
    dct = {
            #'path_reception':'/data/mottak',
            'path_reception':'/mottak',
            'path_gate':'/data/ioessarch/',
            'path_work':'/data/test',
            #'path_control':'/data/control',
            'path_control':'/kontroll',
            'path_ingest':'/data/ingest',
            'path_mimetypesdefinition':'/ESSArch/Tools/env/data',
            }

    # create according to model with two fields
    for key in dct :
        print >> sys.stderr, "**", key
        try:
            le = Path( entity=key, value=dct[key] )
            le.save()
        except:
            pass
    
    return 0 
    
def installogdefaults(): # default logevents
    
    # First remove all existing data 
    LogEvent.objects.all().delete()

    # create logevents dictionaries per zone
    dct = {}
    dct3 = {
            'Received delivery':'21000',
            'Delivery is handed over':'21100',
            'Processing directory structure for IP':'22000',
            'Extracting material':'22100',
            'Testing material':'22200',
            'Changes in the material':'22300',
            'Additions to the material':'22310',
            'Removal of material':'22320',
            'Acquisition of additional information':'22400',
            'Change of metadata':'22500',
            'Letter to creator':'22600',
            }
        
    # set default logevents according to zone
    dct.update(dct3)
    
    # if zone is incorrect
    if dct is None: 
        return 1
    
    # create according to model with two fields
    for key in dct :
        print >> sys.stderr, "**", key
        try:
            le = LogEvent( eventType=dct[key], eventDetail=key )
            le.save()
        except:
            pass

    return 0


def installdefaultschemaprofiles(): # default schema profiles for Sweden and Norway
    
    # First remove all existing data 
    SchemaProfile.objects.all().delete()
    site_profile = "NO"

    if site_profile == "SE" :
        dct = {
               'mets_namespace': 'http://www.loc.gov/METS/',
               'mets_schemalocation': 'http://xml.ra.se/METS/RA_METS_eARD.xsd',
               'mets_profile': 'http://xml.ra.se/METS/RA_METS_eARD.xml',
               'premis_namespace':'http://xml.ra.se/PREMIS',
               'premis_schemalocation':'http://xml.ra.se/PREMIS/RA_PREMIS.xsd',
               'premis_version':'2.0',
               'mods_namespace':'http://www.loc.gov/mods/v3',
               'xlink_namespace':'http://www.w3.org/1999/xlink',
               'xsi_namespace':'http://www.w3.org/2001/XMLSchema-instance',
               'xsd_namespace':'http://www.w3.org/2001/XMLSchema',
               'mix_namespace':'http://xml.ra.se/MIX',
               'mix_schemalocation':'http://xml.ra.se/MIX/RA_MIX.xsd',
               'addml_namespace':'http://xml.ra.se/addml',
               'addml_schemalocation':'http://xml.ra.se/addml/ra_addml.xsd',
               'xhtml_namespace':'http://www.w3.org/1999/xhtml',
               'xhtml_schemalocation':'http://www.w3.org/MarkUp/SCHEMA/xhtml11.xsd'      
               }

    if site_profile == "NO" :
        dct = {
               'mets_namespace': 'http://www.loc.gov/METS/',
               'mets_schemalocation': 'http://xml.ra.se/METS/RA_METS_eARD.xsd',
               'mets_profile': 'http://xml.ra.se/METS/RA_METS_eARD.xml',
               'premis_namespace': 'http://arkivverket.no/standarder/PREMIS',
               'premis_schemalocation': 'http://schema.arkivverket.no/PREMIS/v2.0/DIAS_PREMIS.xsd',
               'premis_version': '2.0',
               'mods_namespace': 'http://www.loc.gov/mods/v3',
               'xlink_namespace': 'http://www.w3.org/1999/xlink',
               'xsi_namespace': 'http://www.w3.org/2001/XMLSchema-instance',
               'xsd_namespace': 'http://www.w3.org/2001/XMLSchema',
               'mix_namespace': 'http://xml.ra.se/MIX',
               'mix_schemalocation': 'http://xml.ra.se/MIX/RA_MIX.xsd',
               'addml_namespace': 'http://www.arkivverket.no/addml',
               'addml_schemalocation': 'http://xml.ra.se/addml/ra_addml.xsd',
               'xhtml_namespace': 'http://www.w3.org/1999/xhtml',
               'xhtml_schemalocation': 'http://www.w3.org/MarkUp/SCHEMA/xhtml11.xsd'      
               }

    # create according to model with two fields
    for key in dct :
        print >> sys.stderr, "**", key
        try:
            le = SchemaProfile( entity=key, value=dct[key] )
            le.save()
        except:
            pass
    
    return 0
######################
def installdefaulteventType_codes(): # default eventType_codes

    eventType_codes_list=((1000,u'Tagit emot objekt föåtidslagring',u'',1,0),
                          (1010,u'Verifiera objektet mot AIS',u'',1,0),
                          (1020,u'Verifiera objektet mot projekt DB',u'',1,0),
                          (1022,u'RES2PREMIS konvertering',u'',1,0),
                          (1025,u'Verifiera objektet format',u'',1,0),
                          (1030,u'Skapa AIP',u'',1,0),
                          (1040,u'Skapa checksumma föIP',u'',1,0),
                          (1041,u'Generera checksumma',u'',1,0),
                          (1042,u'Verifiera checksumma',u'',1,0),
                          (1043,u'Verifiera innehå',u'',1,0),
                          (1050,u'Verifiera AIP',u'',1,0),
                          (1060,u'Ta bort käan till SIP',u'',1,0),
                          (1100,u'Skriv AIP till låtidslagring',u'',1,0),
                          (1101,u'I/O föån',u'',1,0),
                          (1102,u'Skrivning till lagringsmetod disk',u'',1,0),
                          (1103,u'Läing frålagringsmetod disk',u'',1,0),
                          (1104,u'Skrivning till lagringsmetod band',u'',1,0),
                          (1105,u'Läing frålagringsmetod band',u'',1,0),
                          (1150,u'Ta bort käan till AIP',u'',1,0),
                          (1200,u'Dissemination',u'',1,0),
                          (1201,u'DIP Order Request',u'',1,0),
                          (1202,u'DIP Order Accept',u'',1,0),
                          (1203,u'DIP Order Complete',u'',1,0),
                          (1210,u'Extrahera objekt',u'',1,0),
                          (1301,u'Ingest Order Request',u'',1,0),
                          (1302,u'Ingest Order Accept',u'',1,0),
                          (1303,u'Ingest Order Complete',u'',1,0),
                          (2000,u'Montering av band i bandspelare i robot',u'',1,0),
                          (2010,u'Avmontering av band fråbandspelare i robot',u'',1,0),
                          (2201,u'Media quickverify Order Request',u'',1,0),
                          (2202,u'Media quickverify Order Accept',u'',1,0),
                          (2203,u'Media quickverify Order Complete',u'',1,0),
                          (10,u'StorageLogistics Levererad',u'',1,0),
                          (20,u'StorageLogistics Mottagen',u'',1,0),
                          (30,u'StorageLogistics Placerad',u'',1,0),
                          (40,u'StorageLogistics Uttagen',u'',1,0),
                          (30000,u'CheckInFromReception',u'',1,0),
                          (31000,u'CheckOutToWork',u'',1,0),
                          (32000,u'CheckInFromWork',u'',1,0),
                          (33000,u'DiffCheck',u'',1,0),
                          (34000,u'IngestIP',u'',1,0),
                          (35000,u'CheckOutToGateFromWork',u'',1,0),
                          (36000,u'Delete IP',u'',1,0),
    )
    for row in eventType_codes_list:
        if not eventType_codes.objects.filter(code=row[0]).exists():
            print "Adding entry to eventType_codes for %s" % str(row[0])
            eventType_codes_obj = eventType_codes()
            eventType_codes_obj.code=row[0]
            eventType_codes_obj.desc_sv=row[1]
            eventType_codes_obj.desc_en=row[2]
            eventType_codes_obj.localDB=row[3]
            eventType_codes_obj.externalDB=row[4]
            eventType_codes_obj.save()

######################
def installdefaultESSConfig(): # default ESSConfig

    ESSConfig_list=((u'IngestTable',u'IngestObject'),
                    (u'PolicyTable',u'ESSArchPolicy'),
                    (u'StorageTable',u'storage'),
                    (u'RobotTable',u'robot'),
                    (u'RobotDrivesTable',u'robotdrives'),
                    (u'RobotIETable',u'robotie'),
                    (u'RobotReqTable',u'robotreq'),
                    (u'StorageMediumTable',u'storageMedium'),
                    (u'ExtPrjTapedURL',u''),
                    (u'verifydir',u'/ESSArch/verify'),
                    (u'AgentIdentifierValue',u'ESSArch_RA-OSLO'),
                    (u'ExtDBupdate',u'0'),
                    (u'storageMediumLocation',u'IT_OSLO'),
                    (u'MD_FTP_USER',u'meta'),
                    (u'MD_FTP_PASS',u'meta123'),
                    (u'MD_FTP_HOST',u'127.0.0.1'),
                    (u'MD_FTP_PORT',u'2222'),
                    (u'MD_FTP_ROOT_PATH',u'/metadata1'),
                    (u'MD_FTP_ROOT_KEY',u'16'),
                    (u'Robotdev',u'/dev/sg5'),
                    (u'OS',u'FEDORA'),
                    (u'smtp_server',u''),
                    (u'email_from',u'e-archive@essarch.org'),
    )

    for row in ESSConfig_list:
        if not ESSConfig.objects.filter(Name=row[0]).exists():
            print "Adding entry to ESSConfig for %s" % str(row[0])
            ESSConfig_obj = ESSConfig()
            ESSConfig_obj.Name=row[0]
            ESSConfig_obj.Value=row[1]
            ESSConfig_obj.save()

def installdefaultrobotdrives(): # default robotdrives

    robotdrives_list=((0,u'',0,u'Ready',0,u'/dev/nst0',u'IBM_LTO4',u'sn00001',u'fw0001',u'',0),
                      (1,u'',0,u'Ready',0,u'/dev/nst1',u'IBM_LTO4',u'sn00002',u'fw0001',u'',0),
    )
    for row in robotdrives_list:
        if not robotdrives.objects.filter(drive_id=row[0]).exists():
            print "Adding entry to robotdrives for %s" % str(row[0])
            robotdrives_obj = robotdrives()
            robotdrives_obj.drive_id=row[0]
            robotdrives_obj.t_id=row[1]
            robotdrives_obj.slot_id=row[2]
            robotdrives_obj.status=row[3]
            robotdrives_obj.num_mounts=row[4]
            robotdrives_obj.drive_dev=row[5]
            robotdrives_obj.drive_type=row[6]
            robotdrives_obj.drive_serial=row[7]
            robotdrives_obj.drive_firmware=row[8]
            robotdrives_obj.drive_lock=row[9]
            robotdrives_obj.IdleTime=row[10]
            robotdrives_obj.save()

def installdefaultstorageMedium(): # default storageMedium
       
    timestamp = datetime.datetime.now().isoformat()

    if not storageMedium.objects.filter(storageMediumID=u'disk').exists():
        print "Adding disk entry to storageMedium..."
        storageMedium_obj = storageMedium()
        storageMedium_obj.storageMediumUUID=u'fc7d7a5e-9b62-102d-8001-001e4f38d237'
        storageMedium_obj.storageMedium=200
        storageMedium_obj.storageMediumID=u'disk'
        storageMedium_obj.storageMediumDate=timestamp
        storageMedium_obj.storageMediumLocation=u'IT_OSLO'
        storageMedium_obj.storageMediumLocationStatus=50
        storageMedium_obj.storageMediumBlockSize=128
        storageMedium_obj.storageMediumStatus=30
        storageMedium_obj.storageMediumUsedCapacity=0
        storageMedium_obj.storageMediumFormat=103
        storageMedium_obj.storageMediumMounts=0
        storageMedium_obj.linkingAgentIdentifierValue=u'ESSArch_RA-OSLO'
        storageMedium_obj.CreateDate=timestamp
        storageMedium_obj.CreateAgentIdentifierValue=u'ESSArch_RA-OSLO'
        storageMedium_obj.LocalDBdatetime=timestamp
        storageMedium_obj.ExtDBdatetime=timestamp
        storageMedium_obj.save()

def installdefaultESSArchPolicy(): # default ESSArchPolicy

    if not ESSArchPolicy.objects.filter(id=u'1').exists():
        print "Adding NRA entry to ESSArchPolicy..."
        ESSArchPolicy_obj = ESSArchPolicy()
        ESSArchPolicy_obj.id=u'1'
        ESSArchPolicy_obj.PolicyName=u'NRA'
        ESSArchPolicy_obj.PolicyID=u'1'
        ESSArchPolicy_obj.PolicyStat=u'1'
        ESSArchPolicy_obj.AISProjectName=u''
        ESSArchPolicy_obj.AISProjectID=u''
        ESSArchPolicy_obj.Mode=u'0'
        ESSArchPolicy_obj.WaitProjectApproval=u'2'
        ESSArchPolicy_obj.ChecksumAlgorithm=u'2'
        ESSArchPolicy_obj.ValidateChecksum=u'1'
        ESSArchPolicy_obj.ValidateXML=u'1'
        ESSArchPolicy_obj.ManualControll=u'0'
        ESSArchPolicy_obj.AIPType=u'1'
        #ESSArchPolicy_obj.AIPpath=u'/data/essarch_temp'
        ESSArchPolicy_obj.AIPpath=u'/essarch_temp'
        ESSArchPolicy_obj.PreIngestMetadata=u'0'
        ESSArchPolicy_obj.IngestMetadata=u'4'
        ESSArchPolicy_obj.INFORMATIONCLASS=u'1'
        ESSArchPolicy_obj.IngestPath=u'/data/ingest'
        ESSArchPolicy_obj.IngestDelete=u'1'
        ESSArchPolicy_obj.sm_1=u'1'
        ESSArchPolicy_obj.sm_type_1=u'200'
        ESSArchPolicy_obj.sm_format_1=u'103'
        ESSArchPolicy_obj.sm_blocksize_1=u'128'
        ESSArchPolicy_obj.sm_maxCapacity_1=u'0'
        ESSArchPolicy_obj.sm_minChunkSize_1=u'0'
        ESSArchPolicy_obj.sm_minContainerSize_1=u'0'
        ESSArchPolicy_obj.sm_minCapacityWarning_1=u'0'
        #ESSArchPolicy_obj.sm_target_1=u'/data/dsm/dsm00001'
        ESSArchPolicy_obj.sm_target_1=u'/dsm/dsm00001'
        ESSArchPolicy_obj.sm_2=u'0'
        ESSArchPolicy_obj.sm_type_2=u'200'
        ESSArchPolicy_obj.sm_format_2=u'103'
        ESSArchPolicy_obj.sm_blocksize_2=u'128'
        ESSArchPolicy_obj.sm_maxCapacity_2=u'0'
        ESSArchPolicy_obj.sm_minChunkSize_2=u'0'
        ESSArchPolicy_obj.sm_minContainerSize_2=u'0'
        ESSArchPolicy_obj.sm_minCapacityWarning_2=u'0'
        ESSArchPolicy_obj.sm_target_2=u''
        ESSArchPolicy_obj.sm_3=u'0'
        ESSArchPolicy_obj.sm_type_3=u'200'
        ESSArchPolicy_obj.sm_format_3=u'103'
        ESSArchPolicy_obj.sm_blocksize_3=u'128'
        ESSArchPolicy_obj.sm_maxCapacity_3=u'0'
        ESSArchPolicy_obj.sm_minChunkSize_3=u'0'
        ESSArchPolicy_obj.sm_minContainerSize_3=u'0'
        ESSArchPolicy_obj.sm_minCapacityWarning_3=u'0'
        ESSArchPolicy_obj.sm_target_3=u''
        ESSArchPolicy_obj.sm_4=u'0'
        ESSArchPolicy_obj.sm_type_4=u'200'
        ESSArchPolicy_obj.sm_format_4=u'103'
        ESSArchPolicy_obj.sm_blocksize_4=u'128'
        ESSArchPolicy_obj.sm_maxCapacity_4=u'0'
        ESSArchPolicy_obj.sm_minChunkSize_4=u'0'
        ESSArchPolicy_obj.sm_minContainerSize_4=u'0'
        ESSArchPolicy_obj.sm_minCapacityWarning_4=u'0'
        ESSArchPolicy_obj.sm_target_4=u''
        ESSArchPolicy_obj.save()

def installdefaultESSProc(): # default ESSProc

    ESSProc_list=(('1','SIPReceiver','/ESSArch/bin/SIPReceiver.pyc','/ESSArch/log/SIPReceiver.log',30,0,0,0,0),
                   ('3','SIPValidateAIS','/ESSArch/bin/SIPValidateAIS.pyc','/ESSArch/log/SIPValidateAIS.log',5,0,0,0,0),
                   ('4','SIPValidateApproval','/ESSArch/bin/SIPValidateApproval.pyc','/ESSArch/log/SIPValidateApproval.log',5,0,0,0,0),
                   ('5','SIPValidateFormat','/ESSArch/bin/SIPValidateFormat.pyc','/ESSArch/log/SIPValidateFormat.log',5,0,0,0,0),
                   ('6','AIPCreator','/ESSArch/bin/AIPCreator.pyc','/ESSArch/log/AIPCreator.log',5,0,0,0,0),
                   ('7','AIPChecksum','/ESSArch/bin/AIPChecksum.pyc','/ESSArch/log/AIPChecksum.log',5,0,0,0,0),
                   ('8','AIPValidate','/ESSArch/bin/AIPValidate.pyc','/ESSArch/log/AIPValidate.log',5,0,0,0,0),
                   ('9','SIPRemove','/ESSArch/bin/SIPRemove.pyc','/ESSArch/log/SIPRemove.log',5,0,0,0,0),
                   ('10','AIPWriter','/ESSArch/bin/AIPWriter.pyc','/ESSArch/log/AIPWriter.log',15,0,0,0,0),
                   ('11','AIPPurge','/ESSArch/bin/AIPPurge.pyc','/ESSArch/log/AIPPurge.log',5,0,0,0,0),
                   ('12','TLD','/ESSArch/bin/TLD.pyc','/ESSArch/log/TLD.log',5,0,0,0,0),
                   ('13','IOEngine','/ESSArch/bin/IOEngine.pyc','/ESSArch/log/IOEngine.log',5,0,0,0,0),
                   ('14','db_sync_ais','/ESSArch/bin/db_sync_ais.pyc','/ESSArch/log/db_sync_ais.log',10,0,0,0,0),
                   ('16','ESSlogging','/ESSArch/bin/ESSlogging.pyc','/ESSArch/log/ESSlogging.log',5,0,0,0,0),
                   ('17','AccessEngine','/ESSArch/bin/AccessEngine.pyc','/ESSArch/log/AccessEngine.log',5,0,0,0,0),
                   ('18','FTPServer','/ESSArch/bin/FTPServer.pyc','/ESSArch/log/FTPServer.log',5,0,0,0,0),
    )
    for row in ESSProc_list:
        if not ESSProc.objects.filter(Name=row[1]).exists():
            print "Adding entry to ESSProc for %s" % str(row[1])
            ESSProc_obj = ESSProc()
            ESSProc_obj.id=row[0]
            ESSProc_obj.Name=row[1]
            ESSProc_obj.Path=row[2]
            ESSProc_obj.LogFile=row[3]
            ESSProc_obj.Time=row[4]
            ESSProc_obj.Status=row[5]
            ESSProc_obj.Run=row[6]
            ESSProc_obj.PID=row[7]
            ESSProc_obj.Pause=row[8]
            ESSProc_obj.save()

def installdefaultparameters(): # default config parameters
    
    # First remove all data 
    Parameter.objects.all().delete()

    # set default parameters according to zone
    dct = {
           'site_profile':'NO',
           'zone': 'zone3' ,
           'templatefile_log': 'log.xml' ,
           'templatefile_specification':'info.xml',
           'package_descriptionfile':'info.xml',
           'content_descriptionfile':'mets.xml',
           'ip_logfile':'log.xml',
           'preservation_descriptionfile':'administrative_metadata/premis.xml',
           }
    
    # create according to model with two fields
    for key in dct :
        print >> sys.stderr, "**", key
        try:
            le = Parameter( entity=key, value=dct[key] )
            le.save()
        except:
            pass
    
    # install default configuration
    createdefaultusers()             # default users, groups and permissions
    installdefaultpaths()            # default paths
    installdefaultschemaprofiles()   # default schema profiles for Sweden or Norway
    installogdefaults()              # default logevents
    installIPParameter()             # default metadata for IP
    installdefaulteventType_codes()  # default eventType_codes
    installdefaultESSConfig()        # default ESSConfig
    installdefaultrobotdrives()      # default robotdrives
    installdefaultstorageMedium()    # default storageMedium
    installdefaultESSArchPolicy()    # default ESSArchPolicy
    installdefaultESSProc()          # default ESSProc
    
    return 0


def installIPParameter():  # default metadata for IP
    
    # First remove all data 
    IPParameter.objects.all().delete()
    
    # create dictionary for IP elements
    dct = {
           'objid':'UUID:550e8400-e29b-41d4-a716-446655440004',
           'label':'Example of SIP for delivery of personel information',
           'type':'SIP',
           'createdate':'2012-04-26T12:45:00+01:00',
           'recordstatus':'NEW',
           'deliverytype':'ERMS',
           'deliveryspecification':'FGS Personal, version 1',
           'submissionagreement':'RA 13-2011/5329; 2012-04-12',
           'previoussubmissionagreement':'FM 12-2387/12726, 2007-09-19',
           'datasubmissionsession':'Submission, 2012-04-15 15:00',
           'packagenumber':'SIP Number 2938',
           'referencecode':'SE/RA/123456/24/P',
           'previousreferencecode':'SE/FM/123/123.1/123.1.3',
           'appraisal':'Yes',
           'accessrestrict':'Secrecy and PUL',
           'archivist_organization':'Government X',
           'archivist_organization_id':'ORG:2010340987',
           'archivist_organization_software':'HR Employed',
           'archivist_organization_software_id':'5.0.34',
           'creator_organization':'Government X, Dep Y',
           'creator_organization_id':'ORG:2010340987',
           'creator_individual':'Mike Oldfield',
           'creator_individual_details':'+46 (0)8-12 34 56, Mike.Oldfield@company.se',
           'creator_software':'Packageprogram Packager',
           'creator_software_id':'1.0',
           'editor_organization':'Consultancy Company',
           'editor_organization_id':'ORG:2020345987',
           'preservation_organization':'National Archives of X',
           'preservation_organization_id':'ORG:2010340987',
           'preservation_organization_software':'ESSArch',
           'preservation_organization_software_id':'3.0.0',
           'startdate':'2012-01-01', ## kkkk
           'enddate':'2012-12-30',
           'aic_id':'e4d025bc-56b0-11e2-893f-002215836551',
           'informationclass':'1',
           'projectname':'Scanning',
           'policyid':'1',
           'receipt_email':'Mike.Oldfield@company.se',
           'file_id':'ID550e8400-e29b-41d4-a716-4466554400bg', ## kkkk
           'file_name':'file:personalexport.xml',
           'file_createdate':'2012-04-20T13:30:00,+01:00',
           'file_mime_type':'text/xml',
           'file_format':'PDF/A',
           'file_format_size':'8765324',
           'file_type':'Delivery file',
           'file_checksum':'574b69cf71ceb5534c8a2547f5547d',
           'file_checksum_type':'SHA-256',
           'file_transform_type':'DES',
           'file_transform_key':'574b69cf71ceb5534c8a2547f5547d',
           }

    #print dict1.keys()
    #print dict1.values()
    #print dict1.items()
    #print tt3.items()
    
    #new_dict = {}
    #new_lst = []
    
    #new_dict.update(dict2)
    #new_dict.update(dict3)
    #print new_dict.items() 
    
    # create according to model with many fields
    IPParameter.objects.create(**dct)
    #IPMetadata.objects.create(**dct1)  # create from dictionary
    #IPMetadata.objects.filter(id=1).update(**dct1)  # update from dictionary

    return 0

if __name__ == '__main__':
    installdefaultparameters()
