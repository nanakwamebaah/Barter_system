import os
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ads.models import Ad, ExchangeProposal

class AdAndProposalTests(TestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username='user1', password='pass1')
        self.user2 = User.objects.create_user(username='user2', password='pass2')
        # Client instances for both users
        self.client1 = Client()
        self.client1.login(username='user1', password='pass1')
        self.client2 = Client()
        self.client2.login(username='user2', password='pass2')
        # Create sample ads
        self.ad1 = Ad.objects.create(user=self.user1, title='Alpha', description='First', category='CatA', condition='new')
        self.ad2 = Ad.objects.create(user=self.user2, title='Beta', description='Second', category='CatB', condition='used')

    def test_create_ad(self):
        data = {
            'title': 'Gamma',
            'description': 'Third',
            'image_url': '',
            'category': 'CatC',
            'condition': 'new'
        }
        response = self.client1.post(reverse('create_ad'), data)
        self.assertEqual(response.status_code, 302)  # redirect on success
        self.assertTrue(Ad.objects.filter(title='Gamma', user=self.user1).exists())

    def test_edit_ad(self):
        url = reverse('edit_ad', args=[self.ad1.id])
        response = self.client1.post(url, {
            'title': 'Alpha Updated',
            'description': 'First Updated',
            'image_url': '',
            'category': 'CatA',
            'condition': 'used'
        })
        self.assertEqual(response.status_code, 302)
        self.ad1.refresh_from_db()
        self.assertEqual(self.ad1.title, 'Alpha Updated')
        self.assertEqual(self.ad1.condition, 'used')

    def test_delete_ad(self):
        url = reverse('delete_ad', args=[self.ad1.id])
        response = self.client1.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Ad.objects.filter(id=self.ad1.id).exists())

    def test_search_and_filter_ads(self):
        # search by keyword
        resp = self.client1.get(reverse('ad_list') + '?q=Alpha')
        self.assertContains(resp, 'Alpha')
        self.assertNotContains(resp, 'Beta')
        # filter by category
        resp = self.client1.get(reverse('ad_list') + '?category=CatB')
        self.assertContains(resp, 'Beta')
        self.assertNotContains(resp, 'Alpha')
        # filter by condition
        resp = self.client1.get(reverse('ad_list') + '?condition=new')
        self.assertContains(resp, 'Alpha')
        self.assertNotContains(resp, 'Beta')

    def test_create_exchange_proposal(self):
        data = {
            'ad_sender': self.ad1.id,
            'ad_receiver': self.ad2.id,
            'comment': 'Let us swap'
        }
        response = self.client1.post(reverse('create_proposal'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ExchangeProposal.objects.filter(ad_sender=self.ad1, ad_receiver=self.ad2).exists())

    def test_update_exchange_proposal(self):
        proposal = ExchangeProposal.objects.create(ad_sender=self.ad1, ad_receiver=self.ad2, comment='Swap', status='pending')
        url = reverse('update_proposal', args=[proposal.id])
        # user2 (receiver) accepts
        response = self.client2.post(url, {'status': 'accepted'})
        self.assertEqual(response.status_code, 302)
        proposal.refresh_from_db()
        self.assertEqual(proposal.status, 'accepted')


    
    def test_proposal_list_filters(self):
        # first, create “Swap” from user1→user2
        ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment='Swap',
            status='pending'
        )
        # then “Offer” from user2→user1
        ExchangeProposal.objects.create(
            ad_sender=self.ad2,
            ad_receiver=self.ad1,
            comment='Offer',
            status='pending'
        )

        # now user1 should see both
        resp = self.client1.get(reverse('proposal_list'))
        self.assertContains(resp, 'Swap')
        self.assertContains(resp, 'Offer')
        # filter by sender=user2
        resp = self.client1.get(reverse('proposal_list') + '?sender=user2')
        self.assertContains(resp, 'Offer')
        self.assertNotContains(resp, 'Swap')
        # filter by status=accepted
        resp = self.client1.get(reverse('proposal_list') + '?status=accepted')
        self.assertNotContains(resp, 'Swap')
        self.assertNotContains(resp, 'Offer')


    def test_signup_view(self):
        self.client.logout()
        signup_data = {
            'username': 'newuser',
            'email': 'newuser@gmail.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        response = self.client.post(reverse('signup'), signup_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())


'''
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Ad, ExchangeProposal

class AdModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.ad = Ad.objects.create(
            user=self.user,
            title='Test Ad',
            description='Test Description',
            category='Electronics',
            condition='new'
        )

    def test_ad_creation(self):
        self.assertEqual(self.ad.title, 'Test Ad')
        self.assertEqual(self.ad.condition, 'new')

class ExchangeProposalModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.ad1 = Ad.objects.create(
            user=self.user1,
            title='Ad 1',
            description='Description 1',
            category='Books',
            condition='used'
        )
        self.ad2 = Ad.objects.create(
            user=self.user2,
            title='Ad 2',
            description='Description 2',
            category='Books',
            condition='new'
        )
        self.proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment='Interested in exchange',
            status='pending'
        )

    def test_proposal_creation(self):
        self.assertEqual(self.proposal.status, 'pending')
        self.assertEqual(self.proposal.comment, 'Interested in exchange')
'''