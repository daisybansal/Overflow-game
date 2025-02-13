from a1_partc import Queue

def get_overflow_list(grid):

    rows, cols = len(grid), len(grid[0])
    overflow_list = []

    for i in range(rows):
        for j in range(cols):
            neighbors = 0
            if i > 0:
                neighbors += 1  # Top neighbor
            if i < rows - 1:
                neighbors += 1  # Bottom neighbor
            if j > 0:
                neighbors += 1  # Left neighbor
            if j < cols - 1:
                neighbors += 1  # Right neighbor

            if abs(grid[i][j]) >= neighbors:
                overflow_list.append((i, j))
                
    return overflow_list if overflow_list else None

def overflow(grid, a_queue):
    
    overflow_list = get_overflow_list(grid)

    #Base Case:
    if overflow_list == None:
        return 0

    #Checking for same signs.
    same_signs = True
    over_flow = grid[overflow_list[0][0]][overflow_list[0][1]]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] != 0 and  over_flow*grid[i][j] < 0:
                same_signs = False
                break
        if same_signs is False:
            break
            
    if same_signs == True:
        return 0
    
    #Overflowing the list.
    for index, (i, j) in enumerate(overflow_list):
        count = 0
        neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
        for x, y in neighbors:
            if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
                if grid[i][j] < 0 and grid[x][y] >= 0:
                    grid[x][y] = -grid[x][y] - 1
                
                elif grid[i][j] >= 0 and grid[x][y]<0:
                    grid[x][y] = abs(grid[x][y]) + 1
                
                elif grid[i][j] < 0 and grid[x][y] < 0:
                    grid[x][y] -=1
                
                else:
                    grid[x][y] += 1
                if (x,y) in overflow_list[:index]:
                    count += 1
        grid[i][j] = count
    
            
    
    # Add the modified grid to the queue
    a_queue.enqueue([row[:] for row in grid])

    # Recur to check for further overflow
    return 1 + overflow(grid, a_queue)
