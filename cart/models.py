from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie
from django.utils import timezone

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    total = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,
        on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.user.username

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.IntegerField()
    quantity = models.IntegerField()
    order = models.ForeignKey(Order,
        on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie,
        on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name
    
    
class CheckoutFeedback(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, help_text="Optional - leave blank to remain anonymous")
    feedback_text = models.TextField(max_length=500, help_text="Share your thoughts about the checkout process")
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Checkout Feedback"
        verbose_name_plural = "Checkout Feedback"
    
    def __str__(self):
        if self.name:
            return f"Feedback from {self.name} - {self.created_at.strftime('%Y-%m-%d')}"
        else:
            return f"Anonymous feedback - {self.created_at.strftime('%Y-%m-%d')}"
    
    @property
    def display_name(self):
        return self.name if self.name else "Anonymous"