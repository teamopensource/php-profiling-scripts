args <- commandArgs()

dir <- args[6]
filename <- args[7]
files <- args[-(1:7)]

cols <- c("fl", "fn", "li", "tm")

names <- c()
ticks <- 0
sums <- c()

max <- 0

files <- sort(files)

timestamps <- c()
first <- 0

for(file in files) {
	rows <- read.csv(file, header = FALSE)
	colnames(rows) <- cols

	fns <- unique(rows[, "fn"])

	ticks <- ticks + 1

	timestamp <- strsplit(file, "\\.")[[1]]
	timestamp <- timestamp[length(timestamp)-1]
	timestamp <- as.numeric(timestamp)

	if (first == 0) {
		t <- 0
		first <- timestamp
	} else {
		t <-timestamp - first
	}

	timestamps <- c(timestamps, t)

	for(name in fns) {
		names[name] <- name
		
		fnrows <- subset(rows, fn==name)

		sum <- sum(fnrows[, "tm"])

		if(sum > max)
			max <- sum

		sums[paste(name, ticks)] <- sum
	}
}

# dev.new(width=16, height=10)
svg(gsub("%", "_", paste(filename, "accumulation.svg", sep=".")), width=16, height=10)

seconds <- c(-2, timestamps[length(timestamps)])
microseconds <- c(0, max)

plot(
	seconds,
	microseconds,
	type="n"
)

for(name in names) {
	x <- c()
	y <- c()

	for(tick in 1:ticks) {
		x <- c(x, timestamps[tick])
		y <- c(y, sums[paste(name, tick)])
	}

	color <- rgb(runif(5), runif(5), runif(5))

	lines(x, y, type="l", col=color)
	text(c(y[1]), labels=name, col=color)
}

dev.off()