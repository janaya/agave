
################################################
## gsplot (no cutting)                         #
################################################

gsplot <- function(gs, customLayout=NULL, drawnew=FALSE, cutfactor=0.01, drawlabels=TRUE, labelfactor=5,col_membership=FALSE, ... ){
  subg <- subgraph(gs, V(gs)[dweight > cutfactor])
#  subg <- gs
#  palette(rev(rich.colors(100,palette="temperature")))
##  V(subg)$color <- 1 + 100 * V(subg)$res
#  V(gs)$color <- 1 + 100 * V(gs)$res
  if(col_membership==TRUE) {
     palette(rev(rich.colors(max(V(subg)$membership), palette="temperature")))
     V(subg)$color <- 1 + V(subg)$membership
  }
  if(drawnew==TRUE) {
    E(subg)$width <- 0.5
    E(subg)$color <- 'light grey'
    E(subg)[new==TRUE]$width <- 1
    E(subg)[new==TRUE]$color <- 'dark grey'
  }
  if(drawlabels==TRUE) {
     plot(subg,
       vertex.label=V(subg)$name,
       vertex.label.cex = 0.5 + V(subg)$dweight * 2,
       layout=layout.fruchterman.reingold,
       vertex.size=1 + V(subg)$dweight * 5,
       vertex.color = V(subg)$color,
       ...
       )
  }
  if(drawlabels=='few') {
     fewlabels <- V(subg)$name
     fewlabels[which(V(subg)$dweight<(cutfactor*labelfactor))]<-NA
     plot(subg,
       vertex.label= fewlabels,
       vertex.label.cex = 0.3 + V(subg)$dweight * 0.3,
       vertex.label.color = 'blue',
       vertex.label.family = 'sans',
       vertex.label.dist = 0.2,
       vertex.label.degree = -pi/2, 
       #layout=layout.fruchterman.reingold,
       layout= customLayout,
       vertex.size=0.4 + V(subg)$dweight * 6,
       vertex.color = V(subg)$color,
       ...
       )
  } else {
     plot(subg,
       vertex.label = NA,
       layout=layout.fruchterman.reingold,
       vertex.size=1 + V(subg)$degreev * 10,
       vertex.color = V(subg)$color,
       ...
       )
  }
  return(subg)
}



####################################################
# We redefine the function to take cutfactor again # ???
####################################################
cutplot <- function(gs, cutfactor=0.01, drawlabels=TRUE, labelfactor=5, ... ){
##  subg <- subgraph(gs, V(gs)[degreev > cutfactor])
  subg <- gs
  palette(rev(rich.colors(100,palette="temperature")))
##  V(subg)$color <- 1 + 100 * V(subg)$res
  V(gs)$color <- 1 + 100 * V(gs)$res
  if(drawlabels==TRUE) {
     plot(subg,
       vertex.label=V(subg)$name,
       vertex.label.cex = 0.5 + V(subg)$degreev * 2,
#       vertex.label.cex = 0.5,
       layout=layout.fruchterman.reingold,
       vertex.size=1 + V(subg)$degreev * 10,
       vertex.size=1,
       vertex.color = V(subg)$color,
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

