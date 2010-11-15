#loading DATA ++++++++++++++++++++++++++++++++
#library('sqldf')

c_names <- read.csv('../output_csv/C-names.csv',sep=';',head=TRUE)
#f_connames <- file('C_names_list.csv')
#c_names <- sqldf('select * from f_connames', dbname = tempfile(), file.format = list(header=T,sep=';'))
#rm(f_connames)
c_names$index <- sapply(c_names$index, function(x){paste(c("C",x),collapse="")})
c_names$type <- rep("C",length(c_names$index))

a_names <- read.csv('../output_csv/A-names.csv',sep=';',head=TRUE)
a_names$index <- sapply(a_names$index, function(x){paste(c("A",x),collapse="")})
a_names$type <- rep("A",length(a_names$index))

#TODO: add types vector before merge
bip_names <- rbind(a_names, c_names)
