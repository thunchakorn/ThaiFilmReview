# Thai Film Review Web Application

[DEMO](https://thunchakorn.pythonanywhere.com/)

This project is a showcase of my ability to use various Django functionalities. It is a web application where users can review Thai films, like and dislike reviews, and comment on them. Users can also rate different aspects of films, such as Cinematography, Direction, Acting, Screenplay/Story, Music/Score, and Overall Quality.

## Features

- **User Authentication**: Users can sign up, log in, forget password, change password,and manage their profiles.
- **Film Reviews**: Users can write reviews for any Thai film, and other users can like, dislike, and comment on these reviews.
- **Rating System**: Users can rate films on various aspects:
  - Cinematography
  - Direction
  - Acting
  - Screenplay/Story
  - Music/Score
  - Overall Quality
- **Following/Follower**: User can follow other user to see new review on feed.

## Project Apps

- `config`: Project settings and configurations
- `films`: App for managing films
- `profiles`: App for managing user profiles
- `reviews`: App for managing film reviews

## Django functionalities

### Models

- `OneToOneField`: for extending `AUTH_USER_MODEL` and use signal to triggering create profile when user is created
- `SlugField`: for identifying instance instead of pk
- Custom `FileSystemStorage`: for overwritting same file name in `ImageField`
- `ManyToManyField` with additional field through custom intermediate table
- Custom object managers to optimize SQL querying

### Views
- Using class-based views: `DeleteView`, `ListView`, `DetailView`, `UpdateView`, `View` 
- Using mixins: `LoginRequiredMixin`, `SuccessMessageMixin`, `UserPassesTestMixin`

### Forms
- Custom `ChoiceWidget`
- Integrate with crispy_forms helper
- `django_filters` for easily filter and sort in `ListView`

### Templates
- Template inheritance
- Custom filters and tags
- Partial template with `include` tag
- Custom error files e.g. 404.html 500.html etc.

### Admin
- Customize the admin fieldset and inline display 
 
## Tools and Extensions
- **htmx** and **django-htmx** for dynamic website without using javascript
- **Tailwindcss** and **Daisyui** for styling and components
- **whitenoise** for serving static files
- **pytest** and **pytest-django** for testing
- **django-allauth** for authentication, registration, account management
- **django-restframework** for serving APIs
- **django-crispy-forms** for helping with forms
- **django-filter** for easily filtering feature
- **django-debug-toolbar** for monitor debugging and optimizing performance

## Other features
- Use `python manage.py loaddata initial` to load initial fixture data