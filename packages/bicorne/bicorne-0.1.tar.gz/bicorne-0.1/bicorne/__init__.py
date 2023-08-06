## Cours Python Exercices:
import random
import os
import time
from math import *
import imp
from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess
import os

class Ide:
   def __init__(self, name):
      self.name = name + ".py"
      self.compiler = Tk()
      self.compiler.title("Bicorne-IDE")
      self.file_path = ''
      self.output = ""
      self.compiler.protocol("WM_DELETE_WINDOW", self.close)

      menu_bar = Menu(self.compiler)

      file_menu = Menu(menu_bar, tearoff=0)
      file_menu.add_command(label="Sauvegarder", command=self.save_as)
      file_menu.add_command(label="Soummette", command=exit)
      menu_bar.add_cascade(label="Fichier", menu=file_menu)

      run_bar = Menu(menu_bar, tearoff=0)
      run_bar.add_command(label="Lancer", command=self.run)
      menu_bar.add_cascade(label="Run", menu=run_bar)

      self.compiler.config(menu=menu_bar)
      self.editor = Text()
      self.editor.pack()
      self.code_output = Text(height=10)
      self.code_output.pack()
      self.compiler.mainloop()

   def set_file_path(self, path):
      self.file_path = self.path

   def save_as(self):
      self.path = os.getcwd() + '\\'+self.name
      with open(self.path, "w") as file:
         code = self.editor.get("1.0", END)
         file.write(code)
         self.set_file_path(self.path)

   def run(self):
      if self.file_path == "":
         save_prompt = Toplevel()
         text = Label(save_prompt, text="Sauvegardez votre code!")
         text.pack()
         return
      command = f"python {self.file_path}"
      process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr = subprocess.PIPE, shell=True)
      self.output, self.error = process.communicate()
      self.code_output.insert("1.0", self.output)
      self.code_output.insert("1.0", self.error)

   def close(self):
      self.save_as()
      self.run()
      if len(self.error) <= 5:
         self.compiler.destroy()
      else:
         self.code_output.insert("1.0", self.error)

   def getoutput(self):
      return self.output



def premiers(n):
  prem=list(range(2,n+1))
  k=2
  nRacine=sqrt(n)
  while k<nRacine:
    prem=[p for p in prem if p<=k or p%k!=0]
    k=prem[prem.index(k)+1]
  return prem

def wtProg(name):
   ide = Ide(name)

def dwnBar():
   def print_cosmicalisation_des_bicornes (corne,chevelure_argentee, goat = '',variable_arc_en_ciel = '',chevreMagique = 1,chevreCosmique = 100,fill = '>',arc_en_ciel_de_l_espace = "\r"):
           bicorneNb  = ("{0:." + str(chevreMagique) + "f}").format(100 * (corne / float(chevelure_argentee)))
           remplissage_de_la_chevreCosmique = int(chevreCosmique * corne // chevelure_argentee)
           cosmicalisation_des_bicornes = fill * remplissage_de_la_chevreCosmique + '-' * (chevreCosmique - remplissage_de_la_chevreCosmique)
           bicorneNb  = float(bicorneNb )
           print(
               f'\r{goat} <|{cosmicalisation_des_bicornes}|> {bicorneNb }%  * Ouverture de l\'apprentisseur 2000! {variable_arc_en_ciel}',
               end = arc_en_ciel_de_l_espace)

   teleportation = list(range(0, 57))
   l = len(teleportation)
   for i, item in enumerate(teleportation):
       time.sleep(0.01)
       print_cosmicalisation_des_bicornes(i + 1, l, goat = 'Chargement:', variable_arc_en_ciel = '', chevreCosmique = 50)


   time.sleep(1)
   os.system('cls' if os.name == 'nt' else 'clear')

def clear():
   os.system('cls' if os.name == 'nt' else 'clear')

def wait():
   input("Appuyez sur une touche pour continuer...")

def printmenu():
   clear()
   print("#"*50)
   print("Aprentisseur 2000")
   print("#"*50)
   print("\nQue voulez vous étudier jeune padawan?\n(1): Les variables\n(2): Les opérateurs logiques\n(3): La conversion de type\n(4): Les fonctions\n(5): Les conditions\n(6): La boucle While\n(7): Les tableaux\n(8): La boucle For\n(9): try/except\n(10): Les dictionnaires\n(11): Fonctions utiles en Python\n(12): Les imports\n")
   choice = input("")
   if choice == "1":
      exoVariables()
   if choice == "2":
      exoOp()
   if choice == '3':
      exoType()
   if choice == '4':
      exoFct()
   if choice == '5':
      exoCondition()
   if choice == "6":
      exoWhile()
   if choice == '7':
      exoTab()
   if choice == "8":
      exoFor()
   if choice == "9":
      exoTry()
   if choice == "10":
      exoDict()
   if choice == "11":
      exoUseFct()
   if choice == '12':
      exoImport()


def exoVariables():
   clear()
   global point
   point = 0
   allQuestions = [1, "\'a\'", "\'1\'", True, '\"True\"', "\'false\'", '\"32.5\"', 32.5, 32.0, '\"32.0\"']
   for _ in range(10):
      question = random.choice(allQuestions)
      print("#"*10)
      print(question)
      print("#"*10)
      del allQuestions[allQuestions.index(question)]
      def responding():
         print("Voici les réponses possibles:\n-int\n-str\n-bool\n-float")
         answer = input("Veuillez entrer le type de l'élément présenté ci-dessus:\n")
         if answer == 'int':
            answerType = int
         elif answer == 'str':
            answerType = str
         elif answer == 'bool':
            answerType = bool
         elif answer == 'float':
            answerType = float

         if answerType == type(question):
            print("Et c'est une bonne réponse!!")
            wait()
            clear()
            global point
            point += 1
         else:
            print("Hmmm c'est faux...")
            print(f"La réponse était en effet:{type(answer)}")
            wait()
            clear()
      responding()
   print(f"Vous venez d'obtenir {point} points / 10!")
   wait()

def exoOp():
   point = 0
   allQuestions = [["3", "5", "8"], ["3", "5", "-2"], ["3", "5", "15"], ["3", "5", "243"], ["10", "5", "2"], ["3", "5", "3"], ["3", "5", "0"]]
   for question in allQuestions:
      clear()
      print("Réécrire uniquement toute la partie avant le signe égal pour que cette égalité soit vraie:")
      strQuestion = f"{question[0]} _ {question[1]} = {question[2]}"
      print(strQuestion)
      response = input("")
      try:
         if eval(response) == int(question[2]):
            print("Bonne réponse!")
            point += 1
            wait()
         else:
            print("Mauvais opérateur logique...")
            wait()
      except:
         print("Celà ne veut rien dire!!")
         wait()
   print(f"Vous avez eu {point} points sur !")
   wait()

def exoType():
   def answ(allQuestions, allAnswers):
      point = 0
      score = 0
      for place, question in enumerate(allQuestions):
         score += 1
         print("#"*40)
         print(question)
         print("#"*40)
         print("-On ne précisera pas l'arguments.")
         answer = input("")
         if answer == allAnswers[place]:
            print("C'est une bonne réponse!")
            wait()
            clear()
            point += 1
         else:
            print("Hmm, mauvaise réponse!")
      print(f"Vous avez {point} points sur {score}!")
      wait()

   def question1():
      allQuestions = ["Convertir 3 à \'3\'", "Convertir \'3\' à 3", "Convertir 3.0 à 3", "Convertir 3 en 3.0"]
      allAnswers = ["str()", "int()", "int()", "float()"]
      answ(allQuestions, allAnswers)

   def question2():
      allQuestions = ["Convertir True à 1", "Convertir False à 0", "Convertir True à \'True\'", "Convertir 0 à False", "Convertir \'True\' à True"]
      allAnswers = ["int()", "int()", "str()", "bool()", "bool()"]
      answ(allQuestions, allAnswers)

   def menu():
      clear()
      print("Veuillez choisir un numéro d'exercice: ")
      print("(1): Généralités\n(2): Cas particuliers")
      questionNb = input("Veuillez entrer l'index de la question: ")
      if questionNb == '1':
         clear()
         question1()
      elif questionNb == '2':
         clear()
         question2()
      else:
         print("Entrée impossible")
         menu()
   menu()

def exoFct():
   def menu():
      clear()
      print("Veuillez chosir le numéro de l'exercice:")
      print("(1): La fonction carré\n(2): Fonction affine")
      choice = input("Veuillez entrer l'index de l'exercice:")
      if choice == "1":
         question1()
      elif choice == "2":
         question2()
      else:
         print("Ce choix est impossible")
         wait()

   def question1():
      print("Vous allez devoir faire une fonction [fct] (sans crochets) qui prend en argument un nombre x et qui retourne le carré de ce nombre.")
      wtProg('fonction')
      import fonction as fct
      imp.reload(fct)
      try:
         if fct.fct(2)==4 and fct.fct(4)==16:
            print("Tous les tests sont passés!")
            wait()
         else:
            print("Au moins un des tests s'est mal passé...")
            wait()
      except:
         print("Il y a une erreur dans le programme")
         wait()
   def question2():
      print("Vous allez devoir faire une fonction [fct] (sans crochets) qui prend en argument un nombre x et qui retourne 3x+2")
      wtProg('fonction')
      import fonction as fct
      imp.reload(fct)
      try:
         if fct.fct(0) == 2 and fct.fct(1) == 5 and fct.fct(-1) == -1:
            print("Tous les tests sont passés!")
            wait()
         else:
            print("Au moins un des tests est faux!")
            wait()
      except:
         print("Le programme contient au moins une erreur")
         wait()
   menu()

def exoCondition():

   def question1():
      print("Faire une fonction nommée [cond] (sans crochets) qui renvoie True si un nombre x est suppérieur ou égal à 0, sinon False")
      wtProg('condition')
      import condition
      imp.reload(condition)
      try:
         if condition.cond(-1) == False and condition.cond(2) == True and condition.cond(0) == True:
            print("Le programme s'éxécute correctement!!")
            wait()
         else:
            print('Mauvais réponse... Il y a une erreur dans le programme.')
            wait()
      except:
         print("Il y a une erreur dans le programme.")
         wait()

   def question2():
      print("Faire une fonction nommée [cond] (sans crochets) qui renvoie 1 si le mot envoyé est 'bleu', 2 si c'est 'rouge' et 3 sinon.")
      wtProg('condition')
      import condition
      imp.reload(condition)
      try:
         if condition.cond("bleu") == 1 and condition.cond("rouge")==2 and condition.cond("test")==3:
            print("Les tests sont réussis!")
            wait()
         else:
            print("Au moins une sortie du programme est fausse")
            wait()
      except:
         print("Il y a une erreur dans le programme.")
         wait()

   def question3():
      print("Faire une fonction [cond] (sans crochets) qui renvoie True si un nombre x est paire et suppérieur à 7")
      wtProg("condition")
      import condition
      imp.reload(condition)
      try:
         if condition.cond(8) == True and condition.cond(10) == True and condition.cond(4) == False and condition.cond(15) == False:
            print("Les tests sont réussis!")
            wait()

         else:
            print("Au moins une sortie est fausse!")
            wait()
      except:
         print("Le programme ne s'execute pas correctement.")
         wait()
   def question4():
      print("Faire une fonction [cond] (sans crochets) qui renvoie True si un nombre x est strictement suppérieur à 2 ou strictement inférieur à -2, sinon False")
      wtProg("condition")
      import condition
      imp.reload(condition)
      try:
         if condition.cond(-3) == True and condition.cond(3) == True and condition.cond(2) == False and condition.cond(-2) == False and condition.cond(1)==False:
            print("Tous les tests sont réussis!")
            wait()
         else:
            print("Au moins une sortie est fausse!")
            wait()
      except:
         print("Il y a une erreur dans le programme!")
         wait()

   def menu():
      clear()
      print("Veuillez choisir un numéro d'exercice: ")
      print("(1): if/else\n(2): if/elif/else\n(3): and\n(4): or")
      questionNb = input("Veuillez entrer l'index de la question: ")
      if questionNb == '1':
         clear()
         question1()
      elif questionNb == '2':
         clear()
         question2()
      elif questionNb == '3':
         clear()
         question3()
      elif questionNb == '4':
         clear()
         question4()
      else:
         print("Entrée impossible")
         menu()
   menu()

def exoWhile():
   def menu():
      clear()
      print("Veuillez choisir un numéro d'exercice: ")
      print("(1): Exercice 1\n(2): Exercice 2\n(3): Exercice 3")
      questionNb = input("Veuillez entrer l'index de la question: ")
      if questionNb == '1':
         clear()
         question1()
      elif questionNb == '2':
         clear()
         question2()
      elif questionNb == '3':
         clear()
         question3()
      else:
         print("Entrée impossible")
         menu()

   def question1():
      print("Votre but est d'écrire une fonction [boucle] (sans crochets) qui retourne le nombre de fois qu'on peut diviser un nombre par 5 (par exemple 15, comme c'est 3*5, on ne peut le diviser que une fois par 5)")
      wtProg("boucleWhile")
      import boucleWhile as bcl
      imp.reload(bcl)
      try:
         if bcl.boucle(15) == 1:
            print("Test 1 passé!")
            wait()
         else:
            print("Test 1 échoué!")
            wait()
         if bcl.boucle(125) == 3:
               print("Test 2 passé")
               wait()
         else:
               print("Test 2 échoué")
               wait()
         if bcl.boucle(1125) == 3:
            print("Test 3 passé!")
            wait()
         else:
            print("Test 3 échoué!")
            wait()
      except:
         print("Il y a une erreur dans le programme...")
         wait()
   def question2():
      print("Votre but est d'écrire une fonction [boucle] (sans crochets) qui retourne le nombre de fois qu'on peut ajouter 1 à un nombre avant qu'il ne devienne premier (par exemple si on part de 5, on peut ajouter 2 avant d'arriver à 7)")
      wtProg("boucleWhile")
      import boucleWhile as bcl
      imp.reload(bcl)
      try:
         if bcl.boucle(14) == 3:
            print("Test 1 passé!")
            wait()
         else:
            print("Test 1 échoué!")
            wait()
         if bcl.boucle(12) == 1:
            print("Test 2 passé!")
            wait()
         else:
            print("Test 2 échoué!")
         if bcl.boucle(11) == 0:
            print("Test 3 passé!")
            wait()
         else:
            print("Test 3 échoué!")
            wait()
      except:
         print("Le programme contient au moins une erreur")
         wait()

   def question3():
      print("Faire une fronction [boucle] (sans crochets) qui prend en argument une année, un salaire et une somme de départ, et qui renvoie l'année où l'argent total de la personne exedera 1000€.")
      wtProg("boucleWhile")
      import boucleWhile as bcl
      imp.reload(bcl)
      try:
         if bcl.boucle(2020, 10, 10) == 2119 and bcl.boucle(0, 0, 10000) == 0 and bcl.boucle(2020, 50, 0) == 2040:
            print("Tous les tests sont réussis!")
            wait()
         else:
            print("Au moins l'un des tests est échoué...")
            wait()
      except:
         print("Il y a une erreur dans le programme")
         wait()
   menu()

def exoTab():
      def menu():
         clear()
         print("Veuillez choisir un numéro d'exercice: ")
         print("(1): Indexage\n(2): Fonction de bases\n(3): Opérations sur les tableau\n(4): Exercice pour compiler tous ces éléments" )
         questionNb = input("Veuillez entrer l'index de la question: ")
         if questionNb == '1':
            clear()
            question1()
         elif questionNb == '2':
            clear()
            question2()
         elif questionNb == '3':
            clear()
            question3()
         elif questionNb == '4':
            clear()
            question4()
         else:
            print("Entrée impossible")
            menu()

      def question1():
         points = 0
         print("Ecrire les moyens d'obtenir les éléments dans le tableau suivant en respectant les indications.")
         wait()
         allQuestions = ["Afficher le premier élément de la liste", "Afficher le trosième élément de la liste", "Afficher le dernier élément de la liste", "Afficher l'avant dernier élément de la liste"]
         allAnswers = ["tab[0]", "tab[2]", "tab[-1]", "tab[-2]"]
         for question in allQuestions:
            clear()
            print("#"*50)
            print("tab =  [\'salade\', 1, True, \'bob\', ... , 2, 3]")
            print(question)
            print("#"*50)
            answ = input("")
            if answ == allAnswers[allQuestions.index(question)]:
               print("Bonne réponse!")
               points += 1
               wait()
            else:
               print("Réponse fausse")
               wait()
         print(f"Vous avez {points} sur 4!")

      def question2():
         points = 0
         print("Je vais vous poser un problème, et vous allez devoir dire la fonction, sans argument, que vous jugez bon d'utiliser:")
         allQuestions = ["Convertir un tableau en string", "Ajouter un élément à un tableau", "Dire la taille d'un tableau", "Supprimer un élément d'un tableau à partit d'un indexe", "Mettre une liste à l'envers", "Trier une liste", "Retourner l'indexe d'un élément", "Faire l'addition de tous les éléments d'un tableau", "supprimer un élément d'un tableau sans connaitre son index", "compter le nombre de fois qu'un élément apparait dans un tableau"]
         allAnswers = ["join()", "append()", "len()", "del()", "reverse()", "sort()", "index()", 'sum()', 'remove()', "count()"]
         for question in allQuestions:
            clear()
            print("#"*50)
            print(question)
            print("#"*50)
            answ = input("")
            if answ == allAnswers[allQuestions.index(question)]:
               print("Bonne réponse!")
               points += 1
               wait()
            else:
               print("Réponse fausse")
               wait()
         print(f"Vous avez {points} sur 9!")
         wait()
      def question3():
         points = 0
         print("Je vais demander de faire une opération sur un tableau et il va falloir écrire la ligne de code servant à faire cela.")
         wait()
         allQuestions = ["Ajouter un 3 à un tableau tab", "Prendre tous les éléments d'un tableau tab jusqu'au troisième exclu", "Prendre tous les éléments d'un tableau tab au delà de l'indexe 3 exclu"]
         allAnswers = ["tab.append(3)", "tab[:2]", "tab[2:]"]
         for question in allQuestions:
            clear()
            print("#"*50)
            print(question)
            print("#"*50)
            answ = input("")
            if answ.count(allAnswers[allQuestions.index(question)]) >=1:
               print("Bonne réponse!")
               points+=1
               wait()
            else:
               print("Mauvaise réponse!")
               wait()
         print(f"Vous avez eu {points} sur 3!")
      def question4():
         print("Vous allez devoir faire une fonction [tab] qui prend en argument un tableau d'une longueur n+1 (n étant l'indexe du dernier élément). Il faudra supprimer l'élément n-2 et faire la somme de tous les éléments du tableau (ce sont tous des nombres)")
         print("Par exemple: [1, 2, 3, 4, 5] => On supprime l'élément n-2, soit l'élément d'index 2 (on rappelle qu'on commence à 0) => [1, 2, 4, 5] => On fait la somme de tous les éléments => 12")
         print("La fonction s'appelant [tab], on ne peut attribuer ce nom à aucun élément.")
         wait()
         wtProg("tableau")
         import tableau as tb
         imp.reload(tb)
         try:
            if tb.tab([1, 2, 3, 4, 5]) == 12 and tb.tab([12, 98, 67, 56, 90]) == 256:
               print("Tous les tests sont passés!")
               wait()
            else:
               print("Au moins l'un des tests est faux!")
               wait()
         except:
            print("Il y a une erreur dans le programme.")
            wait()
      menu()
def exoFor():
   def menu():
      clear()
      print("Veuillez choisir un numéro d'exercice: ")
      print("(1): Les range\n(2): Parcourir un tableau\n(3): Exercice" )
      questionNb = input("Veuillez entrer l'index de la question: ")
      if questionNb == '1':
         clear()
         question1()
      elif questionNb == '2':
         clear()
         question2()
      elif questionNb == '3':
         clear()
         question3()
      else:
         print("Entrée impossible")
         menu()

   def question1():
      points = 0
      print("Je vais afficher des tableaux de chiffres, et il faudra écrire la range correspondante.\nExemple: [0, 1, 2] => range(3)")
      wait()
      allQuestions = ["[0, 1, 2, 3]", "[0, 2, 4, 6, 8]", "[2, 3, 4]"]
      allAnswers = ["range(4) range(0, 4) range(0,4)", "range(0, 10, +2) range(0,10,+2) range(0, 9, +2) range(0,9,+2)", "range(2, 5) range(2,5)"]
      for place, question in enumerate(allQuestions):
         clear()
         print("#"*40)
         print(question)
         print("#"*40)
         answ = input("")
         if allAnswers[place].count(answ)>=1:
            print("Bonne réponse!")
            points +=1
            wait()
         else:
            print("Mauvaise réponse")
            wait()
      print(f"Vous avez {points} sur 3")

   def question2():
      print("Vous aller devoir écrire une fonction [boucle] qui prendra en argument un tableau et qui retournera un tableau contenant lui même une liste contenant uniquement les mots comportant un \'a\'.")
      wait()
      wtProg("boucle")
      import boucle as bcl
      imp.reload(bcl)
      try:
         if bcl.boucle(["salade", "pomme", "poire"]) == ['salade']:
            print("Test 1 passé")
            wait()
         else:
            print("Test 1 échoué!")
            wait()
         if bcl.boucle([]) == []:
            print("Test 2 passé!")
            wait()
         else:
            print("Test 2 échoué!")
            wait()
         if bcl.boucle(["pomme", "poire"]) == []:
            print("Test 3 passé!")
            wait()
         else:
            print("Test 3 échoué...")
            wait()
      except:
         print("Il y a une erreur dans le programme")
   def question3():
      print("La liste de courses: Vous allez devoir faire un programme composée de plusieurs fonctions pour répondre à un problème.")
      print("Il faut au départ commencer avec un tableau vide, et les fonctions demandées sont:")
      print("Une fonction addToTab(), qui prend en argument notre liste de course et un élément, et qui l'ajoute à cette liste. La fonction retourne alors cette dernière")
      print("Une fonction delFromTab(), qui prend en argument notre liste de course et un élément à enlever de la liste. La fonction retourne alors cette liste")
      print("Une fonction getVegetables() qui prend en argument notre liste de course et une liste de légumes (qui sera définie lors des tests) et qui retourne la liste des légumes compris dans notre liste de course")
      wait()
      wtProg("boucle")
      import boucle as bcl
      imp.reload(bcl)
      try:
         origin_list = ["Pomme de Terre", "Carotte", "Salade"]
         if bcl.addToTab(origin_list, "Poireau") == ["Pomme de Terre", "Carotte", "Salade", "Poireau"]:
            print("La fonction addToTab fonctionne...")
            wait()
         else:
            print("La fonction addToTab ne marche pas...")
            wait()
      except:
         print("Il y a une erreur dans la fonction addToTab")
      try:
         if bcl.delFromTab(origin_list, "Carotte") == ["Pomme de Terre", "Salade", "Poireau"]:
            print("La fonction delFromTab fonctionne...")
            wait()
         else:
            print("La fonction delFromTab ne fonctionne pas...")
            wait()

      except:
         print("Il y a une erreur dans la fonction delFromTab")
      try:
         if bcl.getVegetables(origin_list, ["Salade"]) == ["Salade"]:
            print("La fonction getVegetables fonctionne...")
            wait()
         else:
            print("La fonction getVegetables ne fonctionne pas")
            wait()
      except:
         print("La fonction getVegetables ne fonctionne pas...")
         wait()
   menu()
def exoTry():
   print("Vous allez devoir créer une fonction [exception] (sans crochets) qui prend en argument un élément x, et qui retournera ce même élément converti en int. Attention, il est possible de recevoir un élément non convertissable, auquel cas le programme retournera un 0.")
   wtProg("tryProg")
   import tryProg as tP
   imp.reload(tP)
   if tP.exception("1") == 1:
      print("Test 1 passé!")
      wait()
   else:
      print("Test 1 échoué...")
      wait()
   if tP.exception("10") == 10:
      print("Test 2 passé")
      wait()
   else:
      print("Test 2 échoué")
      wait()
   if tP.exception('a') == 0:
      print("Test 3 passé")
      wait()
   else:
      print("Test 3 échoué.")

def exoDict():

   def mission():
      clear()
      print("Je vais vous transmettre un dictionnaire nommé dico. Votre mission si vous l'aceptez:")
      print("-Vérifier que l'un de ces éléments existe dans le dictionnaire: 'bob', 'rene' ou bien 'frank'")
      print("-Supprimer les éléments de la liste ci-dessus qui existent dans le dictionnaire")
      print("-Ajouter la clé 'remy' qui aura pour valeur 10")
      print("-Assigner à la clé 'paul' la valeur 10")

   def console():
      import dictionnaire as dt
      imp.reload(dt)
      dico = dt.dicoReturn()
      mission()
      print("-"*50)
      print("Bienvenue dans la console, vous pouvez utiliser les commandes que vous voulez ici. Vous pouvez utliser aussi les commandes 'clear()' pour effacer tout le contenu de votre page et 'end' pour soumettre votre dictionnaire modifié. Vous pouvez finalement utiliser 'new()' pour re-tenter votre chance avant la soumission. mission() permet de réafficher les objectifs")
      isTypping = None
      while isTypping != 'end':
         isTypping = input(">>> ")
         try:
            if isTypping == "new()":
               dico = dt.dicoReturn()
               clear()
               mission()
            else:
               exec(isTypping)
         except:
            print("Erreur, ce que vous écrivez ne veut rien dire")
      if dt.dicoCorrection() == dico:
         print("Bravo, vous avez réussi votre mission!")
         wait()
      else:
         print('Hmm... je crois que vous n\'êtes pas allé au bout de vos objectifs!')
         wait()
   console()


def exoUseFct():
   def questions(q,a):
      for place, question in enumerate(q):
         clear()
         print("#"*90)
         print(question)
         print("#"*90)
         answ = input("")
         if answ == a[place]:
            print("Bonne réponse!")
         else:
            print('Mauvaise réponse...')
         wait()
      menu()


   def menu():
      clear()
      print("Veuillez entrer l'index de la catégorie que vous voulez:")
      print("(1): Les entrée utilisateur\n(2): Les conversions de type avancées\n(3): Les fonctions sur les tableaux\n(4): Les fichiers\n(5): Les chaînes de caractères\n(6): Les boucles, astuces")
      choice = input("")
      if choice == "1":
         allQuestions = ["Quelle est la fonction permettant à l'utilisateur de rentrer du texte?", "Quel est la fonction permettant de séparer un string en liste au niveau d'un caractère donné?", "Quelle est la focntion permettant d'afficher un élément?"]
         allAnswers = ["input()", "split()", "print()"]
         questions(allQuestions, allAnswers)
      elif choice == "2":
         allQuestions = ["Quelle est la fonction pour convertir une variable en dictionnaire?", "Quelle est la fonction permettant de convertir une variable en tuple?"]
         allAnswers = ["dict()", "tuple()"]
         questions(allQuestions, allAnswers)
      elif choice == "3":
         allQuestions = ["Quelle' est la fonction qui permet d'insérer un élément dans une liste à un index donné?", "Quelle est la fonction opermettant d'avoir le minimum d'une liste?", "Quelle est la fonction permettant d'avoir le maximum d'une liste?"]
         allAnswers = ["insert()", "min()", "max()"]
         questions(allQuestions, allAnswers)
      elif choice == "4":
         allQuestions = ["Quelle est la fonction permettant d'ouvrir un fichier ? (sans arguments)", "Quelle est la fonction permettant d'écrire un élément dans un fichier?","Quelle est la fonction permettant de convertir un fichier en string?"]
         allAnswers = ["open()", "write()", "readlines()"]
         questions(allQuestions, allAnswers)
      elif choice == "5":
         allQuestions = ["Quelle est la fonction permettant de mettre toutes les lettres d'un string en majuscules", "Quelles est ma fonction permettant de mettre toutes les lettres d'un string en majuscule?", "Quelle est la fonction permettant de mettre en masjucule le premirer caractère d'un string?", "Quelle est la fonction permettant de remplacer tous les élément définis d'une liste (par exemple les a) par un autre élément?", "Quelle est la fonction qui renvoie True si une chaine de caractères commence par une suite de caractères donnée, sinon False?", "Quelle est la fonction qui renvoie True si un string termine par une suite de caractères, sinon False"]
         allAnswers = ["lower()", 'upper()', "capitalize()", "replace()", "startswith()", "endswith()"]
         questions(allQuestions, allAnswers)
      elif choice == "6":
         allQuestions = ["Quelle est la fonction renvoyant un itérable contenant les indexs des éléments d'une liste et ce qu'ils contiennent"]
         allAnswers = ["enumerate()"]
         questions(allQuestions, allAnswers)
      else:
         print("Entrée impossible!")
         wait()
         menu()
   menu()


def exoImport():
   def questions(q,a):
      for place, question in enumerate(q):
         clear()
         print("#"*90)
         print(question)
         print("#"*90)
         answ = input("")
         if answ == a[place]:
            print("Bonne réponse!")
         else:
            print('Mauvaise réponse...')
         wait()
      printmenu()

   def menu():
      clear()
      print("Veuillez choisir un numéro d'exercice: ")
      print("(1): Généralités\n(2): Random\n(3): OS" )
      questionNb = input("Veuillez entrer l'index de la question: ")
      if questionNb == '1':
         clear()
         q = ["Comment importer random?", "Comment importer randint du module random?", 'Comment importer random sous la contraction rd?']
         a = ["import random", "from random import randint", "import random as rd"]
         questions(q, a)
      elif questionNb == '2':
         clear()
         question2()
      elif questionNb == '3':
         clear()
         print("Je vais poser des questions et vous allez devoir y répondre. On prendra en compte que les fonctions à écrire ne prennent aucun argument et sont directement importées (pas besoin de mettre os.fonct() mais seulement fonct())")
         q = ["Quelle est la fonction permettant d'obtenir le chemin courant?", "Quelle est la fonction permettant de changer de dossier courant?", "Quelle est la fonction pour utiliser une commande Shell?", "Quelle est la fonction qui permet de créer un nouveau fichier?", "obtenir le nom de la personne utilisant le terminal"]
         a = ["getcwd()", "chdir()", 'system()', "mkdir()", "getlogin()"]
         questions(q, a)
      else:
         print("Entrée impossible")
         menu()

   def question2():
      clear()
      print("le modulre random:")
      print("Faire une fonction [rand] (sans crochets) qui prend en argument deux nombres a et b, avec a<b et qui renvoie un nombre aléatoire entre a et b")
      print("Faire ensuite une fonction [randTab] (sans crochets) qui prend en argument une liste et qui renvoie un élément aléatoire de cette liste")
      wtProg('rand')
      import rand as rd
      imp.reload(rd)
      try:
         if rd.rand(0, 5) >=0 and rd.rand(0, 8) <=8:
            print("La fonction rand fonctionne!")
            wait()
         else:
            print("La fonction rand est défaillante...")
            wait()
      except:
         print("Il y a une erreur dans le programme")
         wait()
      try:
         tab = [1, 4, 2, 90]
         if tab.count(rd.randTab(tab))>=1:
            print("La fonction randTab fonctionne")
            wait()
         else:
            print("La fonciton randTab ne fonctionne pas")
            wait()
      except:
         print("Il y a une erreur dans le programme")
         wait()


   menu()

def start():
   clear()
   dwnBar()
   while 1:
      printmenu()

start()
