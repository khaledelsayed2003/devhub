from django import forms
from django.forms import ModelForm
from .models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'featured_image', 'description', 'demo_link', 'source_link', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'project-form-input',
                'placeholder': 'Give your project a clear, memorable name',
            }),
            'featured_image': forms.ClearableFileInput(attrs={
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
        self.fields['tags'].help_text = 'Select the technologies that best represent this build.'
