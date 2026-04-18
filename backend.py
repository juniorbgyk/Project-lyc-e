import random

class Pile:
   
   def __init__(self):
      self.pile = []

   def afficher_pile(self):
      return self.pile
   
   def empiler(self, n):
      self.pile.append(n)

   def deplier(self):
     return self.pile.pop(len(self.pile)-1)

   def est_pile_vide(self):
    if not self.pile:
        return True
    else:
        return False 

   def sommet(self):
      return self.pile[len(self.pile)-1]   
   
   def taille_file(self):
      return len(self.pile)

class File:
   
   def __init__(self):
      self.file = []

   def afficher_file(self):
      return self.file
   
   def emfiler(self, n):
      self.file.insert(0, n)

   def defiler(self):
     return self.file.pop(len(self.file)-1)

   def est_file_vide(self):
    if not self.file:
        return True
    else:
        return False

   def sommet(self):
      return self.file[len(self.file)-1]
   
   def taille_file(self):
      return len(self.file)

class Carte:
    def __init__(self, signe, nombre):
        self.signe = signe
        self.nombre = nombre

    def presente(self):
       print(self.nombre, self.signe)

    def compare_signe(self, autre):
       return self.signe == autre.signe
   
class Hand: 
   def __init__(self, name):
      self.name = name
      self.contenu = File()
      self.jeton = False

   def get_hand_lenght(self):
      compteur = 0
      file_bench = File()
      while not self.contenu.est_file_vide():
         file_bench.emfiler(self.contenu.defiler())
         compteur += 1
      while not file_bench.est_file_vide():
         self.contenu.emfiler(file_bench.defiler())
      return compteur   
   
   def afficher(self):
      file_bench = File()
      print(self.name, "a pour carte:")
      while not self.contenu.est_file_vide():
         carte = self.contenu.defiler()
         carte.presente()
         file_bench.emfiler(carte)
      while not file_bench.est_file_vide():
         self.contenu.emfiler(file_bench.defiler())
   
   def emfiler_main(self, n):
      self.contenu.emfiler(n)

   def defiler_main(self):
      return self.contenu.defiler()

   def a_toi(self):
      self.jeton = True
   
   def pas_a_toi(self):
      self.jeton = False

   def est_ce_a_toi(self):
      return self.jeton

    
class Paquet_de_carte:
   signes = ["carreau", "trèfle", "coeur", "pic"]
   nombres = [1, 2, 3, 4, 5, 6, 7, 8]

   def __init__(self):
      self.paquet = []
      for i in self.signes:
         for y in self.nombres:
            self.paquet.append(Carte(i, y))

   def get_paquet_length(self):
      return len(self.paquet)

        
   def get_paquet(self):
      for i in self.paquet:
         print(i.presente())

   def melanger(self):
      return random.shuffle(self.paquet)
   
   def distribuer(self, joueur1, joueur2, carte_donner):
      for x in range(carte_donner):
         joueur1.emfiler_main(self.paquet.pop(0))
         joueur2.emfiler_main(self.paquet.pop(0))
   
class Table:
   def __init__(self):
      self.table = File()

   def ajouter_table(self, joueur):
      self.table.emfiler(joueur.defiler_main())

   def afficher(self):
      pile_bench = File()
      while not self.table.est_file_vide():
         carte = self.table.defiler()
         carte.presente()
         pile_bench.emfiler(carte)
      while not pile_bench.est_file_vide():
         self.table.emfiler(pile_bench.defiler())

   def ramasser(self, joueur):
      while not self.table.est_file_vide():
         joueur.emfiler_main(self.table.defiler())

   def ajouter_carte(self, carte):
      self.table.emfiler(carte)

   def compare(self):
      if self.table.taille_file() < 2:
         return False
      # emfiler insère en position 0 → file[0] = dernière carte jouée
      return self.table.file[0].compare_signe(self.table.file[1])