#!/usr/bin/python3

import tkinter as tk
from ihk_serial import SerialThread
import threading
import queue

DEBUG = 0
DEBUG_NO_COMM = True

class Console_GUI_IHK(tk.Tk):
    def __init__(self) :
        tk.Tk.__init__(self)
        
#        self.root = tk.Tk() # Création de la fenêtre racine
        self.title('ConsoleGUI')
        
#================================================================
# LabelFrame Actions        
#================================================================
        self.l_actions = tk.LabelFrame(self, text="Actions")
        self.l_actions.pack(fill=tk.BOTH, expand=tk.YES)
             
                         # Vertical (y) Scroll Bar
        self.scroll_actions = tk.Scrollbar(self.l_actions)
        self.scroll_actions.pack(side=tk.RIGHT, fill=tk.Y)

        self.button =  [0 for x in range(10)]
        self.listbox =  [0 for x in range(10)]
        self.entry =  [0 for x in range(10)]
        
        # Create a Tkinter variable
        self.tkvar = [tk.StringVar(self) for x in range(10)]          
        self.choices = { 'Pizza','Lasagne','Fries','Fish','Potatoe'}
        
        for i in range(10) :
            self.button[i] = tk.Button(self.l_actions,text=str(i+1))
#            self.button[i] = Button(self.l_actions,text=str(i+1))
            self.button[i].pack()
         
            # Dictionary with options
            self.tkvar[i].set("Pizza") # set the default option
 
            self.listbox[i] = tk.OptionMenu(self.l_actions,self.tkvar[i],*self.choices)
            self.listbox[i].pack()
         
            self.entry[i] = tk.Entry(self.l_actions,width = 50)
            self.entry[i].pack()

#================================================================
# LabelFrame Activite        
#================================================================
        self.l_activite = tk.LabelFrame(self, text="Activite", padx=10, pady=10)
        self.l_activite.pack(fill=tk.X, expand=tk.YES)

#================================================================
# LabelFrame Envoi        
#================================================================
        self.l_envoi = tk.LabelFrame(self.l_activite, text="Envoi", padx=10, pady=10)
        self.l_envoi.pack(fill=tk.X, expand=tk.YES)

        #Partie envoi
        self.entry = tk.Entry(self.l_envoi,width = 100)
        self.entry.grid(row=0, column=0)
        #entry.pack(fill=X, expand=YES)
        #entry.pack(fill = BOTH,expand=YES)
        
        self.button_send = tk.Button(self.l_envoi,text="Send",command=self.send)
        self.button_send.grid(row=0, column=1)
        self.bind('<Return>',self.event_key_return)
        #button_send.pack()
        
#================================================================
# LabelFrame Dialogue        
#================================================================
        self.l_traffic = tk.LabelFrame(self.l_activite, text="Dialogue", padx=10, pady=10)
        self.l_traffic.pack(fill=tk.X, expand=tk.YES)
        
        # Vertical (y) Scroll Bar
        self.scroll = tk.Scrollbar(self.l_traffic)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.textzone = tk.Text(self.l_traffic,height=10, yscrollcommand=self.scroll.set)
        self.textzone.pack(fill = tk.BOTH,expand=tk.YES)
        self.textzone.tag_config('send', foreground="blue")
        self.textzone.tag_config('receive', foreground="green")
        self.textzone.tag_config('comment', foreground="black")
        
#================================================================
# LabelFrame Commande        
#================================================================
        self.l_command = tk.LabelFrame(self, text="Commands", padx=10, pady=10)
        self.l_command.pack(fill=tk.X, expand=tk.YES)
        self.l_command.grid_columnconfigure(0, weight=1)
        self.l_command.grid_columnconfigure(1, weight=1)
        self.l_command.grid_columnconfigure(2, weight=1)
        
        self.button_options = tk.Button(self.l_command,text='OPTIONS')
        self.button_options.grid(row=0, column=0,sticky=tk.W+tk.E,padx=20)
        
        self.button_clear = tk.Button(self.l_command,text='CLEAR')
        self.button_clear.grid(row=0, column=1,sticky=tk.W+tk.E,padx=20)

        self.button_quit = tk.Button(self.l_command,text='QUIT')
        self.button_quit.grid(row=0, column=2,sticky=tk.W+tk.E,padx=20)
 
        self.queue = queue.Queue()
        
        if not DEBUG_NO_COMM :
            self.readThread = SerialThread(self.queue)
            self.readThread.start()
            self.processConsole()        
 
    def processConsole(self) :
        while self.queue.qsize():
            try:
                new=self.queue.get()
                self.textzone.insert(tk.END,new,"receive")
                self.textzone.see(tk.END)
            except queue.Empty:
                pass
        self.after(100, self.processConsole)
      
    def send(self):
        self.readThread.send_frame(self.entry.get())
        self.textzone.insert(tk.END,self.entry.get() + "\n","send")
        self.entry.delete(0, tk.END)
        
    def event_key_return(self,event):
        self.send()
        
if __name__ == '__main__':
    app=Console_GUI_IHK()
    app.mainloop() 
    # Lancement de la boucle principale
