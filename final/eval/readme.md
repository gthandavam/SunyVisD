#Using R to compute SVD

##Interfacing with sqlite db

	>>install.packages("sqldf")
	
	
	>>library(sqldf)
	
	/* Testing the installation */
	>>sqldf("select * from iris limit 3")
	Loading required package: tcltk
	  Sepal_Length Sepal_Width Petal_Length Petal_Width Species
	1          5.1         3.5          1.4         0.2  setosa
	2          4.9         3.0          1.4         0.2  setosa
	3          4.7         3.2          1.3         0.2  setosa
	>>
	
	
	/* http://cran.r-project.org/web/packages/sqldf/INSTALL */
	
	>> drv <- dbDriver("SQLite")
	>> con <- dbConnect(drv, dbname = "tfidf-d80-t2.5-indexed-tfidf-desc.db")
	>> res <- dbSendQuery(con, "SELECT * FROM inverted_index LIMIT 10")
	>> data1 <- fetch(res, n=-1)
	>> data1
	>> library(Matrix)
	>> Y <- sparseMatrix(data1[,1], data1[,2], x=data1[,3], index1=FALSE)
##Memory requirement
	* R uses binary 64 for storing doubles. (8 bytes per double)
	* We have 224970230 entries in tfidf-d80-t2.5-indexed-tfidf-desc.db file
	* This means 1.8GB (roughly) required for representing the inverted_index sparse
	  matrix in memory.
         
##SVD
	References
	* Indexing by Latent Semantic Analysis by Deerwester et al..,
	* Singular Value Decomposition Tutorial by Kirk Baker
