
import os
import re
import sys
import uuid
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# -------- Utility helpers --------
PREFIX_RE = re.compile(r'^\s*(\d{1,4})([._\-\s])\s*')  # matches "01 ", "01_", "01-"

def strip_existing_prefix(name: str) -> str:
    """Remove existing numeric prefixes like '01 ', '001-', '12_' at the start of a filename."""
    base = name
    m = PREFIX_RE.match(base)
    if m:
        base = base[m.end():]
    return base

def safe_join(dirpath: str, name: str) -> str:
    return os.path.join(dirpath, name)

def compute_zero_pad(n: int) -> int:
    return max(2, len(str(n)))

def preview_new_names(items, strip_prefix, zero_pad, separator):
    out = []
    for idx, name in enumerate(items, start=1):
        base = strip_existing_prefix(name) if strip_prefix else name
        new_name = f"{str(idx).zfill(zero_pad)}{separator}{base}"
        out.append((name, new_name))
    return out

def two_phase_rename(dirpath, mapping):
    """
    mapping: list of tuples (old_name, new_name) in the same directory.
    Uses a temp rename phase to avoid name collisions.
    """
    # Phase 0: quick no-op check
    if all(old == new for old, new in mapping):
        return

    # Generate temp names guaranteed to be unique
    temps = {}
    for old, _ in mapping:
        temp = f"__TMP__{uuid.uuid4().hex}__{old}"
        while os.path.exists(safe_join(dirpath, temp)):
            temp = f"__TMP__{uuid.uuid4().hex}__{old}"
        temps[old] = temp

    # Phase 1: rename old -> temp
    for old, _ in mapping:
        os.rename(safe_join(dirpath, old), safe_join(dirpath, temps[old]))

    # Phase 2: rename temp -> final
    for old, new in mapping:
        os.rename(safe_join(dirpath, temps[old]), safe_join(dirpath, new))

# -------- GUI --------

class ReorderListbox(tk.Listbox):
    """
    A Tk Listbox that supports drag-and-drop reordering.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, selectmode=tk.EXTENDED, activestyle='dotbox', **kwargs)
        self.bind('<Button-1>', self._on_click)
        self.bind('<B1-Motion>', self._on_drag)
        self.bind('<ButtonRelease-1>', self._on_drop)
        self.curIndex = None

    def _on_click(self, event):
        self.curIndex = self.nearest(event.y)

    def _on_drag(self, event):
        i = self.nearest(event.y)
        if self.curIndex is None or i == self.curIndex:
            return
        # Move the selected item visually
        item = self.get(self.curIndex)
        self.delete(self.curIndex)
        self.insert(i, item)
        self.selection_clear(0, tk.END)
        self.selection_set(i)
        self.curIndex = i

    def _on_drop(self, event):
        self.curIndex = None

    def get_all(self):
        return list(self.get(0, tk.END))

    def set_items(self, items):
        self.delete(0, tk.END)
        for it in items:
            self.insert(tk.END, it)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("파일/폴더 정렬 후 일괄 번호 접두사 붙이기")
        self.geometry("900x600")

        self.dirpath = tk.StringVar(value="")

        # Controls Frame
        ctrl = ttk.Frame(self)
        ctrl.pack(fill='x', padx=10, pady=10)

        ttk.Label(ctrl, text="대상 폴더:").pack(side='left')
        self.dir_entry = ttk.Entry(ctrl, textvariable=self.dirpath, width=70)
        self.dir_entry.pack(side='left', padx=5)
        ttk.Button(ctrl, text="찾아보기", command=self.browse_dir).pack(side='left', padx=5)
        ttk.Button(ctrl, text="불러오기", command=self.load_dir).pack(side='left', padx=5)

        # Options
        opt = ttk.Frame(self)
        opt.pack(fill='x', padx=10, pady=(0,10))
        self.strip_var = tk.BooleanVar(value=True)
        self.sep_var = tk.StringVar(value=" ")
        ttk.Checkbutton(opt, text="기존 번호 접두사 제거(01-, 01_, 01 )", variable=self.strip_var).pack(side='left')
        ttk.Label(opt, text="구분자:").pack(side='left', padx=(20,5))
        ttk.Combobox(opt, textvariable=self.sep_var, width=5, values=[" ", "-", "_", ". "], state="readonly").pack(side='left')
        ttk.Button(opt, text="이름순 정렬", command=self.sort_by_name).pack(side='left', padx=(20,5))
        ttk.Button(opt, text="위로", command=self.move_up).pack(side='left')
        ttk.Button(opt, text="아래로", command=self.move_down).pack(side='left')

        # Main Paned Window
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill='both', expand=True, padx=10, pady=10)

        # Left: listbox
        left = ttk.Frame(paned)
        ttk.Label(left, text="① 드래그해서 순서를 정렬하세요").pack(anchor='w')
        self.lb = ReorderListbox(left, height=25)
        self.lb.pack(fill='both', expand=True)
        paned.add(left, weight=1)

        # Right: preview
        right = ttk.Frame(paned)
        ttk.Label(right, text="② 미리보기").pack(anchor='w')
        self.preview = tk.Text(right, height=25, wrap='none')
        self.preview.pack(fill='both', expand=True)
        paned.add(right, weight=1)

        # Bottom buttons
        bottom = ttk.Frame(self)
        bottom.pack(fill='x', padx=10, pady=(0,10))
        ttk.Button(bottom, text="미리보기 갱신", command=self.update_preview).pack(side='left')
        ttk.Button(bottom, text="실행(이 순서대로 접두사 붙이기)", command=self.apply_changes).pack(side='right')

        # Status bar
        self.status = tk.StringVar(value="폴더를 선택하고 '불러오기'를 누르세요.")
        ttk.Label(self, textvariable=self.status, anchor='w').pack(fill='x', padx=10, pady=(0,10))

    # -------- Actions --------
    def browse_dir(self):
        d = filedialog.askdirectory(title="대상 폴더 선택")
        if d:
            self.dirpath.set(d)

    def load_dir(self):
        d = self.dirpath.get().strip('"')
        if not d or not os.path.isdir(d):
            messagebox.showerror("오류", "유효한 폴더를 선택하세요.")
            return

        # List files and folders, skip hidden/system (starts with . on Unix, desktop.ini, etc. on Windows)
        names = []
        for name in os.listdir(d):
            if name in ("desktop.ini",) or name.startswith('.'):
                continue
            names.append(name)

        # Default: natural sort by name (case-insensitive)
        names.sort(key=lambda s: s.lower())
        self.lb.set_items(names)
        self.status.set(f"{len(names)}개 항목을 불러왔습니다.")
        self.update_preview()

    def sort_by_name(self):
        items = self.lb.get_all()
        items.sort(key=lambda s: s.lower())
        self.lb.set_items(items)
        self.update_preview()

    def move_up(self):
        cur = self.lb.curselection()
        if not cur:
            return
        index = cur[0]
        if index == 0:
            return
        item = self.lb.get(index)
        self.lb.delete(index)
        self.lb.insert(index-1, item)
        self.lb.selection_set(index-1)
        self.update_preview()

    def move_down(self):
        cur = self.lb.curselection()
        if not cur:
            return
        index = cur[0]
        if index >= self.lb.size()-1:
            return
        item = self.lb.get(index)
        self.lb.delete(index)
        self.lb.insert(index+1, item)
        self.lb.selection_set(index+1)
        self.update_preview()

    def update_preview(self):
        items = self.lb.get_all()
        if not items:
            return
        pad = compute_zero_pad(len(items))
        pairs = preview_new_names(items, self.strip_var.get(), pad, self.sep_var.get())
        self.preview.delete("1.0", tk.END)
        self.preview.insert(tk.END, f"총 {len(pairs)}개 / 자리수: {pad}\n")
        self.preview.insert(tk.END, "-"*40 + "\n")
        for old, new in pairs:
            self.preview.insert(tk.END, f"{old}  -->  {new}\n")

    def apply_changes(self):
        d = self.dirpath.get().strip('"')
        if not d or not os.path.isdir(d):
            messagebox.showerror("오류", "유효한 폴더를 선택하세요.")
            return
        items = self.lb.get_all()
        if not items:
            messagebox.showwarning("알림", "변경할 항목이 없습니다.")
            return

        pad = compute_zero_pad(len(items))
        pairs = preview_new_names(items, self.strip_var.get(), pad, self.sep_var.get())

        # Check collisions (new names must be unique)
        new_names = [new for _, new in pairs]
        if len(set(new_names)) != len(new_names):
            messagebox.showerror("오류", "생성될 새 이름에 중복이 있습니다. 구분자/옵션을 변경해 보세요.")
            return

        # Confirm dialog
        msg = "정말로 다음 변경을 적용할까요?\n\n" + \
              "\n".join([f"{o} -> {n}" for o, n in pairs[:10]])
        if len(pairs) > 10:
            msg += f"\n... (총 {len(pairs)}개)"
        if not messagebox.askyesno("확인", msg):
            return

        try:
            two_phase_rename(d, pairs)
            self.status.set("이름 변경이 완료되었습니다.")
            messagebox.showinfo("완료", "이름 변경 완료!")
            self.load_dir()
        except Exception as e:
            messagebox.showerror("오류", f"이름 변경 중 오류가 발생했습니다:\n{e}")

def main():
    # Optional: allow passing a directory from command line
    if len(sys.argv) > 1:
        start_dir = sys.argv[1]
    else:
        start_dir = ""

    app = App()
    if start_dir and os.path.isdir(start_dir):
        app.dirpath.set(start_dir)
        app.load_dir()
    app.mainloop()

if __name__ == '__main__':
    main()
