from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from posts.models import BBSPosts, BBSReply

def viewSinglePost(request, postID):
    postObj = BBSPosts.objects.get(id = postID)
    replies = BBSReply.objects.filter(parent = postObj)

    context = {
        'postObj': postObj,
        'replies': replies,
    }
    return render(request, 'posts/post_display.html', context)

def partialPostReturn(request):
    if request.user.userProfile.department >= 6:
        postFilter = BBSPosts.objects.filter(priority = 1)
    else:
        postFilter = BBSPosts.objects.filter(priority = 1, department = request.user.userProfile.department)

    stickyPosts = BBSPosts.objects.filter(priority = 2)
    storewidePosts = BBSPosts.objects.filter(department = 8)

    paginator = Paginator(postFilter.order_by('-created_at'), 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'storewidePosts': storewidePosts,
        'stickyPosts': stickyPosts,
    }
    return render(request, 'posts/partial_newpost_return.html', context)

def createNewPost(request):
    if request.method == 'POST':
        userPosting = request.user
        if request.user.userProfile.department >= 6:
            postFilter = BBSPosts.objects.filter(priority = 1)
        else:
            postFilter = BBSPosts.objects.filter(priority = 1, department = request.user.userProfile.department)

        if request.user.userProfile.access_level == 1:
            newPost = BBSPosts.objects.create(
                author = userPosting,
                content = request.POST['bbsPostMessage']
            )
            newPost.save()
        else:
            newPost = BBSPosts.objects.create(
                author = userPosting,
                content = request.POST['bbsPostMessage'],
                priority = request.POST['bbsPostPriority'],
                department = request.POST['bbsPostDepartment']
            )
            newPost.save()

        stickyPosts = BBSPosts.objects.filter(priority = 2)
        storewidePosts = BBSPosts.objects.filter(department = 8)

        paginator = Paginator(postFilter.order_by('-created_at'), 5)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'page_obj': page_obj,
            'storewidePosts': storewidePosts,
            'stickyPosts': stickyPosts,
        }
        return render(request, 'posts/partial_newpost_return.html', context)
    else:
        messages.error(request, 'Sorry, you do not have permission to do this.', extra_tags = 'danger')
        return redirect('bbsHome')

def replyToPost(request):
    pass

def likePost(request, postID):
    pass

def deletePostConfirm(request, postID):
    postToDelete = BBSPosts.objects.get(id = postID)
    context = {
        'postInfo': postToDelete,
        'postType': 1
    }
    return render(request, 'posts/confirm_delete.html', context)

def deleteReplyConfirm(request, postID):
    replyToDelete = BBSReply.objects.get(id = postID)
    context = {
        'postInfo': replyToDelete,
        'postType': 2
        }
    return render(request, 'posts/confirm_delete.html', context)

def deletePostFinal(request, postID):
    if request.method == 'POST':
        deletePost = BBSPosts.objects.get(id = request.POST['postID'])
        deletePost.delete()
        messages.success(request, 'Done. The post has been successfully deleted!')
        return redirect('bbsHome')
    else:
        messages.error(request, 'Sorry, you do not have permission to do this.', extra_tags = 'danger')
        return redirect('bbsHome')

def deleteReplyFinal(request, postID):
    if request.method == 'POST':
        deleteReply = BBSReply.objects.get(id = request.POST['replyID'])
        deleteReply.delete()
        messages.success(request, 'Done. The reply has been successfully deleted!')
        return redirect('bbsHome')
    else:
        messages.error(request, 'Sorry, you do not have permission to do this.', extra_tags = 'danger')
        return redirect('bbsHome')