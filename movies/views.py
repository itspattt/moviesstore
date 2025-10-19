from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Petition, Rating
from django.contrib.auth.decorators import login_required
from .forms import PetitionForm
from django.db.models import Avg 

# Create your views here.
@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html',
            {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
    
@login_required
def like_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if (request.user not in review.whoLiked.all()):
        review.num_likes += 1
        review.whoLiked.add(request.user)
    else:
        review.num_likes -= 1
        review.whoLiked.remove(request.user)
    review.save()
    return redirect('movies.show', id=id)

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html',
                  {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie).order_by('-num_likes')

    # Get user rating if logged in
    user_rating = None
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(movie=movie, user=request.user).first()

    # Handle rating submission
    if request.method == "POST" and "score" in request.POST:
        score = int(request.POST.get("score"))
        Rating.objects.update_or_create(
            movie=movie,
            user=request.user,
            defaults={"score": score}
        )
        return redirect("movies.show", id=id)

    # Calculate average rating
    avg_rating = movie.ratings.aggregate(Avg("score"))["score__avg"] or 0

    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews

    return render(request, 'movies/show.html', {
        'template_data': template_data,
        'user_rating': user_rating,
        'avg_rating': round(avg_rating, 1)
    })


@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment']!= '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
    
@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id,
        user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

def petition_list(request):
    petitions = Petition.objects.all()
    template_data = {}
    template_data['Petitions'] = petitions
    return render(request, 'movies/pIndex.html', {"template_data": template_data})

def petition_vote(request, id):
    petition = get_object_or_404(Petition, id=id)
    petition.num_votes += 1
    petition.whoVoted.add(request.user)
    petition.save()

    return redirect('movies.petition_list')

def create_petition(request):
    if (request.method == 'POST'):
        form = PetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)
            petition.user = request.user
            petition.num_votes = 0
            petition.save()
            return redirect('movies.petition_list')
    else:
        form = PetitionForm()
    
    return render(request, 'movies/create.html', {'form': form})

def movie_map_page(request):
    return render(request, "movies/trending.html")

from django.http import JsonResponse
from collections import defaultdict
from math import exp
from django.utils import timezone
from datetime import timedelta
from cart.models import Order, Item

def movie_map_data(request):
    """
    Returns JSON data for regions with top trending movies.
    """
    days_window = 7   # last 7 days
    top_n = 5         # top 5 movies per region
    decay_factor = 0.3

    cutoff = timezone.now() - timedelta(days=days_window)
    items = Item.objects.filter(order__date__gte=cutoff).select_related('movie', 'order')

    # Aggregate weighted scores per region
    scores = defaultdict(lambda: defaultdict(float))
    coords = {}  # store coordinates per region

    for item in items:
        region = f"{item.order.latitude},{item.order.longitude}"  # simple region key
        coords[region] = {"lat": item.order.latitude or 0, "lng": item.order.longitude or 0}

        days_ago = (timezone.now() - item.order.date).days
        weight = exp(-decay_factor * days_ago) * item.quantity  # weight by recency and quantity
        scores[region][item.movie.name] += weight

    # Build top N per region
    result = []
    for region, movie_dict in scores.items():
        sorted_movies = sorted(movie_dict.items(), key=lambda x: x[1], reverse=True)[:top_n]
        trending_list = [{"title": title, "score": round(score, 2)} for title, score in sorted_movies]

        result.append({
            "region": region,
            "lat": coords[region]["lat"],
            "lng": coords[region]["lng"],
            "trending": trending_list
        })

    return JsonResponse(result, safe=False)

