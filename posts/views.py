import random
from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from marketing.models import Signup
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q

from posts.branding_data import branding




###########################################################################################################
####################### Utility Functions #################################################################

def get_category_count():
    queryset = Post.objects.values('categories__title').annotate(Count('categories__title'))
    return queryset


def get_category_data():
    category_data = {}
    all_categories = Category.objects.all()
    for each in all_categories:
        cat_title = str(each.title)
        num_cat = len(Post.objects.filter(categories=each))
        inner_dict = {'category_id': each.id, 'category_slug': each.slug, 'category_count': num_cat}
        category_data[cat_title] = inner_dict

    return category_data





def get_topic_list():
    queryset = Post.objects.values('categories__title')
    return queryset


def boiler_plate_data():
    boiler_plate_dict = {}
    category_count = get_category_count()

    # BRANDING DATA
    branding_data = branding.branding_data

    # HEADER DATA
    header_topic_list = Category.objects.all()

    # FEATURED
    all_featured_posts = Post.objects.filter(featured=True)
    featured = random.sample(list(all_featured_posts), 3)

    # SIDE_RECENT
    most_recent = Post.objects.order_by('-timestamp')[:8]

    # RECOMMENDED
    all_recommended_posts = Post.objects.filter(recommended=True)
    rec_len = min(len(all_recommended_posts), 6)
    recommended = random.sample(list(all_recommended_posts), rec_len)

    # CATEGORY_DATA
    category_data = get_category_data()

    boiler_plate_dict = {

        'most_recent': most_recent,
        'category_count': category_count,
        'featured': featured,
        'recommended': recommended,
        'header_topic_list': header_topic_list,
        'category_data': category_data,
        'branding_data': branding_data,

    }
    return boiler_plate_dict


def get_paginated_queryset(post_list, request):
    #Paginator
    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    return paginated_queryset


def get_search_results(post_list, request):
    message = ''
    results = False

    query = request.GET.get('q')
    if query:
        post_list = post_list.filter(
            Q(title__icontains=query),
            Q(overview__icontains=query),
            Q(content__icontains=query),
        ).distinct()
        results = True
        if not post_list:
            message = f"No search results found for '{query}'. Please try again."
            results = False

    return post_list, message, results, query

###########################################################################################################
####################### Grid Views ########################################################################

def search(request):

    post_list = Post.objects.all()

    #SEARCH - update post_list via get_search_results function
    post_list, message, results, query = get_search_results(post_list, request)
    view_title = f'Search Results for: {query}'

    paginated_queryset = get_paginated_queryset(post_list, request)
    pag_len = len(paginated_queryset)
    print(f'paginated_queryset: {pag_len}')

    context = {
        'post_list': post_list,
        'results': results,
        'message': message,
        'queryset': paginated_queryset,
        'query': query,
        'view_title': view_title,
    }
    context.update(boiler_plate_data())

    return render(request, 'search_results.html', context)

#comment


def by_topic(request, topic):
    view_topic = Category.objects.get(slug=topic)
    view_title = f'Articles By Topic: {view_topic} '
    post_list = Post.objects.filter(categories__slug=topic)

    paginated_queryset = get_paginated_queryset(post_list, request)
    pag_len = len(paginated_queryset)
    print(f'paginated_queryset: {pag_len}')

    context = {
        'post_list': post_list,
        'queryset': paginated_queryset,
        'view_title': view_title,
    }
    context.update(boiler_plate_data())

    return render(request, 'posts_grid_view.html', context)

def top_pick(request):
    view_title = 'Our Top Picks'
    post_list = Post.objects.filter(top_pick=True)

    paginated_queryset = get_paginated_queryset(post_list, request)

    context = {
        'post_list': post_list,
        'queryset': paginated_queryset,
        'view_title': view_title,
    }
    context.update(boiler_plate_data())

    return render(request, 'posts_grid_view.html', context)


def newest(request):
    view_title = 'Our Newest Articles'
    post_list = Post.objects.order_by('-timestamp')[:50]

    paginated_queryset = get_paginated_queryset(post_list, request)

    context = {
        'post_list': post_list,
        'queryset': paginated_queryset,
        'view_title': view_title,
    }
    context.update(boiler_plate_data())

    return render(request, 'posts_grid_view.html', context)

###########################################################################################################
####################### Post Details Views ########################################################################


def post_by_slug(request, slug):
    post = get_object_or_404(Post, slug=slug)


    # SIMILAR
    post_category = post.primary_category

    all_similar_posts = Post.objects.filter(primary_category=post_category)

    if len(all_similar_posts) > 2:
        display_similar = True
        similar_sample = random.sample(list(all_similar_posts), 3)
    else:
        display_similar = False
        similar_sample = all_similar_posts

    context = {
        'post': post,
        'display_similar': display_similar,
        'similar': similar_sample,
    }
    context.update(boiler_plate_data())

    return render(request, 'post_detail_view.html', context)


def post_by_id(request, id):
    post = get_object_or_404(Post, id=id)
    # post_categories = post.categories
    # print(post_categories)
    category_count = get_category_count()

    #HEADER DATA
    header_topic_list = Category.objects.all()

    #FEATURED
    all_featured_posts = Post.objects.filter(featured=True)
    featured = random.sample(list(all_featured_posts), 3)

    #SIDE_RECENT
    most_recent = Post.objects.order_by('-timestamp')[:3]

    #RECOMMENDED
    all_recommended_posts = Post.objects.filter(recommended=True)
    rec_len = min(len(all_recommended_posts), 9)
    recommended = random.sample(list(all_recommended_posts), rec_len)

    #SIMILAR
    # all_similar_posts = Post.objects.filter(featured=True, categories="")
    # recommended = random.sample(list(all_featured_posts), 3)



    context = {
        'post': post,
        'most_recent': most_recent,
        'category_count': category_count,
        'featured': featured,
        'recommended': recommended,
        'header_topic_list': header_topic_list,
    }
    return render(request, 'post_detail_view.html', context)


###########################################################################################################
#################################### Legal ################################################################

def terms_and_conditions(request):
    # BRANDING DATA
    branding_data = branding.branding_data

    context = {
        'branding_data': branding_data,
    }

    return render(request, 'terms_and_conditions.html', context)


def privacy_policy(request):
    # BRANDING DATA
    branding_data = branding.branding_data

    context = {
        'branding_data': branding_data,
    }

    return render(request, 'privacy_policy.html', context)

def do_not_sell(request):
    # BRANDING DATA
    branding_data = branding.branding_data

    context = {
        'branding_data': branding_data,
    }

    return render(request, 'do-not-sell.html', context)







###########################################################################################################
####################### Unused / Obsolete for Reference ###################################################


def index(request):
    all_featured_posts = Post.objects.filter(featured=True)
    featured = random.sample(list(all_featured_posts), 3)
    latest = Post.objects.order_by('-timestamp')[0:3]

    #HEADER DATA
    header_topic_list = Category.objects.all()

    if request.method == "POST":
        email = request.POST['email']
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()


    context = {
        'object_list': featured,
        'latest': latest,
        'header_topic_list': header_topic_list,
    }
    return render(request, 'home.html', context)


