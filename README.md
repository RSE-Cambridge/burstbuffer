# Generic BurstBuffer

[![Build Status](https://www.travis-ci.org/JohnGarbutt/burstbuffer.svg?branch=master)](https://www.travis-ci.org/JohnGarbutt/burstbuffer)

This project is designed to orchestrate the creation of a burst
buffer built using commodity hardware. The buffer can be accessed
by compute nodes using existing parallel file systems.

Users are expected to request a number of I/O slots, which is a
fixed amount of capacity associated with a fixed amount of
bandwidth. The aim being each burst buffer is independent of any
other burst buffer in the system.

Initially we are targeting two access modes:

1. Shared Scratch (all compute nodes access the same namespace,
   files are striped across all burst buffer nodes using PFS)
2. Dedicated Scratch (accessed by a single node, files striped
   across all burst buffer nodes)

In addition to orchestrating the creation of the buffer, there is
also an option to stage in and stage out files to and from an
existing slower storage tier. For example you might copy from
spinning disk based Lustre to an NVMe backed burst buffer.

## Components

Currently we are targeting integrating with Slurm 17.02.9

The packing is based on:
https://github.com/giovtorres/slurm-docker-cluster

## Installation

For standalone usage, try this:

```Console
virtualenv .venv
. .venv/bin/activate
pip install -U pip
pip install .
```

For install with Slurm integration [please read the docker-slurm
README](docker-slurm/README.md)

## Usage

Try out the fake pools example:
```Console
fakewarp --fuction pools
```

## Demo

When using the [./update-buffer.sh](docker-slurm/update-buffer.sh) script
you get the following demo of the burst buffer:

```Console
***Show current system state***
Name=cray DefaultPool=dedicated_nvme Granularity=1TB TotalSpace=20TB FreeSpace=10TB UsedSpace=0
  Flags=EnablePersistent
  StageInTimeout=30 StageOutTimeout=30 ValidateTimeout=5 OtherTimeout=300
  AllowUsers=root,slurm
  GetSysState=/opt/cray/dw_wlm/default/bin/dw_wlm_cli
***Create persistent buffer***
#!/bin/bash
#BB create_persistent name=mytestbuffer capacity=32GB access=striped type=scratch
Submitted batch job 2
Name=cray DefaultPool=dedicated_nvme Granularity=1TB TotalSpace=20TB FreeSpace=9TB UsedSpace=1TB
  Flags=EnablePersistent
  StageInTimeout=30 StageOutTimeout=30 ValidateTimeout=5 OtherTimeout=300
  AllowUsers=root,slurm
  GetSysState=/opt/cray/dw_wlm/default/bin/dw_wlm_cli
  Allocated Buffers:
    Name=mytestbuffer CreateTime=2018-02-22T13:41:16 Pool=dedicated_nvme Size=1TB State=allocated UserID=slurm(995)
  Per User Buffer Use:
    UserID=slurm(995) Used=1TB
***Create per job buffer***
srun --bb="capacity=3TB" bash -c "sleep 10 && echo \$HOSTNAME"
srun: job 3 queued and waiting for resources
Name=cray DefaultPool=dedicated_nvme Granularity=1TB TotalSpace=20TB FreeSpace=6TB UsedSpace=4TB
  Flags=EnablePersistent
  StageInTimeout=30 StageOutTimeout=30 ValidateTimeout=5 OtherTimeout=300
  AllowUsers=root,slurm
  GetSysState=/opt/cray/dw_wlm/default/bin/dw_wlm_cli
  Allocated Buffers:
    JobID=3 CreateTime=2018-02-22T13:41:21 Pool=dedicated_nvme Size=3TB State=allocated UserID=slurm(995)
    Name=mytestbuffer CreateTime=2018-02-22T13:41:16 Pool=dedicated_nvme Size=1TB State=allocated UserID=slurm(995)
  Per User Buffer Use:
    UserID=slurm(995) Used=4TB
***Delete persistent buffer***
#!/bin/bash
#BB destroy_persistent name=mytestbuffer
Submitted batch job 4
srun: job 3 has been allocated resources
slurmctld
***Show all is cleaned up***
Name=cray DefaultPool=dedicated_nvme Granularity=1TB TotalSpace=20TB FreeSpace=13TB UsedSpace=0
  Flags=EnablePersistent
  StageInTimeout=30 StageOutTimeout=30 ValidateTimeout=5 OtherTimeout=300
  AllowUsers=root,slurm
  GetSysState=/opt/cray/dw_wlm/default/bin/dw_wlm_cli
```

## Running tests

To run unit tests:

```Console
tox -epy35
```

To check the style:

```Console
tox -epep8
```
