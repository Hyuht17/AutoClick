import tkinter as tk
import pyautogui as pag
import pyperclip as clip
from pynput import mouse
import time
import keyboard

mouse_listener = None
mouse_click = False
window = None
txt = ""
is_running = None
stored_hotkey = ""
hotkey_check = True
stored_text = ""
hotkey = ""
label = None
last_click_time = 0
last_hotkey_time = 0
click_interval = 0.5  # Khoảng thời gian tối thiểu giữa hai sự kiện click chuột (đơn vị: giây)
hotkey_interval = 1
selected_button = None  # Nút được chọn mặc định là None
var = None
# Ánh xạ giữa giá trị của biến và giá trị của mouse.Button
button_mapping = {'left': mouse.Button.left, 'right': mouse.Button.right}
def main():
    global window
    global text_entry
    global button 
    global is_running
    global hotkey_check
    global hotkey
    window = tk.Tk()
    window.title("Tool Tự động Click và Gõ Bàn Phím")
    window.geometry("260x165")
    design_theme()
    window.protocol("WM_DELETE_WINDOW", on_close)  # Gán hành động khi nhấn nút "Close"
    window.resizable(width=False, height=False)
    window.mainloop()

#Tạo giao diện

def design_theme():
    create_menu()
    global hotkey
    global click_button
    global display_label
    global hotkey_hook
    global var
    # Tạo và định dạng các thành phần giao diện
    load_saved_data() 
    hotkey = stored_hotkey
    txt = stored_text
    click_button = tk.Button(window, text="Bấm {} để Bắt đầu/Dừng".format(hotkey))
    click_button.config(width=20, height=2)
    click_button.bind("<Enter>",mouseEntered)
    click_button.bind("<Leave>",mouseExited)
    click_button.pack()
    keyboard.on_press_key("Esc", close_soft)
    
    hotkey_hook = keyboard.on_press_key(hotkey, check_hotkey, suppress=True)
    
    var = tk.StringVar()
    # Tạo ô chọn (radio button) cho chuột phải
    frame = tk.Frame(window)
    frame.pack()

    # Tạo ô chọn (radio button) cho chuột phải
    right_radio = tk.Radiobutton(frame, text="Chuột Phải", variable=var, value="right", command=update_selection)
    right_radio.pack(side=tk.LEFT)

    # Tạo ô chọn (radio button) cho chuột trái
    left_radio = tk.Radiobutton(frame, text="Chuột Trái", variable=var, value="left", command=update_selection)
    left_radio.pack(side=tk.LEFT)


    # Mặc định không có nút nào được chọn
    if selected_button == "right":
        var.set("right")
    elif selected_button == "left":
        var.set("left")
    else:
    # Nếu không có lựa chọn trước đó, mặc định là không có nút nào được chọn
        var.set(None)
    #tạo nút thoát và đóng 
    exit_button = tk.Button(window, text="Thoát", command=close_soft2)
    exit_button.pack()
    label1 = tk.Label(window, text="Bấm ESC để thoát")
    label1.pack()
def update_selection():
    global selected_button, var
    selected_button = var.get()
    save_data()

def show_notification():
    global root
    root = tk.Tk()
    root.wm_attributes("-topmost", 1)
    root.overrideredirect(True)  # Ẩn tiêu đề và viền của cửa sổ
    label = tk.Label(root, text="Phần mềm đang hoạt động", bg="black", fg="white")
    label.pack()
    root.geometry("+0+0")  # Di chuyển cửa sổ vào góc trái màn hình
    root.mainloop()
def hide_notification():
    global root  # Kiểm tra xem cửa sổ tồn tại và không được hiển thị
    root.destroy()

    
    
def close_soft(e):
    if is_running:
        stop_func()
    window.destroy()
def close_soft2():
    if is_running:
        stop_func()
    window.destroy()
def on_close():
    window.iconify()
   
def create_menu():
    # Thêm lại nội dung gốc hoặc các yếu tố giao diện bạn muốn
    menubar = tk.Menu(window)
    window.config(menu=menubar)

    filemenu = tk.Menu(menubar)
    menubar.add_cascade(label="Tệp", menu=filemenu)
    filemenu.add_command(label="Thoát", command=close_soft2)  # Đặt lệnh thoát trực tiếp ở đây

    textmenu = tk.Menu(menubar)
    menubar.add_cascade(label="Cài đặt", menu=textmenu)
    textmenu.add_command(label="Nhập văn bản", command=open_second_page)
    textmenu.add_command(label="Nhập số lần nhấp", command=open_second_page2)
# Trong hàm mouseEntered:
 
def mouseEntered(event):
    button = event.widget
    button.config(text = "Đổi Hotkey", command=press_button)

def press_button():
    keyboard.unhook(hotkey_hook)
    global label  # Thêm vào
    label = tk.Label(window, text="Ấn hotkey mới!")
    label.pack()
    window.bind("<Key>", change_hotkey)
    #window.after(3000, label.pack_forget)
    
def mouseExited(event):
    button = event.widget
    button.config(text = "Bấm {} để Bắt đầu/Dừng".format(hotkey))      
    
def create_text_entry(parent):
    text_entry = tk.Entry(parent)
    text_entry.pack()
    txt = text_entry.get()

    
def check_hotkey(e):
    global is_running, hotkey, last_hotkey_time, hotkey_interval, cnt, number, stored_number

    current_time = time.time()

    if not is_running and (current_time - last_hotkey_time) > hotkey_interval:
        cnt = 0
        number = int(stored_number)
        show_po()
        is_running = True
        last_hotkey_time = current_time
    else:
        stop_func()
        is_running = False
        



def change_hotkey(event=None):
    global hotkey
    global stored_hotkey # Thêm vào

    global label
    if event:
        hotkey = event.char
    window.unbind("<Key>")
    update_button_text()
    stored_hotkey = hotkey
    save_data()
    label.pack_forget()
    hotkey_hook = keyboard.on_press_key(hotkey, check_hotkey)
    restart_program()
def restart_program():
    # Xóa tất cả các hotkey
    keyboard.unhook_all()
    
    # Thực hiện các bước restart cần thiết
    # Ví dụ: Đóng giao diện và mở lại
    window.destroy()
    main() 


def update_button_text():
    global click_button
    click_button.config(text="Bấm {} để Bắt đầu/Dừng".format(hotkey))


def open_second_page():
    global second_window
    global stored_text
    global second_text_entry
    second_window = tk.Toplevel(window)
    second_window.title("Nhập văn bản")

    second_text_entry = tk.Entry(second_window)
    second_text_entry.insert(0, stored_text)  # Chèn văn bản đã lưu vào ô nhập văn bản
    second_text_entry.pack()

    second_save_button = tk.Button(second_window, text="Lưu", command=save_and_return)
    second_save_button.pack()
def open_second_page2():
    global second_window2
    global stored_number
    global second_number_entry
    second_window2 = tk.Toplevel(window)
    second_window2.title("Nhập số lần nhấp")

    second_number_entry = tk.Entry(second_window2)
    second_number_entry.insert(0, stored_number)  # Chèn văn bản đã lưu vào ô nhập văn bản
    second_number_entry.pack()

    second_save_button = tk.Button(second_window2, text="Lưu", command=save_and_return2)
    second_save_button.pack()

def save_and_return():
    global txt
    global stored_text
    txt = second_text_entry.get()
    stored_text = txt
    save_data()
    if second_window:
        second_window.destroy()
def save_and_return2():
    global stored_number
    stored_number = second_number_entry.get()
    save_data()
    if second_window2:
        second_window2.destroy()
        
        
def load_saved_data():
    global stored_text, stored_hotkey, selected_button, stored_number
    try:
        with open("saved_data.txt", "r") as file:
            data = file.read().splitlines()
            stored_text = data[0]
            stored_hotkey = data[1]
            selected_button = data[2]
            stored_number = data[3]
    except FileNotFoundError:
        pass

def save_data():
    global stored_hotkey, selected_button, stored_number
    with open("saved_data.txt", "w") as file:
        file.write(stored_text + "\n")
        file.write(stored_hotkey + "\n")
        file.write(selected_button + "\n")
        file.write(stored_number + "\n")

#Phần chạy ứng dụng


#chạy nền
    
# Chọn tọa độ  
def on_click(x, y, button, pressed):
    global last_click_time, click_interval, selected_button, cnt

    if pressed:
        current_time = time.time()
        if (current_time - last_click_time) > click_interval:
            if selected_button and button == button_mapping[selected_button]:
                # Thực hiện hành động khi click chuột
                cnt = cnt + 1
                x, y = pag.position()
                mouse_listener.stop()
                window.after(1, tool_auto_in_zalo, x, y)
                last_click_time = current_time



def click_position():
    global mouse_listener
        # Tạo một thể hiện của Listener chuột
    mouse_listener = mouse.Listener(on_click=on_click)
        # Bắt đầu theo dõi sự kiện chuột
    mouse_listener.start()


#bắt đầu chạy ứng dụng    
def show_po():
    window.after(100, show_notification)
    click_position()
    


def click_func(x, y):
    pag.click(x, y, button='left')
    
def double_click_func(x, y):
    pag.doubleClick(x, y, button='left')

def print_text(text):
    global txt, stored_text
    
    clip.copy(stored_text)

    # Tạm ngừng để clipboard có thể hoạt động
    time.sleep(0.001)

    # Dán văn bản vào ứng dụng mục tiêu
    pag.hotkey('ctrl', 'v')

def press_enter():
    pag.press('enter')
    
    
def tool_auto_in_zalo(x, y):
    global cnt, is_running
    double_click_func(x, y)
    if stored_text != "":
        print_text(txt)
    press_enter()
    if cnt == number and is_running == True:
        stop_func()
        is_running = False
        cnt = 0
    else: 
        click_position()

def stop_func():
    global mouse_listener
    mouse_listener.stop()
    hide_notification()
      
main()  
###lhasjkh