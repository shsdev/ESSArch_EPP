from EarkAipCreation.tasks import EarkAipCreation;result = EarkAipCreation().apply_async(('xyz',), queue='smdisk');print "Status:"+str(result.status);print "Result:"+str(result.result);
