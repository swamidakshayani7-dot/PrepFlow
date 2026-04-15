from flask import Flask,render_template,request,redirect,url_for
import sqlite3
app=Flask(__name__)

#fix route
def create_table():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS problems(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        status TEXT DEFAULT 'Not Solved'
    )
    """)

    conn.commit()
    conn.close()

create_table()   # ✅ MUST CALL

@app.route('/')
def home():
    
    return redirect('/login')

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        conn=sqlite3.connect("users.db")
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?AND password=?",(username,password))
        user=cursor.fetchone()
        conn.close()
        if user:
            return redirect(url_for("dashboard"))
        else:
            return "invalid username or password"
    return render_template("login.html")


@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        print("Register route hit",flush=True)
        username=request.form["username"]
        password=request.form["password"]
        confirm=request.form['confirm_password']
        if password!=confirm:
            return "Password do not match"
        conn=sqlite3.connect("users.db")
        cursor=conn.cursor()
        cursor.execute("INSERT INTO users(username,password)VALUES(?,?)",(username,password))
        conn.commit()
        conn.close()
        #return redirect(url_for('login'))
        return "user registered successfully"
    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    
    search = request.args.get("search")
    filter_type = request.args.get("filter")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # 🎯 Decide query
    if filter_type == "solved":
        cursor.execute("SELECT * FROM problems WHERE status='Solved'")
    elif filter_type == "unsolved":
        cursor.execute("SELECT * FROM problems WHERE status='NOt Solved'")
    elif search:
        cursor.execute("SELECT * FROM problems WHERE name LIKE ?", ('%' + search + '%',))
    else:
        cursor.execute("SELECT * FROM problems")

    problems = cursor.fetchall()

    # 🔢 Get ALL problems for stats
    cursor.execute("SELECT * FROM problems")
    all_problems = cursor.fetchall()

    total = len(all_problems)
    solved = 0
    unsolved = 0

    for p in all_problems:
        if p[2] == "Solved":
            solved += 1
        else:
            unsolved += 1

    conn.close()

    return render_template("dashboard.html",
                           problems=problems,
                           total=total,
                           solved=solved,
                           unsolved=unsolved)

@app.route("/add_problem",methods=["post"])
def add_problem():
    problem_name=request.form["problem_name"]
    conn=sqlite3.connect("users.db")
    cursor=conn.cursor()
    cursor.execute("INSERT INTO problems(name)VALUES(?)",(problem_name,))
    conn.commit()
    conn.close()
    return redirect(url_for("dashboard"))


@app.route("/mark_solved/<int:id>")
def mark_solved(id):
    conn=sqlite3.connect("users.db")
    cursor=conn.cursor()
    cursor.execute("UPDATE problems SET status='Solved' WHERE id=?",(id,))
    conn.commit()
    conn.close()
    return redirect(url_for("dashboard"))

@app.route("/delete/<int:id>")
def delete(id):
    conn=sqlite3.connect("users.db")
    cursor=conn.cursor()
    cursor.execute("DELETE FROM problems WHERE id=?",(id,))
    conn.commit()
    conn.close()
    return redirect(url_for("dashboard"))



    
if __name__=="__main__":
    app.run(debug=True)
