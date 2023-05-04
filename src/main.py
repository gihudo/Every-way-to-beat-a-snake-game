from snake_game import game

if __name__ == "__main__":
    mygame = game.Game(field=(15,15), block_size=50, difficulty=15)
    
    while True:
        mygame.next()
        
        if not mygame.running:
            mygame.reset()