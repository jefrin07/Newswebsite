from django.shortcuts import render,redirect, get_object_or_404
from .forms import RegisterForm,PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from django.contrib.auth.models import User
from .models import Post,Category
from django.http import HttpResponseForbidden
from django.db.models import Q

# Create your views here.
@login_required(login_url='/login')
def create_post(request):
    if request.method=='POST':
        form=PostForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.save()
            return redirect('/home')
    else:
        form=PostForm()
    return render(request,'main/create_post.html',{"form":form})

@login_required(login_url='/login') 
def home(request):
    categories = Category.objects.all()  # Fetch all categories from the database

    category_id = request.GET.get('category', None)
    approved_posts = Post.objects.filter(status='Approved')

    selected_category = None  # Set the default selected_category value
    if category_id:
        approved_posts = approved_posts.filter(category_id=category_id)
        selected_category = int(category_id)  # Convert category_id to int for comparison
    
    return render(request, 'main/home.html', {'approved_posts': approved_posts, 'categories': categories, 'selected_category': selected_category})



def sign_up(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('/home')
    else:
        form=RegisterForm()
    return render(request,'registration/sign_up.html',{"form":form})

@login_required(login_url='/login')
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Check if the user is the author of the post or a superuser
    if request.user == post.author or request.user.is_superuser:
        if request.method == "POST" and "confirm_delete" in request.POST:
            post.delete()
            return redirect('home')
        else:
            return render(request, 'main/delete_post.html', {'post': post})

    # If not authorized, handle the response accordingly (redirect, error message, etc.)
    return HttpResponseForbidden("You are not authorized to delete this post.")

@login_required(login_url='/login')
def user_logout(request):
    logout(request)
    return redirect('/login')

@login_required(login_url='/login')
def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('/home')  # Redirect to the desired page after update
    else:
        form = PostForm(instance=post)
    
    return render(request, 'main/update_post.html', {'form': form, 'post': post})

@login_required(login_url='/login')
def pending_posts(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            post_id = request.POST.get('post_id')  # Assuming you have a hidden input for post_id in the form
            post = Post.objects.get(pk=post_id)
            post.status = 'Approved'
            post.save()
            return redirect('home')  # Redirect to the home page after approving the post
        else:
            pending = Post.objects.filter(status='Pending')
            pending_count = Post.objects.filter(status='Pending').count() 
            return render(request, 'main/pending_post.html', {'pending_posts': pending,'pending_count': pending_count})
    else:
        # Handle scenarios for non-superusers if needed
        pass

@login_required(login_url='/login')
def reject_post(request, post_id):
    if request.user.is_superuser and request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        post.status = 'Rejected'
        post.save()
        return redirect('pending_posts')  # Redirect back to pending posts after the action
    else:
        # Handle scenarios for non-superusers or invalid requests
        pass

@login_required(login_url='/login')
def post_status(request):
    if request.user.is_superuser:
        all_posts = Post.objects.all()
        return render(request, 'main/post_status.html', {'all_posts': all_posts})
    else:
        current_user = request.user
        user_posts = Post.objects.filter(author=current_user)
        return render(request, 'main/post_status.html', {'user_posts': user_posts})
    
@login_required(login_url='/login')
def view_all_users(request):
    if request.user.is_superuser:
        users = User.objects.all()
        return render(request, 'main/all_users.html', {'users': users})
    
from django.http import JsonResponse
from django.db.models import Q
from .models import Post  # Assuming 'Post' is the model used for search


@login_required(login_url='/login')
def searchBar(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            # Filter approved posts based on author's username and approval status
            posts = Post.objects.filter(
                Q(status='Approved') & (Q(title__icontains=query) | Q(author__username__icontains=query))
            )
            return render(request, 'main/search.html', {"posts": posts})
    
    # Handle cases where there's no query or no matching posts
    print("No Posts")
    return render(request, 'main/search.html')