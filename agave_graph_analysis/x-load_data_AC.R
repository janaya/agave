
gdata <- read.csv('../output_csv/AC.csv', head=TRUE)

library(igraph)
#AC_wgt10<-graph.data.frame(gdata[which(gdata$w > 10),],dir=FALSE)
#AC_swgt10<-simplify(AC_wgt10)
#E(AC_swgt10)$w <- gdata[which(gdata$w >10),]$w

AC <- graph.data.frame(gdata, directed=FALSE, vertices=bip_names)
#AC <- graph.data.frame(gdata, directed=FALSE)
rm(gdata)
#am <- as.matrix(get.adjacency(AC))
#get.adjacency(AC)

#subAC <- subgraph(AC, V(AC)[degreev > cutfactor])

#1.5GB!!
