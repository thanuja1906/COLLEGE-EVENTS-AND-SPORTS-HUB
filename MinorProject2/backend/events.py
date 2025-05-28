from flask import Blueprint, render_template
from backend.models import db, Event
from datetime import date

events_bp = Blueprint('events', __name__, url_prefix='/events')

@events_bp.route('/events')
def view_events():
    upcoming_events = Event.query.filter(
        Event.event_date >= date.today(),
        Event.is_active == True
    ).order_by(Event.event_date).all()
    past_events = Event.query.filter(
        Event.event_date < date.today(),
        Event.is_active == True
    ).order_by(Event.event_date.desc()).limit(6).all()
    return render_template('bvritEvents.html', 
                         upcoming_events=upcoming_events,
                         past_events=past_events)

@events_bp.route('/event/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    gallery_images = event.gallery_images if event.gallery_images else []
    return render_template('event_detail.html', 
                         event=event,
                         gallery_images=gallery_images)

@events_bp.route('/event-gallery')
def event_gallery():
    past_events = Event.query.filter(
        Event.event_date < date.today(),
        Event.gallery_images != None
    ).order_by(Event.event_date.desc()).all()
    events_with_gallery = [{
        'event': event,
        'images': event.gallery_images[:3] if event.gallery_images else []
    } for event in past_events if event.gallery_images]
    return render_template('bvritEvents.html', 
                         events=events_with_gallery)