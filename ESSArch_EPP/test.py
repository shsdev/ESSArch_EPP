from EarkAipCreation.tasks import EarkAipCreation
result = EarkAipCreation().apply_async(('xyz',), queue='smdisk')
result.status
result.result

