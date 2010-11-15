
######################################################
# Community detection over CCb

#take larger connected component (leave out isolated)
gCCb<- decompose.graph(CCb_wgt, max.comps=1, min.vertices=2)
gcCCb <- gCCb[[1]]
V(gcCCb)$dweight <- degree(gcCCb) / max(degree(gcCCb))

#spinglass community
#sgc <- spinglass.community(gCCb[[1]] )
sgc <- spinglass.community(gCCb[[1]], weights=E(gcCCb)$weight, gamma=1.25)
V(gcCCb)$membership <- sgc$membership

#took a while !
postscript("../output_plots/CCb-filtered-2010-10-15_Membership_filter2.eps", fonts=c("sans", "Palatino"))
#bitmap('all-AAc-filtered-2010-08-24.png')
#gscut <- gsplot(CCb_wgt)
gscut <- gsplot(gcCCb, cutfactor=0.3, col_membership=TRUE, drawnew=TRUE, drawlabels='few', labelfactor=1)
dev.off()

########################################################
# Comm. detection over CCa
#

#take larger connected component (leave out isolated)
gCCa<- decompose.graph(CCa_wgt, max.comps=1, min.vertices=2)
gcCCa <- gCCa[[1]] # we only have 35 out of 72 in the connected component
V(gcCCa)$dweight <- degree(gcCCa) / max(degree(gcCCa))

#spinglass community
#sgc <- spinglass.community(gCCb[[1]] )
sgc <- spinglass.community(gCCa[[1]], weights=E(gcCCa)$weight, gamma=1.3)
V(gcCCa)$membership <- sgc$membership

#took a while !
postscript("../output_plots/CCa-filtered-2010-08-29_Membership.eps", fonts=c("sans", "Palatino"))
#bitmap('all-AAc-filtered-2010-08-24.png')
#gscut <- gsplot(CCb_wgt)
gscut <- gsplot(gcCCa, cutfactor=0.00, col_membership=TRUE, drawnew=FALSE, drawlabels='few', labelfactor=1)
dev.off()


########################################################

# Comm. detection over AAb
# FIXME -------- THis is one of the chosen graphics

#take larger connected component (leave out isolated)
gAAb<- decompose.graph(AAb_wgt, max.comps=1, min.vertices=2)
gcAAb <- gAAb[[1]] 
V(gcAAb)$dweight <- degree(gcAAb) / max(degree(gcAAb))

#spinglass community
#sgc <- spinglass.community(gCCb[[1]] )
sgc <- spinglass.community(gcAAb, weights=E(gcAAb)$weight, gamma=1.1)
V(gcAAb)$membership <- sgc$membership


community.AAb <- data.frame(cluster=V(gcAAb)$membership, name=V(gcAAb)$name)
write.csv2(community.AAb, file='./AAb_comm.csv')
#FIXME ^^ here we saved the community clusters


##

acb.layout <- layout.fruchterman.reingold(gcAAb, niter=500)

#took a while !
postscript("../output_plots/AAb-filtered-2010-08-29_Membership.eps", fonts=c("sans", "Palatino"))
gscut <- gsplot(gcAAb, customLayout=acb.layout, cutfactor=0.01, col_membership=TRUE, drawnew=TRUE, drawlabels='few', labelfactor=20)
dev.off()


########################################################

# Comm. detection over AAc
#

#take larger connected component (leave out isolated)
gAAc<- decompose.graph(AAc, max.comps=1, min.vertices=2)
gcAAc <- gAAc[[1]] 
V(gcAAc)$dweight <- degree(gcAAc) / max(degree(gcAAc))

#spinglass community
#sgc <- spinglass.community(gCCb[[1]] )
sgc <- spinglass.community(gcAAc, weights=E(gcAAc)$weight, gamma=1.1)
V(gcAAc)$membership <- sgc$membership

aac.layout <- layout.fruchterman.reingold(gcAAc, niter=500)

#took a while !
postscript("../output_plots/AAc-filtered-2010-08-29_Membership.eps", fonts=c("sans", "Palatino"))
gscut <- gsplot(gcAAc, customLayout=aac.layout, cutfactor=0.01, col_membership=TRUE, drawnew=FALSE, drawlabels='few', labelfactor=500)
dev.off()
