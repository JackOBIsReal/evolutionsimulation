rm -r ~/evolutionsimulation/simulationOutput*
#rm -r ~/simulationOutput*
screen -S 1 -dm python ecosimulation.py -hl &
screen -S 2 -dm python ecosimulation.py -hl &
screen -S 3 -dm python ecosimulation.py -hl &
screen -S 4 -dm python ecosimulation.py -hl &
screen -S 5 -dm python ecosimulation.py -hl &
