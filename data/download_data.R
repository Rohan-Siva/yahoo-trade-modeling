if (!require("quantmod")) install.packages("quantmod")
if (!require("tidyverse")) install.packages("tidyverse")

library(quantmod)
library(tidyverse)

download_data_r <- function(tickers, start_date, end_date, output_dir) {
  
  if (!dir.exists(output_dir)) {
    dir.create(output_dir, recursive = TRUE)
  }
  
  for (ticker in tickers) {
    print(paste("Downloading", ticker))
    tryCatch({
      getSymbols(ticker, src = "yahoo", from = start_date, to = end_date, auto.assign = TRUE)
      data <- get(ticker)
      
      df <- data.frame(Date = index(data), coredata(data))
      
      file_path <- file.path(output_dir, paste0(ticker, "_R.csv"))
      write.csv(df, file_path, row.names = FALSE)
      print(paste("Saved", ticker, "to", file_path))
      
    }, error = function(e) {
      print(paste("Error downloading", ticker, ":", e$message))
    })
  }
}

tickers <- c("SPY", "AAPL", "BTC-USD")
start_date <- "2020-01-01"
end_date <- "2023-01-01"
output_dir <- "data/raw"

download_data_r(tickers, start_date, end_date, output_dir)
