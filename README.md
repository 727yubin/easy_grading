# Exam Grading System

## Usage
1. Refer to the file `example_student_list.csv`, and fill in students' names, ID numbers, and emails.
2. `python frontend/generate_user_credentials.py` will create `frontend/user_credentials.csv`. 
**IMPORTANT**: manually add `TA_CS230,MySecurePasswd` to `frontend/user_credentials.csv`. This is the admin account.


3. When exam time comes, `python generate_answer_sheets.py example_student_list.csv 13`. The number is the number of pages that you wish to print.
4. Scan the images into `answer_sheet_scans/raw`. 
5. `cd answer_sheet_scans; python sort_scans.py raw/`.

6. Now we can start the server. 

`docker build . -t <name>`
`docker run -v ./:/easy_grading -p 8080:8080 -it yblee/easy_grading` 

Then in the docker container, run `waitress-serve app:app`. 

The site should be intuitive enough to use. 
Advice: In the user credentials CSV, remove the credentials for the students.
7. Once grading is over, open the server to the students, and they should be able to log in with their credentials, and see their grades.

---

Noto Sans font was used.
