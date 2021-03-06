"""Playlist test cases."""

# Django
from django.test import TestCase

# Models
from apps.users.models import User
from apps.music.models import (
    Artist, 
    Song,
    Playlist,
)

class PlaylistTestCase(TestCase):
    """Playlist test case."""

    def setUp(self):
        """Test case set up."""
        self.user = User.objects.create_user(
            username='test12', 
            email='p@mlh.io', 
            password='test123'
        )
        self.user.save()

        self.artist = Artist.objects.create(
            name='freddie testcase', 
            user=self.user
        )
        self.artist.save()

        self.song = Song.objects.create(
            title='Awesome song',
            release_date='2006-10-25 14:30:59',
            artist=self.artist
        )
        self.song.save()

        self.playlist = Playlist.objects.create(
            title='awesome playlist',
            user=self.user
        )
        self.playlist.save()

    def test_user(self):
        """Test user forieng key relationship."""
        self.assertIsNotNone(self.user and self.song and self.playlist)
        self.assertEqual(self.playlist.user, self.user)

    def test_songs(self):
        """Test relationship with songs adding to the playlist."""
        playlist = self.playlist
        playlist.songs.add(self.song)
        playlist_songs = list(playlist.songs.all())

        self.assertIsNotNone(playlist_songs)
        self.assertEqual(playlist_songs[0], self.song)