import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os
import threading
import time
from tkinter import ttk
import math

class CasinoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Montecarlo Casino 🎰")
        self.balance = 1000
        self.balance_var = tk.IntVar(value=self.balance)

        # Carica sfondo
        try:
            self.background_image = Image.open(os.path.join("assets", "background_hall.png"))
            self.background_photo = ImageTk.PhotoImage(self.background_image)
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.background_photo = None

        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Pulsante per accedere alla slot machine
        self.slot_button = tk.Button(
            self.root, text="🎰 Slot Machine", font=("Arial", 18), command=self.open_slot_machine, bg="white" )
        self.slot_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        # Pulsante per accedere al Blackjack
        self.blackjack_button = tk.Button(
            self.root, text="🃏 Blackjack", font=("Arial", 18), command=self.open_blackjack, bg="white" )
        self.blackjack_button.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        # Pulsante per accedere alla Corsa dei Cavalli
        self.horserace_button = tk.Button(
            self.root, text="🏇 Horse race", font=("Arial", 18), command=self.open_horserace, bg="white")
        self.horserace_button.place(relx=0.5, rely=0.70, anchor=tk.CENTER)



        # Saldo visualizzato (in alto a destra)
        self.balance_label = tk.Label(self.root, text=f"Balance: CHF {self.balance}", font=("Arial", 16, "bold"), fg="black", bg="yellow", padx=10, pady=5)
        self.balance_label.place(relx=0.95, rely=0.05, anchor=tk.NE)

    def open_blackjack(self):
        BlackjackGame(self.root, self.balance, self.update_balance)

    def open_slot_machine(self):
        SlotMachine(self)

    def open_horserace(self):
        HorseRaceGame(self.root, self.balance_var, self.update_balance)

    def update_balance(self, amount):
        self.balance += amount
        self.balance_label.config(text=f"Balance: CHF {self.balance}")

class SlotMachine:
    def __init__(self, casino):
        self.casino = casino
        self.window = tk.Toplevel()
        self.window.title("Slot Machine 🎰")
        self.window.geometry("700x600")

        # Background image
        try:
            self.background_image = Image.open(os.path.join("assets", "background.png"))
            self.background_photo = ImageTk.PhotoImage(self.background_image)
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.background_photo = None

        self.background_label = tk.Label(self.window, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Symbol paths
        self.symbol_paths = [
            "assets/cherry.png",
            "assets/lemon.png",
            "assets/plum.png",
            "assets/bell.png",
            "assets/bar.png",
            "assets/seven.png",
        ]

        # Symbol weights
        self.weights = [30, 25, 20, 15, 7, 3]

        # Payouts for 3 matches
        self.payouts = {
            "cherry.png": 5,
            "lemon.png": 7,
            "plum.png": 10,
            "bell.png": 20,
            "bar.png": 50,
            "seven.png": 100,
        }

        # Payouts for 2 matches
        self.small_payouts = {
            "cherry.png": 0.5,
            "lemon.png": 1,
            "plum.png": 1,
            "bell.png": 2,
            "bar.png": 5,
            "seven.png": 8,
        }

        self.symbol_images = [ImageTk.PhotoImage(Image.open(path).resize((75, 95))) for path in self.symbol_paths]

        self.reel_frame = tk.Frame(self.window, bg="", bd=0)
        self.reel_frame.place(relx=0.48, rely=0.47, anchor=tk.CENTER)

        self.reels = [tk.Label(self.reel_frame, image=random.choice(self.symbol_images), bg="white") for _ in range(3)]
        for reel in self.reels:
            reel.pack(side=tk.LEFT, padx=4)

        # Bet entry
        self.bet_entry = tk.Entry(self.window, font=("Arial", 14))
        self.bet_entry.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        # Spin button
        self.spin_button = tk.Button(self.window, text="🎲 Spin!", font=("Arial", 16), command=self.spin, bg="white")
        self.spin_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        # Result label
        self.result_label = tk.Label(self.window, text="", font=("Arial", 16), bg="white")
        self.result_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        # Increase/decrease bet buttons
        self.increase_bet_button = tk.Button(self.window, text="⬆️ Increase Bet", font=("Arial", 14), command=self.increase_bet)
        self.increase_bet_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.decrease_bet_button = tk.Button(self.window, text="⬇️ Decrease Bet", font=("Arial", 14), command=self.decrease_bet)
        self.decrease_bet_button.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

    def spin(self):
        try:
            bet = int(self.bet_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Insert a valid bet.")
            return

        if bet <= 0:
            messagebox.showerror("Error", "Bet must be greater than 0.")
            return
        if bet > self.casino.balance:
            messagebox.showerror("Error", "Insufficient balance.")
            return

        self.spin_button.config(state="disabled")
        self.bet_entry.config(state="disabled")

        def perform_spin():
            spin_results = []
            spin_symbols = []

            self.roll_reels()
            time.sleep(0.5)

            for i in range(3):
                symbol_index = random.choices(range(len(self.symbol_paths)), weights=self.weights)[0]
                symbol_file = self.symbol_paths[symbol_index].split("/")[-1]
                spin_results.append(symbol_file)
                spin_symbols.append(self.symbol_images[symbol_index])
                self.reels[i].config(image=spin_symbols[i])
                self.window.update()

            payout = 0
            if spin_results[0] == spin_results[1] == spin_results[2]:
                payout = bet * self.payouts[spin_results[0]]
                self.result_label.config(text=f"🎉 Jackpot! +{payout} CHF 🎉", fg="green")
                self.shake_window()
            elif spin_results[0] == spin_results[1] or spin_results[1] == spin_results[2] or spin_results[0] == spin_results[2]:
                matched = spin_results[0] if spin_results[0] == spin_results[1] or spin_results[0] == spin_results[2] else spin_results[1]
                payout = bet * self.small_payouts[matched]
                self.result_label.config(text=f"✨ Pair! +{payout} CHF ✨", fg="blue")
            else:
                payout = -bet
                self.result_label.config(text=f"😢 Maybe next time -{bet} CHF", fg="red")

            self.casino.update_balance(payout)

            self.spin_button.config(state="normal")
            self.bet_entry.config(state="normal")

        threading.Thread(target=perform_spin).start()

    def roll_reels(self):
        for i in range(3):
            self.animate_reel(i)

    def animate_reel(self, reel_index):
        for _ in range(10):
            random_symbol = random.choice(self.symbol_images)
            self.reels[reel_index].config(image=random_symbol)
            self.window.after(50)
            self.window.update()

    def shake_window(self):
        original_x = self.window.winfo_x()
        original_y = self.window.winfo_y()
        shake_distance = 10
        for _ in range(5):
            self.window.geometry(f"{800}x{600}+{original_x + random.randint(-shake_distance, shake_distance)}+{original_y + random.randint(-shake_distance, shake_distance)}")
            self.window.update()
            self.window.after(50)
        self.window.geometry(f"{800}x{600}+{original_x}+{original_y}")

    def increase_bet(self):
        current_bet = int(self.bet_entry.get())
        self.bet_entry.delete(0, tk.END)
        self.bet_entry.insert(0, str(current_bet + 10))

    def decrease_bet(self):
        current_bet = int(self.bet_entry.get())
        if current_bet > 10:
            self.bet_entry.delete(0, tk.END)
            self.bet_entry.insert(0, str(current_bet - 10))
        else:
            messagebox.showwarning("Bet", "Minimum bet is 10 CHF")
class BlackjackGame:
    def __init__(self, master, balance, update_balance_callback):
        self.master = master
        self.balance = balance
        self.update_balance_callback = update_balance_callback

        self.window = tk.Toplevel(master)
        self.window.title("Blackjack")
        self.window.configure(bg="#006400")

        self.card_size = (100, 145)
        self.deck = self.load_deck()
        self.player_hand = []
        self.dealer_hand = []

        self.bet_amount = 0
        self.player_balance = self.balance

        self.init_gui()

    def load_deck(self):
        deck = []
        suits = ['C', 'D', 'H', 'S']
        values = list(range(2, 11)) + ['jack', 'queen', 'king', 'ace']
        for suit in suits:
            for value in values:
                deck.append(f"{value}{suit}")
        return deck * 4

    def init_gui(self):
        self.balance_label = tk.Label(self.window, text=f"Balance: CHF {self.player_balance}", fg="white", bg="#006400", font=("Helvetica", 14))
        self.balance_label.pack(pady=10)

        self.bet_entry = tk.Entry(self.window)
        self.bet_entry.pack()

        self.bet_button = tk.Button(self.window, text="Bet", command=self.place_bet)
        self.bet_button.pack(pady=5)

        self.status_label = tk.Label(self.window, text="", fg="white", bg="#006400", font=("Helvetica", 12))
        self.status_label.pack(pady=5)

        self.cards_frame = tk.Frame(self.window, bg="#006400")
        self.cards_frame.pack(pady=10)

        self.player_label = tk.Label(self.cards_frame, text="You", fg="white", bg="#006400")
        self.player_label.grid(row=0, column=0)
        self.dealer_label = tk.Label(self.cards_frame, text="Dealer", fg="white", bg="#006400")
        self.dealer_label.grid(row=0, column=1)

        self.player_cards_frame = tk.Frame(self.cards_frame, bg="#006400")
        self.player_cards_frame.grid(row=1, column=0, padx=10)
        self.dealer_cards_frame = tk.Frame(self.cards_frame, bg="#006400")
        self.dealer_cards_frame.grid(row=1, column=1, padx=10)

        self.buttons_frame = tk.Frame(self.window, bg="#006400")
        self.buttons_frame.pack(pady=10)

        self.hit_button = tk.Button(self.buttons_frame, text="Hit", command=self.hit, state=tk.DISABLED)
        self.hit_button.grid(row=0, column=0, padx=5)

        self.stand_button = tk.Button(self.buttons_frame, text="Stand", command=self.stand, state=tk.DISABLED)
        self.stand_button.grid(row=0, column=1, padx=5)

        self.double_button = tk.Button(self.buttons_frame, text="Double", command=self.double_down, state=tk.DISABLED)
        self.double_button.grid(row=0, column=2, padx=5)

    def place_bet(self):
        try:
            bet = int(self.bet_entry.get())
            if bet <= 0 or bet > self.player_balance:
                self.status_label.config(text="Invalid bet")
                return
            self.bet_amount = bet
            self.player_balance -= bet
            self.update_gui_balance()
            self.start_game()
        except ValueError:
            self.status_label.config(text="Invalid bet")

    def start_game(self):
        self.status_label.config(text="")
        self.clear_cards()
        self.deck = self.load_deck()
        random.shuffle(self.deck)

        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]

        self.display_cards(initial=True)

        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)
        self.double_button.config(state=tk.NORMAL)

        if self.get_hand_value(self.player_hand) == 21:
            self.end_game("Blackjack!")

    def display_cards(self, initial=False):
        self.clear_cards()
        for idx, card in enumerate(self.player_hand):
            img = self.get_card_image(card)
            label = tk.Label(self.player_cards_frame, image=img, bg="#006400")
            label.image = img
            label.grid(row=0, column=idx)

        for idx, card in enumerate(self.dealer_hand):
            if idx == 0 or not initial:
                img = self.get_card_image(card)
            else:
                img = self.get_card_back()
            label = tk.Label(self.dealer_cards_frame, image=img, bg="#006400")
            label.image = img
            label.grid(row=0, column=idx)

    def get_card_image(self, card):
        card_name = card.replace('C', '_of_clubs').replace('D', '_of_diamonds').replace('H', '_of_hearts').replace('S', '_of_spades')
        path = os.path.join("cards", f"{card_name}.png")
        img = Image.open(path).resize(self.card_size)
        return ImageTk.PhotoImage(img)

    def get_card_back(self):
        path = os.path.join("cards", "back.png")
        img = Image.open(path).resize(self.card_size)
        return ImageTk.PhotoImage(img)

    def clear_cards(self):
        for frame in [self.player_cards_frame, self.dealer_cards_frame]:
            for widget in frame.winfo_children():
                widget.destroy()

    def get_hand_value(self, hand):
        value = 0
        aces = 0
        for card in hand:
            val = card[:-1]
            if val in ['jack', 'queen', 'king']:
                value += 10
            elif val == 'ace':
                aces += 1
                value += 11
            else:
                value += int(val)
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    def hit(self):
        self.player_hand.append(self.deck.pop())
        self.display_cards(initial=True)
        value = self.get_hand_value(self.player_hand)
        if value > 21:
            self.end_game("You busted!")
        elif value == 21:
            self.stand()

    def stand(self):
        self.disable_buttons()
        while self.get_hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.pop())
        self.display_cards(initial=False)

        player_val = self.get_hand_value(self.player_hand)
        dealer_val = self.get_hand_value(self.dealer_hand)

        if dealer_val > 21 or player_val > dealer_val:
            self.end_game("You won!")
        elif player_val == dealer_val:
            self.end_game("It's a draw!")
        else:
            self.end_game("You lost!")

    def double_down(self):
        if self.player_balance >= self.bet_amount:
            self.player_balance -= self.bet_amount
            self.bet_amount *= 2
            self.update_gui_balance()
            self.hit()
            if self.get_hand_value(self.player_hand) <= 21:
                self.stand()

    def disable_buttons(self):
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.double_button.config(state=tk.DISABLED)

    def end_game(self, result):
        self.disable_buttons()
        if "won" in result or "Blackjack" in result:
            self.player_balance += self.bet_amount * 2
        elif "draw" in result:
            self.player_balance += self.bet_amount

        self.status_label.config(text=result)
        self.update_gui_balance()

        amount = self.player_balance - self.balance
        self.update_balance_callback(amount)
        self.balance = self.player_balance

    def update_gui_balance(self):
        self.balance_label.config(text=f"Balance: CHF {self.player_balance}")
class HorseRaceGame:
    def __init__(self, master, balance_var, update_balance_callback):
        self.master = master
        self.balance_var = balance_var
        self.update_balance = update_balance_callback
        self.bet_amount = 0
        self.chosen_horse = tk.IntVar()
        self.horses = []
        self.horse_images = []
        self.running = False

        self.race_window = tk.Toplevel(master)
        self.race_window.title("Horse Race 🐎")

        self.canvas = tk.Canvas(self.race_window, width=600, height=300, bg="green")
        self.canvas.pack()

        self.controls_frame = tk.Frame(self.race_window)
        self.controls_frame.pack(pady=10)

        tk.Label(self.controls_frame, text="Bet on horse (1–4):").grid(row=0, column=0)
        self.horse_entry = ttk.Combobox(self.controls_frame, values=[1, 2, 3, 4], textvariable=self.chosen_horse, width=5)
        self.horse_entry.grid(row=0, column=1)

        tk.Label(self.controls_frame, text="Bet amount:").grid(row=1, column=0)
        self.bet_entry = tk.Entry(self.controls_frame, width=10)
        self.bet_entry.grid(row=1, column=1)

        self.start_btn = tk.Button(self.controls_frame, text="Start", command=self.start_race)
        self.start_btn.grid(row=2, column=0, columnspan=2, pady=5)

        self.countdown_text = None
        self.load_horse_images()
        self.init_horses()

    def load_horse_images(self):
        colors = ["red", "blue", "yellow", "purple"]
        for color in colors:
            try:
                img = Image.open(os.path.join("assets", f"horse_{color}.png"))
                img = img.resize((60, 40), Image.Resampling.LANCZOS)
                self.horse_images.append(ImageTk.PhotoImage(img))
            except Exception as e:
                print(f"Error loading horse_{color}.png: {e}")
                self.horse_images.append(None)

    def init_horses(self):
        self.horses = []
        self.positions = []
        self.canvas.delete("all")

        for i in range(4):
            if self.horse_images[i]:
                horse = self.canvas.create_image(10, 60 + i * 60, anchor=tk.NW, image=self.horse_images[i])
            else:
                horse = self.canvas.create_rectangle(10, 60 + i * 60, 70, 100 + i * 60, fill="gray")
            self.horses.append(horse)
            self.positions.append(10)

        self.canvas.create_line(550, 0, 550, 300, fill="white", dash=(4, 2))

    def start_race(self):
        try:
            bet = int(self.bet_entry.get())
            choice = int(self.horse_entry.get())
            if bet <= 0 or choice not in [1, 2, 3, 4]:
                raise ValueError
            if bet > self.balance_var.get():
                messagebox.showerror("Error", "Insufficient balance.")
                return
        except:
            messagebox.showerror("Error", "Please enter a valid bet.")
            return

        self.bet_amount = bet
        self.chosen_horse.set(choice)
        self.balance_var.set(self.balance_var.get() - bet)
        self.update_balance(-bet)
        self.start_btn.config(state="disabled")
        self.running = True
        self.show_countdown(3)

    def show_countdown(self, number):
        if self.countdown_text:
            self.canvas.delete(self.countdown_text)

        if number == 0:
            self.canvas.delete(self.countdown_text)
            self.animate()
            return

        text = "GO!" if number == 1 else str(number)
        self.countdown_text = self.canvas.create_text(300, 150, text=text, fill="white", font=("Arial", 48, "bold"))
        self.race_window.after(800, lambda: self.show_countdown(number - 1))

    def animate(self):
        winner = None
        for i, horse in enumerate(self.horses):
            move = random.randint(1, 10)
            self.positions[i] += move
            self.canvas.move(horse, move, 0)
            if self.positions[i] >= 550 and not winner:
                winner = i + 1

        if winner:
            self.end_race(winner)
        else:
            self.race_window.after(100, self.animate)

    def end_race(self, winner):
        self.running = False
        result = f"🏁 Horse {winner} won!"
        if winner == self.chosen_horse.get():
            winnings = self.bet_amount * 3
            self.balance_var.set(self.balance_var.get() + winnings)
            self.update_balance(winnings)
            result += f"\nYou won CHF {winnings}!"
        else:
            result += f"\nYou lost CHF {self.bet_amount}."

        messagebox.showinfo("Race Result", result)
        self.init_horses()
        self.start_btn.config(state="normal")




if __name__ == "__main__":
    root = tk.Tk()
    app = CasinoApp(root)
    root.geometry("650x350")
    root.mainloop()
