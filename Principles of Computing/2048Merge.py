"""
Shane Honanie
http://www.codeskulptor.org/#user44_ei6zN67ykK_1.py
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    result = []
    last_added = False
    index_next_available = 0
    for idx in range(len(line)):
        if line[idx] > 0:
            result.insert(index_next_available,line[idx])
            
            if idx > 0 and  not last_added and result[index_next_available] == result[index_next_available - 1]:
                result[index_next_available - 1] *= 2
                last_added = True
                result.pop(index_next_available)
                result.insert(len(result), 0)
            else:
                index_next_available += 1
                last_added = False
        else:
            result.insert(len(result), line[idx])
    
    return result