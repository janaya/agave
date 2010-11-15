
###############################################################
# Doing projection
#
projACb <- bipartite.projection(ACb, type=is.bipartite(ACb)$type, probe1=V(ACb)[name=="A1"])
V(ACb)$type <- is.bipartite(ACb)$type
V(projACb$proj2)$name <- V(ACb)[type == TRUE]$name
V(projACb$proj1)$name <- V(ACb)[type == FALSE]$name

AAb <- projACb$proj1
CCb <- projACb$proj2
rm(projACb)
gc() #garbage collect
