jac <- similarity.jaccard(AC) #2.5g!!
colnames(jac) <- as.vector(V(AC)$name)
rownames(jac) <- as.vector(V(AC)$name)
gc()

E(AAc)$weight <- apply(get.edgelist(AAc), 1, function(e){return(jac[e[1], e[2]])})
E(CCa)$weight <- apply(get.edgelist(CCa), 1, function(e){return(jac[e[1], e[2]])})


#as gdata
#AAc_wgt10<-graph.data.frame(AAc[which(E(AAc)$weight > 0.3),],dir=FALSE)
#AAc_swgt10<-simplify(AAc_wgt10)
#E(AAc_swgt10)$w <- gdata[which(E(AAc)$weight > 0.3),]$w


#V(AAc_wgt10)$degreev <- degree(AAc_wgt10, mode="all")/max(degree(AAc_wgt10,mode="all"))


# filtering

eAAc <- as.data.frame(get.edgelist(AAc))
eAAc$weight <- as.vector(E(AAc)$weight)
AAc_wgt<- graph.edgelist(as.matrix(eAAc[which(eAAc$weight > 0.3),1:2]),dir=FALSE)


eCCa <- as.data.frame(get.edgelist(CCa))
eCCa$weight <- as.vector(E(CCa)$weight)
CCa_wgt<- graph.edgelist(as.matrix(eCCa[which(eCCa$weight > 0.3),1:2]),dir=FALSE)
