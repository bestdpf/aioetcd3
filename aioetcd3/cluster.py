import functools

from aioetcd3.rpc import rpc_pb2 as rpc
from aioetcd3.base import StubMixin


def call_grpc(request, response_func, method):

    def _f(f):
        @functools.wraps(f)
        async def call(self, *args, timeout=None, **kwargs):
            r = await self.grpc_call(method(self), request(*args, **kwargs), timeout=timeout)
            return response_func(r)

        return call

    return _f


class Cluster(StubMixin):
    def _update_channel(self, channel):
        super()._update_channel(channel)
        self._cluster_stub = rpc.ClusterStub(channel)

    @call_grpc(lambda peerurls: rpc.MemberAddRequest(peerURLs=peerurls),
               lambda r: r.member, lambda s: s._cluster_stub.MemberAdd)
    async def member_add(self, peerurls):
        pass

    @call_grpc(lambda mid: rpc.MemberRemoveRequest(ID=mid),
               lambda r: [m for m in r.members],
               lambda s: s._cluster_stub.MemberRemove)
    async def member_remove(self, mid):
        pass

    @call_grpc(lambda mid, urls: rpc.MemberUpdateRequest(ID=mid, peerURLs=urls),
               lambda r: [m for m in r.members],
               lambda s: s._cluster_stub.MemberUpdate)
    async def member_update(self, mid, peerurls):
        pass

    @call_grpc(lambda: rpc.MemberListRequest(), lambda r: [m for m in r.members],
               lambda s: s._cluster_stub.MemberList)
    async def member_list(self):
        pass