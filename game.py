from backend import *
import time
import random
import os

# Début de partie
os.system('cls')
player_one_ask_name = input("Joueur 1, entrez votre nom:\n")
player_two_ask_name = input("Joueur 2, entrez votre nom:\n")
paquet_de_waribatche = Paquet_de_carte()
table = Table()
player_1 = Hand(player_one_ask_name)
player_2 = Hand(player_two_ask_name)

#distribution
print("Vos cartes vous seront distribuer sous peu...")
time.sleep(3)
paquet_de_waribatche.melanger() 
paquet_de_waribatche.distribuer(player_1, player_2, 16)
print("---------------------------------------------------------")
print("Les cartes on été distribué, il reste:", paquet_de_waribatche.get_paquet_length(), "carte dans le paquet de carte.")

#annonces
time.sleep(3)
print("---------------------------------------------------------")
print("Dans cette version, le jeu se déroulera de manière automatique avec des temps d'attentes pour que vous puissiez voir le déroulement de la partie.")
print("---------------------------------------------------------")
time.sleep(3)

ask_for_sure = input("Avez vous compris, tapez: ok\n")
run = False
while run is False:
    if ask_for_sure == "ok":
        os.system('cls')
        print("! LE JEU PEU COMMENCE !")
        time.sleep(3)
        os.system('cls')
        run = True
    else:
        ask_for_sure = input("Dans cette version, le jeu se déroulera de manière automatique avec des temps d'attentes pour que vous puissiez voir le déroulement de la partie.\nAvez vous compris, tapez: ok\n")

# Start
time.sleep(1.4)
have_jeton = random.choice([player_1, player_2])
have_jeton.a_toi()

while player_1.get_hand_lenght()>0 and player_2.get_hand_lenght()>0:
    if player_1.est_ce_a_toi() == True:
        table.ajouter_table(player_1)
        print("------------------",player_one_ask_name,"A JOUER, Il A", player_1.get_hand_lenght(),"CARTES--------------------")
        table.afficher()
        print("---------------------------------------------------------")
        player_1.pas_a_toi()
        player_2.a_toi()
        time.sleep(2)
    else:
        table.ajouter_table(player_2)
        print("------------------",player_two_ask_name,"A JOUER, Il A", player_2.get_hand_lenght(),"CARTES--------------------")
        table.afficher()
        print("---------------------------------------------------------")
        player_2.pas_a_toi()
        player_1.a_toi()
        time.sleep(2)

    if table.compare() == True:
        if player_1.est_ce_a_toi() == False:
            table.ramasser(player_1) 
            print("////////////////////////////////////////////////")
            print(player_one_ask_name, "vien de ramasser, il possède", player_1.get_hand_lenght(), "carte")
            print("////////////////////////////////////////////////")
            time.sleep(2)
        if player_2.est_ce_a_toi() == False:
            table.ramasser(player_2)
            print("////////////////////////////////////////////////")
            print(player_two_ask_name, "vien de ramasser, il possède", player_2.get_hand_lenght(), "carte")
            print("////////////////////////////////////////////////")
            time.sleep(2)

if player_1.get_hand_lenght() == 0:
    print("\n\n\n", player_two_ask_name,"à gagné ! avec", player_2.get_hand_lenght(),"cartes")

if player_2.get_hand_lenght() == 0:
    print("\n\n\n", player_one_ask_name,"à gagné ! avec", player_1.get_hand_lenght(),"cartes")