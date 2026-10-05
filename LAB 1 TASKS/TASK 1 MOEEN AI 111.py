original_marks = float(input("Enter your original marks: "))
total_marks = float(input("Enter total marks: "))

percentage = original_marks * 100 / total_marks

if percentage >= 50:
    print("Percentage:", percentage)
    print("Pass")
else:
    print("Percentage:", percentage)
    print("Fail")