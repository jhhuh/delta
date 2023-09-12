import zmq.asyncio

from delta.network.base import BaseNetworkPublisher

zmq_ctx = zmq.asyncio.Context()


class ZmqPublisher(BaseNetworkPublisher):
    def __init__(self, endpoint: str):
        self._endpoint = endpoint
        self._socket = zmq_ctx.socket(zmq.PUB)
        self._socket.connect(self._endpoint)

    async def publish(self, topic: str, msg: str, encoding="utf-8"):
        await self._socket.send_multipart([topic.encode(encoding), msg])

    def __del__(self):
        self._socket.close()
        zmq_ctx.term()
