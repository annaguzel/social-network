from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth.models import User
from .models import Post
from .serializers import PostSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


class PostModelViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin,
                       ListModelMixin, GenericViewSet):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    @action(detail=False,
            methods=['post'],
            url_path='like',
            url_name='like')
    def like(self, request, *args, **kwargs):
        if request.method == "POST":
            # make sure user can't like the post more than once.
            user = User.objects.get(username=self.request.user.username)
        # find whatever post is associated with like
        print(args['id'])
        post = Post.objects.get(id=args['id'])

        if post.post_like.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        # post = get_object_or_404(Post, id=request.POST.get('id'))
        # if post.likes.filter(id=request.user.id).exists():
        #     post.likes.remove(request.user)
        # else:
        #     post.likes.add(request.user)

        return Response(status=status.HTTP_200_OK)
