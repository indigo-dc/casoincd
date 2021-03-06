# -*- coding: utf-8 -*-

# Copyright 2014 Spanish National Research Council (CSIC)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import json
import pprint

import caso
from caso import exception


class CloudRecord(object):
    """The CloudRecord class holds information for each of the records.

    This class is versioned, following the Cloud Accounting Record versions.
    """

    # Version 0.2: initial version
    # Version 0.4: Add 0.4 fields
    version = "0.4"

    _v02_fields = [
        "VMUUID",
        "SiteName",
        "MachineName",
        "LocalUserId",
        "LocalGroupId",
        "GlobalUserName",
        "FQAN",
        "Status",
        "StartTime",
        "EndTime",
        "SuspendDuration",
        "WallDuration",
        "CpuDuration",
        "CpuCount",
        "NetworkType",
        "NetworkInbound",
        "NetworkOutbound",
        "Memory",
        "Disk",
        "StorageRecordId",
        "ImageId",
        "CloudType",
    ]

    _v04_fields = _v02_fields + [
        "CloudComputeService",
        "BenchmarkType",
        "Benchmark",
        "PublicIPCount",
        "UserName",
        "ProjectName",
    ]

    _version_field_map = {
        "0.2": _v02_fields,
        "0.4": _v04_fields,
    }

    def __init__(self, uuid, site, name, user_id, group_id, fqan,
                 status=None,
                 start_time=None, end_time=None,
                 suspend_duration=None, wall_duration=None, cpu_duration=None,
                 network_type=None, network_in=None, network_out=None,
                 cpu_count=None, memory=None, disk=None,
                 image_id=None, cloud_type=caso.user_agent,
                 storage_record_id=None,
                 vo=None, vo_group=None, vo_role=None,
                 user_dn=None,
                 compute_service=None,
                 benchmark_value=None, benchmark_type=None,
                 public_ip_count=None, user_name=None, project_name=None):

        self.uuid = uuid
        self.site = site
        self.name = name
        self.user_id = user_id
        self.group_id = group_id
        self.fqan = fqan
        self.status = status
        self.start_time = start_time
        self.end_time = end_time
        self.suspend_duration = suspend_duration
        self.wall_duration = wall_duration
        self.cpu_duration = cpu_duration
        self.network_type = network_type
        self.network_in = network_in
        self.network_out = network_out
        self.cpu_count = cpu_count
        self.memory = memory
        self.disk = disk
        self.image_id = image_id
        self.cloud_type = cloud_type
        self.storage_record_id = storage_record_id
        self.user_dn = user_dn
        self.compute_service = compute_service
        self.benchmark_value = benchmark_value
        self.benchmark_type = benchmark_type
        self.public_ip_count = public_ip_count
        self.user_name = user_name
        self.project_name = project_name

    def __repr__(self):
        return pprint.pformat(self.as_dict())

    def as_dict(self, version=None):
        """Return CloudRecord as a dictionary.

        :param str version: optional, if passed it will format the record
                            acording to that account record version

        :returns: A dict containing the record.
        """
        if version is None:
            version = self.version

        if version not in self._version_field_map:
            raise exception.RecordVersionNotFound(version=version)

        return {k: v for k, v in self.map.items()
                if k in self._version_field_map[version]}

    @property
    def map(self):
        d = {'VMUUID': self.uuid,
             'SiteName': self.site,
             'MachineName': self.name,
             'LocalUserId': self.user_id,
             'LocalGroupId': self.group_id,
             'FQAN': self.fqan,
             'Status': self.status,
             'StartTime': self.start_time,
             'EndTime': self.end_time,
             'SuspendDuration': self.suspend_duration,
             'WallDuration': self.wall_duration,
             'CpuDuration': self.cpu_duration,
             'CpuCount': self.cpu_count,
             'NetworkType': self.network_type,
             'NetworkInbound': self.network_in,
             'NetworkOutbound': self.network_out,
             'Memory': self.memory,
             'Disk': self.disk,
             'StorageRecordId': self.storage_record_id,
             'ImageId': self.image_id,
             'CloudType': self.cloud_type,
             'GlobalUserName': self.user_dn,
             'PublicIPCount': self.public_ip_count,
             'Benchmark': self.benchmark_value,
             'BenchmarkType': self.benchmark_type,
             'CloudComputeService': self.compute_service,
             'UserName': self.user_name,
             'ProjectName': self.project_name,
             }
        return d

    def as_json(self, version=None):
        return json.dumps(self.as_dict(version=version))
