from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.utils.crypto import get_random_string
from asgiref.sync import sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import ChatMessage, ForumPost


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")
        if not user or isinstance(user, AnonymousUser) or not user.is_authenticated:
            await self.close()
            return
        self.group_name = f"chat_user_{user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        user = self.scope.get("user")
        if user and user.is_authenticated:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            return
        text = (content or {}).get("message", "").strip()
        is_anon = bool((content or {}).get("is_anonymous", False))
        anon_id = (content or {}).get("anon_id") or (get_random_string(16) if is_anon else "")
        if not text:
            return

        await sync_to_async(ChatMessage.objects.create)(
            user=user, message=text, is_user=True, is_anonymous=is_anon, anon_id=anon_id
        )
        await self.channel_layer.group_send(self.group_name, {
            "type": "chat.message",
            "payload": {"sender": "you", "message": text, "is_anonymous": is_anon, "anon_id": anon_id},
        })

        # Trivial AI echo
        ai_text = "Thanks for sharing. I'm here to help."
        await sync_to_async(ChatMessage.objects.create)(
            user=user, message=ai_text, is_user=False, is_anonymous=is_anon, anon_id=anon_id
        )
        await self.channel_layer.group_send(self.group_name, {
            "type": "chat.message",
            "payload": {"sender": "ai", "message": ai_text, "is_anonymous": is_anon, "anon_id": anon_id},
        })

    async def chat.message(self, event):
        await self.send_json(event.get("payload", {}))


class ForumConsumer(AsyncJsonWebsocketConsumer):
    group_name = "forum_stream"

    async def connect(self):
        user = self.scope.get("user")
        if not user or isinstance(user, AnonymousUser) or not user.is_authenticated:
            await self.close()
            return
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            return
        title = (content or {}).get("title", "").strip()
        body = (content or {}).get("content", "").strip()
        is_anon = bool((content or {}).get("is_anonymous", False))
        anon_id = (content or {}).get("anon_id") or (get_random_string(16) if is_anon else "")
        if not title or not body:
            return
        post = await sync_to_async(ForumPost.objects.create)(
            user=user, title=title, content=body, is_anonymous=is_anon, anon_id=anon_id
        )
        await self.channel_layer.group_send(self.group_name, {
            "type": "forum.message",
            "payload": {
                "title": post.title,
                "content": post.content,
                "is_anonymous": post.is_anonymous,
                "anon_id": post.anon_id,
                "created_at": post.created_at.isoformat(),
                "author": (user.username if not is_anon else f"Anon-{post.anon_id[:6]}")
            },
        })

    async def forum.message(self, event):
        await self.send_json(event.get("payload", {}))


