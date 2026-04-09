from flask import Flask, render_template, request, redirect, url_for
import random
import string

app = Flask(__name__)

brand = {
    "name": "Aureon Motors",
    "hero_title": "A New Era of Electric Luxury",
    "hero_subtitle": "Performance, intelligence, and design without compromise"
}

trim_prices = {
    "Core": 0,
    "Touring": 8500,
    "Signature": 18000
}

color_prices = {
    "Pearl White": 0,
    "Graphite": 1200,
    "Midnight Blue": 1600,
    "Aurora Red": 2200
}

wheel_prices = {
    "19-inch": 0,
    "21-inch": 2800
}

interior_prices = {
    "Light": 0,
    "Dark": 1200,
    "Performance": 3200
}

battery_prices = {
    "Standard Range": 0,
    "Long Range": 9500
}

addon_prices = {
    "Driver Assist Pack": 4200,
    "Premium Audio": 2600,
    "Winter Package": 1800
}

models_data = {
    "aureon-s": {
        "name": "Aureon S",
        "slug": "aureon-s",
        "tagline": "Executive electric sedan crafted for refined long-distance travel.",
        "positioning": "Elegant, intelligent, and supremely balanced—Aureon S delivers flagship serenity with instant electric performance.",
        "starting_price": 689000,
        "range": "710 km",
        "acceleration": "3.9 s",
        "top_speed": "230 km/h",
        "seating": "5",
        "drive_type": "Dual Motor AWD",
        "highlights": [
            "Panoramic glass architecture with active tint control",
            "Aureon OS cockpit with ambient intelligence interface",
            "Adaptive air suspension tuned for executive comfort",
            "Ultra-quiet cabin with sustainable premium materials"
        ],
        "spec_summary": {
            "Battery": "98 kWh",
            "Power": "520 hp",
            "Charging": "10-80% in 24 minutes",
            "Platform": "800V luxury EV architecture"
        },
        "image_label": "Aureon S Gallery"
    },
    "aureon-x": {
        "name": "Aureon X",
        "slug": "aureon-x",
        "tagline": "A sculpted luxury electric SUV for family, exploration, and presence.",
        "positioning": "Aureon X combines elevated versatility with grand touring comfort and commanding all-weather confidence.",
        "starting_price": 759000,
        "range": "680 km",
        "acceleration": "4.4 s",
        "top_speed": "220 km/h",
        "seating": "5-7",
        "drive_type": "Dual Motor AWD",
        "highlights": [
            "Expansive cabin with configurable executive rear space",
            "Terrain-adaptive drive intelligence for all-season capability",
            "Active matrix lighting with signature Aureon light blade",
            "High-capacity thermal management for repeat fast charging"
        ],
        "spec_summary": {
            "Battery": "105 kWh",
            "Power": "560 hp",
            "Charging": "10-80% in 26 minutes",
            "Platform": "Adaptive luxury SUV architecture"
        },
        "image_label": "Aureon X Gallery"
    },
    "aureon-gt": {
        "name": "Aureon GT",
        "slug": "aureon-gt",
        "tagline": "A grand touring performance EV with uncompromising response and drama.",
        "positioning": "Aureon GT is designed for those who want electric exhilaration, precision, and iconic road presence.",
        "starting_price": 899000,
        "range": "620 km",
        "acceleration": "2.9 s",
        "top_speed": "268 km/h",
        "seating": "4",
        "drive_type": "Tri-Motor Performance AWD",
        "highlights": [
            "Tri-motor performance vectoring for extreme agility",
            "Track-ready thermal systems with repeat launch consistency",
            "Low-slung aerodynamic bodywork and carbon detailing",
            "Performance cockpit with immersive driver-centric display"
        ],
        "spec_summary": {
            "Battery": "112 kWh",
            "Power": "780 hp",
            "Charging": "10-80% in 22 minutes",
            "Platform": "Performance GT architecture"
        },
        "image_label": "Aureon GT Gallery"
    }
}

orders_data = [
    {"order_id": "AM-24001", "customer": "Liam Chen", "model": "Aureon S", "trim": "Signature", "status": "Processing", "estimated_delivery": "2026-05-18", "total": "¥796,800"},
    {"order_id": "AM-24002", "customer": "Sophia Wang", "model": "Aureon X", "trim": "Touring", "status": "Confirmed", "estimated_delivery": "2026-04-30", "total": "¥789,500"},
    {"order_id": "AM-24003", "customer": "Ethan Zhao", "model": "Aureon GT", "trim": "Signature", "status": "In Production", "estimated_delivery": "2026-06-12", "total": "¥946,300"},
    {"order_id": "AM-24004", "customer": "Olivia Liu", "model": "Aureon S", "trim": "Core", "status": "Delivered", "estimated_delivery": "2026-03-08", "total": "¥689,000"},
    {"order_id": "AM-24005", "customer": "Noah Xu", "model": "Aureon X", "trim": "Signature", "status": "Processing", "estimated_delivery": "2026-06-01", "total": "¥823,400"},
    {"order_id": "AM-24006", "customer": "Emma Sun", "model": "Aureon GT", "trim": "Touring", "status": "Confirmed", "estimated_delivery": "2026-05-27", "total": "¥922,100"},
    {"order_id": "AM-24007", "customer": "Lucas He", "model": "Aureon S", "trim": "Touring", "status": "In Production", "estimated_delivery": "2026-05-09", "total": "¥721,700"},
    {"order_id": "AM-24008", "customer": "Ava Gao", "model": "Aureon X", "trim": "Core", "status": "Delivered", "estimated_delivery": "2026-02-21", "total": "¥759,000"},
    {"order_id": "AM-24009", "customer": "Mason Tang", "model": "Aureon GT", "trim": "Signature", "status": "Processing", "estimated_delivery": "2026-06-25", "total": "¥958,900"},
    {"order_id": "AM-24010", "customer": "Isabella Qian", "model": "Aureon S", "trim": "Signature", "status": "Confirmed", "estimated_delivery": "2026-05-15", "total": "¥804,200"},
    {"order_id": "AM-24011", "customer": "James Lin", "model": "Aureon X", "trim": "Touring", "status": "In Production", "estimated_delivery": "2026-06-04", "total": "¥801,600"}
]

test_drive_data = [
    {"customer": "Liam Chen", "model": "Aureon S", "date": "2026-04-12", "location": "Shanghai Studio", "status": "Confirmed"},
    {"customer": "Sophia Wang", "model": "Aureon X", "date": "2026-04-14", "location": "Beijing Experience Center", "status": "Pending"},
    {"customer": "Ethan Zhao", "model": "Aureon GT", "date": "2026-04-15", "location": "Shenzhen Gallery", "status": "Confirmed"},
    {"customer": "Olivia Liu", "model": "Aureon S", "date": "2026-04-18", "location": "Hangzhou Studio", "status": "Completed"},
    {"customer": "Noah Xu", "model": "Aureon X", "date": "2026-04-19", "location": "Guangzhou Studio", "status": "Pending"},
    {"customer": "Emma Sun", "model": "Aureon GT", "date": "2026-04-21", "location": "Chengdu Experience Center", "status": "Confirmed"},
    {"customer": "Lucas He", "model": "Aureon S", "date": "2026-04-22", "location": "Nanjing Studio", "status": "Pending"},
    {"customer": "Ava Gao", "model": "Aureon X", "date": "2026-04-24", "location": "Shanghai Studio", "status": "Completed"}
]

customer_data = [
    {"name": "Liam Chen", "email": "liam.chen@example.com", "city": "Shanghai", "orders_count": 2, "last_activity": "2 hours ago"},
    {"name": "Sophia Wang", "email": "sophia.wang@example.com", "city": "Beijing", "orders_count": 1, "last_activity": "5 hours ago"},
    {"name": "Ethan Zhao", "email": "ethan.zhao@example.com", "city": "Shenzhen", "orders_count": 3, "last_activity": "1 day ago"},
    {"name": "Olivia Liu", "email": "olivia.liu@example.com", "city": "Hangzhou", "orders_count": 1, "last_activity": "3 days ago"},
    {"name": "Noah Xu", "email": "noah.xu@example.com", "city": "Guangzhou", "orders_count": 2, "last_activity": "4 hours ago"},
    {"name": "Emma Sun", "email": "emma.sun@example.com", "city": "Chengdu", "orders_count": 1, "last_activity": "6 hours ago"},
    {"name": "Lucas He", "email": "lucas.he@example.com", "city": "Nanjing", "orders_count": 1, "last_activity": "8 hours ago"},
    {"name": "Ava Gao", "email": "ava.gao@example.com", "city": "Shanghai", "orders_count": 2, "last_activity": "1 hour ago"}
]

faq_data = [
    {"q": "交付时间一般多久？", "a": "大多数新车订单会在 6-12 周内完成交付，具体会根据车型、配置与所在城市资源进行动态安排。"},
    {"q": "如何为 Aureon 车辆充电？", "a": "您可通过家庭充电桩、公共 AC 充电桩以及 Aureon 高功率直流快充网络进行补能。"},
    {"q": "车辆保修政策是什么？", "a": "整车提供 4 年或 100,000 公里保修，高压电池与核心电驱系统提供 8 年或 160,000 公里保修。"},
    {"q": "可以预约试驾吗？", "a": "可以。您可通过官网试驾预约页面提交信息，我们的顾问会尽快与您确认时间与地点。"},
    {"q": "订单可以取消或退款吗？", "a": "在车辆进入生产排期前，订单通常可申请取消。相关订金退还规则会依据订单阶段与当地政策执行。"},
    {"q": "支持哪些支付方式？", "a": "支持全款、金融分期及企业采购方案。订单确认页可填写您的支付偏好以便顾问后续跟进。"},
    {"q": "软件系统会持续升级吗？", "a": "会。Aureon 车辆支持 OTA 远程升级，持续带来功能优化、性能调校及体验更新。"},
    {"q": "售后服务网络覆盖如何？", "a": "Aureon 正在核心城市布局服务与交付网络，并提供精选移动服务能力，提升高端用户服务效率。"}
]

def calculate_total(slug, trim, color, wheels, interior, battery, addons):
    model = models_data.get(slug)
    if not model:
        return 0
    total = model["starting_price"]
    total += trim_prices.get(trim, 0)
    total += color_prices.get(color, 0)
    total += wheel_prices.get(wheels, 0)
    total += interior_prices.get(interior, 0)
    total += battery_prices.get(battery, 0)
    for addon in addons:
        total += addon_prices.get(addon, 0)
    return total

def fmt_currency(value):
    return f"¥{value:,.0f}"

def generate_order_ref():
    return "AUR-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

@app.context_processor
def inject_globals():
    return {
        "brand": brand,
        "models_nav": list(models_data.values())
    }

@app.route("/")
def index():
    featured_models = list(models_data.values())
    return render_template("index.html", featured_models=featured_models)

@app.route("/models")
def models():
    return render_template("models.html", models=list(models_data.values()))

@app.route("/model/<slug>")
def model_detail(slug):
    model = models_data.get(slug)
    if not model:
        return redirect(url_for("models"))
    return render_template("model_detail.html", model=model)

@app.route("/compare")
def compare():
    return render_template("compare.html", models=list(models_data.values()))

@app.route("/configure/<slug>")
def configure(slug):
    model = models_data.get(slug)
    if not model:
        return redirect(url_for("models"))
    return render_template(
        "configure.html",
        model=model,
        trims=trim_prices,
        colors=color_prices,
        wheels=wheel_prices,
        interiors=interior_prices,
        batteries=battery_prices,
        addons=addon_prices
    )

@app.route("/order/review", methods=["GET", "POST"])
def order_review():
    errors = []
    summary = {
        "slug": request.values.get("slug", "aureon-s"),
        "trim": request.values.get("trim", "Core"),
        "color": request.values.get("color", "Pearl White"),
        "wheels": request.values.get("wheels", "19-inch"),
        "interior": request.values.get("interior", "Light"),
        "battery": request.values.get("battery", "Standard Range"),
        "addons": request.values.getlist("addons")
    }

    model = models_data.get(summary["slug"], models_data["aureon-s"])
    total = calculate_total(
        summary["slug"],
        summary["trim"],
        summary["color"],
        summary["wheels"],
        summary["interior"],
        summary["battery"],
        summary["addons"]
    )

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        city = request.form.get("city", "").strip()
        payment_preference = request.form.get("payment_preference", "").strip()

        if not full_name:
            errors.append("Full name is required.")
        if not email:
            errors.append("Email is required.")
        if not phone:
            errors.append("Phone is required.")

        if not errors:
            order_ref = generate_order_ref()
            return redirect(url_for("order_success", ref=order_ref, model=model["name"], total=fmt_currency(total)))

        form_data = {
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "city": city,
            "payment_preference": payment_preference
        }
    else:
        form_data = {
            "full_name": "",
            "email": "",
            "phone": "",
            "city": "",
            "payment_preference": ""
        }

    return render_template(
        "order_review.html",
        model=model,
        summary=summary,
        estimated_total=fmt_currency(total),
        errors=errors,
        form_data=form_data
    )

@app.route("/order/success")
def order_success():
    order_ref = request.args.get("ref", generate_order_ref())
    model_name = request.args.get("model", "Aureon Vehicle")
    total = request.args.get("total", "¥0")
    return render_template("order_success.html", order_ref=order_ref, model_name=model_name, total=total)

@app.route("/test-drive", methods=["GET", "POST"])
def test_drive():
    success = False
    errors = []
    form_data = {
        "full_name": "",
        "email": "",
        "phone": "",
        "preferred_model": "Aureon S",
        "preferred_date": "",
        "preferred_location": "",
        "notes": ""
    }

    if request.method == "POST":
        form_data = {
            "full_name": request.form.get("full_name", "").strip(),
            "email": request.form.get("email", "").strip(),
            "phone": request.form.get("phone", "").strip(),
            "preferred_model": request.form.get("preferred_model", "Aureon S"),
            "preferred_date": request.form.get("preferred_date", "").strip(),
            "preferred_location": request.form.get("preferred_location", "").strip(),
            "notes": request.form.get("notes", "").strip()
        }
        if not form_data["full_name"]:
            errors.append("Full name is required.")
        if not form_data["email"]:
            errors.append("Email is required.")
        if not form_data["phone"]:
            errors.append("Phone is required.")
        if not form_data["preferred_date"]:
            errors.append("Preferred date is required.")
        if not form_data["preferred_location"]:
            errors.append("Preferred location is required.")

        if not errors:
            success = True

    return render_template("test_drive.html", success=success, errors=errors, form_data=form_data, models=list(models_data.values()))

@app.route("/account/orders")
def account_orders():
    return render_template("account_orders.html", orders=orders_data[:5])

@app.route("/account/test-drives")
def account_test_drives():
    return render_template("account_test_drives.html", test_drives=test_drive_data[:4])

@app.route("/dashboard")
def dashboard():
    total_orders = len(orders_data)
    pending_orders = len([o for o in orders_data if o["status"] in ["Processing", "Confirmed"]])
    total_test_drives = len(test_drive_data)
    active_customers = len(customer_data)
    top_models = [
        {"name": "Aureon X", "orders": 28, "share": "36%"},
        {"name": "Aureon S", "orders": 24, "share": "31%"},
        {"name": "Aureon GT", "orders": 16, "share": "21%"}
    ]
    return render_template(
        "dashboard.html",
        total_orders=total_orders,
        pending_orders=pending_orders,
        total_test_drives=total_test_drives,
        active_customers=active_customers,
        recent_orders=orders_data[:5],
        upcoming_test_drives=test_drive_data[:5],
        top_models=top_models
    )

@app.route("/dashboard/orders")
def dashboard_orders():
    return render_template("dashboard_orders.html", orders=orders_data)

@app.route("/dashboard/test-drives")
def dashboard_test_drives():
    return render_template("dashboard_test_drives.html", test_drives=test_drive_data)

@app.route("/dashboard/customers")
def dashboard_customers():
    return render_template("dashboard_customers.html", customers=customer_data)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/support")
def support():
    return render_template("support.html", faqs=faq_data)

if __name__ == "__main__":
    app.run(debug=True)