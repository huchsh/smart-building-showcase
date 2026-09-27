import os
import queue
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

try:
    from PIL import Image
except ImportError:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("缺少元件", "尚未安裝 Pillow。\n請先雙擊「啟動程式.bat」，它會自動安裝後啟動。")
    raise


APP_TITLE = "BA 底圖批次瘦身"
SUPPORTED = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}


def human_size(value):
    units = ["B", "KB", "MB", "GB"]
    size = float(value)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.1f} {unit}"
        size /= 1024


def flatten_alpha(image):
    if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
        rgba = image.convert("RGBA")
        background = Image.new("RGB", rgba.size, "white")
        background.paste(rgba, mask=rgba.getchannel("A"))
        return background
    return image.convert("RGB")


def save_optimized(source, destination, quality, convert_to_jpg):
    with Image.open(source) as opened:
        # 不依 EXIF 自動旋轉，確保輸出的像素寬度與高度次序也完全不變。
        image = opened.copy()
        original_dimensions = opened.size

        if convert_to_jpg or source.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
            destination = destination.with_suffix(".jpg")
            image = flatten_alpha(image)
            image.save(
                destination,
                "JPEG",
                quality=quality,
                optimize=True,
                progressive=True,
                subsampling=2,
                exif=b"",
            )
        elif source.suffix.lower() in {".jpg", ".jpeg"}:
            image = flatten_alpha(image)
            image.save(
                destination,
                "JPEG",
                quality=quality,
                optimize=True,
                progressive=True,
                subsampling=2,
                exif=b"",
            )
        else:
            # PNG 維持原格式並採無損最佳化；像素與畫面內容不變。
            image.save(destination, "PNG", optimize=True, compress_level=9)

    with Image.open(destination) as checked:
        if checked.size != original_dimensions:
            destination.unlink(missing_ok=True)
            raise RuntimeError("輸出尺寸與原圖不同，已取消輸出")
    return destination


class OptimizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("720x560")
        self.minsize(650, 500)
        self.events = queue.Queue()
        self.running = False
        self._build_ui()
        self.after(100, self._poll_events)

    def _build_ui(self):
        frame = ttk.Frame(self, padding=18)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="BA 底圖批次瘦身", font=("Microsoft JhengHei UI", 18, "bold")).pack(anchor="w")
        ttk.Label(
            frame,
            text="圖片寬度與高度完全不變；結果輸出到新資料夾，不覆蓋原檔。",
        ).pack(anchor="w", pady=(4, 16))

        source_box = ttk.LabelFrame(frame, text="1. 選擇原圖資料夾", padding=12)
        source_box.pack(fill="x")
        row = ttk.Frame(source_box)
        row.pack(fill="x")
        self.source_var = tk.StringVar()
        ttk.Entry(row, textvariable=self.source_var).pack(side="left", fill="x", expand=True)
        ttk.Button(row, text="瀏覽…", command=self._browse).pack(side="left", padx=(8, 0))

        settings = ttk.LabelFrame(frame, text="2. 瘦身設定", padding=12)
        settings.pack(fill="x", pady=12)
        quality_row = ttk.Frame(settings)
        quality_row.pack(fill="x")
        ttk.Label(quality_row, text="JPG 品質：").pack(side="left")
        self.quality_var = tk.IntVar(value=88)
        ttk.Scale(quality_row, from_=70, to=95, variable=self.quality_var, command=self._show_quality).pack(
            side="left", fill="x", expand=True, padx=8
        )
        self.quality_label = ttk.Label(quality_row, text="88")
        self.quality_label.pack(side="left")

        self.convert_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            settings,
            text="最大瘦身：將 PNG／BMP／TIFF 轉成 JPG（像素尺寸不變，透明區域改白色）",
            variable=self.convert_var,
        ).pack(anchor="w", pady=(10, 0))
        self.subfolders_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings, text="包含所有子資料夾", variable=self.subfolders_var).pack(anchor="w", pady=(6, 0))

        action_row = ttk.Frame(frame)
        action_row.pack(fill="x")
        self.start_button = ttk.Button(action_row, text="開始瘦身", command=self._start)
        self.start_button.pack(side="left")
        self.progress = ttk.Progressbar(action_row, mode="determinate")
        self.progress.pack(side="left", fill="x", expand=True, padx=(12, 0))

        ttk.Label(frame, text="處理紀錄").pack(anchor="w", pady=(14, 4))
        self.log = tk.Text(frame, height=14, wrap="word", state="disabled", font=("Consolas", 9))
        self.log.pack(fill="both", expand=True)

    def _browse(self):
        selected = filedialog.askdirectory(title="選擇 BA 底圖資料夾")
        if selected:
            self.source_var.set(selected)

    def _show_quality(self, value):
        self.quality_label.configure(text=str(round(float(value))))

    def _append_log(self, text):
        self.log.configure(state="normal")
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _start(self):
        if self.running:
            return
        source = Path(self.source_var.get().strip())
        if not source.is_dir():
            messagebox.showwarning(APP_TITLE, "請先選擇有效的原圖資料夾。")
            return
        self.running = True
        self.start_button.configure(state="disabled")
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")
        # Tk variables must be read on the UI thread.
        settings = (round(self.quality_var.get()), self.convert_var.get(), self.subfolders_var.get())
        threading.Thread(target=self._process, args=(source, *settings), daemon=True).start()

    def _process(self, source, quality, convert, subfolders):
        output = source.parent / f"{source.name}_BA瘦身完成"
        output.mkdir(exist_ok=True)
        pattern = "**/*" if subfolders else "*"
        files = [p for p in source.glob(pattern) if p.is_file() and p.suffix.lower() in SUPPORTED]
        self.events.put(("total", len(files)))
        if not files:
            self.events.put(("done", 0, 0, 0, output, 0))
            return

        before_total = after_total = success = failed = 0
        for index, source_file in enumerate(files, 1):
            try:
                relative = source_file.relative_to(source)
                destination = output / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                convert_this = convert and source_file.suffix.lower() not in {".jpg", ".jpeg"}
                if convert_this or source_file.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
                    destination = destination.with_suffix(".jpg")
                before = source_file.stat().st_size
                final_path = save_optimized(source_file, destination, quality, convert_this)
                after = final_path.stat().st_size
                before_total += before
                after_total += after
                success += 1
                ratio = 100 * (1 - after / before) if before else 0
                self.events.put(("log", f"✓ {relative}  {human_size(before)} → {human_size(after)}  減少 {ratio:.1f}%"))
            except Exception as error:
                failed += 1
                self.events.put(("log", f"✗ {source_file.name}：{error}"))
            self.events.put(("progress", index))
        self.events.put(("done", success, failed, before_total, output, after_total))

    def _poll_events(self):
        try:
            while True:
                event = self.events.get_nowait()
                kind = event[0]
                if kind == "total":
                    self.progress.configure(maximum=max(event[1], 1), value=0)
                    self._append_log(f"找到 {event[1]} 張圖片。")
                elif kind == "progress":
                    self.progress.configure(value=event[1])
                elif kind == "log":
                    self._append_log(event[1])
                elif kind == "done":
                    _, success, failed, before, output, after = event
                    self.running = False
                    self.start_button.configure(state="normal")
                    reduction = 100 * (1 - after / before) if before else 0
                    summary = (
                        f"完成：成功 {success} 張，失敗 {failed} 張\n"
                        f"總容量：{human_size(before)} → {human_size(after)}（減少 {reduction:.1f}%）\n"
                        f"輸出位置：{output}"
                    )
                    self._append_log(summary.replace("\n", " | "))
                    messagebox.showinfo(APP_TITLE, summary)
        except queue.Empty:
            pass
        self.after(100, self._poll_events)


if __name__ == "__main__":
    OptimizerApp().mainloop()
