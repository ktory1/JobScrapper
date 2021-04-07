from flask import Flask, render_template, request, redirect
from so_scrapper import get_jobs as so_jobs
from indeed_scrapper import get_jobs as indeed_jobs

app = Flask("SuperScrapper")

db = {}

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/report")
def report():
  word = request.args.get("word")
  if word:
    word = word.lower()
    existingJobs = db.get(word)
    if existingJobs:
      jobs = existingJobs
    else:
      jobs = so_jobs(word) + indeed_jobs(word)
      db[word] = jobs 
  else:
    return redirect("/")
  return render_template(
    "report.html",
    searchingBy = word, 
    resultNumber = len(jobs),
    jobs = jobs)

app.run(host="0.0.0.0",port=1234)