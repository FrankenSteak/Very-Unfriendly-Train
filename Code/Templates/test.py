from keras.models import Sequential
from keras.layers import Dense

network = Sequential()

        #Hidden Layer#1
network.add(Dense(units=37,
                  activation='tanh',
                  kernel_initializer='uniform',
                  input_dim=31))

        #Hidden Layer#2
network.add(Dense(units=36,
                  activation='tanh',
                  kernel_initializer='uniform'))

        #Exit Layer
network.add(Dense(units=1,
                  activation='tanh',
                  kernel_initializer='uniform'))

from ann_visualizer.visualize import ann_viz

ann_viz(network, title="")