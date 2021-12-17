BLOCK_WIDTH = 30
BLOCK_HEIGHT = 16

def cor_surround(x,y):
    return [(i, j) for i in range(max(0, x-1), min(29, x+1) + 1)
            for j in range(max(0, y-1), min(15, y+1)+1) if i != x or j != y]

if __name__ == "__main__":
    print(cor_surround(3,4))