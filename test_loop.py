#!/usr/bin/python3

# Module : test_loop
#
# Requirements :
#
# Module interface :
#    Parametres :
#        debug : mode debug
#    Methodes :
#        __init__(self)
#        configure
#        connect                    ==> TBD
#        send_frame(timeout, destination)
#        err, str = receive_frame()
#        wait_for_receive_frame(str, timeout)    ==> TBD

import json
import time
from utils import load_config
from bcolors import bcolors

 
class test_loop(object) :

    def __init__(self, interface="",json_filename="") :
        self.bLoop = False
        
        self.interface = interface
        
        self.json_filename = json_filename
        
    def main(self) :
        while True:
            try:
                print(bcolors.WARNING + "Type help for list of commands - Type quit to exit program" + bcolors.ENDC)
                s = input(bcolors.ACTION + "Enter a command : " + bcolors.ENDC)
                if not s :
                    raise ValueError('empty string)')
                break
            except ValueError:
                pass

        with open(self.json_filename, 'r') as f:
            self.macros = json.load(f)        

        self.bLoop = False
        var_command_found = False
        loop_actions = []

        str_cmd = s.split(" ")
        parameter_cmd = []
            
        if (str_cmd[0][0:5] == "MACRO") :    
# Parcours de toutes les commandes de test du fichier json
            for macro in self.macros :
# Test si la commande entree correspond � une commande du fichier json            
                if (str_cmd[0] == macro['command']) :
                    print(macro['description'])
                    max_param = len(macro['parameter']['mask'])
                
# Test du bon nombre de parametres                
                    if (len(str_cmd) != max_param+1) :
                        print("Error wrong number of parameters")
                        break
                        
                    for i in range(max_param) :
                        parameter_cmd.append(str_cmd[i+1])
                
# Parcours de toutes les actions du fichier json
                    for action in macro['action'] :
                        str_action = action.split(" ")
                        str_out = [str_action[0]]
                        
                        if (str_action[0] == "LOOP") :
                            print("-> Hit <CTRL-C> to stop the loop and the program")
                            self.bLoop = True
                            while (self.bLoop) :
                                for i in range(len(loop_actions) - int(str_action[1]), len(loop_actions)) :
                                    x = loop_actions[i].split(" ")
                                    if (x[0] == "EXECUTE") :
                                        self.interface.execute(action = " ".join(x[1:]))
                                    elif (x[0] == "SLEEP") :
                                        if (self.interface.debug) :
                                            print("> Sleep " + x[1] + " s")
                                        time.sleep(int(x[1]))
                                    else :
                                        err = self.interface.send_frame(loop_actions[i], destination=macro['destination'])
                        elif(str_action[0] == "EXECUTE") :
                            str_out = ["EXECUTE"]
                            # Parcours de la chaine parametree
                            for i in range(1, len(str_action)) :
                                bTrouve = False
                                for j in range(1,len(str_action)) :
                                    if (str_action[i] == "%" + str(j)) :
                                        str_out.append(parameter_cmd[j - 1])
                                        bTrouve = True
                                if (not(bTrouve)) :
                                    str_out.append(str_action[i])
                
    #                        print(">>> " + " ".join(str_out))
                            self.interface.execute(action = " ".join(str_out[1:])) 
    # Memorisation en cas de Loop                        
                            loop_actions.append(" ".join(str_out))  
                            var_command_found = True         
                        elif (str_action[0] == "SLEEP") :
                            if (str_action[1][0] == "%") :
                                str_action[1] = str_action[1][1:]
                                str_action[1] = parameter_cmd[int(str_action[1])-1] 
                            if (self.interface.debug) :
                                print("> Sleep " + str_action[1] + " s")
                            time.sleep(int(str_action[1]))
    # Memorisation en cas de Loop                        
                            loop_actions.append(" ".join(str_action))  
                            var_command_found = True         
                        else :    
                            # Parcours de la chaine parametree
                            for i in range(1, len(str_action)) :
                                bTrouve = False
                                for j in range(1,len(str_action)) :
                                    if (str_action[i] == "%" + str(j)) :
                                        str_out.append(parameter_cmd[j - 1])
                                        bTrouve = True
                                if (not(bTrouve)) :
                                    str_out.append(str_action[i])
                
    #                        print(">>> " + " ".join(str_out))
                            err = self.interface.send_frame(" ".join(str_out)) 
                            loop_actions.append(" ".join(str_out))  
                            var_command_found = True         
        elif (s == "quit") :
            print("Exiting the program ...")
            quit()

        elif (s == "help") :
            for macro in self.macros :
# Si seulement help a ete saisi                
                if (len(str_cmd) == 1) :
                    print("....................................")
                    print(bcolors.HEADER+macro['command']+bcolors.ENDC)
                    print("   Description : " + macro['description'])
                    if (len(macro['parameter']['mask']) != 0) :
                        print("   Parameters  : " + macro['parameter']['mask'])
                        for p in macro['parameter']['description'] :
                            print("                 - " + p)
# Si help avec chaine de caractere                
                if (len(str_cmd) >= 2) :
                    test_affiche = True
                    for i in range (1,len(str_cmd)) :
                        if (macro['command'].find(str_cmd[i]) == -1) :
                            test_affiche = False
                    if (test_affiche) :
                        print("....................................")
                        print(bcolors.HEADER+macro['command']+bcolors.ENDC)
                        print("   Description : " + macro['description'])
                        if (len(macro['parameter']['mask']) != 0) :
                            print("   Parameters  : " + macro['parameter']['mask'])
                            for p in macro['parameter']['description'] :
                                print("                 - " + p)
            print("....................................")
            err = self.interface.send_frame("help")
            print(err['str'])
        else :
            err = self.interface.send_frame(s) 
             
                        
        
            
            
