from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = "swimming-checkin-feedback-system"

checkin_records = [
    {
        "student_name": "张明",
        "phone": "13800001111",
        "course_name": "游泳基础班",
        "checkin_time": "2026-04-09 08:30:00",
    },
    {
        "student_name": "李雪",
        "phone": "13900002222",
        "course_name": "蛙泳提高班",
        "checkin_time": "2026-04-09 09:05:00",
    },
]

feedback_records = [
    {
        "student_name": "王晨",
        "rating": "5",
        "feedback_text": "教练讲解清晰，签到流程也很方便。",
        "submit_time": "2026-04-09 10:10:00",
    },
    {
        "student_name": "赵宁",
        "rating": "4",
        "feedback_text": "整体体验不错，希望后续增加更详细的到馆路线说明。",
        "submit_time": "2026-04-09 10:20:00",
    },
]

coach_team = [
    {
        "name": "刘洋",
        "specialty": "少儿游泳启蒙、基础水性训练",
        "certification": "国家职业资格游泳教练证、少儿体适能指导证书",
        "intro": "拥有多年青少年教学经验，擅长帮助初学学员建立水中安全感与规范动作基础。",
    },
    {
        "name": "陈楠",
        "specialty": "蛙泳与自由泳提升、成人零基础教学",
        "certification": "中国游泳协会教练员证书、救生员资格证",
        "intro": "教学风格耐心细致，重视动作分解与节奏训练，适合成人学员循序渐进掌握泳姿。",
    },
    {
        "name": "孙悦",
        "specialty": "考试专项训练、体能与耐力提升",
        "certification": "高级游泳教练证、校园体育专项培训资质",
        "intro": "专注于应试与专项能力提升课程，可根据学员目标定制训练计划，提高学习效率。",
    },
]

booking_records = []


@app.route("/")
def index():
    return render_template("index.html", coach_team=coach_team)


@app.route("/checkin", methods=["GET", "POST"])
def checkin():
    success_message = None

    if request.method == "POST":
        student_name = request.form.get("student_name", "").strip()
        phone = request.form.get("phone", "").strip()
        course_name = request.form.get("course_name", "").strip()

        if student_name and phone and course_name:
            checkin_records.insert(
                0,
                {
                    "student_name": student_name,
                    "phone": phone,
                    "course_name": course_name,
                    "checkin_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                },
            )
            success_message = f"{student_name}，签到成功！"
        else:
            success_message = "请完整填写签到信息。"

    recent_checkins = checkin_records[:5]
    return render_template(
        "checkin.html",
        success_message=success_message,
        recent_checkins=recent_checkins,
    )


@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    success_message = None

    if request.method == "POST":
        student_name = request.form.get("student_name", "").strip()
        rating = request.form.get("rating", "").strip()
        feedback_text = request.form.get("feedback_text", "").strip()

        if student_name and rating and feedback_text:
            feedback_records.insert(
                0,
                {
                    "student_name": student_name,
                    "rating": rating,
                    "feedback_text": feedback_text,
                    "submit_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                },
            )
            success_message = "反馈提交成功，感谢您的意见！"
        else:
            success_message = "请完整填写反馈内容。"

    return render_template("feedback.html", success_message=success_message)


@app.route("/navigation")
def navigation():
    return render_template("navigation.html")


@app.route("/booking", methods=["GET", "POST"])
def booking():
    success_message = None

    if request.method == "POST":
        student_name = request.form.get("student_name", "").strip()
        phone = request.form.get("phone", "").strip()
        coach_name = request.form.get("coach_name", "").strip()
        class_type = request.form.get("class_type", "").strip()
        preferred_date = request.form.get("preferred_date", "").strip()
        preferred_time = request.form.get("preferred_time", "").strip()
        notes = request.form.get("notes", "").strip()

        if (
            student_name
            and phone
            and coach_name
            and class_type
            and preferred_date
            and preferred_time
        ):
            booking_records.insert(
                0,
                {
                    "student_name": student_name,
                    "phone": phone,
                    "coach_name": coach_name,
                    "class_type": class_type,
                    "preferred_date": preferred_date,
                    "preferred_time": preferred_time,
                    "notes": notes,
                    "submit_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                },
            )
            success_message = f"{student_name}，预约提交成功！我们会尽快与您确认课程安排。"
        else:
            success_message = "请完整填写预约信息。"

    return render_template(
        "booking.html",
        success_message=success_message,
        coach_team=coach_team,
    )


@app.route("/admin")
def admin():
    return render_template(
        "admin.html",
        checkin_records=checkin_records[:10],
        feedback_records=feedback_records[:10],
        booking_records=booking_records[:10],
    )


if __name__ == "__main__":
    app.run(debug=True)