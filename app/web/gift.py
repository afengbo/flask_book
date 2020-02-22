from flask import current_app, flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app.libs.enums import PendingStatus
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.base import db
from app.models.wish import Wish
from app.view_models.trade import MyTrades
from . import web


@web.route('/my/gifts')
@login_required
def my_gifts():
    my_all_gifts = Gift.get_user_gifts(current_user.id)
    all_gifts_isbn = [gift.isbn for gift in my_all_gifts]
    book_wishes_count_list = Gift.get_wish_count(all_gifts_isbn)
    my_gift_viewmodel = MyTrades(my_all_gifts, book_wishes_count_list)
    return render_template("my_gifts.html", gifts=my_gift_viewmodel.trades)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_db(isbn):
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)
    else:
        flash("这本书已经添加至你的赠送清单或者已经存在于你的心愿清单，请勿重复添加。")
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
@login_required
def redraw_from_gifts(gid):
    # 撤销礼物，不送了
    drift = Drift.query.filter_by(gift_id=gid).first()
    if drift.pending == PendingStatus.Waiting:
        flash("这个礼物尚处于交易状态，请先前往鱼漂处理该交易。")
    else:
        gift = Gift.query.filter_by(id=gid, launched=False).first_or_404()
        with db.auto_commit():
            current_user.beans -= current_app.config["BEANS_UPLOAD_ONE_BOOK"]
            gift.delete()
    return redirect(url_for('web.my_gifts'))
