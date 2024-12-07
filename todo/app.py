import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from tkinter import simpledialog


class Task:
    def __init__(self, title, category, due_date=None, priority="Low"):
        self.title = title
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.completed = False

    def mark_completed(self):
        self.completed = True

    def update(self, title=None, category=None, due_date=None, priority=None):
        if title:
            self.title = title
        if category:
            self.category = category
        if due_date:
            self.due_date = due_date
        if priority:
            self.priority = priority

    def __str__(self):
        status = "Completed" if self.completed else "Not completed"
        return f"Title: {self.title}, Category: {self.category}, Due: {self.due_date}, Priority: {self.priority}, Status: {status}"


class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do Uygulaması")
        self.tasks = []
        self.filtered_tasks = []

        
        self.frames = {}
        self.current_frame = None

   
        self.add_task_frame = tk.Frame(root)
        self.frames["add_task"] = self.add_task_frame


        self.list_task_frame = tk.Frame(root)
        self.frames["list_task"] = self.list_task_frame

        self.show_frame("add_task")


        self.title_label = tk.Label(self.add_task_frame, text="Görev Başlığı")
        self.title_label.pack()
        self.title_entry = tk.Entry(self.add_task_frame)
        self.title_entry.pack()

        self.category_label = tk.Label(self.add_task_frame, text="Kategori")
        self.category_label.pack()
        self.category_entry = tk.Entry(self.add_task_frame)
        self.category_entry.pack()

        self.due_date_label = tk.Label(self.add_task_frame, text="Bitiş Tarihi (YYYY-MM-DD)")
        self.due_date_label.pack()
        self.due_date_entry = tk.Entry(self.add_task_frame)
        self.due_date_entry.pack()

        self.priority_label = tk.Label(self.add_task_frame, text="Öncelik (Low, Medium, High)")
        self.priority_label.pack()
        self.priority_entry = tk.Entry(self.add_task_frame)
        self.priority_entry.pack()

        self.add_button = tk.Button(self.add_task_frame, text="Görev Ekle", command=self.add_task)
        self.add_button.pack()

        self.switch_to_list_button = tk.Button(self.add_task_frame, text="Görev Listele", command=self.show_task_list_page)
        self.switch_to_list_button.pack()


        self.tasks_listbox = tk.Listbox(self.list_task_frame, height=10, width=50)
        self.tasks_listbox.pack()

        self.complete_button = tk.Button(self.list_task_frame, text="Görevi Tamamla", command=self.mark_task_completed)
        self.complete_button.pack()

        self.delete_button = tk.Button(self.list_task_frame, text="Görev Sil", command=self.delete_task)
        self.delete_button.pack()

        self.update_button = tk.Button(self.list_task_frame, text="Görev Güncelle", command=self.update_task)
        self.update_button.pack()

        self.filter_button = tk.Button(self.list_task_frame, text="Filtrele (Tamamlanmış Görevler)", command=self.filter_completed)
        self.filter_button.pack()

        self.clear_filter_button = tk.Button(self.list_task_frame, text="Filtreyi Kaldır", command=self.clear_filter)
        self.clear_filter_button.pack()

        self.switch_to_add_button = tk.Button(self.list_task_frame, text="Görev Ekle", command=self.show_add_task_page)
        self.switch_to_add_button.pack()

        self.update_listbox()

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        if self.current_frame:
            self.current_frame.pack_forget()
        frame.pack()

        self.current_frame = frame

    def add_task(self):
        title = self.title_entry.get()
        category = self.category_entry.get()
        due_date = self.due_date_entry.get()
        priority = self.priority_entry.get()

        if not title or not category or not priority:
            messagebox.showerror("Hata", "Tüm alanları doldurun.")
            return

        task = Task(title, category, due_date, priority)
        self.tasks.append(task)
        self.update_listbox()
        self.clear_entries()

    def mark_task_completed(self):
        selected_task_index = self.tasks_listbox.curselection()
        if selected_task_index:
            task = self.tasks[selected_task_index[0]]
            task.mark_completed()
            self.update_listbox()
        else:
            messagebox.showerror("Hata", "Bir görev seçin.")

    def delete_task(self):
        selected_task_index = self.tasks_listbox.curselection()
        if selected_task_index:
            del self.tasks[selected_task_index[0]]
            self.update_listbox()
        else:
            messagebox.showerror("Hata", "Bir görev seçin.")

    def update_task(self):
        selected_task_index = self.tasks_listbox.curselection()
        if selected_task_index:
            task = self.tasks[selected_task_index[0]]
            new_title = simpledialog.askstring("Güncelle", "Yeni başlık:", initialvalue=task.title)
            new_category = simpledialog.askstring("Güncelle", "Yeni kategori:", initialvalue=task.category)
            new_due_date = simpledialog.askstring("Güncelle", "Yeni bitiş tarihi:", initialvalue=task.due_date)
            new_priority = simpledialog.askstring("Güncelle", "Yeni öncelik:", initialvalue=task.priority)

            task.update(new_title, new_category, new_due_date, new_priority)
            self.update_listbox()
        else:
            messagebox.showerror("Hata", "Bir görev seçin.")

    def filter_completed(self):
        self.filtered_tasks = [task for task in self.tasks if task.completed]
        self.update_listbox(filtered=True)

    def clear_filter(self):
        self.filtered_tasks = []
        self.update_listbox()

    def update_listbox(self, filtered=False):
        self.tasks_listbox.delete(0, tk.END)

        tasks_to_display = self.filtered_tasks if filtered else self.tasks
        for task in tasks_to_display:
            self.tasks_listbox.insert(tk.END, task)

    def show_add_task_page(self):
        self.show_frame("add_task")

    def show_task_list_page(self):
        self.show_frame("list_task")

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
