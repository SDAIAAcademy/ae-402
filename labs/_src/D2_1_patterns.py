# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas>=2.2", "scikit-learn>=1.5"]
# ///
# %% [markdown]
# # Lab 2.1 · Patterns, and the need a classifier serves better
#
# Day 2 · Session 1 (Patterns and when each fits) · 25 min.
#
# Six needs from the Ministry's teams, six patterns. You match them with fit questions instead of habit, then
# test the one match that surprises people: routing citizen reports to departments. You train a small classical
# classifier on 2,400 labelled reports on a laptop processor and compare it, on the same 600 test reports, with
# a recorded run of a generative model asked the same question.
#
# **Reference state.** `data/options/needs.csv`, `data/options/citizen_reports.csv` (3,000 synthetic reports,
# Arabic and English, six categories, 3% labelling noise) and `data/options/recorded_generative_run.csv`
# (a **synthetic** recording of a generative model's answers on the 600 test reports, with latency and tokens).
# Nothing from Day 1.
#
# **Tasks**
# - [ ] 1 · Six patterns, six fit questions (4')
# - [ ] 2 · Match six needs to patterns (6')
# - [ ] 3 · Train a classifier on 2,400 reports (8')
# - [ ] 4 · Compare it with the recorded generative run (7')
# - [ ] ✱ Stretch · Errors by language

# %%
import os, sys, subprocess
from pathlib import Path

IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    REPO_URL = "https://github.com/SDAIAAcademy/ae-402.git"
    if not Path("/content/ae-402").exists():
        subprocess.run(["git", "clone", "-q", REPO_URL, "/content/ae-402"], check=True)
    os.chdir("/content/ae-402/labs")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements-colab.txt"], check=True)
else:
    while not Path("_tools").exists() and Path.cwd() != Path.cwd().parent:
        os.chdir("..")  # solutions/ notebooks run from labs/
sys.path.insert(0, os.getcwd())

import time
import pandas as pd
import asas as A

needs = A.read_csv("options/needs.csv")
print(needs.to_string(index=False))

# %% [markdown]
# ## 1 · Six patterns, six fit questions (4')
#
# | Pattern | Fits when |
# |---|---|
# | `retrieval` | answers must come from a changing body of documents, with a citation |
# | `agentic` | a task needs several steps whose order depends on what earlier steps return |
# | `fine-tuned` | the output form is stable, the volume is high and thousands of good examples exist |
# | `classical` | the output is one of a few labels, labelled examples exist, and speed and cost matter |
# | `batch` | the answer is needed in hours, not seconds, over many records at once |
# | `event-driven` | something must happen when a record changes, not when a person asks |
#
# Read the columns of `needs.csv` as the answers to those questions: labelled examples, how fast, how many
# steps, how the data changes.

# %% [markdown]
# ## 2 · Match six needs to patterns (6')
#
# ✏️ **Exercise** · Return `{need id: pattern}`, one pattern per need, each pattern used once.

# %%
PATTERNS = ["retrieval", "agentic", "fine-tuned", "classical", "batch", "event-driven"]


def match_needs(df: pd.DataFrame) -> dict[str, str]:
    # BEGIN SOLUTION
    return {"N1": "retrieval", "N2": "classical", "N3": "batch", "N4": "event-driven", "N5": "agentic",
            "N6": "fine-tuned"}
    # END SOLUTION

# %%
key = A.reference("patterns_key")
try:
    matched = match_needs(needs)
except NotImplementedError:
    matched = dict(key)
    print("(using the reference match)")
table = needs[["id", "need"]].assign(yours=needs.id.map(matched), reference=needs.id.map(key))
print(table.to_string(index=False))
A.check(sum(matched[i] == key[i] for i in key) >= 5, "at least five of six matches agree with the reference")

# %% [markdown]
# 🔍 **Look at** N6. Fine-tuning fits a stable house style with 9,000 good letters; a prompt with three
# examples might do too. The match is a hypothesis to test, the way step 3 tests N2.

# %% [markdown]
# ## 3 · Train a classifier on 2,400 reports (8')
#
# ✏️ **Exercise** · Fit a TF-IDF of character n-grams (they handle Arabic and English without a tokenizer)
# and a logistic regression on the `train` rows. Return the fitted pipeline. It trains in seconds on a laptop
# processor.

# %%
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

reports = A.read_csv("options/citizen_reports.csv")
train, test = reports[reports.split == "train"], reports[reports.split == "test"].reset_index(drop=True)
print(len(train), "train,", len(test), "test;", reports.category.value_counts().to_dict())


def train_router(df: pd.DataFrame):
    # BEGIN SOLUTION
    model = make_pipeline(TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4)),
                          LogisticRegression(max_iter=2000))
    return model.fit(df.text, df.category)
    # END SOLUTION

# %%
try:
    router = train_router(train)
except NotImplementedError:
    router = make_pipeline(TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4)),
                           LogisticRegression(max_iter=2000)).fit(train.text, train.category)
    print("(using the reference classifier)")
start = time.perf_counter()
pred = router.predict(test.text)
ms_per_report = (time.perf_counter() - start) * 1000 / len(test)
classical_acc = float((pred == test.category).mean())
print(f"classical: accuracy {classical_acc:.3f}, {ms_per_report:.3f} ms per report on this processor")
A.check(classical_acc > 0.90, "the classifier routes more than 90% of the test reports correctly")

# %% [markdown]
# ## 4 · Compare it with the recorded generative run (7')
#
# ✏️ **Exercise** · Build one table with a row per approach: accuracy on the same 600 reports, mean latency,
# and the cost of routing the 95,000 reports a month of N2. Use the recorded tokens and the case's price card
# for the generative model (SAR 8 per million input tokens, SAR 24 per million output tokens). Count the
# classifier's cost as zero per report: it runs on a server the Ministry already has.

# %%
recorded = A.read_csv("options/recorded_generative_run.csv")


def compare(test: pd.DataFrame, pred, recorded: pd.DataFrame, ms_per_report: float) -> pd.DataFrame:
    # BEGIN SOLUTION
    gen_acc = float((recorded.predicted.values == test.category.values).mean())
    per_report = (recorded.in_tokens.mean() * 8.0 + recorded.out_tokens.mean() * 24.0) / 1e6
    return pd.DataFrame([
        {"approach": "classical classifier", "accuracy": round(float((pred == test.category).mean()), 3),
         "mean_latency_ms": round(ms_per_report, 3), "sar_per_month": 0.0},
        {"approach": "generative (recorded)", "accuracy": round(gen_acc, 3),
         "mean_latency_ms": round(float(recorded.latency_ms.mean()), 1),
         "sar_per_month": round(per_report * 95000, 2)},
    ])
    # END SOLUTION

# %%
try:
    result = compare(test, pred, recorded, ms_per_report)
except NotImplementedError:
    result = pd.DataFrame([{"approach": "classical classifier", "accuracy": round(classical_acc, 3)},
                           {"approach": "generative (recorded)",
                            "accuracy": round(float((recorded.predicted.values == test.category.values).mean()), 3)}])
    print("(using a reduced reference table)")
print(result.to_string(index=False))
A.check(result.accuracy.iloc[0] > result.accuracy.iloc[1], "the classifier is more accurate on these 600 reports")

# %% [markdown]
# 🔍 **Look at** the cost column. A few hundred riyals a month is not why the classifier wins: it wins on
# accuracy, on latency, and on a property the table does not show: it gives the same answer twice. The cost
# argument becomes real at the volume of all nine teams, and in Lab 2.2.
#
# The generative run is a synthetic recording: on a live free model your numbers would move. The method,
# same test set and same question for both, is the point.

# %% [markdown]
# ## ✱ Stretch · Errors by language
#
# Is the classifier as good in Arabic as in English? Compute accuracy by `lang` for both approaches.

# %%
def by_language() -> pd.DataFrame:
    # BEGIN SOLUTION
    t = test.assign(classical=pred == test.category, generative=recorded.predicted.values == test.category.values)
    return t.groupby("lang")[["classical", "generative"]].mean().round(3)
    # END SOLUTION


try:
    print(by_language())
except NotImplementedError:
    print("(stretch not done)")

# %% [markdown]
# ## Checkpoint
#
# 1. Which column of `needs.csv` most decides between `classical` and `retrieval`?
# 2. Why use the same 600 reports for both approaches?
# 3. Name one thing that would make the generative router the better choice.
#
# <details><summary>Answers</summary>
#
# 1. Labelled examples, with the shape of the output: a label from a fixed list against an answer with a citation.
# 2. Accuracy on different sets cannot be compared; the 3% labelling noise is the same for both on one set.
# 3. No labelled data, labels that change every month, or reports that need a reply drafted, not only a route.
# </details>
#
# **Carry forward.** The matched table is the "patterns" section of the options paper of the capstone.
