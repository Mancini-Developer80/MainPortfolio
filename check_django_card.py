#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
django.setup()

from pages.models import CaseStudy

# Check Django Portfolio card
cards = CaseStudy.objects.filter(title__icontains='Django')
print(f"\n=== Found {cards.count()} Django cards ===\n")

for card in cards:
    print(f"Title: {card.title}")
    print(f"  live_url: {card.live_url}")
    print(f"  github_url: {card.github_url}")
    print(f"  absolute_url: {card.get_absolute_url()}")
    print(f"  slug: {card.slug}")
    print()
