"""
Sirius Poc Library
"""

__version__ = "0.1.0"
__author__ = 'GW Dev'
__credits__ = 'GalaxyWave'

KEYS_SYS_INGRESS = 'sys:ingress'
KEYS_SYS_DEVICE = 'sys:device'
KEYS_SYS_EGRESS = 'sys:egress'
KEYS_SYS_VIEW_REQUEST = 'sys:view:request'
KEYS_SYS_VIEW_PENDING = 'sys:view:pending'
KEYS_SYS_VIEW_RESULT = 'sys:view:result'
KEYS_SYS_PUBLISH_REQUEST = 'sys:publish:request'
KEYS_SYS_PUBLISH_RESULT = 'sys:publish:result'

KEYS_VGW_GROUP_WORKLOAD = 'vgw:group:workload'
KEYS_VGW_GATEWAY_INGRESS = 'vgw:gateway:ingress'
KEYS_VGW_GATEWAY_EGRESS = 'vgw:gateway:egress'
KEYS_VGW_INGRESS = 'vgw:ingress'
KEYS_VGW_EGRESS = 'vgw:egress'
KEYS_VGW_PUBLISH_REQUEST = 'vgw:publish:request'
KEYS_VGW_GATEWAY_WORKLOAD = 'vgw:gateway:workload'

KEYS_VGW_GATEWAY = 'vgw:gateway'



KEYS_VGW_GATEWAY_INGRESS_ASSIGN_TRIGGER = 'vgw:source:assign:trigger'
KEYS_VGW_GATEWAY_INGRESS_REBALANCE_TRIGGER = 'vgw:source:rebalance:trigger'
KEYS_SYS_VIEW_REQUEST_TRIGGER = 'sys:view:request:trigger'

mkkey = lambda prefix, id = '*': f'{prefix}:{id}'
getid = lambda key : key.split(':')[-1]
streamSourceKey = lambda streamId : mkkey(KEYS_SYS_INGRESS, streamId)
streamViewerKey = lambda viewerId : mkkey(KEYS_SYS_EGRESS, viewerId)
streamDeviceKey = lambda deviceId : mkkey(KEYS_SYS_DEVICE, deviceId)

def assignGateway(streamId):
    ovgGrpId = execute('HGET', mkkey(KEYS_SYS_DEVICE, streamId), 'pubGrpId')
    gatewayId = execute('zrange', mkkey(KEYS_VGW_GROUP_WORKLOAD, ovgGrpId), 0, 0)[0]
    execute('SADD', mkkey(KEYS_VGW_GATEWAY_INGRESS, gatewayId), streamId)
    return gatewayId
