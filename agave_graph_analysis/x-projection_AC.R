proj <- bipartite.projection(AC, type=is.bipartite(AC)$type, probe1=V(AC)[name=="A1"])
V(AC)$type <- is.bipartite(AC)$type
V(proj$proj2)$name <- V(AC)[type == TRUE]$name
V(proj$proj1)$name <- V(AC)[type == FALSE]$name

AAc <- proj$proj1
CCa <- proj$proj2
rm(proj)
gc()
