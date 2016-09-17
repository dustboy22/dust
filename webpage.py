from flask import url_for
import random
import string
import pyfiglet

class Captcha:
	def __init__(self):
		self.font = pyfiglet.Figlet()
		self.code = "".join([random.choice(string.ascii_letters) for i in range(5)])
		self.text = self.font.renderText(self.code)


class WebMaster:
	def __init__(self):
		self.posts = []
		self.name = "dust"
		self.post_split = "-----------"
		self.comment_split = "-----"
		self.count = 0

		self.max_posts = 100

	def new_post(self, title, content, image = None):
		self.count += 1
		self.posts.append(Post(title, content, self.count))

	def prune_posts(self):
		if len(self.posts) > self.max_posts:
			del self.posts[:self.max_posts-1]

	def get_post(self, post_id):
		for post in self.posts:
			if post.post_id == post_id:
				return post

		else:
			return False


class Post:
	def __init__(self, title, content, post_id):
		self.title = title
		self.content = content
		self.post_id = post_id

		self.url = url_for("view_post", post_id = self.post_id)
		
		self.comments = []

	def new_comment(self, content):
		self.comments.append(Comment(content, len(self.comments)))


class Comment:
	def __init__(self, content, comment_id):
		self.content = content
		self.comment_id = comment_id