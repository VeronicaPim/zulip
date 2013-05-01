import datetime
import pytz

from django.core.management.base import BaseCommand
from django.db.models import Q
from zephyr.models import Realm, Stream, Message, Subscription, Recipient

class Command(BaseCommand):
    help = "Generate statistics on the streams for a realm."

    def handle(self, *args, **options):
        if args:
            try:
                realms = [Realm.objects.get(domain=domain) for domain in args]
            except Realm.DoesNotExist, e:
                print e
                exit(1)
        else:
            realms = Realm.objects.all()

        for realm in realms:
            print realm.domain
            print "------------"
            print "%25s %15s %10s" % ("stream", "subscribers", "messages")
            streams = Stream.objects.filter(realm=realm).exclude(Q(name__istartswith="tutorial-"))
            invite_only_count = 0
            for stream in streams:
                if stream.invite_only:
                    invite_only_count += 1
                    continue
                print "%25s" % (stream.name,),
                recipient = Recipient.objects.filter(type=Recipient.STREAM, type_id=stream.id)
                print "%10d" % (len(Subscription.objects.filter(recipient=recipient, active=True)),),
                num_messages = len(Message.objects.filter(recipient=recipient))
                print "%12d" % (num_messages,)
            print "%d invite-only streams" % (invite_only_count,)
            print ""
