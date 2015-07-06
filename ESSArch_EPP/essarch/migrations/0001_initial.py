# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import essarch.fields
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessQueue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ReqUUID', models.CharField(max_length=36)),
                ('ReqType', models.IntegerField(null=True, choices=[(3, b'Generate DIP (package)'), (4, b'Generate DIP (package extracted)'), (1, b'Generate DIP (package & package extracted)'), (2, b'Verify StorageMedium'), (5, b'Get AIP to ControlArea')])),
                ('ReqPurpose', models.CharField(max_length=255)),
                ('user', models.CharField(max_length=45)),
                ('password', models.CharField(max_length=45, blank=True)),
                ('ObjectIdentifierValue', models.CharField(max_length=255, blank=True)),
                ('storageMediumID', models.CharField(max_length=45, blank=True)),
                ('Status', models.IntegerField(default=0, null=True, blank=True, choices=[(0, b'Pending'), (2, b'Initiate'), (5, b'Progress'), (20, b'Success'), (100, b'FAIL')])),
                ('Path', models.CharField(max_length=255)),
                ('posted', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'AccessQueue',
                'permissions': (('list_accessqueue', 'Can list access queue'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='agentIdentifier',
            fields=[
                ('id', essarch.fields.BigAutoField(serialize=False, primary_key=True)),
                ('agentIdentifierValue', models.CharField(max_length=45)),
                ('agentName', models.CharField(max_length=45)),
                ('agentType', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'agentIdentifier',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArchiveObject',
            fields=[
                ('id', essarch.fields.BigAutoField(serialize=False, primary_key=True)),
                ('ObjectUUID', models.CharField(unique=True, max_length=36)),
                ('ObjectIdentifierValue', models.CharField(unique=True, max_length=255)),
                ('ObjectPackageName', models.CharField(max_length=255)),
                ('ObjectSize', models.BigIntegerField(null=True)),
                ('ObjectNumItems', models.IntegerField(null=True)),
                ('ObjectMessageDigestAlgorithm', models.IntegerField(null=True)),
                ('ObjectMessageDigest', models.CharField(max_length=128)),
                ('ObjectPath', models.CharField(max_length=255)),
                ('ObjectActive', models.IntegerField(null=True)),
                ('MetaObjectIdentifier', models.CharField(max_length=255)),
                ('MetaObjectSize', models.BigIntegerField(null=True)),
                ('CMetaMessageDigestAlgorithm', models.IntegerField(null=True)),
                ('CMetaMessageDigest', models.CharField(max_length=128)),
                ('PMetaMessageDigestAlgorithm', models.IntegerField(null=True)),
                ('PMetaMessageDigest', models.CharField(max_length=128)),
                ('DataObjectSize', models.BigIntegerField(null=True)),
                ('DataObjectNumItems', models.IntegerField(null=True)),
                ('Status', models.IntegerField(null=True)),
                ('StatusActivity', models.IntegerField(null=True, choices=[(0, b'OK'), (1, b'New object'), (2, b'Receive'), (3, b'Checking'), (4, b'Need of assistance'), (5, b'Progress'), (6, b'Pending writes'), (7, b'ControlArea'), (8, b'WorkArea'), (100, b'FAIL')])),
                ('StatusProcess', models.IntegerField(null=True, choices=[(0, b'Receive new object'), (5, b'The object is ready to remodel'), (9, b'New object stable'), (10, b"Object don't exist in AIS"), (11, b"Object don't have any projectcode in AIS"), (12, b"Object don't have any local policy"), (13, b'Object already have an AIP!'), (14, b'Object is not active!'), (19, b'Object got a policy'), (20, b'Object not updated from AIS'), (21, b'Object not accepted in AIS'), (24, b'Object accepted in AIS'), (25, b'SIP validate'), (26, b'SIP validate failed'), (29, b'SIP validate OK'), (30, b'Create AIP package'), (31, b'AIP create failed'), (39, b'AIP created OK'), (40, b'Create packge checksum'), (49, b'AIP checksum created OK'), (50, b'AIP validate'), (51, b'AIP validate failed'), (59, b'AIP validate OK'), (60, b'Try to remove IngestObject'), (61, b'Failed to remove IngestObject'), (69, b'Remove OK of IngestObject'), (1000, b'Write AIP to longterm storage'), (1001, b'Fail to write AIP'), (1002, b'No empty media available'), (1003, b'Problem to mount media'), (1004, b'Failed to verify tape after full write'), (1999, b'Write AIP OK'), (2000, b'Try to remove temp AIP object'), (2001, b'Failed to remove temp AIP object'), (2009, b'Remove temp AIP object OK'), (3000, b'Archived'), (5000, b'ControlArea'), (5100, b'WorkArea'), (9999, b'Deleted')])),
                ('LastEventDate', models.DateTimeField(null=True)),
                ('linkingAgentIdentifierValue', models.CharField(max_length=45)),
                ('CreateDate', models.DateTimeField(null=True)),
                ('CreateAgentIdentifierValue', models.CharField(max_length=45)),
                ('EntryDate', models.DateTimeField(null=True)),
                ('EntryAgentIdentifierValue', models.CharField(max_length=45)),
                ('OAISPackageType', models.IntegerField(null=True, choices=[(0, b'SIP'), (1, b'AIC'), (2, b'AIP'), (3, b'AIU'), (4, b'DIP')])),
                ('preservationLevelValue', models.IntegerField(null=True)),
                ('DELIVERYTYPE', models.CharField(max_length=255)),
                ('INFORMATIONCLASS', models.IntegerField(null=True)),
                ('Generation', models.IntegerField(null=True)),
                ('LocalDBdatetime', models.DateTimeField(null=True)),
                ('ExtDBdatetime', models.DateTimeField(null=True)),
                ('PolicyId', models.ForeignKey(db_column=b'PolicyId', default=0, to_field=b'PolicyID', to='configuration.ESSArchPolicy')),
            ],
            options={
                'db_table': 'IngestObject',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArchiveObjectData',
            fields=[
                ('id', essarch.fields.BigAutoField(serialize=False, primary_key=True)),
                ('creator', models.CharField(max_length=255)),
                ('label', models.CharField(max_length=255)),
                ('startdate', models.DateTimeField(null=True)),
                ('enddate', models.DateTimeField(null=True)),
                ('UUID', models.ForeignKey(to='essarch.ArchiveObject', db_column=b'UUID', to_field=b'ObjectUUID')),
            ],
            options={
                'db_table': 'Object_data',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArchiveObjectMetadata',
            fields=[
                ('id', essarch.fields.BigAutoField(serialize=False, primary_key=True)),
                ('ObjectIdentifierValue', models.CharField(max_length=255)),
                ('ObjectMetadataType', models.IntegerField(null=True)),
                ('ObjectMetadataServer', models.IntegerField(null=True)),
                ('ObjectMetadataURL', models.CharField(max_length=255)),
                ('ObjectMetadataBLOB', models.TextField()),
                ('linkingAgentIdentifierValue', models.CharField(max_length=45)),
                ('LocalDBdatetime', models.DateTimeField(null=True)),
                ('ExtDBdatetime', models.DateTimeField(null=True)),
                ('ObjectUUID', models.ForeignKey(to='essarch.ArchiveObject', db_column=b'ObjectUUID', to_field=b'ObjectUUID')),
            ],
            options={
                'db_table': 'IngestObjectMetadata',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArchiveObjectRel',
            fields=[
                ('id', essarch.fields.BigAutoField(serialize=False, primary_key=True)),
                ('AIC_UUID', models.ForeignKey(related_name=b'relaic_set', db_column=b'AIC_UUID', to_field=b'ObjectUUID', to='essarch.ArchiveObject')),
                ('UUID', models.ForeignKey(related_name=b'reluuid_set', db_column=b'UUID', to_field=b'ObjectUUID', to='essarch.ArchiveObject')),
            ],
            options={
                'db_table': 'Object_rel',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ControlAreaQueue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ReqUUID', models.CharField(max_length=36)),
                ('ReqType', models.IntegerField(null=True, choices=[(1, b'CheckIn from Reception'), (2, b'CheckOut to Workarea'), (3, b'CheckIn from Workarea'), (4, b'DiffCheck'), (5, b'Preserve Information Package'), (6, b'CheckOut to Gatearea from WorkArea'), (7, b'CheckIn from Gatearea to WorkArea'), (8, b'Delete IP in control/work area')])),
                ('ReqPurpose', models.CharField(max_length=255)),
                ('user', models.CharField(max_length=45)),
                ('password', models.CharField(max_length=45, blank=True)),
                ('ObjectIdentifierValue', models.CharField(max_length=255, blank=True)),
                ('Status', models.IntegerField(default=0, null=True, blank=True, choices=[(0, b'Pending'), (2, b'Initiate'), (5, b'Progress'), (20, b'Success'), (100, b'FAIL')])),
                ('posted', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'ReqControlAreaQueue',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ESSReg001',
            fields=[
                ('id', essarch.fields.BigAutoField(serialize=False, primary_key=True)),
                ('i000', models.IntegerField(null=True)),
                ('i001', models.IntegerField(null=True)),
                ('i002', models.IntegerField(null=True)),
                ('i003', models.IntegerField(null=True)),
                ('i004', models.IntegerField(null=True)),
                ('i005', models.IntegerField(null=True)),
                ('i006', models.IntegerField(null=True)),
                ('i007', models.IntegerField(null=True)),
                ('i008', models.IntegerField(null=True)),
                ('i009', models.IntegerField(null=True)),
                ('i010', models.IntegerField(null=True)),
                ('i011', models.IntegerField(null=True)),
                ('i012', models.IntegerField(null=True)),
                ('i013', models.IntegerField(null=True)),
                ('i014', models.IntegerField(null=True)),
                ('i015', models.IntegerField(null=True)),
                ('i016', models.IntegerField(null=True)),
                ('i017', models.IntegerField(null=True)),
                ('i018', models.IntegerField(null=True)),
                ('i019', models.IntegerField(null=True)),
                ('s000', models.CharField(max_length=255)),
                ('s001', models.CharField(max_length=255)),
                ('s002', models.CharField(max_length=255)),
                ('s003', models.CharField(max_length=255)),
                ('s004', models.CharField(max_length=255)),
                ('s005', models.CharField(max_length=255)),
                ('s006', models.CharField(max_length=255)),
                ('s007', models.CharField(max_length=255)),
                ('s008', models.CharField(max_length=255)),
                ('s009', models.CharField(max_length=255)),
                ('s010', models.CharField(max_length=255)),
                ('s011', models.CharField(max_length=255)),
                ('s012', models.CharField(max_length=255)),
                ('s013', models.CharField(max_length=255)),
                ('s014', models.CharField(max_length=255)),
                ('s015', models.CharField(max_length=255)),
                ('s016', models.CharField(max_length=255)),
                ('s017', models.CharField(max_length=255)),
                ('s018', models.CharField(max_length=255)),
                ('s019', models.CharField(max_length=255)),
                ('ObjectUUID', models.ForeignKey(to='essarch.ArchiveObject', db_column=b'ObjectUUID', to_field=b'ObjectUUID')),
            ],
            options={
                'db_table': 'ESSReg001',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='eventIdentifier',
            fields=[
                ('id', essarch.fields.BigAutoField(serialize=False, primary_key=True)),
                ('eventIdentifierValue', models.CharField(unique=True, max_length=36)),
                ('eventType', models.IntegerField(null=True)),
                ('eventDateTime', models.DateTimeField(null=True)),
                ('eventDetail', models.CharField(max_length=255)),
                ('eventApplication', models.CharField(max_length=50)),
                ('eventVersion', models.CharField(max_length=45)),
                ('eventOutcome', models.IntegerField(null=True)),
                ('eventOutcomeDetailNote', models.CharField(max_length=255)),
                ('linkingAgentIdentifierValue', models.CharField(max_length=45)),
                ('linkingObjectIdentifierValue', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'eventIdentifier',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='eventType_codes',
            fields=[
                ('id', essarch.fields.BigAutoField(serialize=False, primary_key=True)),
                ('code', models.IntegerField(null=True)),
                ('desc_sv', models.CharField(max_length=100)),
                ('desc_en', models.CharField(max_length=100)),
                ('localDB', models.IntegerField(null=True)),
                ('externalDB', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'eventType_codes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IngestQueue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ReqUUID', models.CharField(max_length=36)),
                ('ReqType', models.IntegerField(null=True, choices=[(1, b'Ingest request'), (2, b'Ingest request without AIS')])),
                ('ReqPurpose', models.CharField(max_length=255)),
                ('user', models.CharField(max_length=45)),
                ('password', models.CharField(max_length=45, blank=True)),
                ('ObjectIdentifierValue', models.CharField(max_length=255, blank=True)),
                ('Status', models.IntegerField(default=0, null=True, blank=True, choices=[(0, b'Pending'), (2, b'Initiate'), (5, b'Progress'), (20, b'Success'), (100, b'FAIL')])),
                ('posted', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'ReqIngestQueue',
                'permissions': (('list_ingestqueue', 'Can list ingest queue'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IOqueue',
            fields=[
                ('id', essarch.fields.BigAutoField(serialize=False, primary_key=True)),
                ('cmd', models.IntegerField(null=True)),
                ('cmdprio', models.IntegerField(null=True)),
                ('work_uuid', models.CharField(max_length=36)),
                ('ObjectIdentifierValue', models.CharField(max_length=255)),
                ('ObjectMessageDigest', models.CharField(max_length=128)),
                ('ObjectPath', models.CharField(max_length=255)),
                ('storageMedium', models.IntegerField(null=True)),
                ('storageMediumID', models.CharField(max_length=45)),
                ('sm_list', models.CharField(max_length=255)),
                ('storageMediumBlockSize', models.IntegerField(null=True)),
                ('storageMediumFormat', models.IntegerField(null=True)),
                ('contentLocationValue', models.IntegerField(null=True)),
                ('storageMediumLocation', models.CharField(max_length=45)),
                ('t_prefix', models.CharField(max_length=6)),
                ('WriteSize', models.BigIntegerField(null=True)),
                ('date_created', models.DateTimeField(null=True)),
                ('Status', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'IOqueue',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MigrationQueue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ReqUUID', models.CharField(max_length=36)),
                ('ReqType', models.IntegerField(null=True, choices=[(1, b'Copy IP to new storage')])),
                ('ReqPurpose', models.CharField(max_length=255)),
                ('user', models.CharField(max_length=45)),
                ('password', models.CharField(max_length=45, blank=True)),
                ('ObjectIdentifierValue', picklefield.fields.PickledObjectField(editable=False)),
                ('TargetMediumID', picklefield.fields.PickledObjectField(editable=False)),
                ('Status', models.IntegerField(default=0, null=True, blank=True, choices=[(0, b'Pending'), (2, b'Initiate'), (5, b'Progress'), (20, b'Success'), (100, b'FAIL')])),
                ('Path', models.CharField(max_length=255)),
                ('CopyPath', models.CharField(max_length=255, blank=True)),
                ('task_id', models.CharField(max_length=36, blank=True)),
                ('posted', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'MigrationQueue',
                'permissions': (('list_migrationqueue', 'Can list migration queue'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='permission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'permissions': (('essadministrate', 'ESSArch admin '), ('essaccess', 'ESSArch access'), ('essingest', 'ESSArch ingest'), ('infoclass_0', 'Information Class 0'), ('infoclass_1', 'Information Class 1'), ('infoclass_2', 'Information Class 2'), ('infoclass_3', 'Information Class 3'), ('infoclass_4', 'Information Class 4')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='robot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slot_id', models.IntegerField(null=True)),
                ('drive_id', models.IntegerField(null=True)),
                ('status', models.CharField(max_length=10)),
                ('t_id', models.CharField(max_length=6)),
            ],
            options={
                'db_table': 'robot',
                'permissions': (('list_robot', 'Can list robot'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='robotdrives',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('drive_id', models.IntegerField(null=True)),
                ('t_id', models.CharField(max_length=6)),
                ('slot_id', models.IntegerField(null=True)),
                ('status', models.CharField(max_length=10)),
                ('num_mounts', models.IntegerField(null=True)),
                ('drive_dev', models.CharField(max_length=15)),
                ('drive_type', models.CharField(max_length=15)),
                ('drive_serial', models.CharField(max_length=20)),
                ('drive_firmware', models.CharField(max_length=20)),
                ('drive_lock', models.CharField(max_length=36)),
                ('IdleTime', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'robotdrives',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='robotie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slot_id', models.IntegerField(null=True)),
                ('drive_id', models.IntegerField(null=True)),
                ('status', models.CharField(max_length=10)),
                ('t_id', models.CharField(max_length=6)),
            ],
            options={
                'db_table': 'robotie',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='robotQueue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ReqUUID', models.CharField(max_length=36)),
                ('ReqType', models.IntegerField(null=True, choices=[(50, b'Mount tape'), (51, b'Unmount tape'), (52, b'Unmount tape (force)'), (1, b'Robot inventory')])),
                ('ReqPurpose', models.CharField(max_length=255)),
                ('user', models.CharField(max_length=45)),
                ('password', models.CharField(max_length=45, blank=True)),
                ('MediumID', models.CharField(max_length=45, blank=True)),
                ('Status', models.IntegerField(default=0, null=True, blank=True, choices=[(0, b'Pending'), (2, b'Initiate'), (5, b'Progress'), (20, b'Success'), (100, b'FAIL')])),
                ('task_id', models.CharField(max_length=36, blank=True)),
                ('posted', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'robotQueue',
                'permissions': (('list_robotqueue', 'Can list robot queue'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='storage',
            fields=[
                ('id', essarch.fields.BigAutoField(serialize=False, primary_key=True)),
                ('contentLocation', models.BigIntegerField(null=True)),
                ('ObjectIdentifierValue', models.CharField(max_length=255)),
                ('contentLocationType', models.IntegerField(null=True)),
                ('contentLocationValue', models.CharField(max_length=45)),
                ('storageMediumID', models.CharField(max_length=45)),
                ('LocalDBdatetime', models.DateTimeField(null=True)),
                ('ExtDBdatetime', models.DateTimeField(null=True)),
                ('ObjectUUID', models.ForeignKey(db_column=b'ObjectUUID', to_field=b'ObjectUUID', to='essarch.ArchiveObject', null=True)),
            ],
            options={
                'db_table': 'storage',
                'permissions': (('list_storage', 'Can list storage'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='storageMedium',
            fields=[
                ('id', essarch.fields.BigAutoField(serialize=False, primary_key=True)),
                ('storageMediumUUID', models.CharField(unique=True, max_length=36)),
                ('storageMedium', models.IntegerField(null=True, choices=[(200, b'DISK'), (301, b'IBM-LTO1'), (302, b'IBM-LTO2'), (303, b'IBM-LTO3'), (304, b'IBM-LTO4'), (305, b'IBM-LTO5')])),
                ('storageMediumID', models.CharField(unique=True, max_length=45)),
                ('storageMediumDate', models.DateTimeField(null=True)),
                ('storageMediumLocation', models.CharField(max_length=45)),
                ('storageMediumLocationStatus', models.IntegerField(null=True, choices=[(10, b'10'), (20, b'20'), (30, b'30'), (40, b'40'), (50, b'Robot')])),
                ('storageMediumBlockSize', models.IntegerField(null=True)),
                ('storageMediumUsedCapacity', models.BigIntegerField(null=True)),
                ('storageMediumStatus', models.IntegerField(null=True, choices=[(0, b'Inactive'), (20, b'Write'), (30, b'Full'), (100, b'FAIL')])),
                ('storageMediumFormat', models.IntegerField(null=True, choices=[(102, b'102 (Media label)'), (103, b'103 (AIC support)')])),
                ('storageMediumMounts', models.IntegerField(null=True)),
                ('linkingAgentIdentifierValue', models.CharField(max_length=45)),
                ('CreateDate', models.DateTimeField(null=True)),
                ('CreateAgentIdentifierValue', models.CharField(max_length=45)),
                ('LocalDBdatetime', models.DateTimeField(null=True)),
                ('ExtDBdatetime', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'storageMedium',
                'permissions': (('list_storageMedium', 'Can list storageMedium'),),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='storage',
            name='storageMediumUUID',
            field=models.ForeignKey(db_column=b'storageMediumUUID', to_field=b'storageMediumUUID', to='essarch.storageMedium', null=True),
            preserve_default=True,
        ),
    ]
