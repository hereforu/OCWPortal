from django.db import models
# Create your models here.
class TagModel(models.Model):
	tag = models.CharField(max_length=40)

class Category(models.Model):
	category_title = models.CharField(max_length=128)
	description = models.TextField(null=True)

class SubCategory(models.Model):
	categoryRef = models.ForeignKey('Category', on_delete=models.CASCADE)
	subcategory_title = models.CharField(max_length=128)
	description = models.TextField(null=True)

class Lecture(models.Model):
	ELEMENTARY_LEVEL = '<0>elementary'
	MIDDLESCHOOL_LEVEL = '<1>middle'
	HIGHSCHOOL_LEVEL = '<2>high'
	UNDERGRADUATE_LEVEL = '<3>undergraduate'
	GRADUATE_LEVEL = '<4>graduate'
	LECTURE_LEVEL_CHOICES=(
		(ELEMENTARY_LEVEL, 'Elementary School Course'),
		(MIDDLESCHOOL_LEVEL, 'Middle School Course'),
		(HIGHSCHOOL_LEVEL, 'High School Course'),
		(UNDERGRADUATE_LEVEL, 'Undergraduate Course'),
		(GRADUATE_LEVEL, 'Graduate Course'),
	)
	categoryRef = models.ForeignKey('Category', on_delete=models.CASCADE)
	subcategoryRef = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
	level =  models.CharField(max_length=20, choices=LECTURE_LEVEL_CHOICES, default=UNDERGRADUATE_LEVEL)
	subject = models.CharField(max_length=128)
	description = models.TextField(null=True)
	image_url = models.TextField(null=True)
	home_recommendation = models.BooleanField(default=True)

	def setlevel(self, strlevel):
		for (level_id, level_display) in self.LECTURE_LEVEL_CHOICES:
			if level_id.find(strlevel) == 3:
				self.level = level_id
				return
		self.level = '<5>'+strlevel

class Chapter(models.Model):
	lectureRef = models.ForeignKey('Lecture', on_delete=models.CASCADE)
	chapter_title = models.CharField(max_length=128)

class Section(models.Model):
	lectureRef = models.ForeignKey('Lecture', null=True)
	chapterRef = models.ForeignKey('Chapter', on_delete=models.CASCADE)
	section_title = models.CharField(max_length=128)

class Provider(models.Model):
	DEFAULT_PK=1
	name = models.CharField(max_length=128)

class Institute(models.Model):
	DEFAULT_PK=1
	name = models.CharField(max_length=128)

class Clip(models.Model):
	lectureRef = models.ForeignKey('Lecture')
	chapterRef = models.ForeignKey('Chapter')
	sectionRef = models.ForeignKey('Section', on_delete=models.CASCADE)
	original_providerRef = models.ForeignKey('Provider', related_name='original_provider', default=Provider.DEFAULT_PK)
	original_instituteRef = models.ForeignKey('Institute', related_name='original_institute', default=Institute.DEFAULT_PK)
	providerRef = models.ForeignKey('Provider', related_name='provider', default=Provider.DEFAULT_PK)
	instituteRef = models.ForeignKey('Institute', related_name='institute', default=Institute.DEFAULT_PK)
	language_type = models.CharField(max_length=40)
	source_from = models.CharField(max_length=40)
	description = models.TextField()
	media_url = models.TextField()
	youtube_id = models.CharField(max_length=20, null=True)
	video_type = models.CharField(max_length=40)
	thumbnail_url = models.TextField(null=True)
	caption_url = models.TextField(null=True)
	subtitles = models.CharField(max_length=40, null=True)
	tags = models.ManyToManyField(TagModel)
	created_date = models.DateField()
	uploaded_date = models.DateTimeField(auto_now_add=True)
	running_time = models.PositiveIntegerField()
	start_time = models.PositiveIntegerField()
	end_time = models.PositiveIntegerField()
	init_rank = models.FloatField()
	review_rate = models.FloatField()
	view_counts = models.PositiveIntegerField()
