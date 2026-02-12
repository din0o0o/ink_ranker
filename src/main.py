import ctypes
import os
import threading
import tkinter as tk
from tkinter import ttk
from engine import (
    CONFIG_FILE,
    load_config, load_font_list, find_fonts,
    process_font, compute_relative, save_json, save_docx, ensure_config,
)

__version__ = "1.0"

GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080


class ProgressBar(tk.Canvas):
    def __init__(self, parent, width=300, height=22):
        super().__init__(parent, width=width, height=height,
                         highlightthickness=0, bd=1, relief="sunken")
        self._bar_w = width
        self._bar_h = height
        self._pct = 0
        self._text = "Ready"
        self.after_idle(self._redraw)

    def _redraw(self):
        self.delete("all")
        self.create_rectangle(0, 0, self._bar_w, self._bar_h, fill="#e0e0e0", outline="")
        fill_w = int(self._bar_w * self._pct / 100)
        if fill_w > 0:
            self.create_rectangle(0, 0, fill_w, self._bar_h, fill="#06b025", outline="")
        self.create_text(self._bar_w // 2, self._bar_h // 2,
                         text=self._text, fill="#222", font=("Segoe UI", 9))

    def set(self, pct, text=None):
        self._pct = max(0, min(100, pct))
        if text is not None:
            self._text = text
        self._redraw()


class InkRankerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"InkRanker v{__version__}")
        self.overrideredirect(True)
        self.resizable(False, False)
        self._busy = False
        self._drag_x = 0
        self._drag_y = 0
        self._build_ui()
        self._center_window()
        self._show_on_taskbar()
        # Blank icon
        blank = tk.PhotoImage(width=1, height=1)
        self.iconphoto(False, blank)

    def _show_on_taskbar(self):
        self.update_idletasks()
        hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        style = (style & ~WS_EX_TOOLWINDOW) | WS_EX_APPWINDOW
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        self.withdraw()
        self.after(10, self.deiconify)

    def _center_window(self):
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"+{x}+{y}")

    def _build_ui(self):
        frame = ttk.Frame(self, padding=12)
        frame.pack(fill="both", expand=True)
        frame.bind("<Button-1>", self._start_drag)
        frame.bind("<B1-Motion>", self._on_drag)

        self.close_btn = tk.Button(
            frame, text="\u2715", fg="red", font=("Segoe UI", 8),
            command=self.destroy, activeforeground="darkred")
        self.close_btn.place(relx=1.0, x=-2, y=-2, anchor="ne")

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=(4, 8))

        self.run_btn = ttk.Button(btn_frame, text="\u25b6", width=4, command=self._run)
        self.run_btn.pack(side="left", padx=4)

        self.cfg_btn = ttk.Button(btn_frame, text="\u2699", width=4, command=self._open_config)
        self.cfg_btn.pack(side="left", padx=4)

        self.progress = ProgressBar(frame, width=300, height=22)
        self.progress.pack(pady=(0, 4))

    def _start_drag(self, e):
        self._drag_x = e.x
        self._drag_y = e.y

    def _on_drag(self, e):
        x = self.winfo_x() + e.x - self._drag_x
        y = self.winfo_y() + e.y - self._drag_y
        self.geometry(f"+{x}+{y}")

    def _open_config(self):
        ensure_config()
        os.startfile(str(CONFIG_FILE))

    def _run(self):
        if self._busy:
            return
        cfg = load_config()
        if not cfg["sample_text"].exists():
            return
        self._busy = True
        self.run_btn.configure(state="disabled")
        self.cfg_btn.configure(state="disabled")
        self.progress.set(0, "Scanning fonts...")
        threading.Thread(target=self._worker, args=(cfg,), daemon=True).start()

    def _worker(self, cfg):
        text = cfg["sample_text"].read_text(encoding="utf-8")
        names = load_font_list(cfg)
        fonts = find_fonts(cfg, names)

        font_names = sorted(fonts.keys())
        baseline = cfg["baseline_font"]
        if baseline in font_names:
            font_names = [baseline] + [f for f in font_names if f != baseline]

        total = len(font_names)
        results = {}

        for i, name in enumerate(font_names, 1):
            pct = int(i / total * 100) if total else 100
            self.after(0, lambda p=pct, n=name, c=i, t=total:
                       self.progress.set(p, f"{c}/{t}  {n}"))
            path, font_idx = fonts[name]
            ink = process_font(text, path, font_idx, cfg)
            if ink is not None:
                results[name] = ink

        relative = compute_relative(results, baseline)
        save_json(cfg, results, relative)
        save_docx(cfg, results, relative)
        self.after(0, self._done)

    def _done(self):
        self.progress.set(100, "Done")
        self._busy = False
        self.run_btn.configure(state="normal")
        self.cfg_btn.configure(state="normal")


if __name__ == "__main__":
    InkRankerApp().mainloop()
