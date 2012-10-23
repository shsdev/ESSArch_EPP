# -*- coding: utf-8 -*-
################################################################################
# Note: Generated by soapbox.wsdl2py at 2012-08-30 15:02:03.945215
#       Try to avoid editing it if you might need to regenerate it.
################################################################################


from soapbox import soap, xsd
from soapbox.xsd import UNBOUNDED


################################################################################
# Schemas


# http://ESSArch_Instance.ra.se/StorageLogisticsService


class StoragelogisticsResponse(xsd.ComplexType):
    '''
    '''
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    returncode = xsd.Element(xsd.Integer, nillable=True)

    @classmethod
    def create(cls, returncode):
        instance = cls()
        instance.returncode = returncode
        return instance


class StoragelogisticsRequest(xsd.ComplexType):
    '''
    '''
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    storagemediumid = xsd.Element(xsd.String)
    eventtype = xsd.Element(xsd.Integer)
    storagemediumlocation = xsd.Element(xsd.String)
    storagemediumdestination = xsd.Element(xsd.String)
    useridentifiervalue = xsd.Element(xsd.String)
    userpassword = xsd.Element(xsd.String)
    eventdatetime = xsd.Element(xsd.String)

    @classmethod
    def create(cls, storagemediumid, eventtype, storagemediumlocation, storagemediumdestination, useridentifiervalue, userpassword, eventdatetime):
        instance = cls()
        instance.storagemediumid = storagemediumid
        instance.eventtype = eventtype
        instance.storagemediumlocation = storagemediumlocation
        instance.storagemediumdestination = storagemediumdestination
        instance.useridentifiervalue = useridentifiervalue
        instance.userpassword = userpassword
        instance.eventdatetime = eventdatetime
        return instance


Schema_55b49 = xsd.Schema(
    imports=[],
    targetNamespace='http://ESSArch_Instance.ra.se/StorageLogisticsService',
    elementFormDefault='unqualified',
    simpleTypes=[],
    attributeGroups=[],
    groups=[],
    complexTypes=[],
    elements={'storagelogisticsResponse': xsd.Element(StoragelogisticsResponse()), 'storagelogisticsRequest': xsd.Element(StoragelogisticsRequest())},
)


################################################################################
# Operations


def storagelogistics(request, storagelogisticsRequest):
    '''
    '''
    # TODO: Put your implementation here.
    return storagelogisticsResponse


################################################################################
# Methods


storagelogistics_method = xsd.Method(function=storagelogistics,
    soapAction='http://ESSArch_Instance.ra.se/StorageLogisticsService/storagelogistics',
    input='storagelogisticsRequest',
    inputPartName='parameters',
    output='storagelogisticsResponse',
    outputPartName='parameters',
    operationName='storagelogistics',
)


################################################################################
# SOAP Service


StorageLogisticsService_Port_SERVICE = soap.Service(
    name='StorageLogisticsService_Port',
    targetNamespace='http://ESSArch_Instance.ra.se/StorageLogisticsService',
    location='%(scheme)s://%(host)s/webservice/StorageLogisticsService',
    schema=Schema_55b49,
    version=soap.SOAPVersion.SOAP11,
    methods=[storagelogistics_method],
)


################################################################################
# Django Dispatch


# Uncomment these lines to turn on dispatching:
#from django.views.decorators.csrf import csrf_exempt
#dispatch = csrf_exempt(soap.get_django_dispatch(StorageLogisticsService_Port_SERVICE))

# Put these lines in the urls.py file of your Django project/application:
#urlpatterns += patterns('',
#    (r'^webservice/StorageLogisticsService$', '<module>.dispatch'),
#)

################################################################################
# vim:et:ft=python:nowrap:sts=4:sw=4:ts=4
