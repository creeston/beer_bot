# -*- coding: utf-8 -*- 
import dateparser

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
        if len(arguments) > 0:
            return self._process_create_request()
        else:
            return self._process_when_request()

    def _process_create_request(self):
        with EventRepository() as rep:
            place = self.arguments[0]
            date = dateparser.parse(" ".join(self.arguments[1:]))
            if not date:
                return u"Ты ебанутый?)) Сначала укажи место(без пробелов), а потом дату в нормальном формате"
            rep.remove(chat_id)
            date = date.replace(year = datetime.now().year)
            date = date - self.local_delta
            rep.create("Beer", place, date, chat_id)
        return self._get_beer_delay_string(place, date)

    def _process_when_request(self):
        with EventRepository() as rep:
            events = rep.list(chat_id)
        if not events:
            return u"Нет пива в ближайшее время"
        event = events[0]
        return self._get_beer_delay_string(event.place, event.date)

    def _get_beer_delay_string(self, place, event_date):
        date = (event_date + self.local_delta).strftime("%d.%m %H:%M")
        delta_seconds = (event_date - datetime.utcnow()).total_seconds
        delta_hours = int(delta_seconds / 3600)
        delta_minutes = int(delta_seconds - (delta_hours * 3600) / 60)
        if delta_minutes != 0:
            delta = u"%d часов %d минут" % (delta_hours, delta_minutes)
        else:
            delta = u"%d часов" % (delta_hours)
        return u"Пиво будет в %s %s (через %s) \U0001F37A" % (place, date, delta)


class UnknownCommandHandler(object):
    angry_threshold = 2
    angry_reply = u"Так, всё, {0}, иди НАХУЙ"

    def __init__(self, arguments):
        pass

    def handle(self, chat_id):
        return u"Я хз че ты хочешь. Кликни на список доступных команд и не ЕБИ мне голову"
