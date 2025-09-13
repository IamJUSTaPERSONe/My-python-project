import winreg
import ctypes
import sys
import tkinter as tk
from tkinter import messagebox as mb

# Блокирует изменения обоев и заставки
def block_changes():
    try:
        key_wallpaper = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Policies\ActiveDesktop')
        winreg.SetValueEx(key_wallpaper, 'NoChangingWallPaper', 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key_wallpaper)

        key_screen = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Policies\System')
        winreg.SetValueEx(key_screen, 'NoDispScrSavPage', 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key_screen)
        return True
    except Exception as e:
        print(f"Ошибка блокировки: {e}")
        return False

# Разрешает изменение обоев и заставки
def enable_changes():
    try:
        try:
            key_wallpaper = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Policies\ActiveDesktop', 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key_wallpaper, 'NoChangingWallPaper')
            winreg.CloseKey(key_wallpaper)
        except FileNotFoundError:
            pass

        try:
            key_screen = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Policies\System', 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key_screen, 'NoDispScrSavPage')
            winreg.CloseKey(key_screen)
        except FileNotFoundError:
            pass
        return True
    except Exception as e:
        print(f"Ощибка разблокировки: {e}")
        return False

# Проверяет статус блокировки обоев
def check_wallpaper_status():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Policies\ActiveDesktop')
        value, _ = winreg.QueryValueEx(key, "NoChangingWallPaper")
        winreg.CloseKey(key)
        return value == 1
    except FileNotFoundError:
        return False
    except Exception:
        return False

# Проверяет статус блокировки заставки
def check_screen_status():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Policies\System')
        value, _ = winreg.QueryValueEx(key, "NoDispScrSavPage")
        winreg.CloseKey(key)
        return value == 1
    except FileNotFoundError:
        return False
    except Exception:
        return False

# Проверяет, админ ли использует программу
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# не помню зачем
def admin_status_get():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

# Создаем класс для интерфейса
class WallpaperControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Контроль изменения обоев и заставки")
        self.root.geometry("300x150")

        self.setup_ui()
        self.update_status()

    # Создает базовый интерфейс
    def setup_ui(self):
        self.status = tk.Label(self.root, text='Статус')
        self.status.pack(pady=5)

        self.wallpaper_status = tk.Label(self.root, text="Обои...проверка")
        self.wallpaper_status.pack(pady=2)

        self.screen_status = tk.Label(self.root, text="Заставка...проверка")
        self.screen_status.pack(pady=2)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        self.block_btn = tk.Button(button_frame, text="Заблокировать изменения", command=self.block)
        self.block_btn.pack()

        self.enable_btn = tk.Button(button_frame, text="Разрешить изменения", command=self.enable)
        self.enable_btn.pack()

    # Обновляет статус
    def update_status(self):
        is_blocked_1 = check_wallpaper_status()
        is_blocked_2 = check_screen_status()

        wallpaper_text = "Обои: ЗАБЛОКИРОВАНЫ" if is_blocked_1 else "Обои: РАЗБЛОКИРОВАНЫ"
        wallpaper_color = "red" if is_blocked_1 else "green"
        self.wallpaper_status.config(text=wallpaper_text, fg=wallpaper_color)

        screen_text = "Заставка: ЗАБЛОКИРОВАНА" if is_blocked_2 else "Заставка: РАЗБЛОКИРОВАНА"
        screen_color = "red" if is_blocked_2 else "green"
        self.screen_status.config(text=screen_text, fg=screen_color)

    # Выводит предупреждения при блокировке
    def block(self):
        if not is_admin():
            mb.showwarning('', 'Требуются права администратора')
            return

        if block_changes():
            mb.showinfo('', 'Изменение обоев и заставки заблокировано')
            self.update_status()
        else:
            mb.showerror('', 'Не удалось заблокировать изменения')

    # Выводит предупреждения при разблокировке
    def enable(self):
        if not is_admin():
            mb.showwarning('', 'Требуются права администратора')
            return
        if enable_changes():
            mb.showinfo('', 'Изменение обоев и заставки разблокировано')
            self.update_status()
        else:
            mb.showerror('','Не удалось разблокировать изменения')

# Главная функция запуска
def main():
    root = tk.Tk()
    app = WallpaperControlApp(root)

    root.eval('tk::PlaceWindow . center')
    root.mainloop()


if __name__=="__main__":
    main()
