from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from movies.models import Movie
from .utils import calculate_cart_total
from .models import Order, Item
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.generic import ListView
from django.core.paginator import Paginator
from .models import CheckoutFeedback
from .forms import CheckoutFeedbackForm


def index(request):
    cart_total = 0
    movies_in_cart = []
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids != []):
        movies_in_cart = Movie.objects.filter(id__in=movie_ids)
        cart_total = calculate_cart_total(cart, movies_in_cart)

    template_data = {}
    template_data['title'] = 'Cart'
    template_data['movies_in_cart'] = movies_in_cart
    template_data['cart_total'] = cart_total
    return render(request, 'cart/index.html', {'template_data': template_data})

def add(request, id):
    get_object_or_404(Movie, id=id)
    cart = request.session.get('cart', {})
    cart[id] = request.POST['quantity']
    request.session['cart'] = cart
    return redirect('cart.index')

def clear(request):
    request.session['cart'] = {}
    return redirect('cart.index')

@login_required
def purchase(request):
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids == []):
        return redirect('cart.index')
    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies_in_cart)
    order = Order()
    order.user = request.user
    order.total = cart_total
    order.save()
    for movie in movies_in_cart:
        item = Item()
        item.movie = movie
        item.price = movie.price
        item.order = order
        item.quantity = cart[str(movie.id)]
        item.save()
    request.session['cart'] = {}
    template_data = {
        'title': 'Purchase confirmation',
        'order_id': order.id,
        'order': order,
        'show_feedback_modal': True  # Flag to show the feedback modal
    }
    return render(request, 'cart/purchase.html',
        {'template_data': template_data})

def submit_checkout_feedback(request):
    """Handle AJAX submission of checkout feedback"""
    if request.method == 'POST':
        form = CheckoutFeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True,
                'message': 'Thank you for your feedback!'
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    return JsonResponse({'success': False, 'message': 'Invalid request'})

class FeedbackListView(ListView):
    """Display all checkout feedback on a separate page"""
    model = CheckoutFeedback
    template_name = 'checkout_feedback_list.html'
    context_object_name = 'feedback_list'
    paginate_by = 10
    
    def get_queryset(self):
        return CheckoutFeedback.objects.all().order_by('-created_at')

# Alternative function-based view for feedback list if you prefer
def feedback_list_view(request):
    """Function-based view to display all feedback"""
    feedback_list = CheckoutFeedback.objects.all().order_by('-created_at')
    paginator = Paginator(feedback_list, 10)  # Show 10 feedback per page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'feedback_list': page_obj,
        'total_feedback': feedback_list.count()
    }
    return render(request, 'checkout_feedback_list.html', context)
