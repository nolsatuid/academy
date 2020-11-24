from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from academy.api.authentications import UserAuthAPIView
from academy.api.inbox.serializer import (
    InboxSerializer, BulkReadUnreadSerializer, InboxListSerializer, BulkDeleteSerializer
)
from academy.api.response import ErrorResponse
from academy.apps.accounts.models import Inbox


class GetInboxList(UserAuthAPIView):
    def get(self, request):
        inbox = Inbox.objects.filter(user=request.user)
        return Response(InboxListSerializer(inbox, many=True).data)


class InboxDetail(UserAuthAPIView):
    def get(self, request, id):
        inbox = get_object_or_404(Inbox, user=request.user, id=id)
        inbox.is_read = True
        inbox.save()
        return Response(InboxSerializer(inbox).data)

    def delete(self, request, id):
        inbox = get_object_or_404(Inbox, user=request.user, id=id)
        inbox.delete()
        return Response({'message': 'Pesan berhasil dihapus'})


class BulkReadUnread(UserAuthAPIView):
    def post(self, request):
        bulk_read = BulkReadUnreadSerializer(data=request.data)

        if bulk_read.is_valid():
            bulk_filter = bulk_read.data['filter']
            read_state = bulk_read.data['read_state']
            if len(bulk_filter) == 1 and bulk_filter[0] == -1:
                # all filter
                inboxs = Inbox.objects.filter(user=request.user)
                inboxs.update(is_read=read_state)
                return Response(InboxSerializer(inboxs, many=True).data)
            else:
                # partial filter
                inboxs = Inbox.objects.filter(user=request.user, id__in=bulk_filter)
                inboxs.update(is_read=read_state)
                return Response(InboxSerializer(inboxs, many=True).data)
        else:
            return ErrorResponse(serializer=bulk_read)


class BulkDelete(UserAuthAPIView):
    def post(self, request):
        bulk_delete = BulkDeleteSerializer(data=request.data)
        if bulk_delete.is_valid():
            bulk_ids = bulk_delete.data["inbox_ids"]
            if len(bulk_ids) == 1 and bulk_ids[0] == -1:
                inboxs = Inbox.objects.filter(user=request.user)
                inboxs.delete()
                return Response({'message': 'Berhasil hapus pesan yang dipilih'})
            else:
                inboxs = Inbox.objects.filter(id__in=bulk_ids, user=request.user)
                inboxs.delete()
                return Response({'message': 'Berhasil hapus pesan yang dipilih'})
        else:
            return ErrorResponse(error_message='Pesan tidak ditemukan')


class GetCountInbox(UserAuthAPIView):
    def get(self, request):
        inbox = Inbox.objects.filter(user=request.user, is_read=False)
        return Response(
            {'count': inbox.count()}
        )
