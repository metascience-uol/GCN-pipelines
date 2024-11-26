library(readxl)

steps <- read_excel("Database.xlsx", sheet = "All_steps")
dat <- read_excel("Database_clean.xlsx")

###Defining nodes
nodes <- steps

nodes$Groups.type <- as.factor(nodes$Groups)
nodes[sapply(nodes, is.factor)] <- data.matrix(nodes[sapply(nodes, is.factor)])
clrs <-  c("mediumpurple3", "darkolivegreen3", "firebrick", "darkorange", "gray","dodgerblue")
nodes$size <- 0

for (nd in 1:nrow(nodes)){
  nd_p <- nodes$Names[nd]
  row_nd <- which(apply(dat, 1, function(x2) all(nd_p %in% x2)))
  nodes$size[[nd]] <- length(row_nd)
}

###Defining links
links <- expand.grid(source = nodes$Names, target = nodes$Names)
links$value <- 0

for (pp in 1:nrow(links)){
  st_l <- as.character(c(links$source[pp], links$target[pp]))
  row_l <- which(apply(dat, 1, function(x1) {
    idx_l <- match(st_l, x1)
    all(!is.na(idx_l)) && all(diff(idx_l) == 1)
  }))
  
  links$value[[pp]] <- length(row_l)
}

# Save nodes and links as CSV files
write.csv(nodes, "nodes_clean.csv", row.names = FALSE)
write.csv(links, "links_clean.csv", row.names = FALSE)


