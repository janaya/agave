
library(ppls)
library(gplots)
#taking (and plotting) subgraph
cutplot <- function(gs, cutfactor=0.01, drawlabels=TRUE, labelfactor=5, ... ){
##  subg <- subgraph(gs, V(gs)[degreev > cutfactor])
  subg <- gs
#  palette(rev(rich.colors(100,palette="temperature")))
##  V(subg)$color <- 1 + 100 * V(subg)$res
#  V(gs)$color <- 1 + 100 * V(gs)$res
  if(drawlabels==TRUE) {
     plot(subg,
       vertex.label=V(subg)$name,
#       vertex.label.cex = 0.5 + V(subg)$degreev * 2,
       vertex.label.cex = 0.5,
       layout=layout.fruchterman.reingold,
#       vertex.size=1 + V(subg)$degreev * 10,
       vertex.size=1,
#       vertex.color = V(subg)$color,
#       edge.arrow.size=0.5,
       ...
       )
  }
  if(drawlabels=='few') {
     fewlabels <- V(subg)$name
     fewlabels[which(V(subg)$degreev<(cutfactor*labelfactor))]<-NA
     plot(subg,
       vertex.label= fewlabels,
       vertex.label.cex = 0.5 + V(subg)$degreev * 2,
       layout=layout.fruchterman.reingold,
       vertex.size=1 + V(subg)$degreev * 10,
#       vertex.color = V(subg)$color,
#       edge.arrow.size=0.5,
       ...
       )
  } else {
     plot(subg,
       vertex.label = NA,
       layout=layout.fruchterman.reingold,
       vertex.size=1 + V(subg)$degreev * 10,
#       vertex.color = V(subg)$color,
#       edge.arrow.size=0.5,
       ...
       )
  }
  return(subg)
}

postscript("../output_plots/AAc-2010-11-14.eps", fonts=c("serif", "Palatino"))
gscut <- cutplot(AAc)
dev.off()


postscript("../output_plots/CCa-2010-11-14.eps", fonts=c("serif", "Palatino"))
gscut <- cutplot(CCa)
dev.off()


postscript("../output_plots/AAc-filtered-2010-11-14.eps", fonts=c("serif", "Palatino"))
gscut <- cutplot(AAc_wgt)
dev.off()


postscript("../output_plots/CCa-filtered-2010-11-14.eps", fonts=c("serif", "Palatino"))
gscut <- cutplot(CCa_wgt)
dev.off()

