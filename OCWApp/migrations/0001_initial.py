# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category_title', models.CharField(max_length=128)),
                ('description', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chapter_title', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Clip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_type', models.CharField(max_length=40)),
                ('source_from', models.CharField(max_length=40)),
                ('description', models.TextField()),
                ('media_url', models.TextField()),
                ('youtube_id', models.CharField(max_length=20, null=True)),
                ('video_type', models.CharField(max_length=40)),
                ('thumbnail_url', models.TextField(null=True)),
                ('caption_url', models.TextField(null=True)),
                ('subtitles', models.CharField(max_length=40, null=True)),
                ('created_date', models.DateField()),
                ('uploaded_date', models.DateTimeField(auto_now_add=True)),
                ('running_time', models.PositiveIntegerField()),
                ('start_time', models.PositiveIntegerField()),
                ('end_time', models.PositiveIntegerField()),
                ('init_rank', models.FloatField()),
                ('review_rate', models.FloatField()),
                ('view_counts', models.PositiveIntegerField()),
                ('chapterRef', models.ForeignKey(to='OCWApp.Chapter')),
            ],
        ),
        migrations.CreateModel(
            name='Institute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.CharField(default=b'<3>undergraduate', max_length=20, choices=[(b'<0>elementary', b'Elementary School Course'), (b'<1>middle', b'Middle School Course'), (b'<2>high', b'High School Course'), (b'<3>undergraduate', b'Undergraduate Course'), (b'<4>graduate', b'Graduate Course')])),
                ('subject', models.CharField(max_length=128)),
                ('description', models.TextField(null=True)),
                ('image_url', models.TextField(null=True)),
                ('home_recommendation', models.BooleanField(default=True)),
                ('categoryRef', models.ForeignKey(to='OCWApp.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('section_title', models.CharField(max_length=128)),
                ('chapterRef', models.ForeignKey(to='OCWApp.Chapter')),
                ('lectureRef', models.ForeignKey(to='OCWApp.Lecture', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subcategory_title', models.CharField(max_length=128)),
                ('description', models.TextField(null=True)),
                ('categoryRef', models.ForeignKey(to='OCWApp.Category')),
            ],
        ),
        migrations.CreateModel(
            name='TagModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(max_length=40)),
            ],
        ),
        migrations.AddField(
            model_name='lecture',
            name='subcategoryRef',
            field=models.ForeignKey(to='OCWApp.SubCategory'),
        ),
        migrations.AddField(
            model_name='clip',
            name='instituteRef',
            field=models.ForeignKey(related_name='institute', default=1, to='OCWApp.Institute'),
        ),
        migrations.AddField(
            model_name='clip',
            name='lectureRef',
            field=models.ForeignKey(to='OCWApp.Lecture'),
        ),
        migrations.AddField(
            model_name='clip',
            name='original_instituteRef',
            field=models.ForeignKey(related_name='original_institute', default=1, to='OCWApp.Institute'),
        ),
        migrations.AddField(
            model_name='clip',
            name='original_providerRef',
            field=models.ForeignKey(related_name='original_provider', default=1, to='OCWApp.Provider'),
        ),
        migrations.AddField(
            model_name='clip',
            name='providerRef',
            field=models.ForeignKey(related_name='provider', default=1, to='OCWApp.Provider'),
        ),
        migrations.AddField(
            model_name='clip',
            name='sectionRef',
            field=models.ForeignKey(to='OCWApp.Section'),
        ),
        migrations.AddField(
            model_name='clip',
            name='tags',
            field=models.ManyToManyField(to='OCWApp.TagModel'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='lectureRef',
            field=models.ForeignKey(to='OCWApp.Lecture'),
        ),
    ]
