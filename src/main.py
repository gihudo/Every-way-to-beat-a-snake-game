from snake_game import game
from plots import plot
from AI import agent

if __name__ == "__main__":
    mygame = game.Game(field=(15,15), block_size=50, difficulty=8)
    
    myplt = plot.Plot()

    ai = agent.Agent()
    while True:
        ai.play(mygame)
        mygame.next()
    
        if not mygame.running:
            myplt.add_vertex(mygame.steps / 10, mygame.score, None)
            mygame.reset()

        if len(myplt.get_data_frame()) > 100:
            break
    
    myplt.create_plot()