#!/usr/bin/python3

import json
import csv
import time

BASE_FILENAME = ["./ihk_tests"]  

labels = []
parameters = []

def ConvertCSVtoJSON(filename = "") :
    print("Utilitaire de conversion csv --> json")
    print("=====================================")
    print()
    print("Fichier original    : " + filename + ".csv.txt")
    print("Fichier destination : " + filename + ".json")
    
    with open(filename + ".csv.txt", 'r') as csvfile :
        r = csv.reader(csvfile, delimiter='\t', quotechar='|')
        
        parameters_count = 0
        line_count = 0
        labels = []
        parameters = []
        for row in r :
            print(".", end = '')
            parameter = {}
            if (line_count == 0) :
                field_count = 0 
                for e in row :
                    labels.append(e)
    #                 x = e.split(".")
    #                 if (len(x) == 1) :
    #                     parameters[field_count] = e
    #                 field_count += 1
            else :
                i = 0
                memo_array = ""
                for e in row :
                    x = labels[i].split("/")
                    if (len(x) == 1) :
                        y = x[0].split(".")
                        if (len(y) == 1) :
                            parameter.update({ x[0] : e })
                        else :
                            if (memo_array != y[1]) :
                                parameter[y[1]] = []
                            if (e != "") :    
                                parameter[y[1]].append(e)
                            memo_array = y[1]
                    if (len(x) == 2) :
                        y = x[1].split(".")
                        if (len(y) == 1) :
                            if (parameter.get(x[0]) == None) :
                                parameter.update({ x[0] : { } })
                            parameter[x[0]].update({ x[1] : e })
                        else :
                            if (memo_array != y[1]) :
                                parameter[x[0]][y[1]] = []
                            if (e != "") :    
                                parameter[x[0]][y[1]].append(e)
                            memo_array = y[1]
                    i += 1  
                parameters.append(parameter)    
            line_count += 1
    
    print()
    
    str = json.dumps(parameters, indent=4, sort_keys=True)
    
    print(str)
    
    with open(filename + ".json", 'w') as outfile:
        outfile.write(str)
    #    json.dump(parameters, outfile)                        

for i in BASE_FILENAME :
    ConvertCSVtoJSON(i)

print("Operation terminee")
time.sleep(1)
