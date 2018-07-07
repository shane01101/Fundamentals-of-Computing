"""
Shane Honanie
http://www.codeskulptor.org/#user44_CnGE5juN5u_9.py

Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    if len(list1) == 0:
        return []
    
    new_list = []
    new_list.append(list1[0])
    
    for index in range(len(list1)):
        if list1[index] != new_list[-1]:
            #print index, list1[index], new_list[-1]
            new_list.append(list1[index])
    
    return new_list

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    new_list = []
    l1_index = 0
    l2_index = 0
        
    while l1_index < len(list1) and l2_index < len(list2):
        if list1[l1_index] < list2[l2_index]:
            l1_index += 1
        elif list1[l1_index] == list2[l2_index]:
            new_list.append(list1[l1_index])
            l2_index += 1
            l1_index += 1
        else:
            l2_index += 1

    return new_list

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """   
    new_list = []
    l1_index = 0
    l2_index = 0
        
    while l1_index < len(list1) and l2_index < len(list2):
        if list1[l1_index] <= list2[l2_index]:
            new_list.append(list1[l1_index])
            l1_index += 1
        else:
            new_list.append(list2[l2_index]) 
            l2_index += 1
        
    while l1_index < len(list1):
        new_list.append(list1[l1_index])
        l1_index += 1
            
    while l2_index < len(list2):
        new_list.append(list2[l2_index])
        l2_index +=1

    return new_list
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) < 2:
        return list1
    
    new_l1 = merge_sort(list1[:len(list1)//2])
    new_l2 = merge_sort(list1[len(list1)//2:])
    return merge(new_l1, new_l2)

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if word == "":
        return [""]
    else:
        first = word[0]
        rest = word[1:]
        rest_strings = gen_all_strings(rest)
        string_list = []
        
        for word in rest_strings:
            for index in range(len(word) + 1):
                string_list.append(word[0:index] + first + word[index:])

    return string_list + rest_strings

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    #print url
    netfile = urllib2.urlopen(url)
    lines = []
    for line in netfile.readlines():  
        lines.append(line[:-1])  
    #print lines
    return lines 

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

    
# Uncomment when you are ready to try the game
run()

#Test
#test_list = ['test1', 'test1', 'test2', 'test2', 'test3', 'test3', 'test6']
#test_list2 = ['test2', 'test3', 'test4', 'test5']
#print remove_duplicates(test_list)
#print intersect(test_list, test_list2)
#print merge(test_list, test_list2)
#test_list3 = ['test6', 'test1', 'test2', 'test2', 'test9', 'test3', 'test8']
#print merge_sort(test_list3)
#print gen_all_strings("aab")

    
    