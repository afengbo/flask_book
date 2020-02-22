from flask import flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app.libs.email import send_email
from app.libs.enums import PendingStatus
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.trade import MyTrades
from . import web
from app.models.base import db

__author__ = '七月'


@web.route('/my/wish')
def my_wish():
    my_all_wishes = Wish.get_user_wishes(current_user.id)
    all_wishes_isbn = [wish.isbn for wish in my_all_wishes]
    book_wishes_count_list = Wish.get_gift_count(all_wishes_isbn)
    my_wish_viewmodel = MyTrades(my_all_wishes, book_wishes_count_list)
    return render_template("my_wish.html", wishes=my_wish_viewmodel.trades)


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_db(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id
            db.session.add(wish)
    else:
        flash("这本书已经添加至你的赠送清单或者已经存在于你的心愿清单，请勿重复添加。")
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
@login_required
def satisfy_wish(wid):
    wish = Wish.query.get_or_404(wid)
    gift = Gift.query.filter_by(uid=current_user.id, isbn=wish.isbn).first()
    if not gift:
        flash("你还没有上传此书，请点击‘赠送此书’以后再向他人赠送。")
    else:
        send_email(wish.user.email, "有人向你赠送书籍",
                   "email/satisify_wish.html", wish=wish, gift=gift)
        flash("已成功向ta发送一封邮件，如果ta愿意接受赠送，你将会收到一个鱼漂。")
    return redirect(url_for("web.book_detail", isbn=gift.isbn))


@web.route('/wish/book/<isbn>/redraw')
@login_required
def redraw_from_wish(isbn):
    # 撤销愿望，不要了
    drift = Drift.query.filter_by(isbn=isbn).first()
    if drift.pending == PendingStatus.Waiting:
        flash("这个礼物尚处于交易状态，请先前往鱼漂处理该交易。")
    else:
        wish = Wish.query.filter_by(isbn=isbn, launched=False).first_or_404()
        with db.auto_commit():
            wish.delete()
    return redirect(url_for('web.my_wish'))
