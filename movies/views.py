from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Petition
from django.contrib.auth.decorators import login_required
from .forms import PetitionForm

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
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html',
                  {'template_data': template_data})

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

    


