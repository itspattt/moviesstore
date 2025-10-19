from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    def __str__(self):
        return str(self.id) + ' - ' + self.name
    
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
<<<<<<< HEAD
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
=======
    movie = models.ForeignKey(Movie,
        on_delete=models.CASCADE)
    user = models.ForeignKey(User,
        on_delete=models.CASCADE)
>>>>>>> 9a9c5298988c2391fa9c7a3449315154049a3ce9
    num_likes = models.PositiveIntegerField(default=0)
    whoLiked = models.ManyToManyField(User, related_name='liked_reviews', blank=True)
    
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name
    
class Petition(models.Model):
    title = models.CharField(max_length = 255)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,
        on_delete=models.CASCADE)
    num_votes = models.PositiveIntegerField(default=0)
    whoVoted = models.ManyToManyField(User, related_name="who_voted", blank = True)
    
    def __str__(self):
        return str(self.id) + ' - ' + self.title
<<<<<<< HEAD
    
class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    class Meta:
        unique_together = ("movie", "user")
=======
    
>>>>>>> 9a9c5298988c2391fa9c7a3449315154049a3ce9
