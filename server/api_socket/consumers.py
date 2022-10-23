from djangochannelsrestframework import permissions
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import ListModelMixin
from djangochannelsrestframework.observer import model_observer

from .models import Todo
from .serializers import TodoSerializer



class TodoConsumer(ListModelMixin, GenericAsyncAPIConsumer):

    queryset =Todo.objects.all()
    serializer_class = TodoSerializer
    permissions = (permissions.AllowAny,)

    async def connect(self, **kwargs):
        await self.model_change.subscribe()
        await super().connect()

    @model_observer(Todo)
    async def model_change(self, message, observer=None, **kwargs):
        print(message)
        await self.send_json(message)

    @model_change.serializer
    def model_serialize(self, instance, action, **kwargs):
        return dict(data=TodoSerializer(instance=instance).data, action=action.value)