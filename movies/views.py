from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth.forms import AuthenticationForm
from django.http.response import JsonResponse
from .models import Movie, Genre, MovieReview
from .forms import MovieReviewForm

@require_GET
def index(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, 'movies/index.html', context)


@require_GET
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    comments = movie.moviereview_set.all()
    movie_comment_form = MovieReviewForm()
    context = {
        'movie': movie,
        'movie_comment_form': movie_comment_form,
        'comments': comments,
    }
    return render(request, 'movies/detail.html', context)


@require_POST
def movie_create_comment(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    movie_comment_form = MovieReviewForm(request.POST)
    if movie_comment_form.is_valid():
        comment = movie_comment_form.save(commit=False)
        comment.movie = movie
        comment.user = request.user
        comment.save()
        return redirect('movies:detail', movie.pk)
    context = {
        'movie_comment_form': movie_comment_form,
        'movie': movie,
        'comments': movie.moviereview_set.all(),
    }
    return render(request, 'movies/detail.html', context)

@require_POST
def movie_comments_delete(request, movie_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(MovieReview, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('movies:detail', movie_pk)

@require_GET
def recommend(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, 'movies/recommend.html', context)


@require_GET
def recommendpopularity(request):
    if request.user.is_authenticated:
        movies = Movie.objects.order_by('-popularity')[:20]
        context = {
            'movies':movies,
        }
        return render(request, 'movies/recommendpopularity.html', context)
    return render(request, 'accounts/login.html', context)

@require_GET
def recommendvoteaverage(request):
    if request.user.is_authenticated:
        movies = Movie.objects.order_by('-vote_average')[:20]
        context = {
            'movies':movies,
        }
        return render(request, 'movies/recommendvoteaverage.html', context)
    return render(request, 'accounts/login.html', context)

@require_GET
def recommendgenre(request):
    if request.user.is_authenticated:
        if request.GET.get('genreId'):
            genrebox = request.GET.get('genreId')
            movies = Movie.objects.filter(genre_ids=genrebox)
            movies_json = []

            for movie in movies:
                movies_json.append({
                    'title': movie.title,
                })
            return JsonResponse({'text': movies_json})

        genres = Genre.objects.all()
        context = {
            'genres': genres,
        }
        return render(request, 'movies/recommendgenre.html', context)
    return render(request, 'accounts/login.html', context)