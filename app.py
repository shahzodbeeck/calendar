from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from flask_migrate import Migrate
import calendar

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True
app.config['SECRET_KEY'] = '123'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Years(db.Model):
    tablename = 'years'
    id = Column(Integer, primary_key=True)
    year = Column(String)
    month = db.relationship("Month", backref="years", order_by="Month.id")


class Month(db.Model):
    tablename = "month"
    id = Column(Integer, primary_key=True)
    month = Column(String)
    years_id = Column(Integer, ForeignKey('years.id'))
    days = db.relationship("Month", backref="month", order_by="Days.id")

    def add(self):
        db.session.add(self)
        db.session.commit()


class Days(db.Model):
    tablename = "days"
    id = Column(Integer, primary_key=True)
    day = Column(String)
    month = Column(Integer, ForeignKey('month.id'))
    year = Column(Integer, ForeignKey('years.id'))
    lessons = db.relationship("Day_lessons", backref="days", order_by="Day_lessons.id")


class Day_lessons(db.Model):
    __tablename = "lessons"
    id = Column(Integer, primary_key=True)
    days = Column(Integer, ForeignKey('days.id'))
    status = Column(Boolean)


def get_calendar(current_year, next_year):
    for year in range(current_year, next_year + 1):
        for month in range(1, 13):
            year = Month.query.order_by(Month.id)
            add_month = Month(month=month, year=year)

            if month == 7 or month == 6 or month == 8:
                pass
            else:
                month_name = calendar.month_name[month]
                cal = calendar.monthcalendar(year, month)
                for week in cal:
                    for day in week:
                        day_str = str(day) if day != 0 else "  "
                        if day != 0:
                            day_of_week = calendar.day_name[calendar.weekday(year, month, day)]
                            print(f'{year}-{month}-{day_str} - {day_of_week} - {month_name}')


@app.route('/')
def hello_world():
    print(get_calendar(2023, 2024))
    return render_template('index.html')


if __name__ == 'main':
    app.run()
