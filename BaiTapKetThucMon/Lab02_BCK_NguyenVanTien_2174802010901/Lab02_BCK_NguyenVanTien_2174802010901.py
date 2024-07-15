import tkinter as tk
from tkinter import messagebox
import psycopg2
from psycopg2 import sql
import textwrap

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database App")
        self.root.geometry("1920x1080")

        self.table_name = tk.StringVar()
        self.search_id = tk.StringVar()
        self.search_release_date = tk.StringVar()
        self.search_title = tk.StringVar()

        self.db_name = tk.StringVar(value='postgres')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='123456')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        self.table_name = tk.StringVar(value='moviedata')
        self.search_term = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Tạo khung trái và phải
        left_frame = tk.Frame(self.root)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

        right_frame = tk.Frame(self.root)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Phần kết nối
        connection_frame = tk.LabelFrame(left_frame, text="Kết nối cơ sở dữ liệu")
        connection_frame.pack(fill=tk.BOTH, padx=10, pady=10)

        tk.Label(connection_frame, text="DB Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.db_name).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="User:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.user).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.password, show="*").grid(row=2, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Host:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.host).grid(row=3, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Port:").grid(row=4, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.port).grid(row=4, column=1, padx=5, pady=5)

        tk.Button(connection_frame, text="Kết nối", command=self.connect_db).grid(row=5, columnspan=2, pady=10)

        # Phần truy vấn
        query_frame = tk.LabelFrame(left_frame, text="Truy vấn dữ liệu")
        query_frame.pack(fill=tk.BOTH, padx=10, pady=10)

        tk.Label(query_frame, text="Table Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(query_frame, textvariable=self.table_name).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(query_frame, text="Tải dữ liệu", command=self.load_data).grid(row=1, column=0, columnspan=2, pady=5)

        tk.Button(query_frame, text="Mở cửa sổ Insert", command=self.open_new_window).grid(row=2, column=0, columnspan=2, pady=5)

        # Phần tìm kiếm
        search_frame = tk.LabelFrame(right_frame, text="Tìm kiếm dữ liệu")
        search_frame.pack(fill=tk.BOTH, padx=10, pady=10)

        tk.Label(search_frame, text="ID:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(search_frame, textvariable=self.search_id).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(search_frame, text="Release Date:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(search_frame, textvariable=self.search_release_date).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(search_frame, text="Title:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(search_frame, textvariable=self.search_title).grid(row=2, column=1, padx=5, pady=5)

        tk.Button(search_frame, text="Tìm kiếm", command=self.search_data).grid(row=3, columnspan=2, pady=10)
        tk.Button(search_frame, text="Xóa bỏ", command=self.delete_data).grid(row=4, columnspan=2, pady=10)

        # Data display
        self.data_display = tk.Text(right_frame, height=30, width=200)
        self.data_display.pack(pady=20)

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name.get(),
                user=self.user.get(),
                password=self.password.get(),
                host=self.host.get(),
                port=self.port.get()
            )
            self.cur = self.conn.cursor()
            messagebox.showinfo("Thành công", "Đã kết nối với cơ sở dữ liệu thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể kết nối với cơ sở dữ liệu: {e}")

    def load_data(self):
        try:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(query)
            rows = self.cur.fetchall()
            self.display_data(rows)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không tải được dữ liệu: {e}")

    def search_data(self):
        try:
            id_term = self.search_id.get()
            release_date_term = self.search_release_date.get()
            title_term = self.search_title.get()

            print(f"ID Term: {id_term}, Release Date Term: {release_date_term}, Title Term: {title_term}")

            conditions = []
            params = []

            if id_term:
                conditions.append("id = %s")
                params.append(id_term)
            if release_date_term:
                conditions.append("release_date = %s")
                params.append(release_date_term)
            if title_term:
                conditions.append("title LIKE %s")
                params.append(f"%{title_term}%")

            if not conditions:
                messagebox.showwarning("Lỗi đầu vào", "Vui lòng nhập ít nhất một tiêu chí tìm kiếm.")
                return

            query = sql.SQL("SELECT * FROM {} WHERE {}").format(
                sql.Identifier(self.table_name.get()),
                sql.SQL(" AND ").join(sql.SQL(cond) for cond in conditions)
            )
            self.cur.execute(query, tuple(params))
            rows = self.cur.fetchall()
            self.display_data(rows)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tìm kiếm dữ liệu: {e}")

    def delete_data(self):
        try:
            id_term = self.search_id.get()
            release_date_term = self.search_release_date.get()
            title_term = self.search_title.get()

            print(f"ID Term: {id_term}, Release Date Term: {release_date_term}, Title Term: {title_term}")

            conditions = []
            params = []

            if id_term:
                conditions.append("id = %s")
                params.append(id_term)
            if release_date_term:
                conditions.append("release_date = %s")
                params.append(release_date_term)
            if title_term:
                conditions.append("title LIKE %s")
                params.append(f"%{title_term}%")

            if not conditions:
                messagebox.showwarning("Lỗi đầu vào", "Vui lòng nhập ít nhất một tiêu chí tìm kiếm.")
                return

            query = sql.SQL("DELETE FROM {} WHERE {}").format(
                sql.Identifier(self.table_name.get()),
                sql.SQL(" AND ").join(sql.SQL(cond) for cond in conditions)
            )
            self.cur.execute(query, tuple(params))
            self.conn.commit()
            messagebox.showinfo("Thành công", "Dữ liệu đã được xóa thành công!")
            self.load_data()  # Tải lại dữ liệu để phản ánh các thay đổi
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa dữ liệu: {e}")

    def display_data(self, rows):
        self.data_display.delete(1.0, tk.END)
        max_width = 250
        for row in rows:
            row_str = f"{row}"
            wrapped_row = textwrap.fill(row_str, width=max_width)
            self.data_display.insert(tk.END, f"{wrapped_row}\n")

    def open_new_window(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Chèn dữ liệu")
        new_window.geometry("300x400")

        fields = {
            "Genres": tk.Entry(new_window),
            "ID": tk.Entry(new_window),
            "Original Language": tk.Entry(new_window),
            "Release Date": tk.Entry(new_window),
            "Runtime": tk.Entry(new_window),
            "Title": tk.Entry(new_window),
            "Vote Average": tk.Entry(new_window),
            "Director": tk.Entry(new_window)
        }

        for idx, (label_text, entry) in enumerate(fields.items()):
            label = tk.Label(new_window, text=label_text + ":")
            label.grid(row=idx, column=0, padx=5, pady=5, sticky=tk.E)
            entry.grid(row=idx, column=1, padx=5, pady=5)

        def submit_data():
            data = {label_text: entry.get() for label_text, entry in fields.items()}
            
            if all(data.values()):
                try:
                    conn = psycopg2.connect(
                        dbname="postgres", 
                        user="postgres", 
                        password="123456", 
                        host="localhost", 
                        port="5432"
                    )
                    cursor = conn.cursor()
                    insert_query = """
                    INSERT INTO moviedata (genres, id, original_language, release_date, runtime, title, vote_average, director) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, tuple(data.values()))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    messagebox.showinfo("Thành công", "Dữ liệu được chèn thành công")
                except Exception as e:
                    messagebox.showerror("Lỗi", str(e))
            else:
                messagebox.showwarning("Lỗi đầu vào", "Tất cả các trường là bắt buộc")

        submit_button = tk.Button(new_window, text="Nộp", command=submit_data)
        submit_button.grid(row=len(fields), column=1, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
