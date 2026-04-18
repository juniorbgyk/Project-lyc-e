import tkinter as tk
import random
from backend import Paquet_de_carte, Table, Hand, Carte

# ── Constantes ────────────────────────────────────────────────────────────────
CARD_W  = 72
CARD_H  = 105

SYMBOLS = {"coeur": "♥", "carreau": "♦", "trèfle": "♣", "pic": "♠"}
COLORS  = {"coeur": "#c0392b", "carreau": "#c0392b",
           "trèfle": "#111111", "pic":    "#111111"}
LABELS  = {1: "A", 2: "2", 3: "3", 4: "4",
           5: "5", 6: "6", 7: "7", 8: "8"}


# ── Sprite de carte ───────────────────────────────────────────────────────────
class CardSprite:
    def __init__(self, canvas: tk.Canvas, carte: Carte,
                 x: float, y: float, face_up: bool = True):
        self.canvas   = canvas
        self.carte    = carte
        self.x        = float(x)
        self.y        = float(y)
        self.face_up  = face_up
        self.items: list[int] = []
        self._draw()

    # ── Dessin ────────────────────────────────────────────────────
    def _draw(self):
        self._clear()
        c          = self.canvas
        x, y, w, h = self.x, self.y, CARD_W, CARD_H

        if self.face_up:
            sym = SYMBOLS[self.carte.signe]
            col = COLORS[self.carte.signe]
            num = LABELS[self.carte.nombre]
            self.items += [
                self._rrect(x, y, x+w, y+h, 8,
                            fill="white", outline="#555", width=1),
                c.create_text(x+7,   y+7,    text=num, anchor="nw",
                              fill=col, font=("Georgia", 12, "bold")),
                c.create_text(x+7,   y+22,   text=sym, anchor="nw",
                              fill=col, font=("Georgia", 11)),
                c.create_text(x+w/2, y+h/2,  text=sym,
                              fill=col, font=("Georgia", 28, "bold")),
                c.create_text(x+w-7, y+h-7,  text=num, anchor="se",
                              fill=col, font=("Georgia", 12, "bold")),
                c.create_text(x+w-7, y+h-22, text=sym, anchor="se",
                              fill=col, font=("Georgia", 11)),
            ]
        else:
            self.items += [
                self._rrect(x, y, x+w, y+h, 8,
                            fill="#1a6b3c", outline="#444", width=1),
                self._rrect(x+5, y+5, x+w-5, y+h-5, 5,
                            fill="", outline="#6fcf97", width=1),
                c.create_text(x+w/2, y+h/2,
                              text="♦♣\n♥♠", fill="#6fcf97",
                              font=("Georgia", 13)),
            ]

    def _rrect(self, x1, y1, x2, y2, r, **kw) -> int:
        pts = [x1+r, y1,  x2-r, y1,  x2, y1+r,  x2, y2-r,
               x2-r, y2,  x1+r, y2,  x1, y2-r,  x1, y1+r]
        return self.canvas.create_polygon(pts, smooth=True, **kw)

    def _clear(self):
        for i in self.items:
            self.canvas.delete(i)
        self.items = []

    # ── API publique ──────────────────────────────────────────────
    def flip(self, face_up: bool):
        self.face_up = face_up
        self._draw()

    def lift(self):
        for i in self.items:
            self.canvas.tag_raise(i)

    def delete(self):
        self._clear()

    def move_to(self, tx: float, ty: float,
                steps: int = 22, delay: int = 10, callback=None):
        tx, ty = float(tx), float(ty)
        if steps <= 0:
            for i in self.items:
                self.canvas.move(i, tx - self.x, ty - self.y)
            self.x, self.y = tx, ty
            if callback:
                callback()
            return
        dx = (tx - self.x) / steps
        dy = (ty - self.y) / steps

        def _step(n: int):
            for i in self.items:
                self.canvas.move(i, dx, dy)
            self.x += dx
            self.y += dy
            if n > 1:
                self.canvas.after(delay, lambda: _step(n - 1))
            else:
                for i in self.items:               # snap exact
                    self.canvas.move(i, tx - self.x, ty - self.y)
                self.x, self.y = tx, ty
                if callback:
                    callback()

        _step(steps)


# ── Application principale ────────────────────────────────────────────────────
class WARIBATCHEApp:
    W, H = 980, 700

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("WARIBATCHE")
        self.root.resizable(False, False)
        self.root.configure(bg="#0b3319")

        self.canvas = tk.Canvas(root, width=self.W, height=self.H,
                                bg="#1a5c32", highlightthickness=0)
        self.canvas.pack()

        self._status_lbl  = None
        self.animating    = False
        self.game_running = False

        # La touche espace est toujours bindée — elle vérifie l'état du jeu
        self.root.bind("<space>", self._on_space)

        self._show_setup()

    # ═══════════════════════════════════════════════════════════════
    #  TOUCHE ESPACE
    # ═══════════════════════════════════════════════════════════════
    def _on_space(self, _event=None):
        if self.game_running and not self.animating:
            self._step()

    # ═══════════════════════════════════════════════════════════════
    #  ÉCRAN D'ACCUEIL
    # ═══════════════════════════════════════════════════════════════
    def _show_setup(self):
        self.game_running = False
        self.animating    = False
        self.canvas.delete("all")
        for w in self.canvas.winfo_children():
            w.destroy()
        if self._status_lbl:
            self._status_lbl.destroy()
            self._status_lbl = None

        cx = self.W // 2

        # Cartes décoratives aux coins
        for signe, nombre, x, y in [
            ("coeur",   7, 110, 155), ("pic",    3, self.W - 155, 145),
            ("carreau", 5,  95, 430), ("trèfle", 2, self.W - 140, 420),
        ]:
            CardSprite(self.canvas, Carte(signe, nombre), x, y, face_up=True)

        # Titre
        self.canvas.create_text(cx, 125, text="WARIBATCHE",
                                fill="#f9e79f", font=("Georgia", 52, "bold"))
        self.canvas.create_text(
            cx, 190,
            text="Même signe = ramasse les cartes   •   0 carte = perdu",
            fill="#abebc6", font=("Georgia", 13, "italic"))

        # Formulaire noms
        frm = tk.Frame(self.canvas, bg="#0e3d1e", padx=16, pady=16)
        for row, txt in enumerate(["Nom Joueur 1 :", "Nom Joueur 2 :"]):
            tk.Label(frm, text=txt, bg="#0e3d1e", fg="#d5f5e3",
                     font=("Georgia", 12)).grid(
                         row=row, column=0, pady=10, padx=10, sticky="e")
        self._e1 = tk.Entry(frm, font=("Georgia", 12), width=16, bg="#d5f5e3")
        self._e2 = tk.Entry(frm, font=("Georgia", 12), width=16, bg="#d5f5e3")
        self._e1.insert(0, "Joueur 1")
        self._e2.insert(0, "Joueur 2")
        self._e1.grid(row=0, column=1, pady=10, padx=10)
        self._e2.grid(row=1, column=1, pady=10, padx=10)
        self.canvas.create_window(cx, 295, window=frm)

        # Bouton démarrer
        btn = tk.Button(
            self.canvas, text="▶   COMMENCER LA PARTIE",
            font=("Georgia", 14, "bold"),
            bg="#e74c3c", fg="white",
            activebackground="#c0392b", activeforeground="white",
            padx=18, pady=10, relief="flat", cursor="hand2",
            command=self._start_game)
        self.canvas.create_window(cx, 435, window=btn)

    # ═══════════════════════════════════════════════════════════════
    #  INITIALISATION DE LA PARTIE
    # ═══════════════════════════════════════════════════════════════
    def _start_game(self):
        p1_name = self._e1.get().strip() or "Joueur 1"
        p2_name = self._e2.get().strip() or "Joueur 2"

        self.paquet    = Paquet_de_carte()
        self.table_obj = Table()
        self.p1        = Hand(p1_name)
        self.p2        = Hand(p2_name)
        self.paquet.melanger()
        self.paquet.distribuer(self.p1, self.p2, 16)

        # Tirage au sort du premier joueur
        first = random.choice([self.p1, self.p2])
        first.a_toi()
        (self.p2 if first == self.p1 else self.p1).pas_a_toi()

        self.p1_sprites: list[CardSprite] = []
        self.p2_sprites: list[CardSprite] = []
        self.table_sprites: list[CardSprite] = []

        self.canvas.delete("all")
        for w in self.canvas.winfo_children():
            w.destroy()

        self._draw_ui()
        self._redraw_hands()

        self.game_running = True
        self.animating    = False
        self._set_turn_status()

    # ═══════════════════════════════════════════════════════════════
    #  INTERFACE STATIQUE
    # ═══════════════════════════════════════════════════════════════
    def _draw_ui(self):
        c  = self.canvas
        cx = self.W // 2

        def zone(x1, y1, x2, y2, label, col_outline):
            c.create_rectangle(x1, y1, x2, y2,
                               fill="#0d3b1f", outline=col_outline, width=2)
            c.create_text((x1 + x2) // 2, y2 - 10, text=label,
                          fill=col_outline, font=("Georgia", 9, "bold"))

        zone(8,  8,          self.W - 8,  175,         self.p2.name, "#52be80")
        zone(8,  self.H-180, self.W - 8,  self.H - 8,  self.p1.name, "#52be80")
        zone(cx-200, 205,    cx + 200,   self.H - 210, "TABLE",      "#7fb3d3")

        # Compteurs de cartes
        self.p2_cnt = tk.StringVar(value="16")
        self.p1_cnt = tk.StringVar(value="16")
        for var, y, fg in [(self.p2_cnt, 92, "#f9e79f"),
                           (self.p1_cnt, self.H - 95, "#f9e79f")]:
            lbl = tk.Label(c, textvariable=var, bg="#1a5c32", fg=fg,
                           font=("Georgia", 17, "bold"), width=3)
            c.create_window(46, y, window=lbl)

        # Barre de statut
        self.status_var = tk.StringVar(value="")
        self._status_lbl = tk.Label(
            self.root, textvariable=self.status_var,
            bg="#0a2514", fg="#f0e6a2",
            font=("Georgia", 13, "bold"), pady=7)
        self._status_lbl.pack(fill="x")

    def _set_turn_status(self):
        """Affiche à qui c'est le tour et rappelle la touche."""
        name = self.p1.name if self.p1.est_ce_a_toi() else self.p2.name
        self.status_var.set(f"Tour de {name}  —  ESPACE pour jouer")

    # ═══════════════════════════════════════════════════════════════
    #  GESTION DES MAINS
    # ═══════════════════════════════════════════════════════════════
    def _peek_hand(self, hand: Hand) -> list[Carte]:
        """Lecture non-destructive de la main (plus ancienne → plus récente)."""
        cards = []
        while not hand.contenu.est_file_vide():
            cards.append(hand.contenu.defiler())
        for c in cards:
            hand.contenu.emfiler(c)
        return cards

    def _redraw_hands(self):
        for sp in self.p1_sprites:
            sp.delete()
        for sp in self.p2_sprites:
            sp.delete()
        self.p1_sprites.clear()
        self.p2_sprites.clear()

        # Les deux mains sont toujours face cachée
        self._fan(self._peek_hand(self.p1), self.p1_sprites,
                  y_center=self.H - 95, face_up=False)
        self._fan(self._peek_hand(self.p2), self.p2_sprites,
                  y_center=92,           face_up=False)

        self.p1_cnt.set(str(self.p1.get_hand_lenght()))
        self.p2_cnt.set(str(self.p2.get_hand_lenght()))

    def _fan(self, cards: list[Carte], sprite_list: list,
             y_center: int, face_up: bool):
        n = len(cards)
        if n == 0:
            return
        avail    = self.W - 160
        spacing  = max(10, min(CARD_W + 3, avail // max(n, 1)))
        total_w  = spacing * (n - 1) + CARD_W
        x0       = (self.W - total_w) // 2
        y        = y_center - CARD_H // 2
        for i, card in enumerate(cards):
            sprite_list.append(
                CardSprite(self.canvas, card, x0 + i * spacing, y,
                           face_up=face_up)
            )

    # ═══════════════════════════════════════════════════════════════
    #  BOUCLE DE JEU  (déclenchée par ESPACE)
    # ═══════════════════════════════════════════════════════════════
    def _step(self):
        if self.p1.get_hand_lenght() == 0 or self.p2.get_hand_lenght() == 0:
            self._end_game()
            return
        if self.p1.est_ce_a_toi():
            self._play(self.p1, self.p1_sprites, self.p2)
        else:
            self._play(self.p2, self.p2_sprites, self.p1)

    def _play(self, player: Hand, sprites: list, other: Hand):
        if not sprites:
            return
        self.animating = True
        self.status_var.set(f"{player.name} joue...")

        sprite = sprites.pop(0)
        card   = player.defiler_main()
        self.table_obj.ajouter_carte(card)

        # Position sur la table avec léger décalage en cascade
        n  = len(self.table_sprites)
        tx = self.W // 2 - CARD_W // 2 + min(n, 9) * 16
        ty = self.H // 2 - CARD_H // 2 + min(n, 9) * 7

        # La carte se retourne face visible en arrivant sur la table
        sprite.flip(True)
        sprite.lift()
        self.table_sprites.append(sprite)
        self.p1_cnt.set(str(self.p1.get_hand_lenght()))
        self.p2_cnt.set(str(self.p2.get_hand_lenght()))

        sprite.move_to(tx, ty, callback=lambda: self._check(player, other))

    def _check(self, player: Hand, other: Hand):
        if self.table_obj.compare():
            # Match de signe → pickup automatique puis attente espace
            self.status_var.set(f"{player.name} ramasse !")
            self.root.after(700, lambda: self._pickup(player, other))
        else:
            # Pas de match → changer de tour et attendre espace
            player.pas_a_toi()
            other.a_toi()
            self.animating = False
            self._set_turn_status()

    def _pickup(self, player: Hand, other: Hand):
        to_fly = list(self.table_sprites)
        self.table_sprites.clear()
        self.table_obj.ramasser(player)

        dest_y = self.H - CARD_H - 12 if player == self.p1 else 12
        dest_x = self.W // 2 - CARD_W // 2
        total  = len(to_fly)

        def fly_one(i: int):
            if i >= total:
                for sp in to_fly:
                    sp.delete()
                player.pas_a_toi()
                other.a_toi()
                self._redraw_hands()
                self.animating = False
                # Vérifier fin de partie puis attendre espace
                if self.p1.get_hand_lenght() == 0 or self.p2.get_hand_lenght() == 0:
                    self.root.after(400, self._end_game)
                else:
                    self._set_turn_status()
                return
            sp = to_fly[i]
            sp.flip(False)
            sp.move_to(dest_x, dest_y, steps=16, delay=8,
                       callback=lambda: fly_one(i + 1))

        fly_one(0)

    # ═══════════════════════════════════════════════════════════════
    #  FIN DE PARTIE
    # ═══════════════════════════════════════════════════════════════
    def _end_game(self):
        self.game_running = False
        p1n    = self.p1.get_hand_lenght()
        loser  = self.p1.name if p1n == 0 else self.p2.name
        winner = self.p2.name if p1n == 0 else self.p1.name

        cx, cy = self.W // 2, self.H // 2
        self.canvas.create_rectangle(
            cx - 280, cy - 130, cx + 280, cy + 150,
            fill="#051a0c", outline="#f9e79f", width=3)
        self.canvas.create_text(cx, cy - 80,
                                text="FIN DE PARTIE",
                                fill="#f9e79f", font=("Georgia", 32, "bold"))
        self.canvas.create_text(cx, cy - 20,
                                text=f"{winner}  GAGNE !",
                                fill="#f1c40f", font=("Georgia", 26, "bold"))
        self.canvas.create_text(cx, cy + 35,
                                text=f"{loser} n'a plus de cartes.",
                                fill="#e74c3c", font=("Georgia", 15))

        def restart():
            if self._status_lbl:
                self._status_lbl.destroy()
                self._status_lbl = None
            self._show_setup()

        btn = tk.Button(
            self.canvas, text="Rejouer",
            font=("Georgia", 13, "bold"),
            bg="#27ae60", fg="white",
            activebackground="#1e8449",
            padx=14, pady=8, relief="flat", cursor="hand2",
            command=restart)
        self.canvas.create_window(cx, cy + 105, window=btn)


# ── Lancement ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    WARIBATCHEApp(root)
    root.mainloop()
