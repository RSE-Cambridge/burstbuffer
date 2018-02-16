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

"""
Presents the execution facade in the form needed by the fakewarp cli,
to iterate with Slurm burst buffer
"""

from burstbuffer import execution_facade


def get_pools():
    pool_stats = execution_facade.get_all_pool_stats()
    pools = []
    for pool_stat in pool_stats:
        warp_pool = {
            "id": pool_stat.name,
            "units": "bytes",
            "granularity": pool_stat.slice_bytes,
            "quantity": pool_stat.total_slices,
            "free": pool_stat.free_slices,
        }
        pools.append(warp_pool)
    return {"pools": pools}


def get_instances():
    buffers = execution_facade.get_all_buffers()
    instances = []
    for buff in buffers:
        instance = {
            "id": int(buff.id),
            "capacity": {
                "bytes": int(buff.capacity_bytes),
                "nodes": int(buff.capacity_slices),
            },
            "links": {"session": int(buff.id)},
        }
        instances.append(instance)
    return {'instances': instances}


def get_sessions():
    buffers = execution_facade.get_all_buffers()
    sessions = []
    for buff in buffers:
        session = {
            "id": int(buff.id),
            "created": int(buff.created_at),
            "owner": int(buff.user_id),
        }
        if buff.job_id and not buff.persistent:
            session['token'] = str(buff.job_id)
        elif buff.name and buff.persistent:
            session['token'] = str(buff.name)
        else:
            raise Exception("Unable to convert buffer to fakewarp view")
        sessions.append(session)
    return {"sessions": sessions}
