# -*- coding: iso-8859-1 -*-
#takes the raw data file and creates 4 text files that can each be loaded into a table in mySQL
#!/usr/bin/python

# step 1. open the data file done

infile = "GDS5093_full.soft" #Name of the input file

fh = open(infile)

#step 2. read the first line and then read more lines while the line doesn't match a specific pattern
#while : #need to complete this   done
line= fh.readline()
while line[:20] != '!dataset_table_begin':    #line is currently set to 0, change to appropriate ine later
    line=fh.readline()

header= fh.readline().strip()
#capture the column names
colnames={}
index=0
for title in header.split('\t'):
    colnames[title]=index
    print '%s\t%s'%(title,index)
    index=index+1



#open our output files, one per table.
# do it your self....   done

genefile=open('genes.txt', 'w')
expressionfile=open('expression.txt','w')
probefile=open('probes.txt', 'w')

genefields=['Gene ID', 'Gene symbol', 'Gene title']
samples=header.split('\t')[2:int(colnames['Gene title'])]
probefields=['ID_REF','Gene ID']

#defines which columns are to go in each output file. For samples it is the 3rd header until the gene title header and they will be separated by '\t'
genefields=['Gene ID', 'Gene symbol', 'Gene title']# you can add more fileds, jsut depends how you design your tables
samples=header.split('\t')[2:int(colnames['Gene title'])]
probefields=['ID_REF','Gene ID']

#use this to take out columns from a row!!!!
def buildrow(row, fields):
    '''Creates a tab separated list of values according to the columns listed in fields
	row: a list of values...... Pulls out from a row the selected columns 
	fields: a list of columns. Only the values in row corresponding to the columns in fields are output
	returns: A string that is a tab separated list of values terminated with a newline
	'''
    newrow=[]
    for f in fields:
        newrow.append(row[int(colnames[f])])
        return "\t".join(newrow)+"\n"   #INDENT change


	#creates the rows for the expression file, is slightly different because for each probe and experiment there are several gene expression values.
row_count=0
def build_expression(row, samples):
    '''Builds tab separated rows for expression data. For each of the samples listed 
	it generates a line with the probe id, sample id and expression value.
	row: a list of values
	samples: a list of column headings corresponding to the samples
	'''
    exprrows=[]
    for s in samples:
        newrow=[s,]
	newrow.append(row[int(colnames['ID_REF'])]) # you add on the probe name
	newrow.append(row[int(colnames[s])])         # then the row name
	exprrows.append("\t".join(newrow))
        return "\n".join(exprrows)+"\n"                 #INDENT CHANGE add it onto a new row per same expression value
	
	
#initialise a counter to count how many probe rows were processed.    done
#writes the data to the files 
for line in fh.readlines():
    try:
        if line[0]=='!': #if they dont start with ! then they are split, taking off new line with strip
            continue
            row=line.strip().split('\t') #indent
            genefile.write(buildrow(row, genefields))
            probefile.write(buildrow(row,probefields)) # builds line for genes, and probe files
            expressionfile.write(build_expression(row, samples))	
            row_count=row_count+1 #increment the row counter    CREATE done
    except:
		pass

#close the created files after the data has been writen to them CREATE done

#print out a message to indicate success with outputting the data. CREATE done

genefile.close()
probefile.close()
expressionfile.close()


print '%s row_count'%row_count
    

