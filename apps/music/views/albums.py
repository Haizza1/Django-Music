"""Album views."""

# Rest Framework
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework import status, viewsets, mixins

# Permissions
from rest_framework.permissions import IsAuthenticated
from apps.music.permissions import IsAlbumOwner, IsArtist

# Serializers
from apps.music.serializers import (
    CreateAlbumSerializer,
    AlbumModelSerializer,
    AddSongSerializer
)

# Models
from apps.music.models import Album, Artist

class AlbumViewSet(mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """Album view set."""

    serializer_class = AlbumModelSerializer

    def get_permissions(self):
        """Assing permissions based on actions."""
        if self.action == 'retrieve':
            permissions = [IsAuthenticated]
        elif self.action == 'createAlbum':
            permissions = [IsAuthenticated, IsArtist]
        elif self.action == 'addSong':
            permissions = [IsAuthenticated, IsAlbumOwner]

        return [p() for p in permissions]

    def get_object(self):
        """Return specific album."""

        return get_object_or_404(
            Album,
            pk=self.kwargs['pk']
        )

    def get_queryset(self):
        """Assing querys based on actions."""

        query = Album.objects.all()

        if self.action == 'retrieve':
            return query.get(pk=self.kwargs['pk'])

        return query

    @action(detail=False, methods=['POST'])
    def createAlbum(self, request):
        """Handle album creation."""
        artist = Artist.objects.get(user=request.user)
        serializer = CreateAlbumSerializer(
            context={'artist': artist},
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        album = serializer.save()

        data = AlbumModelSerializer(album).data

        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['POST'])
    def addSong(self, request):
        """Handle adding songs to the album instance."""

        serializer = AddSongSerializer(
            context={'album': self.get_object()},
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        album = serializer.save()
        data = AlbumModelSerializer(album).data

        return Response(data, status=status.HTTP_200_OK)

        