from tkinter import *
from tkinter.messagebox import *
from tkinter.simpledialog import *
import webbrowser

class MyApp():
    """"""
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        self.root = parent
        parent.title("Fanorona")
        
        btn = Button(parent, text="Jouer", command=self.openjouer , width=15, bd=0)
        btn.pack(pady=20)
        
        btn2 = Button(parent, text="Aide", command=self.aide, width= 15, bd=0)
        btn2.pack(pady=10)
        
        btn3 = Button(parent, text="A propos", command=self.openpropos, width= 15, bd=0)
        btn3.pack(pady=20)
        
        btn4 = Button(parent, text="Quitter", command=self.quitter, width= 15, bd=0)
        btn4.pack(pady=10)
        
    #----------------------------------------------------------------------
    def hide(self):
        """"""
        self.root.withdraw()
        
    def aide(self):
        webbrowser.open('http://fanorona.16mb.com/regles.html')
       
    #----------------------------------------------------------------------
    def openjouer(self):
        """"""
        #--- définition des fonctions gérants les évenements ---
        def damier():
            "Dessine le damier"
            i = 0
            
            while i < 10:
                j = 0
                while j < 10:
                    if (i%2)==0:
                        if (j%2)==0:
                            can1.create_rectangle(j*case, i*case, (j*case)+case, (i*case)+case, fill='black')
                        else:
                            can1.create_rectangle(j*case, i*case, (j*case)+case, (i*case)+case,fill='white')
                    else:
                        if (j%2)==0:
                            can1.create_rectangle(j*case, i*case, (j*case)+case, (i*case)+case, fill='white')
                        else:
                            can1.create_rectangle(j*case, i*case, (j*case)+case, (i*case)+case, fill='black')
                    j+=1
                i+=1

        def place_pions():
            "On place les pions"
            # on marque les scores
            if started:
                txt1.configure(text=j1+' (Rouge): '+str(rouge))
                txt2.configure(text=j2+' (Bleu): '+str(bleu))
                if joueur == 1:
                    chaine.configure(text="Les BLEUS jouent...", fg='blue')
                else:
                    chaine.configure(text="Les ROUGES jouent...", fg='red')
            # on commence par les pions blancs (rouge)
            i = 0
            while i < len(pions_b):
                if pions_b[i] != -1:
                    y = (((pions_b[i]/10)*case) + case/2)
                    x = ((pions_b[i]%10)*case) + case/2
                    # On a calculé le centre du cercle. On le dessine
                    if i in dame_b:
                        can1.create_rectangle(x-10, y-10, x+10, y+10, fill='red')
                    else:
                        can1.create_oval(x-15, y-15, x+15, y+15, fill='red')
                i += 1
            # ensuite les pions noirs (bleu)
            i = 0
            while i < len(pions_n):
                if pions_n[i] != -1:
                    y = (((pions_n[i]/10)*case) + case/2)
                    x = ((pions_n[i]%10)*case) + case/2
                    # On a calculé le centre du cercle. On le dessine
                    if i in dame_n:
                        can1.create_rectangle(x-10, y-10, x+10, y+10, fill='blue')
                    else:
                        can1.create_oval(x-15, y-15, x+15, y+15, fill='blue')
                i += 1

        def pions_prenable():
            "on test si le joueur pouvait prendre une pièce pour la règle \"sauter n'est pas jouer\""
            global sauter_pas_jouer
            sauter_pas_jouer = []
            if joueur == 0:
                i = 0;
                while i < len(pions_b):
                    pr = possibilitees(False, pions_b[i])
                    if len(pr) != 0:
                        sauter_pas_jouer.append(i)
                        sauter_pas_jouer.append(pr[0])
                        sauter_pas_jouer.append(pr[1])
                        return True
                    i += 1
            else:
                i = 0;
                while i < len(pions_n):
                    pr = possibilitees(False, pions_n[i])
                    if len(pr) != 0:
                        sauter_pas_jouer.append(i)
                        sauter_pas_jouer.append(pr[0])
                        sauter_pas_jouer.append(pr[1])
                        return True            
                    i += 1
            return False

        def ColorCase(num):
                y = ((num/10)*case) + case/2
                x = ((num%10)*case) + case/2
                can1.create_oval(x-15, y-15, x+15, y+15, fill='orange')
            
        def deplacement(dest):
            "On effectue le déplacement des pions"
            global pions_n, pions_b, rouge, bleu
            ligne = dest/10
            if dest in pos:
                if selected in pions_b:
                    if dest in prenable:
                        pions_n[pions_n.index(prenable[prenable.index(dest)+1])] = -1
                        pions_b[pions_b.index(selected)] = dest
                        rouge += 1
                    elif pions_prenable():
                        # sauter n'est pas jouer
                        ColorCase(pions_b[sauter_pas_jouer[0]])
                        ColorCase(pions_n[pions_n.index(sauter_pas_jouer[2])])                
                        showinfo("Sauter n'est pas jouer", "Si vous pouvez capturer un pion vous devez le faire")
                        pions_n[pions_n.index(sauter_pas_jouer[2])] = -1
                        pions_b[sauter_pas_jouer[0]] = sauter_pas_jouer[1]
                        dest = sauter_pas_jouer[1]
                        ligne = dest/10
                        rouge += 1
                    else:
                        pions_b[pions_b.index(selected)] = dest
                    if ligne == 9:
                        dame_b.append(pions_b.index(dest))           
                else:
                    if dest in prenable:
                        pions_b[pions_b.index(prenable[prenable.index(dest)+1])] = -1
                        pions_n[pions_n.index(selected)] = dest
                        bleu += 1
                    elif pions_prenable():
                        # sauter n'est pas jouer
                        ColorCase(pions_n[sauter_pas_jouer[0]])
                        ColorCase(pions_b[pions_b.index(sauter_pas_jouer[2])])
                        showinfo("Sauter n'est pas jouer", "Si vous pouvez capturer un pion vous devez le faire")
                        pions_b[pions_b.index(sauter_pas_jouer[2])] = -1
                        pions_n[sauter_pas_jouer[0]] = sauter_pas_jouer[1]
                        dest = sauter_pas_jouer[1]
                        ligne = dest/10
                        bleu += 1
                    else:
                        pions_n[pions_n.index(selected)] = dest
                    if ligne == 9:
                        dame_n.append(pions_n.index(dest)) 
                return True
            else:
                return False

        def case_libre(c):
            ligne = c/10
            colonne = c%10
            if ((ligne%2)==0 and (colonne%2)!= 0) or ((ligne%2)!=0 and (colonne%2)== 0):
                return False 
            else:
                if c in pions_b or c in pions_n:
                    return False
                else:
                    return True

        def possibilitees(glob=True, num_case=0):
            "Procédure évaluant les possibilitées de coup en fonction de la case selectionnées"
            if glob:
                global pos, prenable, selected
                
            pos = []
            prenable = []

            if not glob:
                n_case = num_case
            else:
                n_case = selected
                
            s_ligne = n_case/10
            s_colonne = n_case%10
                   
            # on évalue les positions autorisées
            if n_case in pions_b:
                # il s'agit d'un pion rouge
                c = (s_ligne+1)*10+(s_colonne-1)
                if case_libre(c):
                    pos.append(c)
                else:
                    c2 = (s_ligne+2)*10+(s_colonne-2)
                    if case_libre(c2) and c in pions_n:
                        pos.append(c2)
                        prenable.append(c2)
                        prenable.append(c)
                    
                c = (s_ligne+1)*10+(s_colonne+1)
                if case_libre(c):        
                    pos.append(c)
                else:
                    c2 = (s_ligne+2)*10+(s_colonne+2)
                    if case_libre(c2) and c in pions_n:
                        pos.append(c2)
                        prenable.append(c2)
                        prenable.append(c)

                # si il s'agit d'une dame, il y a d'autre possibilitées
                if pions_b.index(n_case) in dame_b:
                    # déplacement haut-droit
                    i = 1
                    while i < 10:
                        l = s_ligne - i
                        cl = s_colonne + i
                        if l >= 0 and cl < 10:
                            c = l*10+cl
                            if case_libre(c):
                                pos.append(c)
                            elif c in pions_b:
                                break
                            else:
                                c2 = (l-1)*10+(cl+1)
                                if case_libre(c2):
                                    pos.append(c2)
                                    prenable.append(c2)
                                    prenable.append(c)
                                break
                        else:
                            break
                        i+=1
                    # déplacement haut-gauche
                    i = 1
                    while i < 10:
                        l = s_ligne - i
                        cl = s_colonne - i
                        if l >= 0 and cl >= 0:
                            c = l*10+cl
                            if case_libre(c):
                                pos.append(c)
                            elif c in pions_b:
                                break
                            else:
                                c2 = (l-1)*10+(cl-1)
                                if case_libre(c2):
                                    pos.append(c2)
                                    prenable.append(c2)
                                    prenable.append(c)
                                break
                        else:
                            break
                        i+=1
                    # déplacement bas-droit
                    i = 1
                    while i < 10:
                        l = s_ligne + i
                        cl = s_colonne + i
                        if l < 10 and cl < 10:
                            c = l*10+cl
                            if case_libre(c):
                                pos.append(c)
                            elif c in pions_b:
                                break
                            else:
                                c2 = (l+1)*10+(cl+1)
                                if case_libre(c2):
                                    pos.append(c2)
                                    prenable.append(c2)
                                    prenable.append(c)
                                break
                        else:
                            break
                        i+=1
                    # déplacement bas-gauche
                    i = 1
                    while i < 10:
                        l = s_ligne + i
                        cl = s_colonne - i
                        if l < 10 and cl >= 0:
                            c = l*10+cl
                            if case_libre(c):
                                pos.append(c)
                            elif c in pions_b:
                                break
                            else:
                                c2 = (l+1)*10+(cl-1)
                                if case_libre(c2):
                                    pos.append(c2)
                                    prenable.append(c2)
                                    prenable.append(c)
                                break
                        else:
                            break
                        i+=1
                
            else:
                # il s'agit d'un pion bleu       
                c = (s_ligne-1)*10+(s_colonne-1)
                if case_libre(c):
                    pos.append(c)
                else:
                    c2 = (s_ligne-2)*10+(s_colonne-2)
                    if case_libre(c2) and c in pions_b:
                        pos.append(c2)
                        prenable.append(c2)
                        prenable.append(c)
                        
                c = (s_ligne-1)*10+(s_colonne+1)
                if case_libre(c):        
                    pos.append(c)
                else:
                    c2 = (s_ligne-2)*10+(s_colonne+2)
                    if case_libre(c2) and c in pions_b:
                        pos.append(c2)
                        prenable.append(c2)
                        prenable.append(c)

                # si il s'agit d'une dame, il y a d'autre possibilitées
                if pions_n.index(n_case) in dame_n:
                    # déplacement haut-droit
                    i = 1
                    while i < 10:
                        l = s_ligne - i
                        cl = s_colonne + i
                        if l >= 0 and cl < 10:
                            c = l*10+cl
                            if case_libre(c):
                                pos.append(c)
                            elif c in pions_n:
                                break
                            else:
                                c2 = (l-1)*10+(cl+1)
                                if case_libre(c2):
                                    pos.append(c2)
                                    prenable.append(c2)
                                    prenable.append(c)
                                break
                        else:
                            break
                        i+=1
                    # déplacement haut-gauche
                    i = 1
                    while i < 10:
                        l = s_ligne - i
                        cl = s_colonne - i
                        if l >= 0 and cl >= 0:
                            c = l*10+cl
                            if case_libre(c):
                                pos.append(c)
                            elif c in pions_n:
                                break
                            else:
                                c2 = (l-1)*10+(cl-1)
                                if case_libre(c2):
                                    pos.append(c2)
                                    prenable.append(c2)
                                    prenable.append(c)
                                break
                        else:
                            break
                        i+=1
                    # déplacement bas-droit
                    i = 1
                    while i < 10:
                        l = s_ligne + i
                        cl = s_colonne + i
                        if l < 10 and cl < 10:
                            c = l*10+cl
                            if case_libre(c):
                                pos.append(c)
                            elif c in pions_n:
                                break
                            else:
                                c2 = (l+1)*10+(cl+1)
                                if case_libre(c2):
                                    pos.append(c2)
                                    prenable.append(c2)
                                    prenable.append(c)
                                break
                        else:
                            break
                        i+=1
                    # déplacement bas-gauche
                    i = 1
                    while i < 10:
                        l = s_ligne + i
                        cl = s_colonne - i
                        if l < 10 and cl >= 0:
                            c = l*10+cl
                            if case_libre(c):
                                pos.append(c)
                            elif c in pions_n:
                                break
                            else:
                                c2 = (l+1)*10+(cl-1)
                                if case_libre(c2):
                                    pos.append(c2)
                                    prenable.append(c2)
                                    prenable.append(c)
                                break
                        else:
                            break
                        i+=1                

            if glob:
                # pour les tests on affiche les positions possibles
                i = 0
                while i < len(pos):
                    y = (((pos[i]/10)*case) + case/2)
                    x = ((pos[i]%10)*case) + case/2
                    # On a calculé le centre du cercle. On le dessine
                    can1.create_oval(x-15, y-15, x+15, y+15, fill='green')
                    i+=1
            else:
                return prenable

        def joueur_suivant():
            "on passe au joueur suivant"
            global joueur
            if joueur == 0:
                joueur = 1
            else:
                joueur = 0

            pions_prenable()

        def select(event):
            "Traite les clicks sur la souris"
            global selected
            # on détermine la case ou s'est passé la selection 
            ligne = event.y/case
            colonne = event.x/case
            num_case = ligne*10+colonne

            if selected == -1:
                y = ligne*case + case/2
                x = colonne*case + case/2
                if num_case in pions_b and joueur == 0:
                    if pions_b.index(num_case) in dame_b:
                        can1.create_rectangle(x-10, y-10, x+10, y+10, fill='yellow')
                    else:    
                        can1.create_oval(x-15, y-15, x+15, y+15, fill='yellow')
                    selected = num_case
                    possibilitees()
                elif num_case in pions_n and joueur == 1:
                    if pions_n.index(num_case) in dame_n:
                        can1.create_rectangle(x-10, y-10, x+10, y+10, fill='yellow')
                    else:
                        can1.create_oval(x-15, y-15, x+15, y+15, fill='yellow')
                    selected = num_case
                    possibilitees()
            else:
                # déplacement ou deselection
                if selected == num_case:
                    selected = -1
                    y = ligne*case + case/2
                    x = colonne*case + case/2
                    if num_case in pions_b:
                        can1.create_oval(x-15, y-15, x+15, y+15, fill='red')
                    else:
                        can1.create_oval(x-15, y-15, x+15, y+15, fill='blue')
                    # on redessine le plateau
                    damier()
                    place_pions()
                else:
                    if deplacement(num_case):
                        joueur_suivant()
                    selected = -1
                    damier()
                    place_pions()

        def restart():
            "Redémarre la partie"
            global bleu, rouge, pions_b, pions_n, selected, joueur, dame_b, dame_n, j1, j2, started
            bleu, rouge, selected, joueur = 0, 0, -1, 0
            pions_b = [0, 2, 4, 6, 8, 11, 13, 15, 17, 19, 20, 22, 24, 26, 28, 31, 33, 35, 37, 39]
            pions_n = [60, 62, 64, 66, 68, 71, 73, 75, 77, 79, 80, 82, 84, 86, 88, 91, 93, 95, 97, 99]
            dame_n = []
            dame_b = []
            j1 = askstring("Nouvelle Partie...", "Joueur 1:")
            j2 = askstring("Nouvelle Partie...", "Joueur 2:")
            started = True
            #damier()
            #place_pions()
            
        def interface():
            "Dessine la GUI"
            global fenjeu, can0, can1, bt1, bt2, chaine, txt1, txt2
            self.hide()
            fenjeu = Toplevel()

            #Dimensions fenjeu
            w=800
            h=800

            #Récup dimensions écran
            ws = fenjeu.winfo_screenwidth()
            hs = fenjeu.winfo_screenheight()

            #Calcul pt haut-gauche canvas 
            x = (ws/2) - (w/2)
            y = (hs/2) - (h/2)

            #Création fenêtre
            fenjeu.geometry('%dx%d+%d+%d' % (w, h, x, y))
            fenjeu.title("Fanorona | Jouer")
            fenjeu.resizable(0,0)
            
            can1 = Canvas(fenjeu, width=800, height=600, bg="lightgrey")
            can1.bind("<Button-1>", select)
            can1.pack()

            bt1 = Button(fenjeu, text='Quitter', command=self.quitter)
            bt1.pack(side=LEFT)
            '''
            chaine = Label(fenjeu)
            chaine.configure(text="", fg='red')
            chaine.pack()
            txt1 = Label(fenjeu, text='')
            txt2 = Label(fenjeu, text='')
            txt1.pack()
            txt2.pack()

            bt2 = Button(fenjeu, text='Nouvelle Partie', command=restart)
            bt2.pack(side=RIGHT)
            damier()
            place_pions()
	    '''
            
            def onClosefenjeu(fenjeu):
                """"""
                fenjeu.destroy()
                self.show()

            root.protocol("WM_DELETE_WINDOW", onClosefenjeu)
            
            fenjeu.mainloop()
        #--- Programme principal ---

        started = False
        selected = -1
        j1 = ''
        j2 = ''
        joueur = 0
        bleu = 0
        rouge = 0
        case = 40
        # on définit notre tableau de pions

        #pions blanc
        pions_b = []
        dame_b = []
        #pions noir
        pions_n = []
        dame_n = []
        sauter_pas_jouer = []
  
        interface()

    def openpropos(self):
        """"""
        fenpropos = Toplevel()
        w=400
        h=200
        ws = fenpropos.winfo_screenwidth()
        hs = fenpropos.winfo_screenheight() 
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        fenpropos.geometry('%dx%d+%d+%d' % (w, h, x, y))
        fenpropos.title("Fanorona | A propos")
        
        label = Label(fenpropos, text="Fanorona a été crée par Ryan, Yoan et Mathieu \n pour le projet ISN 2016")
        label.pack(pady=50)
        
        handler = lambda: self.onClosefenpropos(fenpropos)
        btn = Button(fenpropos, text="Fermer", command=handler, width=15)
        btn.pack(pady=10)
                
     
    #----------------------------------------------------------------------       
    def onClosefenpropos(self, fenpropos):
        fenpropos.destroy()
        
    def quitter(self):
        self.root.destroy()
            
    #----------------------------------------------------------------------
    def show(self):
        """"""
        self.root.deiconify()    
    
#----------------------------------------------------------------------
if __name__ == "__main__":
    root = Tk()
    w=800
    h=600
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight() 
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
    background_image = PhotoImage(file="media/background_menu.png")
    background_label = Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    can=Canvas(root,width=295,height=140, bd=0, highlightthickness=0)
    photo = PhotoImage(file="media/fanorona.png")
    can.create_image(150,70,image=photo)
    can.pack()  
    
    app = MyApp(root)
    root.mainloop()
