# ETL AI Automation: Execution Walkthrough & Demo

This guide walks through executing the sample dataset through the ETL pipeline, detailing input, transformation state, and final output.

---

## Sample Input Data

Raw records containing un-normalized strings, invalid contact details, and missing values:

```csv
Student_ID,Name,Email,Phone,Course,Fee_Paid,City,Enrolled_Date
STU1002,priya s,priya.s@yahoo.com,,ml,no,coimbatore,06-05-2025
STU1004,ANITHA R,anitha@gmail.com,9000011111,machine learning,no,chennai,05-04-2025
STU1006,deepa m,deepam@gmail.com,8123456789,data science,yes,salem,09-03-2025
STU1008,kavitha,kavitha99@gmail.com,9988776655,ml,yes,chennai,15-01-2025
STU1010,Nithya R,nithyar@yahoo.com,9765432109,data science,no,madurai,25-04-2025
```

---

## Transformation Trace

1. **`STU1002` (Priya S)**:
   - `Name`: `"priya s"` -> `"Priya S"`
   - `Course`: `"ml"` -> `"Machine Learning"`
   - `Phone`: Missing -> `"Invalid/Missing"`
   - `Email`: `priya.s@yahoo.com` -> Valid (`is_valid_email = True`)
   - **Filter Result**: Accepted (Valid Email).

2. **`STU1004` (Anitha R)**:
   - `Name`: `"ANITHA R"` -> `"Anitha R"`
   - `Course`: `"machine learning"` -> `"Machine Learning"`
   - `Fee_Paid`: `"No"`
   - `Email`: Valid (`is_valid_email = True`)
   - **Filter Result**: Accepted (Valid Email).

3. **`STU1006` (Deepa M)**:
   - `Fee_Paid`: `"Yes"`
   - `Email`: Valid (`is_valid_email = True`)
   - **Filter Result**: Accepted (Both conditions satisfied).

---

## Cleaned Output Data

The generated file matches the required schema:

```csv
Student_ID,Name,Email,Phone,Course,Fee_Paid,City,Enrolled_Date,is_valid_email
STU1002,Priya S,priya.s@yahoo.com,Invalid/Missing,Machine Learning,No,Coimbatore,06-05-2025,TRUE
STU1004,Anitha R,anitha@gmail.com,9000011111,Machine Learning,No,Chennai,05-04-2025,TRUE
STU1006,Deepa M,deepam@gmail.com,8123456789,Data Science,Yes,Salem,09-03-2025,TRUE
STU1008,Kavitha,kavitha99@gmail.com,9988776655,Machine Learning,Yes,Chennai,15-01-2025,TRUE
STU1010,Nithya R,nithyar@yahoo.com,9765432109,Data Science,No,Madurai,25-04-2025,TRUE
```

---

## Verifying the Pipeline
- **Validation accuracy**: 100% of emails tested against RFC regular expressions.
- **Normalization**: Zero un-capitalized or lowercase courses remained.
- **Binary Conversion**: Stream seamlessly exported back to binary CSV without manual intervention.
