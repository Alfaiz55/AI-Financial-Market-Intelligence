import tkinter as tk
from datetime import datetime

import threading

from src.ai.agent import run_market_agent

APP_BG = "#0f1117"
SIDEBAR_BG = "#171a21"
PANEL_BG = "#1c2028"
INPUT_BG = "#20242d"
TEXT = "#f3f4f6"
MUTED = "#9ca3af"
BORDER = "#2b313c"
ACCENT = "#5b8def"
USER_BUBBLE = "#26364f"

class MarketChatUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Market Intelligence")
        self.root.geometry("1280x800")
        self.root.minsize(900, 600)
        self.root.configure(bg=APP_BG)

        self.chats = []
        self.current_messages = []
        self.dark = True

        self.build_ui()
        self.show_welcome()

    def build_ui(self):
        self.sidebar = tk.Frame(self.root, bg=SIDEBAR_BG, width=270)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        top = tk.Frame(self.sidebar, bg=SIDEBAR_BG)
        top.pack(fill="x", padx=16, pady=(18, 12))

        self.new_btn = tk.Button(
            top, text="+  New Chat", command=self.new_chat,
            bg=PANEL_BG, fg=TEXT, activebackground="#252b35",
            activeforeground=TEXT, relief="flat", bd=0,
            font=("Segoe UI", 11), padx=12, pady=10, cursor="hand2"
        )
        self.new_btn.pack(fill="x")

        tk.Label(
            self.sidebar, text="Recent", bg=SIDEBAR_BG, fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=20, pady=(18, 8))

        self.history = tk.Frame(self.sidebar, bg=SIDEBAR_BG)
        self.history.pack(fill="both", expand=True, padx=10)

        bottom = tk.Frame(self.sidebar, bg=SIDEBAR_BG)
        bottom.pack(fill="x", side="bottom", padx=16, pady=16)

        self.theme_btn = tk.Button(
            bottom, text="☾  Dark mode", command=self.toggle_theme,
            bg=SIDEBAR_BG, fg=MUTED, activebackground=SIDEBAR_BG,
            activeforeground=TEXT, relief="flat", bd=0,
            font=("Segoe UI", 10), anchor="w", cursor="hand2"
        )
        self.theme_btn.pack(fill="x")

        self.main = tk.Frame(self.root, bg=APP_BG)
        self.main.pack(side="left", fill="both", expand=True)

        self.header = tk.Frame(self.main, bg=APP_BG, height=70)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        tk.Label(
            self.header, text="Market Intelligence",
            bg=APP_BG, fg=TEXT, font=("Segoe UI Semibold", 13)
        ).pack(side="left", padx=28, pady=22)

        self.chat_canvas = tk.Canvas(
            self.main, bg=APP_BG, highlightthickness=0, bd=0
        )
        self.chat_canvas.pack(fill="both", expand=True, padx=30)

        self.chat_frame = tk.Frame(self.chat_canvas, bg=APP_BG)
        self.canvas_window = self.chat_canvas.create_window(
            (0, 0), window=self.chat_frame, anchor="nw"
        )
        self.chat_frame.bind("<Configure>", self._resize_scroll)
        self.chat_canvas.bind("<Configure>", self._resize_canvas)

        self.bottom = tk.Frame(self.main, bg=APP_BG)
        self.bottom.pack(fill="x", padx=30, pady=(8, 25))

        self.input_shell = tk.Frame(
            self.bottom, bg=INPUT_BG, highlightbackground=BORDER,
            highlightthickness=1
        )
        self.input_shell.pack(fill="x")

        self.input = tk.Text(
            self.input_shell, height=3, wrap="word",
            bg=INPUT_BG, fg=TEXT, insertbackground=TEXT,
            relief="flat", bd=0, font=("Segoe UI", 11),
            padx=15, pady=12
        )
        self.input.pack(side="left", fill="both", expand=True)
        self.input.bind("<Return>", self.handle_enter)

        self.send_btn = tk.Button(
            self.input_shell, text="➤", command=self.send_message,
            bg=ACCENT, fg="white", activebackground=ACCENT,
            activeforeground="white", relief="flat", bd=0,
            font=("Segoe UI Semibold", 12), width=4, height=2,
            cursor="hand2"
        )
        self.send_btn.pack(side="right", padx=8, pady=8)

        tk.Label(
            self.bottom, text="Market data and analysis are for informational purposes.",
            bg=APP_BG, fg=MUTED, font=("Segoe UI", 8)
        ).pack(pady=(7, 0))

    def _resize_scroll(self, event=None):
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))

    def _resize_canvas(self, event):
        self.chat_canvas.itemconfigure(self.canvas_window, width=event.width)

    def show_welcome(self):
        for w in self.chat_frame.winfo_children():
            w.destroy()

        spacer = tk.Frame(self.chat_frame, bg=APP_BG, height=130)
        spacer.pack(fill="x")

        tk.Label(
            self.chat_frame,
            text="Ask about stock price movements",
            bg=APP_BG, fg=TEXT,
            font=("Segoe UI Semibold", 26)
        ).pack(pady=(15, 8))

        tk.Label(
            self.chat_frame,
            text="Analyze prices, volume, volatility, trends, and market news using natural language.",
            bg=APP_BG, fg=MUTED,
            font=("Segoe UI", 11), wraplength=720, justify="center"
        ).pack(pady=(0, 25))

        examples = [
            "What is the latest price of IBM?",
            "What happened to IBM recently?",
            "Show me IBM's recent volatility.",
            "What news was reported around IBM's recent movement?"
        ]

        cards = tk.Frame(self.chat_frame, bg=APP_BG)
        cards.pack(pady=10)

        for i, text in enumerate(examples):
            b = tk.Button(
                cards, text=text, command=lambda q=text: self.use_example(q),
                bg=PANEL_BG, fg=TEXT, activebackground="#252b35",
                activeforeground=TEXT, relief="flat", bd=0,
                font=("Segoe UI", 9), padx=14, pady=10, cursor="hand2"
            )
            b.grid(row=i//2, column=i%2, padx=6, pady=6, sticky="ew")

    def use_example(self, question):
        self.input.delete("1.0", "end")
        self.input.insert("1.0", question)
        self.send_message()

    def handle_enter(self, event):
        if not (event.state & 0x0001):  # Enter sends; Shift+Enter creates a newline
            self.send_message()
            return "break"

    def send_message(self):
        text = self.input.get("1.0", "end").strip()

        if not text:
            return

        if not self.current_messages:
            self.chats.insert(
                0,
                text[:32] + ("..." if len(text) > 32 else "")
            )
            self.refresh_history()

        # Add user message
        self.current_messages.append(("user", text))
        self.add_message("user", text)

        # Clear input
        self.input.delete("1.0", "end")

        # Disable input while processing
        self.input.config(state="disabled")
        self.send_btn.config(state="disabled")

        # Show three-dot indicator
        self.show_typing()

        # Run the actual AI agent in background
        thread = threading.Thread(
            target=self.process_question,
            args=(text,),
            daemon=True
        )

        thread.start() 

    def process_question(self, question):
        try:
            answer=run_market_agent(question)# Call your actual AI market agent
        
        # Update Tkinter safely from the main thread
            self.root.after(
                0,
                lambda: self.show_agent_response(answer)
            )

        except Exception as error:

                error_message = (
                    "I couldn't process your request right now.\n\n"
                    f"Error: {error}"
                )

                self.root.after(
                0,
                lambda: self.show_agent_response(error_message)
                )

    def show_agent_response(self, answer):

    # Remove typing indicator
        if hasattr(self, "typing") and self.typing.winfo_exists():
            self.typing.destroy()

    # Add assistant response
        self.current_messages.append(
            ("assistant", answer)
        )

        self.add_message(
            "assistant",
            answer
        )

    # Enable input again
        self.input.config(state="normal")
        self.send_btn.config(state="normal")

    # Put cursor back into input
        self.input.focus_set()        

    def show_typing(self):
        self.typing = tk.Frame(self.chat_frame, bg=APP_BG)
        self.typing.pack(fill="x", pady=12)
        tk.Label(
            self.typing, text="●  ●  ●", bg=APP_BG, fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=20)

        self.chat_canvas.update_idletasks()
        self.chat_canvas.yview_moveto(1)

    def show_placeholder_response(self, question):
        if hasattr(self, "typing") and self.typing.winfo_exists():
            self.typing.destroy()

        answer = (
            "This is the UI prototype. The market-data and AI agent are not connected yet.\n\n"
            "Once the backend is added, this area will show the evidence-based market "
            "analysis returned by your agent, including price movement, volume, volatility, "
            "relevant news, and uncertainty where appropriate."
        )
        self.current_messages.append(("assistant", answer))
        self.add_message("assistant", answer)

    def add_message(self, role, text):
        row = tk.Frame(self.chat_frame, bg=APP_BG)
        row.pack(fill="x", pady=8)

        if role == "user":
            bubble = tk.Frame(row, bg=USER_BUBBLE)
            bubble.pack(anchor="e", padx=20)

            tk.Label(
                bubble, text=text, bg=USER_BUBBLE, fg=TEXT,
                font=("Segoe UI", 10), wraplength=650,
                justify="left", padx=15, pady=10
            ).pack()
        else:
            inner = tk.Frame(row, bg=APP_BG)
            inner.pack(fill="x", padx=20)

            tk.Label(
                inner, text="AI", bg=APP_BG, fg=ACCENT,
                font=("Segoe UI Semibold", 9)
            ).pack(anchor="w", pady=(0, 4))

            tk.Label(
                inner, text=text, bg=APP_BG, fg=TEXT,
                font=("Segoe UI", 10), wraplength=760,
                justify="left", anchor="w"
            ).pack(anchor="w")

        self.chat_canvas.update_idletasks()
        self.chat_canvas.yview_moveto(1)

    def refresh_history(self):
        for w in self.history.winfo_children():
            w.destroy()

        for title in self.chats[:12]:
            b = tk.Button(
                self.history, text=title, anchor="w",
                bg=SIDEBAR_BG, fg=TEXT, activebackground=PANEL_BG,
                activeforeground=TEXT, relief="flat", bd=0,
                font=("Segoe UI", 9), padx=10, pady=9
            )
            b.pack(fill="x", pady=1)

    def new_chat(self):
        self.current_messages = []
        self.show_welcome()
        self.input.focus_set()


    def toggle_theme(self):
        global APP_BG, SIDEBAR_BG, PANEL_BG
        global INPUT_BG, TEXT, MUTED, BORDER
        global ACCENT, USER_BUBBLE

        if self.dark:
            # Light theme
            APP_BG = "#f5f7fa"
            SIDEBAR_BG = "#e9edf3"
            PANEL_BG = "#ffffff"
            INPUT_BG = "#ffffff"
            TEXT = "#1f2937"
            MUTED = "#6b7280"
            BORDER = "#d1d5db"
            ACCENT = "#4f7fe8"
            USER_BUBBLE = "#dbeafe"

            self.dark = False
            theme_text = "☾  Dark mode"

        else:
            # Dark theme
            APP_BG = "#0f1117"
            SIDEBAR_BG = "#171a21"
            PANEL_BG = "#1c2028"
            INPUT_BG = "#20242d"
            TEXT = "#f3f4f6"
            MUTED = "#9ca3af"
            BORDER = "#2b313c"
            ACCENT = "#5b8def"
            USER_BUBBLE = "#26364f"

            self.dark = True
            theme_text = "☀  Light mode"

        # Rebuild the UI using the selected theme
        for widget in self.root.winfo_children():
            widget.destroy()

        self.build_ui()

        self.theme_btn.config(text=theme_text)

        self.refresh_history()

        if self.current_messages:
            for role, message in self.current_messages:
                self.add_message(role, message)
        else:
            self.show_welcome()

if __name__ == "__main__":
    root = tk.Tk()
    app = MarketChatUI(root)
    root.mainloop()
