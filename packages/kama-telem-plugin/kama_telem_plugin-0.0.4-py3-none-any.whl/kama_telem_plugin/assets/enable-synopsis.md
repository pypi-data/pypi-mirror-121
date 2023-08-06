# Telemetry Storage Setup

This operation lets you setup or connect to a storage medium required 
for telemetry persistence. The telemetry plugin lets you store application
configuration backups (variables + manifests), as well as
telemetry from operations. 
 

## Choosing a Strategy

You need to decide where the telemetry database will live. If you change
your mind later on, you should be able to migrate your data to another medium.


### Option 1: In-Cluster Managed Database

This approach gives you the best balance of data ownership, cost, 
and simplicity. Here, the plugin is responsible for generating the manifest, 
updating itself, running migrations, etc... 

The cost of this approach in terms of Kubernetes resources, 
is one PersistentVolumeClaim, one deployment, one service, and one secret. 
If you opt for this strategy, a resource-level configuration interface will be 
available in the NMachine client, letting you customize things like the 
PVC's storage class/capacity, the deployment's compute etc...


### Option 2: NMachine Cloud

If data ownership is not a priority, your NMachine can store its telemetry
data on the NMachine cloud. For details about the security and cost of this 
option, visit the **[dedicated guide](https://docs.nmachine.io/nope)**.

The main benefit of this approach, beyond ease of setup, is that it gives
you most straightforward path to sharing configurations between 
NMachines.


### Option 3: Bring your Own Database

If you want fine control over the storage medium, you can provide 
a pointer to a MongoDB database that you manage, whether it be in the
cluster, or in the cloud. 

To find out about the database's requirements, read the 
**[dedicated guide](https://docs.nmachine.io/nope)**.   







