from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import CaseStudy, ContactSubmission

def home(request):
	if request.method == 'POST':
		# Get form data
		subject = request.POST.get('subject', '').strip()
		name = request.POST.get('name', '').strip()
		email = request.POST.get('email', '').strip()
		message = request.POST.get('message', '').strip()
		
		# Validate required fields
		if not all([subject, name, email, message]):
			messages.error(request, 'All fields are required.')
			return render(request, 'pages/home.html')
		
		try:
			# Save to database
			submission = ContactSubmission.objects.create(
				subject=subject,
				name=name,
				email=email,
				message=message
			)
			
			# Send notification email to admin (when EMAIL_HOST is configured)
			# Only attempt to send email if we're not in DEBUG mode
			if not settings.DEBUG:
				try:
					if hasattr(settings, 'EMAIL_HOST') and settings.EMAIL_HOST:
						admin_subject = f'New Contact Form Submission: {subject}'
						admin_message = f"""
New contact form submission received:

From: {name} ({email})
Subject: {subject}

Message:
{message}

---
Submitted at: {submission.submitted_at.strftime('%Y-%m-%d %H:%M:%S')}
View in admin: {request.build_absolute_uri('/admin/pages/contactsubmission/')}
"""
						send_mail(
							admin_subject,
							admin_message,
							settings.DEFAULT_FROM_EMAIL,
							[settings.CONTACT_EMAIL],
							fail_silently=False,
						)
						
						# Send auto-reply to submitter
						reply_subject = f'Thank you for contacting me - {subject}'
						reply_message = f"""
Hi {name},

Thank you for reaching out! I've received your message and will get back to you as soon as possible.

Your message:
"{message}"

Best regards,
Giuseppe Mancini
Full Stack Web Developer

---
This is an automated response. Please do not reply to this email.
"""
						send_mail(
							reply_subject,
							reply_message,
							settings.DEFAULT_FROM_EMAIL,
							[email],
							fail_silently=False,
						)
				except Exception as email_error:
					# Log email error but don't fail the submission
					import traceback
					print(f"Email sending failed: {email_error}")
					print(traceback.format_exc())
					# Continue to show success message since submission was saved
			
			messages.success(request, 'Thank you for your message! I will get back to you soon.')
			return redirect('pages:home')
			
		except Exception as e:
			import traceback
			print(f"Form submission error: {e}")
			print(traceback.format_exc())
			messages.error(request, 'An error occurred. Please try again later.')
			return render(request, 'pages/home.html', {'case_studies': CaseStudy.objects.filter(is_featured=True).order_by('order')[:3]})
	
	# Get featured case studies for homepage
	featured_case_studies = CaseStudy.objects.filter(is_featured=True).order_by('order')[:3]
	return render(request, 'pages/home.html', {'case_studies': featured_case_studies})

def projects(request):
	case_studies = CaseStudy.objects.all().order_by('order')
	return render(request, 'pages/projects.html', {'case_studies': case_studies})

def about(request):
	return render(request, 'pages/about.html')

def contact(request):
	return render(request, 'pages/contact.html')

def case_study_detail(request, slug):
	case_study = get_object_or_404(CaseStudy, slug=slug)
	return render(request, 'pages/case_detail.html', {'case_study': case_study})
