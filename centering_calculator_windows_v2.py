import tkinter as tk


class CenteringCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Centering Calculator")
        self.geometry("900x620")
        self.minsize(780, 520)
        self.configure(bg="#727272")

        self.left_var = tk.StringVar()
        self.right_var = tk.StringVar()
        self.top_var = tk.StringVar()
        self.bottom_var = tk.StringVar()
        self.result_lr_var = tk.StringVar()
        self.result_tb_var = tk.StringVar()

        self._build_ui()
        self._bind_updates()

    def _build_ui(self):
        self.grid_rowconfigure(0, weight=0)   # header
        self.grid_rowconfigure(1, weight=0)   # labels
        self.grid_rowconfigure(2, weight=0)   # inputs
        self.grid_rowconfigure(3, weight=0)   # clear
        self.grid_rowconfigure(4, weight=1)   # results
        self.grid_columnconfigure(0, weight=1)

        self._build_header()
        self._build_input_section()
        self._build_clear_row()
        self._build_results()

    def _build_header(self):
        header = tk.Frame(self, bg="#5b5b5b", height=78)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)

        tk.Label(
            header,
            text="CENTERING CALCULATOR",
            bg="#5b5b5b",
            fg="#63ff33",
            font=("Segoe UI", 30, "bold"),
        ).place(relx=0.5, rely=0.5, anchor="center")

    def _build_input_section(self):
        labels = tk.Frame(self, bg="#666666", height=28)
        labels.grid(row=1, column=0, sticky="ew")
        labels.grid_propagate(False)

        inputs = tk.Frame(self, bg="#2f2f2f", height=82)
        inputs.grid(row=2, column=0, sticky="ew")
        inputs.grid_propagate(False)

        for i in range(4):
            labels.grid_columnconfigure(i, weight=1, uniform="cols")
            inputs.grid_columnconfigure(i, weight=1, uniform="cols")
        labels.grid_rowconfigure(0, weight=1)
        inputs.grid_rowconfigure(0, weight=1)

        names = ["LEFT", "RIGHT", "TOP", "BOTTOM"]
        variables = [self.left_var, self.right_var, self.top_var, self.bottom_var]
        self.entries = []

        for i, (name, var) in enumerate(zip(names, variables)):
            tk.Label(
                labels,
                text=name,
                bg="#666666",
                fg="#f1f1f1",
                font=("Segoe UI", 12),
            ).grid(row=0, column=i, sticky="nsew")

            cell = tk.Frame(
                inputs,
                bg="#2b2b2b",
                highlightbackground="#565656",
                highlightthickness=1,
            )
            cell.grid(row=0, column=i, sticky="nsew")
            cell.grid_propagate(False)

            entry = tk.Entry(
                cell,
                textvariable=var,
                bg="#2b2b2b",
                fg="#f3f3f3",
                insertbackground="#f3f3f3",
                relief="flat",
                bd=0,
                highlightthickness=0,
                font=("Consolas", 28),
                justify="left",
            )
            entry.place(x=14, y=14, width=150, height=40)
            self.entries.append(entry)

    def _build_clear_row(self):
        clear_row = tk.Frame(self, bg="#666666", height=26)
        clear_row.grid(row=3, column=0, sticky="ew")
        clear_row.grid_propagate(False)

        clear_label = tk.Label(
            clear_row,
            text="CLEAR",
            bg="#666666",
            fg="#ff3030",
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
        )
        clear_label.place(relx=0.5, rely=0.5, anchor="center")
        clear_label.bind("<Button-1>", lambda _e: self.clear())

    def _build_results(self):
        results = tk.Frame(self, bg="#767676")
        results.grid(row=4, column=0, sticky="nsew")
        results.grid_rowconfigure(0, weight=1)
        results.grid_columnconfigure(0, weight=1, uniform="result_cols")
        results.grid_columnconfigure(1, weight=0)
        results.grid_columnconfigure(2, weight=1, uniform="result_cols")

        left_panel = tk.Frame(results, bg="#767676")
        left_panel.grid(row=0, column=0, sticky="nsew")

        divider = tk.Frame(results, bg="#8c8c8c", width=1)
        divider.grid(row=0, column=1, sticky="ns")

        right_panel = tk.Frame(results, bg="#767676")
        right_panel.grid(row=0, column=2, sticky="nsew")

        # Put both result blocks in identical top-left aligned containers
        left_inner = tk.Frame(left_panel, bg="#767676")
        left_inner.place(x=18, y=18, anchor="nw")

        right_inner = tk.Frame(right_panel, bg="#767676")
        right_inner.place(x=18, y=18, anchor="nw")

        result_font = ("Consolas", 28, "bold")

        self.left_result_label = tk.Label(
            left_inner,
            textvariable=self.result_lr_var,
            bg="#767676",
            fg="#f4f4f4",
            anchor="nw",
            justify="left",
            font=result_font,
        )
        self.left_result_label.pack(anchor="nw")

        self.right_result_label = tk.Label(
            right_inner,
            textvariable=self.result_tb_var,
            bg="#767676",
            fg="#f4f4f4",
            anchor="nw",
            justify="left",
            font=result_font,
        )
        self.right_result_label.pack(anchor="nw")

        self.after(50, lambda: self.entries[0].focus_set())

    def _bind_updates(self):
        for var in (self.left_var, self.right_var, self.top_var, self.bottom_var):
            var.trace_add("write", self._recalculate)

    def _parse_number(self, value):
        value = value.strip()
        if not value:
            return None
        try:
            num = float(value)
        except ValueError:
            return "invalid"
        if num < 0:
            return "invalid"
        return num

    def _fmt(self, num):
        if abs(num - round(num)) < 1e-9:
            return str(int(round(num)))
        return f"{num:.1f}"

    def _recalculate(self, *_args):
        left = self._parse_number(self.left_var.get())
        right = self._parse_number(self.right_var.get())
        top = self._parse_number(self.top_var.get())
        bottom = self._parse_number(self.bottom_var.get())

        values = [left, right, top, bottom]
        if any(v == "invalid" for v in values):
            self.result_lr_var.set("—")
            self.result_tb_var.set("—")
            return

        if all(v is None for v in values):
            self.result_lr_var.set("")
            self.result_tb_var.set("")
            return

        left = 0 if left is None else left
        right = 0 if right is None else right
        top = 0 if top is None else top
        bottom = 0 if bottom is None else bottom

        horizontal_total = left + right
        vertical_total = top + bottom

        if horizontal_total > 0:
            left_pct = (left / horizontal_total) * 100
            right_pct = (right / horizontal_total) * 100
            self.result_lr_var.set(f"{self._fmt(left_pct)}L/{self._fmt(right_pct)}R")
        else:
            self.result_lr_var.set("")

        if vertical_total > 0:
            top_pct = (top / vertical_total) * 100
            bottom_pct = (bottom / vertical_total) * 100
            self.result_tb_var.set(f"{self._fmt(top_pct)}T/{self._fmt(bottom_pct)}B")
        else:
            self.result_tb_var.set("")

    def clear(self):
        self.left_var.set("")
        self.right_var.set("")
        self.top_var.set("")
        self.bottom_var.set("")
        self.result_lr_var.set("")
        self.result_tb_var.set("")
        self.entries[0].focus_set()


if __name__ == "__main__":
    CenteringCalculatorApp().mainloop()
