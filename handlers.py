# -*- coding: utf-8 -*- 
import dateparser
from datetime import timedelta, datetime
from repository import EventRepository

class BeerHandler(object):
    angry_threshold = 3
    angry_reply = ""
    command = "beer"

    local_delta = timedelta(hours=3)
    def __init__(self, arguments):
        self.arguments = arguments
        if len(arguments) == 0:
            self.angry_reply = u"{0}, ты буквально только что это спрашивал."
        else:
            self.angry_reply = u"{0} определись сначала когда и куда вы там пойдете, лишний раз не надо меня дергать."

    def handle(self, chat_id):
        if len(self.arguments) > 0:
            return self._process_create_request(chat_id)
        else:
            return self._process_when_request(chat_id)

    def _process_create_request(self, chat_id):
        with EventRepository() as rep:
            place = self.arguments[0]
            date = dateparser.parse(" ".join(self.arguments[1:]), languages=['ru', 'ru'])
            if not date:
                return u"Ты ебанутый?)) Сначала укажи место(без пробелов), а потом дату в нормальном формате"
            rep.remove(chat_id)
            date = date.replace(year = datetime.now().year)
            date = date - self.local_delta
            rep.create("Beer", place, date, chat_id)
        return self._get_beer_delay_string(place, date)

    def _process_when_request(self, chat_id):
        with EventRepository() as rep:
            events = rep.list(chat_id)
        if not events:
            return u"Нет пива в ближайшее время"
        event = events[0]
        return self._get_beer_delay_string(event.place, event.date)

    def _get_beer_delay_string(self, place, event_date):
        date = (event_date + self.local_delta).strftime("%d.%m %H:%M")
        delta_seconds = (event_date - datetime.utcnow()).total_seconds()
        delta_hours = int(delta_seconds / 3600)
        delta_minutes = int((delta_seconds - (delta_hours * 3600)) / 60)
        hours_string = self._get_hours_string(delta_hours)
        minute_string = self._get_minute_string(delta_minutes)
        if delta_minutes != 0 and delta_seconds != 0:
            delta = u"%d %s %d %s" % (delta_hours, hours_string, delta_minutes, minute_string)
        elif delta_minutes == 0:
            delta = u"%d %s" % (delta_hours, hours_string)
        else:
            delta = u"%d %s" % (delta_minutes, minute_string)
        return u"Пиво будет в %s %s (через %s) \U0001F37A" % (place, date, delta)

    def _get_hours_string(self, hours):
        if hours >= 5 and hours <= 20:
            return u"часов"
        elif hours % 10 == 1:
            return u"час"
        elif hours % 10 >= 2 and hours % 10 <= 4:
            return u"часа"
        else:
            return u"часов"

    def _get_minute_string(self, minutes):
        if minutes >= 5 and minutes <= 20:
            return u"минут"
        elif minutes % 10 == 1:
            return u"минуту"
        elif minutes % 10 >= 2 and minutes % 10 <= 4:
            return u"минуты"
        else:
            return u"минут"


class UnknownCommandHandler(object):
    angry_threshold = 2
    angry_reply = u"Так, всё, {0}, иди НАХУЙ"

    def __init__(self, arguments):
        pass

    def handle(self, chat_id):
        return u"Я хз че ты хочешь. Кликни на список доступных команд и не ЕБИ мне голову"
