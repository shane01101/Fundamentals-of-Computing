"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    result = []
    index_next_available = 0
    for i in range(len(line)):
        if line[i] > 0:
            result.insert(index_next_available,line[i])
            
            if i > 0 and result[index_next_available] == result[index_next_available - 1]:
                result[index_next_available - 1] *= 2
                result.pop(index_next_available)
                result.insert(len(result), 0)
                
            index_next_available += 1
        else:
            result.insert(len(result), line[i])
        
    
    return result

print merge([2,0,2,4])
