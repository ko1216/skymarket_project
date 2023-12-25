from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.models import Ad, Comment
from ads.serializers import AdSerializer
from ads.permissions import IsOwnerOrAdmin
from ads.pagination import AdPagination


class AdListAPIView(ListAPIView):
    serializer_class = AdSerializer
    pagination_class = AdPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ordering = self.request.query_params.get('ordering', '-created_at')
        return Ad.objects.order_by(ordering)


class AdCreateAPIView(CreateAPIView):
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AdMyListAPIView(ListAPIView):
    serializer_class = AdSerializer
    pagination_class = AdPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ordering = self.request.query_params.get('ordering', '-created_at')
        return Ad.objects.filter(author=self.request.user).order_by(ordering)


class AdRetrieveAPIView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]


class AdPatchAPIView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsOwnerOrAdmin, IsAuthenticated]


class AdDestroyAPIView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsOwnerOrAdmin, IsAuthenticated]


class CommentViewSet(ModelViewSet):
    pass
