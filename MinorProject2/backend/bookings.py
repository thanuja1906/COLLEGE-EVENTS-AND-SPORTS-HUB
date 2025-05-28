from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, send_file
from flask_login import login_required, current_user
from datetime import datetime, date, time, timedelta
from backend.models import db, Booking, User
import pandas as pd
import io

bookings_bp = Blueprint('bookings', __name__, url_prefix='/bookings')

TIME_SLOTS = [
    {'start': time(15, 0), 'end': time(16, 0)},  # 3pm-4pm
    {'start': time(16, 0), 'end': time(17, 0)},  # 4pm-5pm
    {'start': time(17, 0), 'end': time(18, 0)},  # 5pm-6pm
    {'start': time(18, 0), 'end': time(19, 0)},  # 6pm-7pm
    {'start': time(19, 0), 'end': time(20, 0)},  # 7pm-8pm
]

@bookings_bp.route('/sports-selection')
@login_required
def sport_selection():
    today = date.today()
    existing_booking = Booking.query.filter_by(
        user_id=current_user.id,
        booking_date=today,
        status='confirmed'
    ).first()
    if existing_booking:
        flash('You already have a booking for today.')
        return redirect(url_for('bookings.booking'))
    return render_template('sports_selection.html')

@bookings_bp.route('/available-slots', methods=['GET'])
@login_required
def available_slots():
    selected_date = request.args.get('date')
    try:
        booking_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    booked_slots = Booking.query.filter_by(
        booking_date=booking_date,
        status='confirmed'
    ).all()

    available_slots = []
    current_time = datetime.now().time()

    for slot in TIME_SLOTS:
        for court_num in range(1, 5):  # Courts 1-4
            slot_booked = any(
                booking.court_number == court_num and
                booking.start_time == slot['start'] and
                booking.booking_date == booking_date
                for booking in booked_slots
            )
            if court_num == 1:  # Faculty court
                if current_user.is_faculty:
                    continue  # Faculty can't book via this (spot registration only)
                slot_start_datetime = datetime.combine(booking_date, slot['start'])
                cutoff_time = slot_start_datetime - timedelta(minutes=10)
                if datetime.now() < cutoff_time or slot_booked:
                    continue
            else:  # Student courts (2-4)
                if current_user.is_faculty:
                    continue
            if booking_date == date.today() and slot['start'] <= current_time:
                continue
            if not slot_booked:
                available_slots.append({
                    'court': court_num,
                    'start_time': slot['start'].strftime('%H:%M'),
                    'end_time': slot['end'].strftime('%H:%M'),
                    'display': f"Court {court_num} - {slot['start'].strftime('%I:%M %p')} to {slot['end'].strftime('%I:%M %p')}"
                })

    return jsonify(available_slots)

@bookings_bp.route('/book-slot', methods=['POST'])
@login_required
def book_slot():
    court_number = int(request.form.get('court_number'))
    booking_date = datetime.strptime(request.form.get('booking_date'), '%Y-%m-%d').date()
    time_slot = request.form.get('time_slot')
    start_time = datetime.strptime(time_slot.split('-')[0].strip(), '%I:%M %p').time()
    end_time = datetime.strptime(time_slot.split('-')[1].strip(), '%I:%M %p').time()

    existing_booking = Booking.query.filter_by(
        user_id=current_user.id,
        booking_date=booking_date,
        status='confirmed'
    ).first()
    if existing_booking:
        flash('You already have a booking for this date.')
        return redirect(url_for('bookings.sports_selection'))

    if court_number == 1 and not current_user.is_faculty:
        slot_start_datetime = datetime.combine(booking_date, start_time)
        cutoff_time = slot_start_datetime - timedelta(minutes=10)
        if datetime.now() < cutoff_time:
            flash('Court 1 is for faculty only until 10 minutes before slot time.')
            return redirect(url_for('bookings.sports_selection'))

    if court_number in [2, 3, 4] and current_user.is_faculty:
        flash('Faculty can only book Court 1.')
        return redirect(url_for('bookings.sports_selection'))

    existing_booking = Booking.query.filter_by(
        court_number=court_number,
        booking_date=booking_date,
        start_time=start_time,
        status='confirmed'
    ).first()
    if existing_booking:
        flash('This slot has already been booked.')
        return redirect(url_for('bookings.sports_selection'))

    booking = Booking(
        user_id=current_user.id,
        court_number=court_number,
        start_time=start_time,
        end_time=end_time,
        booking_date=booking_date,
        status='confirmed'
    )
    db.session.add(booking)
    db.session.commit()
    flash('Slot booked successfully!')
    return redirect(url_for('bookings.booking'))

@bookings_bp.route('/booking')
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(
        Booking.booking_date, Booking.start_time
    ).all()
    for booking in bookings:
        booking.can_cancel = (datetime.now() < (datetime.combine(booking.booking_date, booking.start_time) - timedelta(minutes=10)))
    return render_template('booking.html', bookings=bookings)

@bookings_bp.route('/cancel-booking/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        flash('You can only cancel your own bookings')
        return redirect(url_for('bookings.booking'))
    if datetime.now() >= (datetime.combine(booking.booking_date, booking.start_time) - timedelta(minutes=10)):
        flash('Cancellation is only allowed at least 10 minutes before the booking time')
        return redirect(url_for('bookings.booking'))
    booking.status = 'cancelled'
    db.session.commit()
    flash('Booking cancelled successfully')
    return redirect(url_for('bookings.booking'))

@bookings_bp.route('/admin/export')
@login_required
def export_bookings():
    if not current_user.is_faculty:
        flash('Access denied')
        return redirect(url_for('bookings.booking'))
    bookings = Booking.query.all()
    data = [{
        'Booking ID': b.id,
        'User Name': b.user.name,
        'User Email': b.user.email,
        'User Type': 'Faculty' if b.user.is_faculty else 'Student',
        'Court': b.court_number,
        'Date': b.booking_date.strftime('%Y-%m-%d'),
        'Start Time': b.start_time.strftime('%H:%M'),
        'End Time': b.end_time.strftime('%H:%M'),
        'Status': b.status.upper(),
        'Booked At': b.created_at.strftime('%Y-%m-%d %H:%M')
    } for b in bookings]
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Bookings')
    output.seek(0)
    filename = f"BVRIT_Bookings_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    return send_file(
        output,
        download_name=filename,
        as_attachment=True,
        mimetype='application/vnd.openpyxlformats-officedocument.spreadsheetml.sheet'
    )