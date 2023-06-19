import pandas as pd
import matplotlib.pyplot as plt

class Plot:
    def __init__(self):
        self.__data_frame = pd.DataFrame(columns=['id', 'steps', 'score', 'state'])
        
    def get_data_frame(self):
        return self.__data_frame
    
    def set_data_frame(self, data_frame):
        self.__data_frame = data_frame

    def create_plot(self):
        self.__data_frame.plot(x = 'id', y=['steps', 'score'])
        plt.grid(True)
        plt.show()
        
    def add_vertex(self, steps, score, state):
        self.__data_frame.loc[len(self.__data_frame)] = [len(self.__data_frame), steps, score, state]