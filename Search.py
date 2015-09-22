''' Project - Text-Based Search Engine '''
''' Author - Sanjeev Singh '''

import os
import sys
import re
from time import time, clock

"""
split_text
parameters: string
returns: list of tokens    
"""
def split_text(text):
    text = re.compile("[^\w]|_").sub(" ", text)
    word_list = re.findall("\w+", text.lower())    
    return word_list

def sp_text(text):
    word_list = re.split('\s+', text.lower())
    punctuation = re.compile(r'[-.?!,":;()|0-9]')
    
    for i, word in enumerate(word_list):
        word_list[i] = punctuation.sub("", word)
    
    return word_list


"""
create_dict
parameters: the location of the base directory where all the test files are placed
returns: dictionary with key as string and value as another dictionary
    with key as the filename and value as the positional indices.
"""
def create_dict(base_dir):
    file_list = os.listdir(base_dir)
    global_dict = {}
    
    start = time()
    for file in file_list:
        filename = os.path.join(base_dir, file)
        f = open(filename, "r")
        text = f.read()
        f.close()
        words = split_text(text)
        
        for i, word in enumerate(words):
            local_dict = {}
            local_list = []
            
            if word in global_dict:
                local_dict = global_dict[word]
                
                if file in local_dict:
                    local_list = local_dict[file]
                    local_list.append(i)
                else:
                    local_list.append(i) 
                local_dict[file] = local_list
                
            else:
                local_list.append(i)
                local_dict[file] = local_list
            
            global_dict[word] = local_dict
           
        
    print "Time taken for creating the global dictionary: ", (time()-start)
            
    return global_dict
            
"""
boolean_query
parameters: 
    global dictionary which is created with create_dict() and list of terms to be queried
returns: list containing resulting file names satisfying the boolean query over query_terms
"""
def boolean_query(dict, query_terms):
    result = []
    
    for term in query_terms:
        temp = {}
        if term in dict:
            temp = dict[term]
            if len(result) == 0:
                result = temp.keys()
            else:
                result = [x for x in result if x in temp.keys()]
        else:
            result = []
            break
            
    return result
        
"""
phrase_query
parameters:
    global dictionary created with create_dict() and a string which is to be phrase queried
returns: list containing resulting file names after getting phrase queried
"""   
def phrase_query(dict, query):
    keys = dict.keys()
    temp_query = query
    query = split_text(query)
    bool_query_res = boolean_query(dict, query)
    result = []
    
    for res in bool_query_res:
        list = []
        for term in query:
            if term in keys:
                temp_dict = dict[term]
                
                if res in temp_dict:
                    list.append(temp_dict[res])
                    
        for index in range(len(list)):
            list[index] = [x-index for x in list[index]]
            
        intersect = set(list[0]).intersection(*list)
        if len(intersect) != 0:
            result.append(res)
            
    return result
               
"""
rotate
parameters: string to be rotated and number of indices to be considered while rotating
returns: rotated string
"""
def rotate(str,n):
    return str[n:] + str[:n]

"""
create_permuterm
parameters: list of strings 
returns: a dictionary with key as the permuterm and value as the string 
    from the word list from which the permuterm is created
"""
def create_permuterm(word_list):
    dict = {}
    
    strt = time()
    for word in word_list:
        temp = word + '$'
        for i in range(len(temp)):
            temp = rotate(temp, 1)
            dict[temp] = word
            
    print "Time taken for creating the permuterm index is: ", (time()-strt)            
    return dict
        
"""
wc_query
parameters:
    dictionary from the create_dict()
    dictionary from create_permuterm()
    list of strings to be considered to for the wild card query
returns: list containing resulting file names for wild card query
"""
def wc_query(dict, pdict, query_terms):
    pkeys = pdict.keys()
    result = []
    
    for term in query_terms:
        term = term + '$'
        while(term[-1] != '*'):
            term = rotate(term, 1)
            
        term = term[:-1]
        temp_list = []
        
        for pkey in pkeys:
            if term in pkey:
                pk = pdict[pkey]
                if pk in temp_list:
                    continue
                else:
                    temp_list.append(pk)
                
        temp_result = []
        for temp in temp_list:
            t_list = []
            t_list.append(temp)
            temp_result = temp_result + boolean_query(dict, t_list)
            
        if len(result) == 0:
            result = temp_result
        else:
            result = [x for x in result if x in temp_result]
        
    result_set = set(result)
    result = list(result_set)
        
    return result

"""
main
parameters: None
This function is mainly for getting the input query from the user and then
segregating the input query and calling the needed query functions
(boolean_query(), phrase_query(), wc_query()) and then combing the results 
obtained from different query functions and then outputs the final result.
"""                 
def main():
    if len(sys.argv) != 3:
        print "usage: ./Search.py <directory to read test files> <file for outputting index table>"
        sys.exit(1)
    
    base_dir = sys.argv[1]
    file_list = os.listdir(base_dir)
    
    dict = create_dict(base_dir)
    pdict = create_permuterm(dict.keys())
    
    print "Press 1 for query search;  2 for generating global index table; 3 for generating permuterm index table"
    choice = raw_input("Enter your choice: ")
    
    if choice == '1':
    
        while 1:
            input_query = raw_input("Enter query: ")
            
            result = []
            if input_query == "":
                print "Please enter a non-empty query!"
            else:
                input_terms = sp_text(input_query)
                
                w_query_terms = []
                b_query_terms = []
                for w in input_terms:
                    if '*' in w:
                        w_query_terms.append(w)
                    else:
                        b_query_terms.append(w)
                      
                if len(w_query_terms) > 0:
                    result1 = wc_query(dict, pdict, w_query_terms) 
                    result.append(result1)  
    
                matches = re.findall(r'\"(.+?)\"', input_query)
                ph_query = ",".join(matches)
                p_query_list = ph_query.split(",")
                
                result2 = []
                if ph_query != "":
                    for p_query in p_query_list:
                        temp = phrase_query(dict, p_query)
                        
                        if len(result2) == 0:
                            result2 = temp
                        else:
                            result2 = [x for x in result2 if x in temp]
                    result.append(result2)
                    
                if len(b_query_terms) > 0:
                    result3 = boolean_query(dict, b_query_terms)
                    result.append(result3)
                 
            if len(result) > 0:       
                result_set = set(result[0]).intersection(*result)
                result = list(result_set)
            
                if len(result) > 0:
                    result = [x[:-4] for x in result]
                    print result
                else:
                    print "Sorry no match :("
    
    elif choice == '2':
        sys.stdout = open(sys.argv[2], 'w')
        for key, value in dict.items():
            print key, value
    
    elif choice == '3':
        sys.stdout = open(sys.argv[2], 'w')
        for key, value in pdict.items():
            print key, "  ", value
            
    else:
        print "Please try again and enter the correct choice!"
               
    return 0
     
if __name__ == '__main__':
    main()
