from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.messages import get_messages
from django.db.models import Q
from urlparse import urlparse, parse_qs
from MySQLdb import IntegrityError
from OCWApp.models import Category
from OCWApp.models import SubCategory
from OCWApp.models import Lecture
from OCWApp.models import Section
from OCWApp.models import Chapter
from OCWApp.models import Provider
from OCWApp.models import Institute
from OCWApp.models import Clip
from OCWApp.models import TagModel
from OCWApp.forms import DocumentForm
from OCWApp.forms import SearchForm


import datetime
import json


def convert_time(str_time):
    int_time = 0
    time_list = str_time.split(':')
    if len(time_list) == 2:
        int_time = int(time_list[0])*60+int(time_list[1])
    else:
        if len(time_list) == 3:
            int_time = int(time_list[0])*60*60+int(time_list[1])*60+int(time_list[2])
    return int_time

def getvideotype(media_url):
    str_video_type = "video/youtube"
    if media_url.find("rtmp") >= 0:
        str_video_type = "video/rtmp"
    else:
        if media_url.find(".mp4") >= 0:
            str_video_type = "video/mp4"
    return str_video_type

def dropyoutubeplaylist(media_url):
    str_list = media_url.split('&');
    return str_list[0]

def getyoutubeid(media_url):
    url_data = urlparse(media_url)
    query = parse_qs(url_data.query)
    if 'v' in query:
        return query["v"][0]
    return url_data.path

def getyoutubethumbnailurl(youtube_id):
    return "http://i1.ytimg.com/vi/" + youtube_id + "/hqdefault.jpg"


def addcategory(lecture):
    newcategory = Category(category_title=lecture['category'])
    if Category.objects.filter(category_title = lecture['category']).count()==0:
        newcategory.save()
    else:
        newcategory = Category.objects.get(category_title = lecture['category'])
    return newcategory

def addsubcategory(lecture, category):
    newsubcategory = SubCategory(categoryRef=category, subcategory_title=lecture['subcategory'])
    if SubCategory.objects.filter(subcategory_title=lecture['subcategory']).count() == 0:
        newsubcategory.save()
    else:
        newsubcategory = SubCategory.objects.get(subcategory_title=lecture['subcategory'])
    return newsubcategory

def addlecture(lecture, category, subcategory):
    newlecture = Lecture(
        categoryRef = category,
        subcategoryRef = subcategory,
        description = lecture['description'],
        subject=lecture['subject'],
        image_url=lecture['image_url'])
    newlecture.setlevel(lecture['level'])
    if Lecture.objects.filter(subject=lecture['subject']).count()==0:
        newlecture.save()
    else:
        newlecture = Lecture.objects.get(subject=lecture['subject'])
    return newlecture

def addchapter(chapter, lectureobj):
    newchapter = Chapter(
        lectureRef = lectureobj,
        chapter_title = chapter['chapter_title']
    )
    if Chapter.objects.filter(Q(lectureRef=lectureobj) & Q(chapter_title=chapter['chapter_title'])).count()==0:
        newchapter.save()
    else:
        newchapter = Chapter.objects.get(Q(lectureRef=lectureobj) & Q(chapter_title=chapter['chapter_title']))
    return newchapter

def addsection(section, lectureobj, chapterobj):
    newsection = Section(
        lectureRef = lectureobj,
        chapterRef = chapterobj,
        section_title = section['section_title']
    )
    if Section.objects.filter(Q(lectureRef=lectureobj) & Q(chapterRef=chapterobj) & Q(section_title=section['section_title'])).count()==0:
        newsection.save()
    else:
        newsection = Section.objects.get(Q(lectureRef=lectureobj) & Q(chapterRef=chapterobj) & Q(section_title=section['section_title']))
    return newsection

def getstringvalue(clip, field):
    if field in clip:
        return clip[field]
    return "null"

def getstringvaluewithdefault(clip, field, default_field):
    if field in clip:
        return clip[field]
    return clip[default_field]

def getintvalue(clip, field):
    if field in clip:
        return clip[field]
    return 0

def addifnot(modelobj, strname):
    newobject = modelobj(name=strname)
    if modelobj.objects.filter(name = strname).count()==0:
        newobject.save()
    else:
        newobject = modelobj.objects.get(name = strname)
    return newobject

def addclip(clip, lectureobj, chapterobj, sectionobj):
    str_media_url = clip['media_url']
    str_video_type = getvideotype(str_media_url)
    str_thumbnail_url = clip['thumbnail_url']
    str_youtube_id = "null"
    if str_video_type == "video/youtube":
        str_media_url = dropyoutubeplaylist(str_media_url)
        str_youtube_id = getyoutubeid(str_media_url)
        str_thumbnail_url = getyoutubethumbnailurl(str_youtube_id)

    if Clip.objects.filter(Q(sectionRef=sectionobj) & Q(media_url=str_media_url) & Q(start_time=convert_time(clip['start_time']))).count()!=0:
        return Clip.objects.get(Q(sectionRef=sectionobj) & Q(media_url=str_media_url) & Q(start_time=convert_time(clip['start_time'])))

    str_subtitles = getstringvalue(clip, 'subtitles')
    rank = getintvalue(clip, 'init_rank')
    rate = getintvalue(clip, 'review_rate')
    counts = getintvalue(clip, 'view_counts')
    str_description = getstringvalue(clip, 'description')
    str_original_provider = getstringvaluewithdefault(clip, 'original_provider', 'provider')
    str_original_institute = getstringvaluewithdefault(clip, 'original_institute', 'institute')
    newprovider = addifnot(Provider, clip['provider'])
    neworiginal_provider = addifnot(Provider, str_original_provider)
    newinstitute = addifnot(Institute, clip['institute'])
    neworiginal_institute = addifnot(Institute, str_original_institute)
    newclip = Clip(
        lectureRef = lectureobj,
        chapterRef = chapterobj,
        sectionRef = sectionobj,
        original_providerRef = neworiginal_provider,
        original_instituteRef = neworiginal_institute,
        providerRef = newprovider,
        instituteRef = newinstitute,
        language_type = clip['type'],
        source_from = clip['from'],
        description = str_description,
        media_url = str_media_url,
        video_type = str_video_type,
        thumbnail_url = str_thumbnail_url,
        youtube_id = str_youtube_id,
        caption_url = clip['caption_url'],
        created_date = clip['created_date'].strip(),
        uploaded_date = datetime.date.today,
        running_time = convert_time(clip['running_time']),
        start_time = convert_time(clip['start_time']),
        end_time = convert_time(clip['end_time']),
        subtitles = str_subtitles,
        init_rank = rank,
        review_rate = rate,
        view_counts = counts
    )
    newclip.save()
    return newclip;

def addtags(clip, clipobj):
    if len(clip['tags']) > 0:
        tag_list = []
        for newtag in clip['tags']:
            tag_list.append(TagModel.objects.get_or_create(tag=newtag)[0])
        for newtag in tag_list:
            clipobj.tags.add(newtag)
        clipobj.save()

def insert_data_to_model(js_obj):
    for lecture in js_obj['Lecture']:
        newcategory = addcategory(lecture)
        newsubcategory = addsubcategory(lecture, newcategory)
        newlecture = addlecture(lecture, newcategory, newsubcategory)
        for chapter in lecture['chapters']:
            newchapter = addchapter(chapter, newlecture)
            for section in chapter['sections']:
                newsection = addsection(section, newlecture, newchapter)
                for clip in section['clips']:
                    newclip = addclip(clip, newlecture, newchapter, newsection)
                    addtags(clip, newclip)
    return "Success"

def home(request):
    lectures = Lecture.objects.filter(home_recommendation=True)
    form = SearchForm()
    return render_to_response(
        'index.html',
        {'form': form, 'lectures':lectures},
        context_instance=RequestContext(request)
    )

def classes(request):
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    lectures = Lecture.objects.all().order_by('-level', 'categoryRef_id', 'subcategoryRef_id')
    levels = lectures.values('level').distinct()
    form = SearchForm()
    return render_to_response(
        'lectures_by_subject.html',
        {'form': form, 'levels':levels, 'categories':categories, 'subcategories':subcategories, 'lectures':lectures, 'user': request.user},
        context_instance=RequestContext(request)
    )

def searchresult(request, keyword):
    form = SearchForm()
    keyword_list = keyword.split(u'_')
    keyword_qlist = Q()
    for i in keyword_list:
        keyword_qlist.add(Q(tags__tag__icontains=i), Q.AND)
    clips = Clip.objects.filter(keyword_qlist).distinct().order_by('lectureRef_id', 'providerRef_id')

    return render(request, 'searchresult.html', {'form': form, 'clips' : clips})

def lecture_tree(request, lecture_id):
    lectures = Lecture.objects.filter(id=lecture_id)
    clips = Clip.objects.filter(lectureRef_id=lecture_id).order_by('chapterRef_id', 'sectionRef_id')
    clips_by_youtubeid = Clip.objects.filter(lectureRef_id=lecture_id).order_by('youtube_id', 'start_time')
    return render(request, 'lecture_tree.html', {'lecture':lectures[0], 'clips':clips, 'clips_by_youtubeid':clips_by_youtubeid})

def playclip(request, clip_id):
    requested_clip = Clip.objects.filter(id=clip_id)
    lecture_id = requested_clip.values('lectureRef_id')
    provider_id = requested_clip.values('providerRef_id')
    institute_id = requested_clip.values('instituteRef_id')
    lectures = Lecture.objects.filter(id=lecture_id)
    clips = Clip.objects.filter(Q(lectureRef_id=lecture_id) & Q(providerRef_id=provider_id) & Q(instituteRef_id=institute_id)).order_by('chapterRef_id', 'sectionRef_id')
    clips_by_youtubeid = Clip.objects.filter(Q(lectureRef_id=lecture_id) & Q(providerRef_id=provider_id) & Q(instituteRef_id=institute_id)).order_by('youtube_id', 'start_time')
    return render(request, 'lecture_tree.html', {'lecture':lectures[0], 'clips':clips, 'clips_by_youtubeid':clips_by_youtubeid, 'requested_clip':requested_clip})


def searchpage(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            input_keyword = form.cleaned_data['search_keyword']
            keyword_list = input_keyword.split(u' ')
            search_keyword="_".join(keyword_list)
            redirect_url = reverse('searchresult', args=(search_keyword,))
            return HttpResponseRedirect(redirect_url)

def uploadresult(request):
    return render(request, 'message.html')

def uploadcourse(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            js_obj={}
            try:
                docfile = request.FILES['docfile']
                js_obj = json.loads(docfile.read())
            except ValueError as err:
                messages.info(request, err);
                return HttpResponseRedirect('/uploadcourse/uploadresult/')
            msg = insert_data_to_model(js_obj)
            messages.info(request, msg);
            return HttpResponseRedirect('/uploadcourse/uploadresult/')
    else:
        form = DocumentForm()
    return render_to_response(
        'upload.html',
        {'form': form},
        context_instance=RequestContext(request)
    )
