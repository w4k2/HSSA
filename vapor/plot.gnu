#!/usr/bin/env gnuplot

reset

load 'plot.cfg'

set output 'signatures.png'
#set title db_name
file = 'signatures.csv'

classes = 'background Broccoli Corn Lettuce4 Lettuce5 Lettuce6'

plot for [i=2:10] file u ($1):(column(i+1)) w l ls i t word(classes,i)

