from django.core.management.base import BaseCommand
from pages.models import CaseStudy
from blog.models import BlogPost


class Command(BaseCommand):
    help = 'Loads initial data for case studies and blog posts'

    def handle(self, *args, **options):
        self.stdout.write('Loading initial data...')
        
        # Create sample case studies
        if not CaseStudy.objects.exists():
            case_studies = [
                {
                    'title': 'Sample Project 1',
                    'slug': 'sample-project-1',
                    'short_description': 'A brief description of the project',
                    'client': 'Client Name',
                    'timeline': '3 months',
                    'role': 'Full Stack Developer',
                    'technologies': 'Django, React, PostgreSQL',
                    'overview': 'Detailed project overview...',
                    'challenge': 'The main challenge was...',
                    'solution': 'We solved it by...',
                    'results': 'The project resulted in...',
                    'is_featured': True,
                },
                # Add more case studies here
            ]
            
            for cs_data in case_studies:
                CaseStudy.objects.create(**cs_data)
                self.stdout.write(self.style.SUCCESS(f'Created case study: {cs_data["title"]}'))
        else:
            self.stdout.write(self.style.WARNING('Case studies already exist. Skipping.'))
        
        # Create sample blog posts
        if not BlogPost.objects.exists():
            blog_posts = [
                {
                    'title': 'Sample Blog Post',
                    'slug': 'sample-blog-post',
                    'excerpt': 'A brief excerpt of the blog post',
                    'content': 'Full blog post content goes here...',
                    'is_published': True,
                },
                # Add more blog posts here
            ]
            
            for bp_data in blog_posts:
                BlogPost.objects.create(**bp_data)
                self.stdout.write(self.style.SUCCESS(f'Created blog post: {bp_data["title"]}'))
        else:
            self.stdout.write(self.style.WARNING('Blog posts already exist. Skipping.'))
        
        self.stdout.write(self.style.SUCCESS('Initial data loaded successfully!'))
