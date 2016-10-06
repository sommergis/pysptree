instanceName=sp_strassennetz_unigis.net
time ./SPTSolve_LQueue ../../network_flow/netgen_instances/$instanceName
time ./SPTSolve_LQueue ../../network_flow/netgen_instances/$instanceName allDest
time ./SPTSolve_LDeque ../../network_flow/netgen_instances/$instanceName
time ./SPTSolve_LDeque ../../network_flow/netgen_instances/$instanceName allDest
time ./SPTSolve_Dijkstra ../../network_flow/netgen_instances/$instanceName
time ./SPTSolve_Dijkstra ../../network_flow/netgen_instances/$instanceName allDest
time ./SPTSolve_Heap ../../network_flow/netgen_instances/$instanceName
time ./SPTSolve_Heap ../../network_flow/netgen_instances/$instanceName allDest
