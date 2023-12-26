from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, \
    get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.models import Ad, Comment
from ads.serializers import AdSerializer, CommentSerializer
from ads.permissions import IsOwnerOrAdmin, IsCommentOwnerOrAdmin
from ads.pagination import AdPagination, CommentPagination


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


class CommentListAPIView(ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = CommentPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ad_pk = self.kwargs.get('ad_pk')
        ordering = self.request.query_params.get('ordering', '-created_at')
        return Comment.objects.filter(ad__pk=ad_pk).order_by(ordering)


class CommentCreateAPIView(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        ad_pk = self.kwargs.get('ad_pk')
        ad = get_object_or_404(Ad, pk=ad_pk)
        serializer.save(author=self.request.user, ad=ad)


class CommentRetrieveAPIView(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return self.queryset.get(ad_id=self.kwargs['ad_pk'], id=self.kwargs['com_pk'])
        except Comment.DoesNotExist:
            return None


class CommentPatchAPIView(UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentOwnerOrAdmin, IsAuthenticated]

    def get_object(self):
        try:
            return self.queryset.get(ad_id=self.kwargs['ad_pk'], id=self.kwargs['com_pk'])
        except Comment.DoesNotExist or Ad.DoesNotExist:
            return None


class CommentDestroyAPIView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentOwnerOrAdmin, IsAuthenticated]

    def get_object(self):
        try:
            return self.queryset.get(ad_id=self.kwargs['ad_pk'], id=self.kwargs['com_pk'])
        except Comment.DoesNotExist or Ad.DoesNotExist:
            return None
