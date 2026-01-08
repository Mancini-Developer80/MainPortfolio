from django.core.management.base import BaseCommand
from pages.models import CaseStudy
from blog.models import BlogPost
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Imports case studies and blog posts data'

    def handle(self, *args, **options):
        author = User.objects.filter(is_superuser=True).first()
        if not author:
            self.stdout.write(self.style.ERROR('No superuser found. Create one first.'))
            return

        self.stdout.write('Importing data...')
        
        # ============================================
        # CASE STUDIES - FILL WITH YOUR DATA
        # ============================================
        case_studies_data = [
            # EXAMPLE - Replace with your actual data
            # {
            #     'title': 'Your Project Title',
            #     'slug': 'your-project-slug',
            #     'short_description': 'Brief description',
            #     'client': 'Client Name',
            #     'timeline': '3 months',
            #     'role': 'Full Stack Developer',
            #     'technologies': 'Django, React, PostgreSQL',
            #     'overview': 'Detailed overview...',
            #     'challenge': 'The challenge was...',
            #     'solution': 'We solved it by...',
            #     'results': 'Results achieved...',
            #     'is_featured': True,
            # },
        ]
        
        for cs_data in case_studies_data:
            cs, created = CaseStudy.objects.update_or_create(
                slug=cs_data['slug'],
                defaults=cs_data
            )
            status = 'Created' if created else 'Updated'
            self.stdout.write(self.style.SUCCESS(f'{status} case study: {cs.title}'))
        
        # ============================================
        # BLOG POSTS - FILL WITH YOUR DATA
        # ============================================
        blog_posts_data = [
            # EXAMPLE - Replace with your actual data
            # {
            #     'title': 'Your Blog Post Title',
            #     'slug': 'your-blog-post-slug',
            #     'excerpt': 'Brief excerpt...',
            #     'content': '<p>Full HTML content...</p>',
            #     'author': author,
            #     'is_published': True,
            # },
        ]
        
        for bp_data in blog_posts_data:
            bp, created = BlogPost.objects.update_or_create(
                slug=bp_data['slug'],
                defaults=bp_data
            )
            status = 'Created' if created else 'Updated'
            self.stdout.write(self.style.SUCCESS(f'{status} blog post: {bp.title}'))
        
        self.stdout.write(self.style.SUCCESS('\n✓ Data import complete!'))
        self.stdout.write(f'  Case Studies: {len(case_studies_data)}')
        self.stdout.write(f'  Blog Posts: {len(blog_posts_data)}')
