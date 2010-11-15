
# Plotting AAc without filtering
#
postscript("AAb-2010-10-15.eps", fonts=c("serif", "Palatino"))
#bitmap('all-AAc-not-filtered-2010-08-24.png')
gscut <- gsplot(AAb)
dev.off()

# Plotting AAb filtered
postscript("AAb-filtered-2010-10-15.eps", fonts=c("serif", "Palatino"))
#bitmap('all-AAc-filtered-2010-08-24.png')
gscut <- gsplot(AAb_wgt)
dev.off()


# Plot CCb without filtering

postscript("CCb-2010-10-15", fonts=c("serif", "Palatino"))
#bitmap('all-AAc-filtered-2010-08-24.png')
gscut <- gsplot(CCb)
dev.off()

############################## FOCUSING @ THIS ONE
# RESOURCING ... handy
source('./x-PLOTTING_FUNCTIONS.R')
##################################################

# Plotting CCb filtered
postscript("2009-CCb-filtered-2010-08-28_NEW_EDGES.eps", fonts=c("serif", "Palatino"))
#bitmap('all-AAc-filtered-2010-08-24.png')
#gscut <- gsplot(CCb_wgt)
gscut <- gsplot(CCb_wgt, drawnew=TRUE)
dev.off()

