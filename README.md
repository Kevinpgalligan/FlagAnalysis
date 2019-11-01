# FlagAnalysis

### Questions
* What happens when you average the pixels of all of the national flags in the world?
* What are the most common colours in national flags?

### Answers
![average flag](https://raw.githubusercontent.com/Kevinpgalligan/FlagAnalysis/master/results/average_flag.jpg)

![colour frequency](https://raw.githubusercontent.com/Kevinpgalligan/FlagAnalysis/master/results/barchart.png)

### Notes on most common colours
Since there is huge variety in the colours of the national flags, it makes sense to "round" each pixel to the "nearest" of a selection of common colours (measured by Euclidean distance). Otherwise, we would have 1000s of colours, most of them with negligible frequency. The common colours used were: white, silver, gray, black, red, maroon, yellow, olive, lime, green, aqua, teal, blue, navy, fuchsia and purple. We see that red is the most common colour in national flags; the colour of passion, excitement, danger, and McDonald's.
