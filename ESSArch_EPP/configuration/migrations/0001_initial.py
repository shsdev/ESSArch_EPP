# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entity', models.CharField(unique=True, max_length=255)),
                ('value', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['entity'],
                'verbose_name': 'Default value',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ESSArchPolicy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('PolicyName', models.CharField(max_length=255, verbose_name=b'Policy Name')),
                ('PolicyID', models.IntegerField(unique=True, verbose_name=b'Policy ID')),
                ('PolicyStat', models.IntegerField(default=0, verbose_name=b'Policy Status', choices=[(0, b'Disabled'), (1, b'Enabled')])),
                ('AISProjectName', models.CharField(max_length=255, verbose_name=b'AIS Policy Name', blank=True)),
                ('AISProjectID', models.CharField(max_length=255, verbose_name=b'AIS Policy ID', blank=True)),
                ('Mode', models.IntegerField(default=0, choices=[(0, b'Master'), (2, b'AIS')])),
                ('WaitProjectApproval', models.IntegerField(default=2, verbose_name=b'Wait for approval', choices=[(0, b'No'), (2, b'IngestRequest')])),
                ('ChecksumAlgorithm', models.IntegerField(default=1, verbose_name=b'Checksum algorithm', choices=[(1, b'MD5'), (2, b'SHA-256')])),
                ('ValidateChecksum', models.IntegerField(default=1, verbose_name=b'Validate checksum', choices=[(0, b'Disabled'), (1, b'Enabled')])),
                ('ValidateXML', models.IntegerField(default=1, verbose_name=b'Validate XML', choices=[(0, b'Disabled'), (1, b'Enabled')])),
                ('ManualControll', models.IntegerField(default=0, verbose_name=b'Manual Control', choices=[(0, b'Disabled'), (1, b'Enabled')])),
                ('AIPType', models.IntegerField(default=1, verbose_name=b'AIP type', choices=[(1, b'TAR')])),
                ('AIPpath', models.CharField(default=b'/ESSArch/work', max_length=255, verbose_name=b'Temp work directory')),
                ('PreIngestMetadata', models.IntegerField(default=0, verbose_name=b'Pre ingest metadata', choices=[(0, b'Disabled'), (1, b'RES')])),
                ('IngestMetadata', models.IntegerField(default=4, verbose_name=b'Ingest metadata', choices=[(1, b'METS'), (4, b'METS (eArd)')])),
                ('INFORMATIONCLASS', models.IntegerField(default=0, verbose_name=b'Information class', choices=[(0, b'0'), (1, b'1'), (2, b'2'), (3, b'3'), (4, b'4')])),
                ('IngestPath', models.CharField(default=b'/ESSArch/ingest', max_length=255, verbose_name=b'Ingest directory')),
                ('IngestDelete', models.IntegerField(default=1, verbose_name=b'Delete SIP after success to create AIP', choices=[(0, b'Disabled'), (1, b'Enabled')])),
                ('sm_1', models.IntegerField(default=0, verbose_name=b'Storage method', choices=[(0, b'Disabled'), (1, b'Enabled')])),
                ('sm_type_1', models.IntegerField(default=200, verbose_name=b'Type', choices=[(200, b'DISK'), (301, b'IBM-LTO1'), (302, b'IBM-LTO2'), (303, b'IBM-LTO3'), (304, b'IBM-LTO4'), (305, b'IBM-LTO5')])),
                ('sm_format_1', models.IntegerField(default=103, verbose_name=b'Format', choices=[(102, b'102 (Media label)'), (103, b'103 (AIC support)')])),
                ('sm_blocksize_1', models.BigIntegerField(default=1024, verbose_name=b'BlockSize (tape)', choices=[(128, b'64K'), (256, b'128K'), (512, b'256K'), (1024, b'512K'), (2048, b'1024K')])),
                ('sm_maxCapacity_1', models.BigIntegerField(default=0, verbose_name=b'Max capacity (0=Disabled)')),
                ('sm_minChunkSize_1', models.BigIntegerField(default=0, verbose_name=b'Min chunk size', choices=[(0, b'Disabled'), (1000000, b'1 MByte'), (1073741824, b'1 GByte'), (53687091201, b'5 GByte'), (10737418240, b'10 GByte'), (107374182400, b'100 GByte')])),
                ('sm_minContainerSize_1', models.BigIntegerField(default=0, verbose_name=b'Min container size (0=Disabled)', choices=[(0, b'Disabled')])),
                ('sm_minCapacityWarning_1', models.BigIntegerField(default=0, verbose_name=b'Min capacity warning (0=Disabled)')),
                ('sm_target_1', models.CharField(max_length=255, verbose_name=b'Target (path or barcodeprefix)', blank=True)),
                ('sm_2', models.IntegerField(default=0, verbose_name=b'Storage method', choices=[(0, b'Disabled'), (1, b'Enabled')])),
                ('sm_type_2', models.IntegerField(default=200, verbose_name=b'Type', choices=[(200, b'DISK'), (301, b'IBM-LTO1'), (302, b'IBM-LTO2'), (303, b'IBM-LTO3'), (304, b'IBM-LTO4'), (305, b'IBM-LTO5')])),
                ('sm_format_2', models.IntegerField(default=103, verbose_name=b'Format', choices=[(102, b'102 (Media label)'), (103, b'103 (AIC support)')])),
                ('sm_blocksize_2', models.BigIntegerField(default=1024, verbose_name=b'BlockSize (tape)', choices=[(128, b'64K'), (256, b'128K'), (512, b'256K'), (1024, b'512K'), (2048, b'1024K')])),
                ('sm_maxCapacity_2', models.BigIntegerField(default=0, verbose_name=b'Max capacity (0=Disabled)')),
                ('sm_minChunkSize_2', models.BigIntegerField(default=0, verbose_name=b'Min chunk size', choices=[(0, b'Disabled'), (1000000, b'1 MByte'), (1073741824, b'1 GByte'), (53687091201, b'5 GByte'), (10737418240, b'10 GByte'), (107374182400, b'100 GByte')])),
                ('sm_minContainerSize_2', models.BigIntegerField(default=0, verbose_name=b'Min container size (0=Disabled)', choices=[(0, b'Disabled')])),
                ('sm_minCapacityWarning_2', models.BigIntegerField(default=0, verbose_name=b'Min capacity warning (0=Disabled)')),
                ('sm_target_2', models.CharField(max_length=255, verbose_name=b'Target (path or barcodeprefix)', blank=True)),
                ('sm_3', models.IntegerField(default=0, verbose_name=b'Storage method', choices=[(0, b'Disabled'), (1, b'Enabled')])),
                ('sm_type_3', models.IntegerField(default=200, verbose_name=b'Type', choices=[(200, b'DISK'), (301, b'IBM-LTO1'), (302, b'IBM-LTO2'), (303, b'IBM-LTO3'), (304, b'IBM-LTO4'), (305, b'IBM-LTO5')])),
                ('sm_format_3', models.IntegerField(default=103, verbose_name=b'Format', choices=[(102, b'102 (Media label)'), (103, b'103 (AIC support)')])),
                ('sm_blocksize_3', models.BigIntegerField(default=1024, verbose_name=b'BlockSize (tape)', choices=[(128, b'64K'), (256, b'128K'), (512, b'256K'), (1024, b'512K'), (2048, b'1024K')])),
                ('sm_maxCapacity_3', models.BigIntegerField(default=0, verbose_name=b'Max capacity (0=Disabled)')),
                ('sm_minChunkSize_3', models.BigIntegerField(default=0, verbose_name=b'Min chunk size', choices=[(0, b'Disabled'), (1000000, b'1 MByte'), (1073741824, b'1 GByte'), (53687091201, b'5 GByte'), (10737418240, b'10 GByte'), (107374182400, b'100 GByte')])),
                ('sm_minContainerSize_3', models.BigIntegerField(default=0, verbose_name=b'Min container size (0=Disabled)', choices=[(0, b'Disabled')])),
                ('sm_minCapacityWarning_3', models.BigIntegerField(default=0, verbose_name=b'Min capacity warning (0=Disabled)')),
                ('sm_target_3', models.CharField(max_length=255, verbose_name=b'Target (path or barcodeprefix)', blank=True)),
                ('sm_4', models.IntegerField(default=0, verbose_name=b'Storage method', choices=[(0, b'Disabled'), (1, b'Enabled')])),
                ('sm_type_4', models.IntegerField(default=200, verbose_name=b'Type', choices=[(200, b'DISK'), (301, b'IBM-LTO1'), (302, b'IBM-LTO2'), (303, b'IBM-LTO3'), (304, b'IBM-LTO4'), (305, b'IBM-LTO5')])),
                ('sm_format_4', models.IntegerField(default=103, verbose_name=b'Format', choices=[(102, b'102 (Media label)'), (103, b'103 (AIC support)')])),
                ('sm_blocksize_4', models.BigIntegerField(default=1024, verbose_name=b'BlockSize (tape)', choices=[(128, b'64K'), (256, b'128K'), (512, b'256K'), (1024, b'512K'), (2048, b'1024K')])),
                ('sm_maxCapacity_4', models.BigIntegerField(default=0, verbose_name=b'Max capacity (0=Disabled)')),
                ('sm_minChunkSize_4', models.BigIntegerField(default=0, verbose_name=b'Min chunk size', choices=[(0, b'Disabled'), (1000000, b'1 MByte'), (1073741824, b'1 GByte'), (53687091201, b'5 GByte'), (10737418240, b'10 GByte'), (107374182400, b'100 GByte')])),
                ('sm_minContainerSize_4', models.BigIntegerField(default=0, verbose_name=b'Min container size (0=Disabled)', choices=[(0, b'Disabled')])),
                ('sm_minCapacityWarning_4', models.BigIntegerField(default=0, verbose_name=b'Min capacity warning (0=Disabled)')),
                ('sm_target_4', models.CharField(max_length=255, verbose_name=b'Target (path or barcodeprefix)', blank=True)),
            ],
            options={
                'db_table': 'ESSArchPolicy',
                'verbose_name': 'Archive policy',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ESSConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name', models.CharField(max_length=255)),
                ('Value', models.CharField(max_length=255, blank=True)),
                ('Status', models.CharField(max_length=10, blank=True)),
            ],
            options={
                'db_table': 'ESSConfig',
                'verbose_name': 'Parameter (core)',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ESSProc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name', models.CharField(max_length=255)),
                ('Path', models.CharField(max_length=255)),
                ('LogFile', models.CharField(max_length=255)),
                ('expected_pids', models.IntegerField(default=1)),
                ('Time', models.CharField(max_length=4)),
                ('Status', models.CharField(max_length=10)),
                ('Run', models.CharField(max_length=10)),
                ('PID', models.IntegerField()),
                ('child_pids', picklefield.fields.PickledObjectField(null=True, editable=False)),
                ('Pause', models.IntegerField()),
                ('checked', models.DateTimeField(default=b'2014-01-01 00:01')),
                ('alarm', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'ESSProc',
                'verbose_name': 'Worker processes (core)',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IPParameter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('objid', models.CharField(unique=True, max_length=255)),
                ('label', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('createdate', models.CharField(max_length=255)),
                ('recordstatus', models.CharField(max_length=255)),
                ('deliverytype', models.CharField(max_length=255)),
                ('deliveryspecification', models.CharField(max_length=255)),
                ('submissionagreement', models.CharField(max_length=255)),
                ('previoussubmissionagreement', models.CharField(max_length=255)),
                ('datasubmissionsession', models.CharField(max_length=255)),
                ('packagenumber', models.CharField(max_length=255)),
                ('referencecode', models.CharField(max_length=255)),
                ('previousreferencecode', models.CharField(max_length=255)),
                ('appraisal', models.CharField(max_length=255)),
                ('accessrestrict', models.CharField(max_length=255)),
                ('archivist_organization', models.CharField(max_length=255)),
                ('archivist_organization_id', models.CharField(max_length=255)),
                ('archivist_organization_software', models.CharField(max_length=255)),
                ('archivist_organization_software_id', models.CharField(max_length=255)),
                ('creator_organization', models.CharField(max_length=255)),
                ('creator_organization_id', models.CharField(max_length=255)),
                ('creator_individual', models.CharField(max_length=255)),
                ('creator_individual_details', models.CharField(max_length=255)),
                ('creator_software', models.CharField(max_length=255)),
                ('creator_software_id', models.CharField(max_length=255)),
                ('editor_organization', models.CharField(max_length=255)),
                ('editor_organization_id', models.CharField(max_length=255)),
                ('preservation_organization', models.CharField(max_length=255)),
                ('preservation_organization_id', models.CharField(max_length=255)),
                ('preservation_organization_software', models.CharField(max_length=255)),
                ('preservation_organization_software_id', models.CharField(max_length=255)),
                ('startdate', models.CharField(max_length=255)),
                ('enddate', models.CharField(max_length=255)),
                ('aic_id', models.CharField(max_length=255)),
                ('informationclass', models.CharField(max_length=255)),
                ('projectname', models.CharField(max_length=255)),
                ('policyid', models.IntegerField(default=0)),
                ('receipt_email', models.CharField(max_length=255)),
                ('file_id', models.CharField(max_length=255)),
                ('file_name', models.CharField(max_length=255)),
                ('file_createdate', models.CharField(max_length=255)),
                ('file_mime_type', models.CharField(max_length=255)),
                ('file_format', models.CharField(max_length=255)),
                ('file_format_size', models.CharField(max_length=255)),
                ('file_type', models.CharField(max_length=255)),
                ('file_checksum', models.CharField(max_length=255)),
                ('file_checksum_type', models.CharField(max_length=255)),
                ('file_transform_type', models.CharField(max_length=255)),
                ('file_transform_key', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['type'],
                'verbose_name': 'Default values for IP parameter',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LogEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('eventType', models.IntegerField(default=0, unique=True)),
                ('eventDetail', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['eventType'],
                'permissions': (('Can_view_log_menu', 'Can_view_log_menu'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entity', models.CharField(unique=True, max_length=255)),
                ('value', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['entity'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Path',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entity', models.CharField(unique=True, max_length=255)),
                ('value', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['entity'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SchemaProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entity', models.CharField(unique=True, max_length=255)),
                ('value', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['entity'],
                'verbose_name': 'XML schema',
            },
            bases=(models.Model,),
        ),
    ]
