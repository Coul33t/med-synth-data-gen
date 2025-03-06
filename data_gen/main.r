library("synthpop")

single_data <- function(data) {
    # data = read.csv(csv_file_name, header=TRUE)

    #codebook.syn(data)
    vars_names = names(data)
    vars_to_excluse <- names(data) %in% c("Date_Time_measured", "pacient_id")
    new_data <- data[!vars_to_excluse]
    new_data = transform(new_data, arrythmia = as.logical(arrythmia))
    mysyn <- syn(new_data)
    #write.syn(mysyn, file="test", filetype="csv")
    return(mysyn)
}



all_data <- function() {
    filenames <- list.files("split_data", pattern="*.csv", full.names=TRUE)
    ldf <- lapply(filenames, read.csv)
    res <- lapply(ldf, single_data)

    nb_data <- length(filenames)

    for (i in 1:nb_data) {
        new_name <- substring(filenames[i], nchar("split_data/") + 1, nchar(filenames[i]) - nchar(".csv"))
        new_name <- paste("gen_data/", new_name, sep="")
        write.syn(res[i], file=new_name, filetype="csv")
    }
}

all_data()
#single_data("split_data/patient_2.csv")