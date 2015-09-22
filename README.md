Author: Sanjeev Singh

This Search Engine supports term/boolean queries, phrase queries as well as wild card queries.

Command to execute: 
python Search.py <directory location where test files are located> <file where index is to be generated>

After exectuting the above command the command prompt looks like this:

Time taken for creating the global dictionary:  <time>
Time taken for creating the permuterm index is:  <time>
Press 1 for query search;  2 for generating global index; 3 for generating permuterm index
Enter your choice: 
_____________________________________________________________________________________________

choice 1: user can enter his/her query and get the respective result.

choice 2: user need to check the file (passed as the second argument) to see the global index table
		  Global index table is a dictionary with key as string and value as dictionary
		
choice 3: user need to check the file (passed as the second argument) to see the permuterm index table
		  Permuterm index table is dictionary with key as permuterm and value as the key from the global dictionary
		  
		  



