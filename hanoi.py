import tkinter as tk
from tkinter import messagebox


class HanoiGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Torre de Hanoi")

        # Top frame: controls
        ctrl = tk.Frame(root)
        ctrl.pack(fill=tk.X, pady=6)

        tk.Label(ctrl, text="Discos:").pack(side=tk.LEFT, padx=(6, 0))
        self.disk_var = tk.IntVar(value=3)
        self.disk_spin = tk.Spinbox(ctrl, from_=3, to=8, width=3, textvariable=self.disk_var, command=self.on_disk_count_change)
        self.disk_spin.pack(side=tk.LEFT, padx=4)

        self.move_label = tk.Label(ctrl, text="Movimientos: 0")
        self.move_label.pack(side=tk.LEFT, padx=12)

        tk.Button(ctrl, text="Reiniciar", command=self.reset_game).pack(side=tk.RIGHT, padx=6)
        tk.Button(ctrl, text="Auto-resolver", command=self.start_autosolve).pack(side=tk.RIGHT)

        # Canvas for towers and disks
        self.canvas = tk.Canvas(root, width=640, height=360, bg="#f8f8ff")
        self.canvas.pack(padx=8, pady=6)

        # Status / hints
        self.status = tk.Label(root, text="Selecciona un disco para moverlo.")
        self.status.pack(fill=tk.X, padx=8)

        # Game state
        self.towers = [[], [], []]
        self.disks = []
        self.selected_disk = None
        self.move_count = 0
        self.is_solving = False

        self.canvas.bind("<Button-1>", self.on_click)

        # Create initial game
        self.create_towers()
        self.create_disks()

    # --- UI / creation ---
    def create_towers(self):
        self.canvas.delete("tower")
        for i in range(3):
            x = 120 + i * 200
            self.canvas.create_rectangle(x - 4, 100, x + 4, 300, fill="#333", tags=("tower", f"tower{i}"))
            # base
            self.canvas.create_rectangle(x - 90, 300, x + 90, 312, fill="#666", tags=("tower",))
            self.towers[i] = []

    def create_disks(self):
        # Remove old disks
        for d in self.disks:
            try:
                self.canvas.delete(d)
            except Exception:
                pass
        self.disks = []
        for t in self.towers:
            t.clear()

        n = max(3, min(8, int(self.disk_var.get())))
        colors = ["#e74c3c", "#f39c12", "#2ecc71", "#3498db", "#9b59b6", "#1abc9c", "#e67e22", "#95a5a6"]
        max_width = 160
        min_width = 40
        step = (max_width - min_width) // (n - 1)

        for i in range(n):
            w = max_width - i * step
            x = 120
            y = 280 - i * 22
            disk = self.canvas.create_rectangle(x - w // 2, y - 18, x + w // 2, y, fill=colors[i % len(colors)], outline="#222", width=2, tags=("disk", f"disk{i}"))
            # store size as a tag for easy comparison
            self.canvas.addtag_withtag(f"w{w}", disk)
            self.towers[0].append(disk)
            self.disks.append(disk)

        self.move_count = 0
        self.update_move_label()
        self.selected_disk = None

    # --- Helpers ---
    def get_tower_index(self, x):
        if x < 220:
            return 0
        elif x < 420:
            return 1
        else:
            return 2

    def on_disk_count_change(self):
        if self.is_solving:
            return
        self.create_towers()
        self.create_disks()

    # --- Interaction ---
    def on_click(self, event):
        if self.is_solving:
            return

        tower_index = self.get_tower_index(event.x)
        tower = self.towers[tower_index]

        # If no selection, pick top of clicked tower
        if self.selected_disk is None:
            if tower:
                self.selected_disk = tower[-1]
                # highlight
                self.canvas.itemconfigure(self.selected_disk, outline="#ffff00", width=3)
                self.status.config(text=f"Disco seleccionado en torre {tower_index + 1}")
        else:
            # clicking same tower cancels selection
            if tower and self.selected_disk == tower[-1]:
                self.canvas.itemconfigure(self.selected_disk, outline="#222", width=2)
                self.selected_disk = None
                self.status.config(text="Movimiento cancelado.")
                return

            if not tower or self.is_smaller(self.selected_disk, tower[-1]):
                self.move_disk(self.selected_disk, tower_index)
                self.selected_disk = None
                self.update_move_label()
                self.check_win()
            else:
                messagebox.showinfo("Movimiento inválido", "No puedes colocar un disco grande sobre uno pequeño.")
                # un-highlight
                self.canvas.itemconfigure(self.selected_disk, outline="#222", width=2)
                self.selected_disk = None

    def is_smaller(self, disk1, disk2):
        x1, _, x2, _ = self.canvas.coords(disk1)
        w1 = x2 - x1
        x1, _, x2, _ = self.canvas.coords(disk2)
        w2 = x2 - x1
        return w1 < w2

    def move_disk(self, disk, tower_index):
        # remove from source
        for tower in self.towers:
            if disk in tower:
                tower.remove(disk)
                break

        # compute destination coords
        self.towers[tower_index].append(disk)
        x = 120 + tower_index * 200
        y = 280 - (len(self.towers[tower_index]) - 1) * 22
        coords = self.canvas.coords(disk)
        w = coords[2] - coords[0]
        self.canvas.coords(disk, x - w // 2, y - 18, x + w // 2, y)
        # reset outline
        self.canvas.itemconfigure(disk, outline="#222", width=2)

        self.move_count += 1

    def update_move_label(self):
        self.move_label.config(text=f"Movimientos: {self.move_count}")

    def check_win(self):
        n = max(3, min(8, int(self.disk_var.get())))
        if len(self.towers[2]) == n:
            messagebox.showinfo("¡Victoria!", f"Has completado la Torre de Hanoi en {self.move_count} movimientos.")

    # --- Reset / autosolve ---
    def reset_game(self):
        if self.is_solving:
            return
        self.create_towers()
        self.create_disks()
        self.status.config(text="Juego reiniciado.")

    def start_autosolve(self):
        if self.is_solving:
            return
        n = max(3, min(8, int(self.disk_var.get())))
        self.is_solving = True
        self.status.config(text="Auto-resolviendo...")
        # build list of moves
        moves = []

        def hanoi_moves(k, src, dst, aux):
            if k == 0:
                return
            hanoi_moves(k - 1, src, aux, dst)
            moves.append((src, dst))
            hanoi_moves(k - 1, aux, dst, src)

        hanoi_moves(n, 0, 2, 1)

        # animate moves
        def animate(i=0):
            if i >= len(moves):
                self.is_solving = False
                self.status.config(text="Auto-resuelto.")
                self.check_win()
                return
            src, dst = moves[i]
            if self.towers[src]:
                disk = self.towers[src][-1]
                self.move_disk(disk, dst)
            # schedule next
            self.root.after(250, lambda: animate(i + 1))

        self.root.after(300, lambda: animate(0))


if __name__ == "__main__":
    root = tk.Tk()
    game = HanoiGame(root)
    root.mainloop()