import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

HOST = "127.0.0.1"
PORT = 12345

class ChatClientGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Mini Game Đoán Số")
        self.window.geometry("400x500")
        self.window.resizable(False, False)

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((HOST, PORT))
        except Exception as e:
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối đến server: {e}")
            self.window.destroy()
            return

        
        self.chat_area = scrolledtext.ScrolledText(self.window, state='disabled', wrap=tk.WORD)
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_area.tag_config('server', foreground="blue", font=("Arial", 10, "bold"))
        self.chat_area.tag_config('user', foreground="black")
        
        input_frame = tk.Frame(self.window)
        input_frame.pack(padx=10, pady=5, fill=tk.X)

        self.msg_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.msg_entry.bind("<Return>", self.send_message)

        btn_frame = tk.Frame(self.window)
        btn_frame.pack(padx=10, pady=(0, 10), fill=tk.X)

        send_btn = tk.Button(btn_frame, text="Gửi Chat", width=10, command=self.send_message, bg="#dddddd")
        send_btn.pack(side=tk.LEFT, padx=5)

        guess_btn = tk.Button(btn_frame, text="ĐOÁN SỐ", width=10, command=self.send_guess, bg="#90ee90", font=("Arial", 9, "bold"))
        guess_btn.pack(side=tk.RIGHT, padx=5)

        self.running = True
        receive_thread = threading.Thread(target=self.receive_loop)
        receive_thread.daemon = True
        receive_thread.start()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def add_to_chat(self, message, tag='user'):
        """Hàm hỗ trợ thêm tin nhắn vào khung chat"""
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + "\n", tag)
        self.chat_area.yview(tk.END) 
        self.chat_area.config(state='disabled')

    def receive_loop(self):
        """Luồng nhận tin nhắn từ server"""
        while self.running:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                msg = data.decode()
                tag = 'server' if msg.startswith("Server:") else 'user'
                self.add_to_chat(msg, tag)
            except:
                if self.running:
                    self.add_to_chat("[Lỗi] Mất kết nối đến Server!", 'server')
                break

    def send_message(self, event=None):
        """Gửi tin nhắn chat thông thường"""
        msg = self.msg_entry.get().strip()
        if msg:
            try:
                self.client_socket.send(msg.encode())
                self.add_to_chat(f"Bạn: {msg}", 'user')
                self.msg_entry.delete(0, tk.END)
            except:
                self.add_to_chat("[Lỗi] Không gửi được tin nhắn", 'server')

    def send_guess(self):
        """Gửi lệnh đoán số (/guess <so>)"""
        msg = self.msg_entry.get().strip()
        if msg.isdigit():
            full_cmd = f"/guess {msg}"
            try:
                self.client_socket.send(full_cmd.encode())
                self.add_to_chat(f"Bạn đoán: {msg}", 'user')
                self.msg_entry.delete(0, tk.END)
            except:
                self.add_to_chat("[Lỗi] Không gửi được", 'server')
        else:
            messagebox.showwarning("Sai cú pháp", "Vui lòng nhập một số nguyên vào ô chat để đoán!")

    def on_closing(self):
        """Dọn dẹp khi đóng cửa sổ"""
        self.running = False
        try:
            self.client_socket.close()
        except:
            pass
        self.window.destroy()

if __name__ == "__main__":
    ChatClientGUI()