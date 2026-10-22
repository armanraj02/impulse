import pandas as pd
import random
from faker import Faker
from datetime import date
import sys
sys.stdout.reconfigure(encoding='utf-8')

import random
Faker.seed(42)

fake = Faker("en_IN")

CURRENT_DATE = pd.Timestamp("2026-08-13")

ACADEMIC_START = pd.Timestamp("2026-01-01")
ACADEMIC_END = pd.Timestamp("2026-06-30")


# ============================================================
# 1. DEPARTMENTS
# ============================================================

departments = [
    [1, "CSE", "Computer Science and Engineering",
     "Dr. Rajesh Kumar", "rajesh.kumar@sahyadri.edu.in"],

    [2, "AIML", "Artificial Intelligence and Machine Learning",
     "Dr. Priya Sharma", "priya.sharma@sahyadri.edu.in"],

    [3, "ISE", "Information Science and Engineering",
     "Dr. Anil Rao", "anil.rao@sahyadri.edu.in"],

    [4, "ECE", "Electronics and Communication Engineering",
     "Dr. Meena Patel", "meena.patel@sahyadri.edu.in"],

    [5, "ME", "Mechanical Engineering",
     "Dr. Suresh Nair", "suresh.nair@sahyadri.edu.in"]
]

departments_df = pd.DataFrame(
    departments,
    columns=[
        "department_id",
        "department_code",
        "department_name",
        "hod_name",
        "hod_email"
    ]
)

print(departments_df)

# ============================================================
# 2. BRANCHES
# ============================================================

branches = [
    [1, "CSE", "Computer Science and Engineering", 1],
    [2, "AIML", "Artificial Intelligence and Machine Learning", 2],
    [3, "ISE", "Information Science and Engineering", 3],
    [4, "ECE", "Electronics and Communication Engineering", 4],
    [5, "ME", "Mechanical Engineering", 5]
]

branches_df = pd.DataFrame(
    branches,
    columns=[
        "branch_id",
        "branch_code",
        "branch_name",
        "department_id"
    ]
)

print(branches_df)

# ============================================================
# 3. BATCHES
# ============================================================

batches = [
    [1, "2021-2025", "2021-2022", 2],
    [2, "2022-2026", "2022-2023", 3],
    [3, "2023-2027", "2023-2024", 4],
    [4, "2024-2028", "2024-2025", 5],
    [5, "2025-2029", "2025-2026", 6],
    [6, "2026-2030", "2026-2027", 2]
]

batches_df = pd.DataFrame(
    batches,
    columns=[
        "batch_id",
        "batch_name",
        "academic_year",
        "semester"
    ]
)

print(batches_df)

# ============================================================
# 4. STUDENTS
# ============================================================

NUM_STUDENTS = 5000

students = []

branch_usn_codes = {
    1: "CS",
    2: "AI",
    3: "IS",
    4: "EC",
    5: "ME"
}

# Realistic distribution across batches
batch_weights = {
    1: 0.12,
    2: 0.15,
    3: 0.18,
    4: 0.20,
    5: 0.20,
    6: 0.15
}

batch_ids = list(batch_weights.keys())
batch_probs = list(batch_weights.values())

# DOB ranges
batch_birth_years = {
    1: (2002, 2004),
    2: (2003, 2005),
    3: (2004, 2006),
    4: (2005, 2007),
    5: (2006, 2008),
    6: (2007, 2009)
}

for student_id in range(1, NUM_STUDENTS + 1):

    # Branch
    branch_id = random.choices(
        [1, 2, 3, 4, 5],
        weights=[30, 25, 20, 15, 10],
        k=1
    )[0]

    # Batch
    batch_id = random.choices(
        batch_ids,
        weights=batch_probs,
        k=1
    )[0]

    student_name = fake.name()

    clean_name = (
        student_name
        .lower()
        .replace(" ", ".")
        .replace("'", "")
    )

    email = (
        f"{clean_name}.{student_id}"
        f"@sahyadri.edu.in"
    )

    # DOB
    min_year, max_year = batch_birth_years[batch_id]

    birth_year = random.randint(
        min_year,
        max_year
    )

    dob = date(
        birth_year,
        random.randint(1, 12),
        random.randint(1, 28)
    )

    # Batch starting year
    batch_start_year = int(
        batches_df.loc[
            batches_df["batch_id"] == batch_id,
            "batch_name"
        ].iloc[0][:4]
    )

    # USN
    usn = (
        f"4SF"
        f"{str(batch_start_year)[-2:]}"
        f"{branch_usn_codes[branch_id]}"
        f"{student_id:04d}"
    )

    gender = random.choices(
        ["Male", "Female"],
        weights=[55, 45],
        k=1
    )[0]

    students.append([
        student_id,
        usn,
        student_name,
        email,
        branch_id,
        batch_id,
        gender,
        dob
    ])


students_df = pd.DataFrame(
    students,
    columns=[
        "student_id",
        "usn",
        "student_name",
        "email",
        "branch_id",
        "batch_id",
        "gender",
        "date_of_birth"
    ]
)

print("Students:", len(students_df))

print(students_df.head(10))

# ============================================================
# 5. COURSES
# ============================================================

courses = [
    [1, "ROB101", "Robotics", 1, 2, 4],

    [2, "FS101", "Full Stack Development", 1, 3, 4],

    [3, "DE101", "Data Engineering", 3, 4, 4],

    [4, "AI101", "Artificial Intelligence", 2, 5, 4],

    [5, "EMB101", "Embedded Systems", 4, 6, 4],

    [6, "IOT101", "Internet of Things", 4, 6, 4]
]

courses_df = pd.DataFrame(
    courses,
    columns=[
        "course_id",
        "course_code",
        "course_name",
        "department_id",
        "semester",
        "credits"
    ]
)

print(courses_df)

# ============================================================
# 6. SECTIONS
# SEMESTER CONSISTENCY + FULL BRANCH COVERAGE
# ============================================================

sections = []

section_id = 1

# ------------------------------------------------------------
# IMPORTANT
#
# Every course can be offered to all branches in this
# synthetic dataset.
#
# The IMPORTANT restriction is semester:
#
# course.semester == batch.semester
#
# ------------------------------------------------------------

course_branch_map = {

    1: [1, 2, 3, 4, 5],   # Robotics - Semester 2

    2: [1, 2, 3, 4, 5],   # Full Stack - Semester 3

    3: [1, 2, 3, 4, 5],   # Data Engineering - Semester 4

    4: [1, 2, 3, 4, 5],   # AI - Semester 5

    5: [1, 2, 3, 4, 5],   # Embedded - Semester 6

    6: [1, 2, 3, 4, 5]    # IoT - Semester 6
}


for _, course in courses_df.iterrows():

    course_id = course["course_id"]

    course_semester = course["semester"]

    eligible_branches = course_branch_map[
        course_id
    ]

    # --------------------------------------------------------
    # CRITICAL:
    # Only batches having the SAME semester
    # --------------------------------------------------------

    valid_batches = batches_df[
        batches_df["semester"]
        ==
        course_semester
    ]

    for branch_id in eligible_branches:

        for _, batch in valid_batches.iterrows():

            batch_id = batch["batch_id"]

            academic_year = batch[
                "academic_year"
            ]

            for section_name in ["A", "B", "C"]:

                sections.append([
                    section_id,
                    section_name,
                    course_id,
                    branch_id,
                    batch_id,
                    academic_year
                ])

                section_id += 1


sections_df = pd.DataFrame(
    sections,
    columns=[
        "section_id",
        "section_name",
        "course_id",
        "branch_id",
        "batch_id",
        "academic_year"
    ]
)

print(
    "Total sections:",
    len(sections_df)
)

print(
    sections_df.head(10)
)

# ============================================================
# 7. INSTRUCTORS
# ============================================================

instructors = [
    [1, "Pulkit Garg",
     "pulkit.garg@sahyadri.edu.in", 1],

    [2, "Kashi Sharma",
     "kashi.sharma@sahyadri.edu.in", 1],

    [3, "Akshiljit Gigi",
     "akshiljit.gigi@sahyadri.edu.in", 1],

    [4, "Rushikesh Rajulwar",
     "rushikesh.rajulwar@sahyadri.edu.in", 3],

    [5, "Shiv Bhaskar",
     "shiv.bhaskar@sahyadri.edu.in", 2],

    [6, "Nischay",
     "nischay@sahyadri.edu.in", 2],

    [7, "Shrinivas Naik",
     "shrinivas.naik@sahyadri.edu.in", 1],

    [8, "Akshay Kumar",
     "akshay.kumar@sahyadri.edu.in", 1],

    [9, "KBC",
     "kbc@sahyadri.edu.in", 4],

    [10, "Vineet",
     "vineet@sahyadri.edu.in", 4]
]

instructors_df = pd.DataFrame(
    instructors,
    columns=[
        "instructor_id",
        "instructor_name",
        "email",
        "department_id"
    ]
)

print(instructors_df)

# ============================================================
# 8. INSTRUCTOR EXPERTISE
# HELPER DATAFRAME
# ============================================================

instructor_expertise = [
    [1, "Pulkit Garg", "Robotics"],

    [2, "Kashi Sharma", "Full Stack"],

    [3, "Akshiljit Gigi", "Robotics"],

    [4, "Rushikesh Rajulwar", "Data Engineering"],

    [5, "Shiv Bhaskar", "AI"],

    [6, "Nischay", "Data Engineering"],
    [6, "Nischay", "AI"],

    [7, "Shrinivas Naik", "Full Stack"],

    [8, "Akshay Kumar", "Full Stack"],

    [9, "KBC", "Embedded"],
    [9, "KBC", "IoT"],

    [10, "Vineet", "Embedded"],
    [10, "Vineet", "IoT"]
]

instructor_expertise_df = pd.DataFrame(
    instructor_expertise,
    columns=[
        "instructor_id",
        "instructor_name",
        "expertise"
    ]
)

print(instructor_expertise_df)

# ============================================================
# 9. ENROLLMENTS
# SEMESTER-CONSISTENT + 100% STUDENT COVERAGE
# ============================================================

enrollments = []

enrollment_id = 1


# ------------------------------------------------------------
# Create section lookup
# ------------------------------------------------------------

section_lookup = {}

for _, section in sections_df.iterrows():

    key = (
        section["course_id"],
        section["branch_id"],
        section["batch_id"]
    )

    section_lookup.setdefault(
        key,
        []
    ).append(
        section["section_id"]
    )


# ------------------------------------------------------------
# Generate enrollments
# ------------------------------------------------------------

for _, student in students_df.iterrows():

    student_id = student["student_id"]

    branch_id = student["branch_id"]

    batch_id = student["batch_id"]

    # --------------------------------------------------------
    # Get student's batch semester
    # --------------------------------------------------------

    student_semester = batches_df.loc[
        batches_df["batch_id"] == batch_id,
        "semester"
    ].iloc[0]


    # --------------------------------------------------------
    # ONLY courses belonging to student's semester
    # --------------------------------------------------------

    valid_courses = courses_df[
        courses_df["semester"]
        ==
        student_semester
    ]


    # --------------------------------------------------------
    # Find courses that actually have a section
    # for this student's branch + batch
    # --------------------------------------------------------

    available_courses = []

    for course_id in valid_courses[
        "course_id"
    ]:

        key = (
            course_id,
            branch_id,
            batch_id
        )

        if key in section_lookup:

            available_courses.append(
                course_id
            )


    # --------------------------------------------------------
    # SAFETY CHECK
    # Every student MUST have at least one course
    # --------------------------------------------------------

    if not available_courses:

        raise ValueError(
            f"No valid course found for "
            f"student_id={student_id}, "
            f"branch_id={branch_id}, "
            f"batch_id={batch_id}, "
            f"semester={student_semester}"
        )


    # --------------------------------------------------------
    # Select courses
    #
    # Since semester consistency is mandatory,
    # select only from available courses.
    # --------------------------------------------------------

    number_of_courses = random.randint(
        1,
        min(
            2,
            len(available_courses)
        )
    )

    selected_courses = random.sample(
        available_courses,
        number_of_courses
    )


    # --------------------------------------------------------
    # Create enrollment
    # --------------------------------------------------------

    for course_id in selected_courses:

        key = (
            course_id,
            branch_id,
            batch_id
        )

        section_id = random.choice(
            section_lookup[key]
        )

        enrollment_date = (
            ACADEMIC_START
            +
            pd.Timedelta(
                days=random.randint(
                    0,
                    14
                )
            )
        )

        status = random.choices(
            ["Active", "Completed"],
            weights=[80, 20],
            k=1
        )[0]

        enrollments.append([
            enrollment_id,
            student_id,
            course_id,
            section_id,
            enrollment_date.strftime(
                "%Y-%m-%d"
            ),
            status
        ])

        enrollment_id += 1


enrollments_df = pd.DataFrame(
    enrollments,
    columns=[
        "enrollment_id",
        "student_id",
        "course_id",
        "section_id",
        "enrollment_date",
        "status"
    ]
)


print(
    "Total enrollments:",
    len(enrollments_df)
)

print(
    "Unique enrolled students:",
    enrollments_df[
        "student_id"
    ].nunique()
)

print(
    enrollments_df.head(10)
)

# ============================================================
# 10. COURSE INSTRUCTORS
# ============================================================

course_instructor_map = {

    1: [1, 3],       # Robotics
    2: [2, 7, 8],    # Full Stack
    3: [4, 6],       # Data Engineering
    4: [5, 6],       # AI
    5: [9, 10],      # Embedded
    6: [9, 10]       # IoT
}

role_map = {
    1: "Robotics Instructor",
    2: "Full Stack Instructor",
    3: "Data Engineering Instructor",
    4: "AI Instructor",
    5: "Embedded Systems Instructor",
    6: "IoT Instructor"
}

course_instructors = []

course_instructor_id = 1


for course_id, instructor_ids in (
    course_instructor_map.items()
):

    course_sections = sections_df[
        sections_df["course_id"]
        ==
        course_id
    ]

    for _, section in course_sections.iterrows():

        section_id = section["section_id"]

        instructor_id = random.choice(
            instructor_ids
        )

        course_instructors.append([
            course_instructor_id,
            course_id,
            section_id,
            instructor_id,
            role_map[course_id]
        ])

        course_instructor_id += 1


course_instructors_df = pd.DataFrame(
    course_instructors,
    columns=[
        "course_instructor_id",
        "course_id",
        "section_id",
        "instructor_id",
        "role"
    ]
)

print(
    course_instructors_df.head(10)
)

# ============================================================
# 11. MODULES
# ============================================================

module_names = {

    1: [
        "Robotics Fundamentals",
        "Robot Kinematics",
        "Sensors and Actuators",
        "Robot Control",
        "Robotics Applications"
    ],

    2: [
        "HTML and CSS",
        "JavaScript",
        "Frontend Development",
        "Backend Development",
        "Full Stack Integration"
    ],

    3: [
        "Data Engineering Fundamentals",
        "ETL and ELT Pipelines",
        "Data Warehousing",
        "Data Lakes",
        "Pipeline Orchestration"
    ],

    4: [
        "AI Fundamentals",
        "Machine Learning",
        "Deep Learning",
        "Natural Language Processing",
        "AI Applications"
    ],

    5: [
        "Embedded Systems Fundamentals",
        "Microcontrollers",
        "Embedded Programming",
        "Embedded Communication",
        "Embedded Applications"
    ],

    6: [
        "IoT Fundamentals",
        "IoT Architecture",
        "Sensors and Connectivity",
        "IoT Communication",
        "IoT Applications"
    ]
}


modules = []

module_id = 1

total_days = (
    ACADEMIC_END
    -
    ACADEMIC_START
).days + 1

module_duration = total_days // 5


for course_id in courses_df[
    "course_id"
]:

    for module_order in range(1, 6):

        module_name = module_names[
            course_id
        ][module_order - 1]

        start_date = (
            ACADEMIC_START
            +
            pd.Timedelta(
                days=(
                    module_order - 1
                )
                *
                module_duration
            )
        )

        if module_order < 5:

            end_date = (
                start_date
                +
                pd.Timedelta(
                    days=module_duration - 1
                )
            )

        else:

            end_date = ACADEMIC_END

        modules.append([
            module_id,
            course_id,
            module_name,
            module_order,
            start_date.strftime(
                "%Y-%m-%d"
            ),
            end_date.strftime(
                "%Y-%m-%d"
            )
        ])

        module_id += 1


modules_df = pd.DataFrame(
    modules,
    columns=[
        "module_id",
        "course_id",
        "module_name",
        "module_order",
        "start_date",
        "end_date"
    ]
)

print(
    "Total modules:",
    len(modules_df)
)

print(modules_df.head(10))

# ============================================================
# 12. ASSESSMENTS
# ============================================================

assessment_pattern = [
    ("Quiz 1", "Quiz", 5),
    ("Quiz 2", "Quiz", 5),
    ("Assignment", "Assignment", 10),
    ("CIE", "CIE", 25),
    ("Assessment", "Assessment", 50)
]

assessments = []

assessment_id = 1


for _, module in modules_df.iterrows():

    start_date = pd.to_datetime(
        module["start_date"]
    )

    end_date = pd.to_datetime(
        module["end_date"]
    )

    assessment_dates = pd.date_range(
        start=start_date,
        end=end_date,
        periods=5
    )

    for i, (
        assessment_name,
        assessment_type,
        max_marks
    ) in enumerate(
        assessment_pattern
    ):

        assessments.append([
            assessment_id,
            module["course_id"],
            module["module_id"],
            assessment_name,
            assessment_type,
            max_marks,
            assessment_dates[i].strftime(
                "%Y-%m-%d"
            )
        ])

        assessment_id += 1


assessments_df = pd.DataFrame(
    assessments,
    columns=[
        "assessment_id",
        "course_id",
        "module_id",
        "assessment_name",
        "assessment_type",
        "max_marks",
        "assessment_date"
    ]
)

print(
    "Total assessments:",
    len(assessments_df)
)

print(
    assessments_df.head(10)
)

# ============================================================
# 13. ASSESSMENT SCORES
# ============================================================

assessment_scores = []

score_id = 1


student_profiles = {}

for student_id in students_df[
    "student_id"
]:

    student_profiles[
        student_id
    ] = random.choices(
        ["High", "Medium", "Low"],
        weights=[25, 55, 20],
        k=1
    )[0]


# Only assessments belonging to student's enrolled courses
for _, enrollment in enrollments_df.iterrows():

    student_id = enrollment["student_id"]
    course_id = enrollment["course_id"]

    course_assessments = assessments_df[
        assessments_df["course_id"]
        ==
        course_id
    ]

    profile = student_profiles[
        student_id
    ]

    for _, assessment in (
        course_assessments.iterrows()
    ):

        max_marks = assessment[
            "max_marks"
        ]

        submitted = (
            random.random() > 0.05
        )

        # NOT SUBMITTED
        if not submitted:

            marks_obtained = None
            graded = False

        else:

            graded = (
                random.random() > 0.10
            )

            # SUBMITTED BUT NOT GRADED
            if not graded:

                marks_obtained = None

            else:

                if profile == "High":

                    percentage = random.uniform(
                        0.75,
                        0.98
                    )

                elif profile == "Medium":

                    percentage = random.uniform(
                        0.55,
                        0.80
                    )

                else:

                    percentage = random.uniform(
                        0.30,
                        0.60
                    )

                marks_obtained = round(
                    max_marks * percentage,
                    2
                )

        assessment_scores.append([
            score_id,
            assessment["assessment_id"],
            student_id,
            marks_obtained,
            submitted,
            graded
        ])

        score_id += 1


assessment_scores_df = pd.DataFrame(
    assessment_scores,
    columns=[
        "score_id",
        "assessment_id",
        "student_id",
        "marks_obtained",
        "submitted",
        "graded"
    ]
)

print(
    assessment_scores_df.head(10)
)

# ============================================================
# 14. ATTENDANCE
# ============================================================

attendance = []

attendance_id = 1


for _, enrollment in enrollments_df.iterrows():

    student_id = enrollment["student_id"]
    course_id = enrollment["course_id"]
    section_id = enrollment["section_id"]

    course_modules = modules_df[
        modules_df["course_id"]
        ==
        course_id
    ]

    start_date = pd.to_datetime(
        course_modules["start_date"].min()
    )

    end_date = pd.to_datetime(
        course_modules["end_date"].max()
    )

    class_dates = pd.date_range(
        start=start_date,
        end=end_date,
        freq="2D"
    )

    profile = student_profiles[
        student_id
    ]

    for attendance_date in class_dates:

        if profile == "High":

            status = random.choices(
                ["Present", "Absent"],
                weights=[95, 5],
                k=1
            )[0]

        elif profile == "Medium":

            status = random.choices(
                ["Present", "Absent"],
                weights=[85, 15],
                k=1
            )[0]

        else:

            status = random.choices(
                ["Present", "Absent"],
                weights=[65, 35],
                k=1
            )[0]

        attendance.append([
            attendance_id,
            student_id,
            course_id,
            section_id,
            attendance_date.strftime(
                "%Y-%m-%d"
            ),
            status
        ])

        attendance_id += 1


attendance_df = pd.DataFrame(
    attendance,
    columns=[
        "attendance_id",
        "student_id",
        "course_id",
        "section_id",
        "attendance_date",
        "status"
    ]
)

print(
    attendance_df.head(10)
)

# ============================================================
# 15. FEEDBACK FORMS
# ============================================================

feedback_forms = []

feedback_form_id = 1


for _, module in modules_df.iterrows():

    course_id = module["course_id"]
    module_id = module["module_id"]

    course_sections = sections_df[
        sections_df["course_id"]
        ==
        course_id
    ]

    for _, section in course_sections.iterrows():

        section_id = section[
            "section_id"
        ]

        # Find assigned instructor
        assigned = (
            course_instructors_df[
                course_instructors_df[
                    "section_id"
                ]
                ==
                section_id
            ]
        )

        if assigned.empty:
            continue

        instructor_id = assigned.iloc[0][
            "instructor_id"
        ]

        feedback_forms.append([
            feedback_form_id,
            course_id,
            module_id,
            section_id,
            instructor_id,
            module["end_date"],
            "Module Feedback"
        ])

        feedback_form_id += 1


feedback_forms_df = pd.DataFrame(
    feedback_forms,
    columns=[
        "feedback_form_id",
        "course_id",
        "module_id",
        "section_id",
        "instructor_id",
        "feedback_date",
        "feedback_type"
    ]
)

print(
    "Feedback forms:",
    len(feedback_forms_df)
)

print(
    feedback_forms_df.head(10)
)

# ============================================================
# 16. FEEDBACK QUESTIONS
# ============================================================

feedback_question_templates = [

    (
        "How would you rate the facilitator for today's session?",
        "Rating",
        True
    ),

    (
        "Why did you give this rating? Please provide a brief explanation for your rating.",
        "Text",
        True
    ),

    (
        "How would you rate your overall experience for today's session?",
        "Rating",
        True
    ),

    (
        "Why did you give this rating? Please provide a brief explanation for your rating.",
        "Text",
        True
    ),

    (
        "If you have any feedback or suggestions, please share them with us",
        "Text",
        False
    ),

    (
        "Trainers (Optional)",
        "Text",
        False
    )
]


feedback_questions = []

question_id = 1


for _, form in feedback_forms_df.iterrows():

    for display_order, (
        question_text,
        question_type,
        is_required
    ) in enumerate(
        feedback_question_templates,
        start=1
    ):

        feedback_questions.append([
            question_id,
            form["feedback_form_id"],
            question_text,
            question_type,
            is_required,
            display_order
        ])

        question_id += 1


feedback_questions_df = pd.DataFrame(
    feedback_questions,
    columns=[
        "question_id",
        "feedback_form_id",
        "question_text",
        "question_type",
        "is_required",
        "display_order"
    ]
)

print(
    feedback_questions_df.head(10)
)

# ============================================================
# 17. FEEDBACK RESPONSES
# ============================================================

feedback_responses = []

response_id = 1


# ------------------------------------------------------------
# Eligible students
# ------------------------------------------------------------

eligible_students = enrollments_df.merge(
    feedback_forms_df[
        [
            "feedback_form_id",
            "course_id",
            "section_id"
        ]
    ],
    on=[
        "course_id",
        "section_id"
    ],
    how="inner"
)


response_rate_options = [
    0.65,
    0.75,
    0.85,
    0.95
]


for feedback_form_id, group in (
    eligible_students.groupby(
        "feedback_form_id"
    )
):

    eligible_student_ids = (
        group[
            "student_id"
        ]
        .drop_duplicates()
        .tolist()
    )

    total_eligible = len(
        eligible_student_ids
    )

    if total_eligible == 0:
        continue

    response_rate = random.choice(
        response_rate_options
    )

    number_of_respondents = max(
        1,
        round(
            total_eligible
            *
            response_rate
        )
    )

    number_of_respondents = min(
        number_of_respondents,
        total_eligible
    )

    responding_students = random.sample(
        eligible_student_ids,
        number_of_respondents
    )

    form_questions = (
        feedback_questions_df[
            feedback_questions_df[
                "feedback_form_id"
            ]
            ==
            feedback_form_id
        ]
    )

    feedback_date = pd.to_datetime(
        feedback_forms_df.loc[
            feedback_forms_df[
                "feedback_form_id"
            ]
            ==
            feedback_form_id,
            "feedback_date"
        ].iloc[0]
    )

    for student_id in responding_students:

        submitted_at = (
            feedback_date
            +
            pd.Timedelta(
                hours=random.randint(9, 17),
                minutes=random.randint(0, 59)
            )
        )

        for _, question in (
            form_questions.iterrows()
        ):

            question_text = question[
                "question_text"
            ]

            question_type = question[
                "question_type"
            ]

            if question_type == "Rating":

                score = random.choices(
                    [1, 2, 3, 4, 5],
                    weights=[
                        2,
                        5,
                        15,
                        40,
                        38
                    ],
                    k=1
                )[0]

                answer_text = {
                    1: "Poor",
                    2: "Below Average",
                    3: "Good",
                    4: "Very Good",
                    5: "Excellent"
                }[score]

            else:

                score = None

                if "Trainers" in question_text:

                    answer_text = random.choice([
                        "Pulkit Garg",
                        "Kashi Sharma",
                        "Akshiljit Gigi",
                        "Rushikesh Rajulwar",
                        "Shiv Bhaskar",
                        "Nischay",
                        "Shrinivas Naik",
                        "Akshay Kumar",
                        "KBC",
                        "Vineet"
                    ])

                elif (
                    "Why did you give this rating"
                    in question_text
                ):

                    answer_text = random.choice([
                        "The facilitator explained the concepts clearly.",
                        "The session was interactive and easy to understand.",
                        "The examples were practical and useful.",
                        "The trainer answered questions effectively.",
                        "The session was informative and well structured.",
                        "More practical examples would make the session better."
                    ])

                else:

                    answer_text = random.choice([
                        "The session was very useful.",
                        "The content was clear and easy to understand.",
                        "The session was interactive and informative.",
                        "More practical examples would be helpful.",
                        "More hands-on activities would be useful.",
                        "The pace of the session was good."
                    ])

            feedback_responses.append([
                response_id,
                feedback_form_id,
                question["question_id"],
                student_id,
                answer_text,
                score,
                submitted_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            ])

            response_id += 1


feedback_responses_df = pd.DataFrame(
    feedback_responses,
    columns=[
        "response_id",
        "feedback_form_id",
        "question_id",
        "student_id",
        "answer_text",
        "score",
        "submitted_at"
    ]
)

print(
    "Feedback responses:",
    len(feedback_responses_df)
)

print(
    feedback_responses_df.head(10)
)

# ============================================================
# SEMESTER CONSISTENCY VALIDATION
# ============================================================

print("=" * 80)
print("SEMESTER CONSISTENCY VALIDATION")
print("=" * 80)


# ------------------------------------------------------------
# SECTION → COURSE → BATCH
# ------------------------------------------------------------

section_check = (
    sections_df
    .merge(
        courses_df[
            [
                "course_id",
                "semester"
            ]
        ],
        on="course_id",
        how="left"
    )
    .merge(
        batches_df[
            [
                "batch_id",
                "semester"
            ]
        ],
        on="batch_id",
        how="left",
        suffixes=(
            "_course",
            "_batch"
        )
    )
)


section_invalid = (
    section_check[
        "semester_course"
    ]
    !=
    section_check[
        "semester_batch"
    ]
)


print(
    "Invalid sections:",
    section_invalid.sum()
)

assert section_invalid.sum() == 0


# ------------------------------------------------------------
# ENROLLMENT → STUDENT BATCH → COURSE
# ------------------------------------------------------------

enrollment_check = (
    enrollments_df
    .merge(
        students_df[
            [
                "student_id",
                "batch_id"
            ]
        ],
        on="student_id",
        how="left"
    )
    .merge(
        batches_df[
            [
                "batch_id",
                "semester"
            ]
        ],
        on="batch_id",
        how="left"
    )
    .merge(
        courses_df[
            [
                "course_id",
                "semester"
            ]
        ],
        on="course_id",
        how="left",
        suffixes=(
            "_batch",
            "_course"
        )
    )
)


enrollment_invalid = (
    enrollment_check[
        "semester_batch"
    ]
    !=
    enrollment_check[
        "semester_course"
    ]
)


print(
    "Invalid enrollments:",
    enrollment_invalid.sum()
)

assert enrollment_invalid.sum() == 0


print()
print("SEMESTER CONSISTENCY PASSED")
print("Every section matches its course and batch semester.")
print("Every enrollment matches the student's batch semester.")

# ============================================================
# COMPLETE FOREIGN KEY VALIDATION
# ============================================================

print("=" * 80)
print("FOREIGN KEY VALIDATION")
print("=" * 80)


checks = {

    "branches → departments":
        branches_df["department_id"].isin(
            departments_df["department_id"]
        ).all(),

    "courses → departments":
        courses_df["department_id"].isin(
            departments_df["department_id"]
        ).all(),

    "instructors → departments":
        instructors_df["department_id"].isin(
            departments_df["department_id"]
        ).all(),

    "students → branches":
        students_df["branch_id"].isin(
            branches_df["branch_id"]
        ).all(),

    "students → batches":
        students_df["batch_id"].isin(
            batches_df["batch_id"]
        ).all(),

    "sections → courses":
        sections_df["course_id"].isin(
            courses_df["course_id"]
        ).all(),

    "sections → branches":
        sections_df["branch_id"].isin(
            branches_df["branch_id"]
        ).all(),

    "sections → batches":
        sections_df["batch_id"].isin(
            batches_df["batch_id"]
        ).all(),

    "enrollments → students":
        enrollments_df["student_id"].isin(
            students_df["student_id"]
        ).all(),

    "enrollments → courses":
        enrollments_df["course_id"].isin(
            courses_df["course_id"]
        ).all(),

    "enrollments → sections":
        enrollments_df["section_id"].isin(
            sections_df["section_id"]
        ).all(),

    "modules → courses":
        modules_df["course_id"].isin(
            courses_df["course_id"]
        ).all(),

    "assessments → courses":
        assessments_df["course_id"].isin(
            courses_df["course_id"]
        ).all(),

    "assessments → modules":
        assessments_df["module_id"].isin(
            modules_df["module_id"]
        ).all(),

    "scores → assessments":
        assessment_scores_df["assessment_id"].isin(
            assessments_df["assessment_id"]
        ).all(),

    "scores → students":
        assessment_scores_df["student_id"].isin(
            students_df["student_id"]
        ).all(),

    "attendance → students":
        attendance_df["student_id"].isin(
            students_df["student_id"]
        ).all(),

    "attendance → courses":
        attendance_df["course_id"].isin(
            courses_df["course_id"]
        ).all(),

    "attendance → sections":
        attendance_df["section_id"].isin(
            sections_df["section_id"]
        ).all(),

    "course_instructors → courses":
        course_instructors_df["course_id"].isin(
            courses_df["course_id"]
        ).all(),

    "course_instructors → sections":
        course_instructors_df["section_id"].isin(
            sections_df["section_id"]
        ).all(),

    "course_instructors → instructors":
        course_instructors_df["instructor_id"].isin(
            instructors_df["instructor_id"]
        ).all(),

    "feedback_forms → courses":
        feedback_forms_df["course_id"].isin(
            courses_df["course_id"]
        ).all(),

    "feedback_forms → modules":
        feedback_forms_df["module_id"].isin(
            modules_df["module_id"]
        ).all(),

    "feedback_forms → sections":
        feedback_forms_df["section_id"].isin(
            sections_df["section_id"]
        ).all(),

    "feedback_forms → instructors":
        feedback_forms_df["instructor_id"].isin(
            instructors_df["instructor_id"]
        ).all(),

    "feedback_questions → forms":
        feedback_questions_df["feedback_form_id"].isin(
            feedback_forms_df["feedback_form_id"]
        ).all(),

    "responses → forms":
        feedback_responses_df["feedback_form_id"].isin(
            feedback_forms_df["feedback_form_id"]
        ).all(),

    "responses → questions":
        feedback_responses_df["question_id"].isin(
            feedback_questions_df["question_id"]
        ).all(),

    "responses → students":
        feedback_responses_df["student_id"].isin(
            students_df["student_id"]
        ).all()
}


for relationship, result in checks.items():

    print(
        f"{'' if result else '❌'} {relationship}"
    )

    assert result


print()
print(" ALL FOREIGN-KEY RELATIONSHIPS ARE VALID")

# ============================================================
# FINAL DATA QUALITY CHECK
# ============================================================

print("=" * 80)
print("FINAL DATA QUALITY CHECK")
print("=" * 80)


# Students
assert len(students_df) == 5000
assert students_df["student_id"].is_unique
assert students_df["usn"].is_unique
assert students_df["email"].is_unique


# Batches
assert len(batches_df) == 6
assert batches_df["semester"].isin(
    [2, 3, 4, 5, 6]
).all()


# Modules
module_counts = (
    modules_df
    .groupby("course_id")
    .size()
)

assert (module_counts == 5).all()


# Assessments
assessment_counts = (
    assessments_df
    .groupby("module_id")
    .size()
)

assert (assessment_counts == 5).all()


# Assessment marks
assert assessments_df[
    "max_marks"
].isin(
    [5, 10, 25, 50]
).all()


# Ungraded cannot have marks
assert not (
    (
        assessment_scores_df["graded"]
        == False
    )
    &
    (
        assessment_scores_df[
            "marks_obtained"
        ].notna()
    )
).any()


# Not submitted cannot have marks
assert not (
    (
        assessment_scores_df[
            "submitted"
        ]
        == False
    )
    &
    (
        assessment_scores_df[
            "marks_obtained"
        ].notna()
    )
).any()


# Graded must have marks
assert not (
    (
        assessment_scores_df[
            "graded"
        ]
        == True
    )
    &
    (
        assessment_scores_df[
            "marks_obtained"
        ].isna()
    )
).any()


# Dates
modules_df["start_date"] = pd.to_datetime(
    modules_df["start_date"]
)

modules_df["end_date"] = pd.to_datetime(
    modules_df["end_date"]
)

assessments_df["assessment_date"] = pd.to_datetime(
    assessments_df["assessment_date"]
)

feedback_forms_df["feedback_date"] = pd.to_datetime(
    feedback_forms_df["feedback_date"]
)


assert (
    modules_df["end_date"]
    <= CURRENT_DATE
).all()

assert (
    assessments_df["assessment_date"]
    <= CURRENT_DATE
).all()

assert (
    feedback_forms_df["feedback_date"]
    <= CURRENT_DATE
).all()


# Feedback: 6 questions per form
question_counts = (
    feedback_questions_df
    .groupby("feedback_form_id")
    .size()
)

assert (question_counts == 6).all()


# Feedback: 5 modules per course
feedback_modules = (
    feedback_forms_df
    .groupby("course_id")[
        "module_id"
    ]
    .nunique()
)

assert (feedback_modules == 5).all()


# Every student should have enrollment
students_with_enrollment = (
    enrollments_df[
        "student_id"
    ].nunique()
)

assert students_with_enrollment == 5000


print()
print("=" * 80)
print("ALL DATA QUALITY CHECKS PASSED")
print("=" * 80)

# ============================================================
# PRINT 10 ROWS FROM ALL TABLES
# ============================================================

tables = {
    "departments": departments_df,
    "branches": branches_df,
    "batches": batches_df,
    "students": students_df,
    "courses": courses_df,
    "sections": sections_df,
    "instructors": instructors_df,
    "enrollments": enrollments_df,
    "course_instructors": course_instructors_df,
    "modules": modules_df,
    "assessments": assessments_df,
    "assessment_scores": assessment_scores_df,
    "attendance": attendance_df,
    "feedback_forms": feedback_forms_df,
    "feedback_questions": feedback_questions_df,
    "feedback_responses": feedback_responses_df
}


import os
os.makedirs('csv_outputs', exist_ok=True)
for table_name, df in tables.items():
    print(f'Saving {table_name}.csv...')
    df.to_csv(f'csv_outputs/{table_name}.csv', index=False)
print('Done saving CSVs!')
