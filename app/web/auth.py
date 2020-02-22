from flask import render_template, request, redirect, url_for, flash

from app.libs.email import send_email
from app.models.base import db
from app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm
from app.models.user import User
from . import web
from flask_login import login_user, logout_user


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)
        return redirect(url_for('web.login'))
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            # 将用户信息写入cookie中
            login_user(user, remember=True)
            next = request.args.get('next')
            if not next or not next.startswith("/"):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash("账号密码不正确！")
    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == "POST":
        if form.validate():
            account = form.email.data
            user_obj = User.query.filter_by(email=account).first_or_404()
            send_email(account, "重置密码", "email/reset_password.html",
                       user=user_obj, token=user_obj.generate_token())
            flash("密码重置邮件已发送至邮箱【" + account + "】 请注意查收!")
    return render_template("auth/forget_password_request.html", form=form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == "POST" and form.validate():
        success = User.reset_password(token, form.password1.data)
        if success:
            flash("密码重置成功，请重新登录！")
            return redirect(url_for('web.login'))
        else:
            flash("密码重置失败, 请检查网址是否正确。")
    return render_template("auth/forget_password.html", form=form)


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("web.index"))
