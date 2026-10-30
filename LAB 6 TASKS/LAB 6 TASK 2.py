
# Naive Bayes Assignment: Spam Email Classification

# Dataset
emails = [
    ("Yes", "Spam"),
    ("Yes", "Spam"),
    ("No", "Spam"),
    ("Yes", "Spam"),
    ("No", "Spam"),
    ("Yes", "Not Spam"),
    ("No", "Not Spam"),
    ("No", "Not Spam"),
    ("No", "Not Spam"),
    ("Yes", "Not Spam")
]

# Task 1: Count Spam and Not Spam emails
total_emails = len(emails)

spam_emails = [email for email in emails if email[1] == "Spam"]
not_spam_emails = [email for email in emails if email[1] == "Not Spam"]

spam_count = len(spam_emails)
not_spam_count = len(not_spam_emails)

print("TASK 1: Count Emails")
print("Total emails:", total_emails)
print("Spam emails:", spam_count)
print("Not Spam emails:", not_spam_count)

# Task 2: Calculate prior probabilities
p_spam = spam_count / total_emails
p_not_spam = not_spam_count / total_emails

print("\nTASK 2: Prior Probabilities")
print("P(Spam) =", p_spam)
print("P(Not Spam) =", p_not_spam)

# Task 3: P(Prize=Yes | Spam)
spam_prize_yes = sum(
    1 for email in spam_emails if email[0] == "Yes"
)

p_prize_yes_spam = spam_prize_yes / spam_count

print("\nTASK 3: P(Prize=Yes | Spam)")
print("Spam emails with Prize=Yes:", spam_prize_yes)
print("P(Prize=Yes | Spam) =", p_prize_yes_spam)

# Task 4: P(Prize=Yes | Not Spam)
not_spam_prize_yes = sum(
    1 for email in not_spam_emails if email[0] == "Yes"
)

p_prize_yes_not_spam = not_spam_prize_yes / not_spam_count

print("\nTASK 4: P(Prize=Yes | Not Spam)")
print("Not Spam emails with Prize=Yes:", not_spam_prize_yes)
print("P(Prize=Yes | Not Spam) =", p_prize_yes_not_spam)

# Task 5: Calculate Spam score
spam_score = p_spam * p_prize_yes_spam

print("\nTASK 5: Spam Score")
print("Spam score =", p_spam, "*", p_prize_yes_spam)
print("Spam score =", spam_score)

# Task 6: Calculate Not Spam score
not_spam_score = p_not_spam * p_prize_yes_not_spam

print("\nTASK 6: Not Spam Score")
print("Not Spam score =", p_not_spam, "*",
      p_prize_yes_not_spam)
print("Not Spam score =", not_spam_score)

# Task 7: Compare scores and predict class
print("\nTASK 7: Final Prediction")

if spam_score > not_spam_score:
    prediction = "Spam"
else:
    prediction = "Not Spam"

print("Spam score:", spam_score)
print("Not Spam score:", not_spam_score)
print("Predicted class:", prediction)

# Normalize scores into posterior probabilities
total_score = spam_score + not_spam_score

p_spam_given_prize = spam_score / total_score
p_not_spam_given_prize = not_spam_score / total_score

print("\nNormalized Probabilities")
print("P(Spam | Prize=Yes) =", p_spam_given_prize)
print("P(Not Spam | Prize=Yes) =", p_not_spam_given_prize)
