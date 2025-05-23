from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Ad, ExchangeProposal
from .forms import AdForm, ExchangeProposalForm, SignUpForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import login



@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('ad_detail', ad_id = ad.id)
    else:
        form = AdForm()
    return render(request,'ads/create_ad.html', {'form':form})

@login_required
def edit_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id, user=request.user)
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ad_detail', ad_id=ad.id)
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/edit_ad.html', {'form': form})

@login_required
def delete_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id, user=request.user)
    if request.method == 'POST':
        ad.delete()
        return redirect('ad_list')
    return render(request, 'ads/delete_ad.html', {'ad': ad})

def ad_list(request):
    ads = Ad.objects.all()
    query = request.GET.get('q')
    category = request.GET.get('category')
    condition = request.GET.get('condition')

    if query:
        ads = ads.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category:
        ads = ads.filter(category__iexact=category)
    if condition:
        ads = ads.filter(condition__iexact=condition)

    paginator = Paginator(ads, 10)  # Show 10 ads per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'ads/ad_list.html', {'page_obj': page_obj})

def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    return render(request, 'ads/ad_detail.html', {'ad': ad})

@login_required
def create_exchange_proposal(request):
    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.status = 'pending'
            proposal.save()
            return redirect('proposal_detail', proposal_id=proposal.id)
    else:
        form = ExchangeProposalForm()
    return render(request, 'ads/create_proposal.html', {'form': form})

@login_required
def proposal_detail(request, proposal_id):
    proposal = get_object_or_404(ExchangeProposal, id=proposal_id)
    return render(request, 'ads/proposal_detail.html', {
        'proposal': proposal
    })

@login_required
def update_exchange_proposal(request, proposal_id):
    proposal = get_object_or_404(ExchangeProposal, id=proposal_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(ExchangeProposal.STATUS_CHOICES):
            proposal.status = status
            proposal.save()
            return redirect('proposal_detail', proposal_id=proposal.id)
    return render(request, 'ads/update_proposal.html', {'proposal': proposal})

@login_required
def proposal_list(request):
    proposals = ExchangeProposal.objects.filter(
        Q(ad_sender__user=request.user) |
        Q(ad_receiver__user=request.user)
    ).distinct()
    sender = request.GET.get('sender')
    receiver = request.GET.get('receiver')
    status = request.GET.get('status')

    if sender:
        proposals = proposals.filter(ad_sender__user__username=sender)
    if receiver:
        proposals = proposals.filter(ad_receiver__user__username=receiver)
    if status:
        proposals = proposals.filter(status=status)

    return render(request, 'ads/proposal_list.html', {'proposals': proposals})


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('ad_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup1.html', {'form': form})