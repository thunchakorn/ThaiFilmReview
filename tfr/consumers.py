from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.template.loader import get_template

from django.urls import reverse


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            self.close()
            return
        self.GROUP_NAME = f"{self.user.profile.name}-notifications"

        async_to_sync(self.channel_layer.group_add)(self.GROUP_NAME, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        if self.user.is_authenticated:
            async_to_sync(self.channel_layer.group_discard)(
                self.GROUP_NAME, self.channel_name
            )

    def recieve_comment(self, event):
        instance = event["instance"]
        commentor = instance.profile
        review = instance.review
        html = get_template("pages/partials/notification.html").render(
            context={
                "message": f"{commentor} has commented your review on {review.film}",
                "link": reverse("reviews:detail", kwargs={"pk": review.pk}),
            }
        )
        self.send(text_data=html)

    def recieve_like(self, event):
        instance = event["instance"]
        liker = instance.profile
        review = instance.review
        html = get_template("pages/partials/notification.html").render(
            context={
                "message": f"{liker} has liked your review on {review.film}",
                "link": reverse("reviews:detail", kwargs={"pk": review.pk}),
            }
        )
        self.send(text_data=html)
