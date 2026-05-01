from django import forms
from django.forms import ModelForm
from django.db.models import Q
from .models import Project, Review, Tag


class ProjectForm(ModelForm):
    remove_featured_image = forms.BooleanField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Project
        fields = ['title', 'featured_image', 'description', 'demo_link', 'source_link', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'project-form-input',
                'placeholder': 'Give your project a clear, memorable name',
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'project-form-file-input',
                'accept': 'image/*',
            }),
            'description': forms.Textarea(attrs={
                'class': 'project-form-textarea',
                'placeholder': 'Explain what the project does, the stack behind it, the architecture choices, and what you would improve next.',
                'rows': 8,
            }),
            'demo_link': forms.URLInput(attrs={
                'class': 'project-form-input',
                'placeholder': 'https://your-live-demo.com',
            }),
            'source_link': forms.URLInput(attrs={
                'class': 'project-form-input',
                'placeholder': 'https://github.com/username/project',
            }),
            'tags': forms.CheckboxSelectMultiple(attrs={
                'class': 'project-form-tag-input',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].label = 'Project Title'
        self.fields['featured_image'].label = 'Featured Image'
        self.fields['description'].label = 'Project Story'
        self.fields['demo_link'].label = 'Live Demo Link'
        self.fields['source_link'].label = 'Source Code Link'
        self.fields['tags'].label = 'Tech Stack'

        self.fields['title'].help_text = 'Make it easy for developers to recognize what you built.'
        self.fields['featured_image'].help_text = 'Upload a strong cover image or screenshot for your project card.'
        self.fields['description'].help_text = 'Share the problem, the build, and the tradeoffs behind the project.'
        self.fields['demo_link'].help_text = 'Optional. Add it only if the project has a live demo.'
        self.fields['source_link'].help_text = 'Optional. Add it only if the code is publicly available.'
        self.fields['tags'].help_text = 'Select approved public technologies that best represent this build. Custom project tags can be added below.'

        tag_queryset = Tag.objects.filter(is_approved=True)
        if self.instance and self.instance.pk:
            project_tag_ids = self.instance.tags.values_list('id', flat=True)
            tag_queryset = Tag.objects.filter(Q(is_approved=True) | Q(id__in=project_tag_ids)).distinct()

        self.fields['tags'].queryset = tag_queryset.order_by('name')

    def save(self, commit=True):
        project = super().save(commit=False)
        remove_featured_image = self.cleaned_data.get('remove_featured_image')
        image_field = Project._meta.get_field('featured_image')
        default_image = image_field.default

        if project.pk and remove_featured_image:
            current_image = getattr(project, 'featured_image', None)
            if current_image and current_image.name and current_image.name != default_image:
                current_image.delete(save=False)
            project.featured_image = default_image

        if commit:
            project.save()
            self.save_m2m()

        return project



class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']
        labels = {
            'value': 'Your vote',
            'body': 'Your comment',
        }
        widgets = {
            'value': forms.RadioSelect(attrs={
                'class': 'review-form-choice-input',
            }),
            'body': forms.Textarea(attrs={
                'class': 'review-form-textarea',
                'placeholder': 'Share what worked well, what could be improved, or what stood out to you.',
                'rows': 5,
            }),
        }
        help_texts = {
            'value': 'Choose the option that best matches your feedback.',
            'body': 'Optional, but helpful. Written feedback makes the project stronger.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['value'].choices = [
            ('like', 'Positive feedback'),
            ('dislike', 'Needs improvement'),
        ]
