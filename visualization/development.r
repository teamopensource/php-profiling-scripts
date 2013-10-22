args <- commandArgs()

dir <- args[6]
files <- args[-(1:6)]

cols <- c("fl", "fn", "li", "tm")

names <- c()
ticks <- 0
sums <- c()

max <- 0

for(file in files) {
	rows <- read.csv(file, header = FALSE)
	colnames(rows) <- cols

	fns <- unique(rows[, "fn"])

	ticks <- ticks + 1
	
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
svg(paste(dir, "accumulation.svg", sep="/"), width=16, height=10)

plot(
	c(0, ticks),
	c(0, max),
	type="n"
)

for(name in names) {
	x <- c()
	y <- c()

	for(t in 1:ticks) {
		x <- c(x, t)
		y <- c(y, sums[paste(name, t)])
	}

	color <- rgb(runif(5), runif(5), runif(5))

	lines(x, y, type="b", col=color)
	text(c(y[1]), labels=name, col=color)
}

dev.off()