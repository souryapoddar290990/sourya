rm(list=ls())
library(stringdist)

th <- 0.83

data <- read.csv("D:/317583/Jaccard/Input/Input.csv",header=T)
data$FULL_NAME <- toupper(data$FULL_NAME)
data$PAN <- toupper(data$PAN)
data$PAN <- 1
data <- unique(data)

data <- data[1:50,]

Sys.time() -> start
check <- data.frame()

final <- data.frame()

for(i in 1:(nrow(data)-1))
{ seq <- (i+1):nrow(data)-i+nrow(check) 
  check[seq,"dist"] <- stringdist(data$FULL_NAME[i],data$FULL_NAME[(i+1):nrow(data)],method='jaccard',q=2)
  check[seq,"Name_1"] <- data$FULL_NAME[i]
  check[seq,"Name_2"] <- data$FULL_NAME[(i+1):nrow(data)]
}

check_ord <- check[order(-check$dist),]
check_dif <- subset(check_ord,check_ord$dist>th)
check_sim <- subset(check_ord,check_ord$dist<=th)

sim <- c(check_sim$Name_1,check_sim$Name_2)
sim <- data.frame(table(sim))

dif_id <- setdiff(data$FULL_NAME,sim$sim)
final[1:length(dif_id),"FULL_NAME"] <- dif_id
final[1:length(dif_id),"ID"] <- 1:length(dif_id)

check_sim2 <- merge(check_sim,sim,by.x="Name_1",by.y="sim")
check_sim2 <- merge(check_sim2,sim,by.x="Name_2",by.y="sim")
check_sim2$sum <- check_sim2$Freq.x+check_sim2$Freq.y
check_sim2 <- subset(check_sim2,check_sim2$sum==2)

if(nrow(check_sim2)>0)
  for(i in 1:nrow(check_sim2))
  { id <- max(final$ID)+1
    final[nrow(final)+1,"FULL_NAME"] <- check_sim2$Name_1[i]
    final[nrow(final),"ID"] <- id
    final[nrow(final)+1,"FULL_NAME"] <- check_sim2$Name_2[i]
    final[nrow(final),"ID"] <- id
  }
  
com_id <- setdiff(data$FULL_NAME,final$FULL_NAME)

rm(check,check_dif,check_ord,check_sim,check_sim2)

r <- length(com_id)
x <- id
while(r>1&length(com_id)>1)
{
  N <- length(com_id)
  x <- x+1
  list <- 0
  lst <- 99999999
  
  for(r in N:2)
    if(length(list)==1){d <- data.frame(combn(1:N,r))
    for(m in 1:ncol(d))
    { var <- 0
    dt <- com_id[unlist(d[m])]
    for(j in 1:(r-1))
    {var <- max(var,stringdist(dt[j],dt[(j+1):r],method='jaccard',q=2))
    if(var>th) break }
    if(var<=th) {list <- c(list,m)
    lst <- c(lst,var)
    break
    }
    }
    } else break
  
  if(length(list)>1|r!=2)
  {id_name <- com_id[unlist(d[list[which.min(lst)]])]
  com_id <- com_id[-unlist(d[list[which.min(lst)]])]
  } else {
    id_name <- com_id[1]
    com_id <- com_id[-1]
  }
  id_dt <- data.frame("FULL_NAME"=id_name)
  id_dt[,"ID"] <- x
  final <- rbind(final,id_dt)
}
  
id_dt <- data.frame("FULL_NAME"=com_id)
id_dt[,"ID"] <- x+1
final <- rbind(final,id_dt)
  
Sys.time() - start ##1.238254 mins



