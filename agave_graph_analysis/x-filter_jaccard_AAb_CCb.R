
# Taking jaccard coefficient for filtering
#
jacACb <- similarity.jaccard(ACb) #2.5g!!
colnames(jacACb) <- as.vector(V(ACb)$name)
rownames(jacACb) <- as.vector(V(ACb)$name)
gc()

E(AAb)$weight <- apply(get.edgelist(AAb), 1, function(e){return(jacACb[e[1], e[2]])})
E(CCb)$weight <- apply(get.edgelist(CCb), 1, function(e){return(jacACb[e[1], e[2]])})


###################################################################
# Which edges are new with respect to the version without broaders?
#
# we add a "new" column, meaning that the edge did not exist in the
# projections from the original AC.
# i.e., new == edge coming from Broader relations.

### WATCH OUT! we need to have loaded the AAc / CCa projections here
### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

E(AAb)$new <- apply(get.edgelist(AAb), 1, function(e){return( !are.connected(AAc, e[1], e[2]))})
E(CCb)$new <- apply(get.edgelist(CCb), 1, function(e){return( !are.connected(CCa, e[1], e[2]))})

#
#
#
#
#as gdata
#AAc_wgt10<-graph.data.frame(AAc[which(E(AAc)$weight > 0.3),],dir=FALSE)
#AAc_swgt10<-simplify(AAc_wgt10)
#E(AAc_swgt10)$w <- gdata[which(E(AAc)$weight > 0.3),]$w



#plot(AAc_wgt10,
#       vertex.label = NA,
#       layout=layout.fruchterman.reingold,
#       vertex.size=1 + V(AAc_wgt10)$degreev * 10,
##       vertex.color = V(subg)$color,
#       edge.arrow.size=0.5,
#       ...
#       )



####################################################################
## Filtering


# Filtering AAb
#
eAAb <- as.data.frame(get.edgelist(AAb))
eAAb$weight <- as.vector(E(AAb)$weight)
eAAb$new <- as.vector(E(AAb)$new)
AAb_wgt<- graph.edgelist(as.matrix(eAAb[which(eAAb$weight > 0.10),1:2]),dir=FALSE)
E(AAb_wgt)$new <- eAAb[which(eAAb$weight > 0.10),]$new
E(AAb_wgt)$weight <- eAAb[which(eAAb$weight > 0.10),]$weight

# Filtering CCb
#

eCCb <- as.data.frame(get.edgelist(CCb))
eCCb$weight <- as.vector(E(CCb)$weight)
eCCb$new <- as.vector(E(CCb)$new)
CCb_wgt<- graph.edgelist(as.matrix(eCCb[which(eCCb$weight > 0.12),1:2]),dir=FALSE)
E(CCb_wgt)$new <- eCCb[which(eCCb$weight > 0.12),]$new
E(CCb_wgt)$weight <- eCCb[which(eCCb$weight > 0.12),]$weight

