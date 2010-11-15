
#################################################################
# Take linear regression eig~bet on CCb
#
centCCb <- data.frame(bet=betweenness(CCb), eig=evcent(CCb)$vector)
# evcent returns lots of data associated with the EC, but we only need the
# leading eigenvector
resCCb<-lm(eig~bet, data=centCCb)$residuals
# We will use the residuals in the next step
V(CCb)$res <- resCCb
centCCb<-transform(centCCb, res=resCCb)

library('ggplot2')
#plotting eigenvector vs. betweenness for CCb graph
postscript("CCb-eigenvector-2010-10-15.eps", fonts=c("serif", "Palatino"))
p<-ggplot(centCCb, aes(x=bet,y=eig,label=V(CCb)$name, colour=resCCb, size=abs(resCCb)))+xlab("Betweenness Centrality")+ylab("Eigenvector Centrality")
p+geom_text()+opts(title="Mesh Concept broader relations from linked data")
dev.off()
####################################################################

# ??? FIXME 
V(CCb)$degreev <- degree(CCb, mode="all")/max(degree(CCb,mode="all"))
#V(AAc_wgt10)$degreev <- degree(AAc_wgt10, mode="all")/max(degree(AAc_wgt10,mode="all"))


# 
postscript("CCb-colors-2010-10-15.eps", fonts=c("serif", "Palatino"), width = 4.0, height = 4.0,)
gscut <- cutplot(CCb, 0.01,  labelfactor=20)
dev.off()



#fgCCb <- fastgreedy.community(as.undirected(CCb))
#membCCb <- community.to.membership(CCb, CCb$merges[1:10], steps=5)
#palette(rev(rich.colors(max(membCCb$membership)+1)))

#postscript("CCb-community-2010-10-15.eps", fonts=c("serif", "Palatino")
#plot(gscut,
#     layout=layout.fruchterman.reingold,
#     vertex.label = V(gscut)$name,
#     vertex.label.cex = 0.2 + V(gscut)$dweight * 2,
#     vertex.size = 5 + V(gscut)$dweight * 10,
#     vertex.color = 1 + memb$membership,
#     edge.arrow.size = 0.5)
#dev.off()


#CCbblocks <- cohesive.blocks(CCb)
#postscript("CCb-blocks-2010-10-15.eps", fonts=c("serif", "Palatino")
#plot(CCbblocks, layout=layout.fruchterman.reingold, vertex.size=1 + V(gCCbblocks)$degreev * 10, edge.arrow.size=0.1, vertex.label=NA)
#dev.off()
