from tkinter import messagebox
import tkinter as tk
import json
import os
import random

search_entry = None
current_term = ""
current_meaning = ""


FILENAME = "terms.json"

def save_term():
    term = entry_term.get().strip()
    meaning = entry_meaning.get().strip()
    
    if not term or not meaning:
        return
    
    
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as f:
            data = json.load(f)
            
    else:
        data = {}
        
    if term in data:
        result_label.config(text="すでに登録されています！", fg="red")
        return
        
    data[term] = meaning
    
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    update_display(data)
    
    entry_term.delete(0, tk.END)
    entry_meaning.delete(0, tk.END)
    
def update_display(data=None):
    listbox.delete(0, tk.END)
    
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as f:
            data = json.load(f)
                
    else:
        data = {}
            
    
    keyword = search_entry.get().strip().lower()
    
    sorted_items = sorted(data.items(), key=lambda x: x[0].lower())
    
    for term, meaning in sorted_items:
        if keyword in term.lower() or keyword in meaning.lower():
            listbox.insert(tk.END, f"{term} : {meaning}")
            
def delete_term():
    if not listbox.curselection():
        return
    
    
    
    selected = listbox.get(listbox.curselection())
    term = selected.split(":")[0].strip()
        
    
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for key in list(data.keys()):
            if key.lower() == term.lower():
                del data[key]
                with open (FILENAME, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                update_display()
                break
    
def reset_terms():
    answer = messagebox.askyesno("確認", "本当に単語帳をリセットしますか？")
    if answer:
        if os.path.exists(FILENAME):
            os.remove(FILENAME)
        update_display()
        result_label.config(text="単語帳をリセットしました！", fg="blue")
    else:
        result_label.config(text="リセットをキャンセルしました", fg="gray")
def start_quiz():
    global current_term, current_meaning
    cover.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        if not data:
            quiz_label.config(text="登録された用語がありません。 ")
            return
        
        current_term, current_meaning = random.choice(list(data.items()))
        quiz_label.config(text=f"意味: {current_meaning}")
        answer_entry.delete(0, tk.END)
        result_label.config(text="")
        
        answer_entry.focus_set()
        
def check_answer():
    user_answer = answer_entry.get().strip().lower()
    correct_term = current_term.lower()
    
    if user_answer == correct_term:
        result_label.config(text="正解！", fg="green")
    else:
        result_label.config(text=f"不正解　正解は: {current_term}", fg="red")
        
    
    cover.place_forget()
        
def select_line(event):
    try:
        index = display_text.index(f"@{event.x},{event.y}")
        line_start = f"{index.split('.')[0]}.0"
        line_end = f"{int(index.split('.')[0]) + 1}.0"
        display_text.tag_remove(tk.SEL, "1.0", tk.END)
        display_text.tag_add(tk.SEL, line_start, line_end)
    except:
        pass
        
root = tk.Tk()
root.title("プログラミング用語メモ")
root.geometry("400x800")

top_frame = tk.Frame(root)
top_frame.pack(fill="x")

middle_frame = tk.Frame(root)
middle_frame.pack(fill="both", expand=True)

bottom_frame = tk.Frame(root)
bottom_frame.pack(fill="x")

cover = tk.Label(root, bg="black")
tk.Label(top_frame, text="用語").pack()
entry_term = tk.Entry(top_frame)
entry_term.pack()
entry_term.bind("<KeyRelease>", lambda e: cover.place_forget())
entry_term.bind("<FocusIn>", lambda e: cover.place_forget())

tk.Label(top_frame, text="意味").pack()
entry_meaning = tk.Entry(top_frame)
entry_meaning.pack()
entry_meaning.bind("<KeyRelease>", lambda e: cover.place_forget())
entry_meaning.bind("<Return>", lambda e: (cover.place_forget(), save_term()))
entry_meaning.bind("<FocusIn>", lambda e: cover.place_forget())

tk.Button(top_frame, text="登録", command=lambda: (cover.place_forget(), save_term())).pack(pady=5)

tk.Button(top_frame, text="単語帳リセット", command=lambda: (cover.place_forget(), reset_terms())).pack(pady=5)

scrollbar = tk.Scrollbar(middle_frame)
scrollbar.pack(side="right", fill="y")

listbox = tk.Listbox(middle_frame, selectmode=tk.SINGLE, yscrollcommand=scrollbar.set)
listbox.pack(fill="both", expand=True, pady=10)


scrollbar.config(command=listbox.yview)
cover = tk.Label(listbox, bg="black")

tk.Button(top_frame, text="削除", command=lambda: (cover.place_forget(), delete_term())).pack(pady=5)

tk.Label(top_frame, text="検索").pack()
search_entry = tk.Entry(top_frame)
search_entry.pack()
search_entry.bind("<KeyRelease>", lambda e: (cover.place_forget(), root.after_idle(update_display)))

tk.Label(bottom_frame, text="クイズモード").pack(pady=10)

quiz_label = tk.Label(bottom_frame, text="ここに意味が出ます", font=("Arial", 12))
quiz_label.pack()

answer_entry = tk.Entry(bottom_frame)
answer_entry.pack()

tk.Button(bottom_frame, text="クイズを開始", command=start_quiz).pack(pady=3)
tk.Button(bottom_frame, text="答え合わせ", command=check_answer).pack(pady=3)

result_label = tk.Label(bottom_frame, text="", font=("Arial", 12))
result_label.pack(pady=5)
        

update_display()

root.mainloop()