from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
# from scrapper2 import get_jobs2
from exporter import save_to_file

app = Flask("JobScrapper")

db = {}

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/report")
def report():
  word = request.args.get('word')
  if word:
    word = word.lower()
    existingJobs = db.get(word)
    if existingJobs:
      jobs = existingJobs
    else:
      jobs = get_jobs(word)
      # jobs2 = get_jobs2(word)
      # jobs = jobs + jobs2
      db[word] = jobs
  else:
    return redirect("/")
  return render_template(
        "report.html", 
        searchingBy=word, 
        resultNumber=len(jobs),
        jobs = jobs
        )

@app.route("/export")
def export():
  try:
    word = request.args.get('word')
    if not word:
      raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file("jobs.csv")
  except:
    return redirect("/")

    
app.run(host="0.0.0.0")
