from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
	owner = models.ForeignKey(User)
	text = models.CharField(max_length = 160)
	time = models.DateTimeField(auto_now_add = True)
	picture = models.ImageField(upload_to="blog-photos", blank=True)
	
	def __unicode__(self):
		return "Post text:   " + self.text + "     Post time : " + unicode(self.time)

	@staticmethod
	def get_posts(owner):
		return Post.objects.filter(owner = owner)

class User_Token(models.Model):
    user=models.ForeignKey(User)
    token=models.CharField(max_length=30)

class Follower(models.Model):
	user = models.ForeignKey(User, related_name = 'follow_user')
	following = models.ForeignKey(User, related_name='follow_following')
