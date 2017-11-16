from pulsar.apps.data import register_store

from ..redis import store


class PulsarStore(store.RedisStore):
    pass


register_store('pulsar', 'pulsar.apps.data.pulsards:PulsarStore')
