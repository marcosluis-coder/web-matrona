from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Usuari, Cita
from . import db
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

import datetime

main = Blueprint("main", __name__)


# ---------------- HOME ----------------
@main.route("/")
def home():
    return render_template("index.html")


# ---------------- REGISTER ----------------
@main.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        nom = request.form.get("nom")
        email = request.form.get("email")
        password = request.form.get("password")
        rol = request.form.get("rol")

        hashed_password = generate_password_hash(password)

        user = Usuari(
            nom=nom,
            email=email,
            contrasenya=hashed_password,
            rol=rol
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("main.login"))

    return render_template("register.html")


# ---------------- LOGIN ----------------
@main.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = Usuari.query.filter_by(email=email).first()

        if user and check_password_hash(user.contrasenya, password):

            login_user(user)

            return redirect(url_for("main.home"))

        flash("Credencials incorrectes")

    return render_template("login.html")


# ---------------- LOGOUT ----------------
@main.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("main.login"))


# ---------------- NOVA CITA ----------------
@main.route("/cita", methods=["GET", "POST"])
@login_required
def nova_cita():

    hores_base = [
        "09:00", "09:30",
        "10:00", "10:30",
        "11:00", "11:30",
        "12:00", "12:30",
        "16:00", "16:30",
        "17:00", "17:30"
    ]

    today_date = datetime.date.today()

    # Ajust horari Render (UTC -> Espanya)
    now_time = (
        datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    ).time()

    # ---------- OBTENIR DATA ----------
    data_seleccionada = request.args.get("data")

    if not data_seleccionada:
        data_seleccionada = request.form.get("data")

    # ---------- POST ----------
    if request.method == "POST":

        data_str = data_seleccionada
        hora_str = request.form.get("hora")

        # ❌ Falten dades
        if not data_str or not hora_str:
            flash("Falten dades per reservar la cita")
            return redirect(url_for("main.nova_cita"))

        data_cita = datetime.datetime.strptime(
            data_str,
            "%Y-%m-%d"
        ).date()

        hora_cita = datetime.datetime.strptime(
            hora_str,
            "%H:%M"
        ).time()

        # ❌ Data passada
        if data_cita < today_date:
            flash("No pots reservar cites en dates passades")

            return redirect(
                url_for("main.nova_cita", data=data_str)
            )

        # ❌ Caps de setmana
        if data_cita.weekday() >= 5:
            flash("No es poden reservar cites en cap de setmana")

            return redirect(
                url_for("main.nova_cita", data=data_str)
            )

        # ❌ Hora passada
        if data_cita == today_date and hora_cita <= now_time:
            flash("No pots reservar una hora passada")

            return redirect(
                url_for("main.nova_cita", data=data_str)
            )

        # ❌ Hora ocupada
        cita_existente = Cita.query.filter_by(
            data=data_str,
            hora=hora_str
        ).first()

        if cita_existente:
            flash("Aquesta hora ja està reservada")

            return redirect(
                url_for("main.nova_cita", data=data_str)
            )

        # ✔ Crear cita
        cita = Cita(
            data=data_str,
            hora=hora_str,
            usuari_id=current_user.id
        )

        db.session.add(cita)
        db.session.commit()

        flash("Cita reservada correctament")

        return redirect(url_for("main.mis_citas"))

    # ---------- GET ----------
    hores_disponibles = []

    if data_seleccionada:

        data_cita = datetime.datetime.strptime(
            data_seleccionada,
            "%Y-%m-%d"
        ).date()

        # ❌ Caps de setmana també al GET
        if data_cita.weekday() >= 5:

            flash("No es poden reservar cites en cap de setmana")

            return render_template(
                "cita.html",
                hores=[],
                today=today_date.isoformat(),
                data_seleccionada=data_seleccionada
            )

        # Hores ocupades
        cites = Cita.query.filter_by(
            data=data_seleccionada
        ).all()

        hores_ocupades = [c.hora for c in cites]

        hores_disponibles = [
            h for h in hores_base
            if h not in hores_ocupades
        ]

        # Eliminar hores passades
        if data_cita == today_date:

            hores_disponibles = [
                h for h in hores_disponibles
                if datetime.datetime.strptime(
                    h,
                    "%H:%M"
                ).time() > now_time
            ]

    return render_template(
        "cita.html",
        hores=hores_disponibles,
        today=today_date.isoformat(),
        data_seleccionada=data_seleccionada
    )


# ---------------- MIS CITES ----------------
@main.route("/mis-citas")
@login_required
def mis_citas():

    citas = Cita.query.filter_by(
        usuari_id=current_user.id
    ).all()

    return render_template(
        "mis_citas.html",
        citas=citas
    )


# ---------------- TOTES CITES ----------------
@main.route("/totes-cites")
@login_required
def totes_cites():

    if current_user.rol != "comare":
        return "Accés denegat"

    citas = Cita.query.order_by(
        Cita.data,
        Cita.hora
    ).all()

    return render_template(
        "totes_cites.html",
        citas=citas
    )


# ---------------- CONFIRMAR CITA ----------------
@main.route("/confirmar/<int:id>")
@login_required
def confirmar_cita(id):

    if current_user.rol != "comare":
        return "Accés denegat"

    cita = Cita.query.get(id)

    cita.estat = "confirmada"

    db.session.commit()

    return redirect(url_for("main.totes_cites"))


# ---------------- CANCELAR CITA COMARE ----------------
@main.route("/cancelar/<int:id>")
@login_required
def cancelar_cita(id):

    if current_user.rol != "comare":
        return "Accés denegat"

    cita = Cita.query.get(id)

    cita.estat = "cancelada"

    db.session.commit()

    return redirect(url_for("main.totes_cites"))


# ---------------- CANCELAR PACIENT ----------------
@main.route("/cancelar-pacient/<int:id>")
@login_required
def cancelar_pacient(id):

    cita = Cita.query.get(id)

    # ❌ No existeix
    if not cita:
        flash("La cita no existeix")

        return redirect(url_for("main.mis_citas"))

    # ❌ No és seva
    if cita.usuari_id != current_user.id:
        return "Accés denegat"

    # ❌ Confirmada
    if cita.estat == "confirmada":

        flash("No pots cancel·lar una cita confirmada")

        return redirect(url_for("main.mis_citas"))

    # ✔ Cancel·lar
    cita.estat = "cancelada"

    db.session.commit()

    return redirect(url_for("main.mis_citas"))


# ---------------- ELIMINAR CITA ----------------
@main.route("/eliminar-cita/<int:id>")
@login_required
def eliminar_cita(id):

    cita = Cita.query.get(id)

    # ❌ No existeix
    if not cita:
        flash("La cita no existeix")

        return redirect(url_for("main.home"))

    # ❌ No és seva
    if (
        current_user.rol == "pacient"
        and cita.usuari_id != current_user.id
    ):
        return "Accés denegat"

    # ❌ Confirmada
    if cita.estat == "confirmada":

        flash("No es pot eliminar una cita confirmada")

        if current_user.rol == "comare":
            return redirect(url_for("main.totes_cites"))

        return redirect(url_for("main.mis_citas"))

    # ✔ Eliminar
    db.session.delete(cita)
    db.session.commit()

    if current_user.rol == "comare":
        return redirect(url_for("main.totes_cites"))

    return redirect(url_for("main.mis_citas"))


# ---------------- DASHBOARD ----------------
@main.route("/dashboard")
@login_required
def dashboard():

    if current_user.rol != "comare":
        return "Accés denegat"

    avui = datetime.date.today().isoformat()

    cites_avui = Cita.query.filter_by(
        data=avui
    ).all()

    pendents = Cita.query.filter_by(
        estat="pendent"
    ).count()

    confirmades = Cita.query.filter_by(
        estat="confirmada"
    ).count()

    cancelades = Cita.query.filter_by(
        estat="cancelada"
    ).count()

    return render_template(
        "dashboard.html",
        cites_avui=cites_avui,
        pendents=pendents,
        confirmades=confirmades,
        cancelades=cancelades
    )


# ---------------- CALCULADORA ----------------
@main.route("/calculadora", methods=["GET", "POST"])
@login_required
def calculadora():

    fpp = None
    propera_regla = None

    if request.method == "POST":

        tipus = request.form.get("tipus")
        data_str = request.form.get("data")

        if data_str:

            data = datetime.datetime.strptime(
                data_str,
                "%Y-%m-%d"
            ).date()

            # Data probable de part
            if tipus == "embaras":

                fpp = data + datetime.timedelta(days=280)

            # Propera regla
            elif tipus == "cicle":

                propera_regla = (
                    data + datetime.timedelta(days=28)
                )

    return render_template(
        "calculadora.html",
        fpp=fpp,
        propera_regla=propera_regla
    )