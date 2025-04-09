from django.shortcuts import render

# Create your views here.
@login_required(login_url='login')
def createListing(request):
    form = ListingForm()
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            return redirect('home')  # or a listing confirmation page
    return render(request, 'base/create_listing.html', {'form': form})

