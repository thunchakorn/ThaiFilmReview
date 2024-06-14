# Thai Film Review Web Application

[Heroku-demo](https://thaifilmreview-89c6f8cce2d8.herokuapp.com/)

This project is a showcase of my ability to use various Django functionalities. It is a web application where users can review Thai films, like and dislike reviews, and comment on them. Users can also rate different aspects of films, such as Cinematography, Direction, Acting, Screenplay/Story, Music/Score, and Overall Quality.

## Features

- **User Authentication**: Users can sign up and log in with Google, forget password, change password,and manage their profiles.
- **Film Reviews**: Write, like, dislike, and comment on reviews.
- **Rating System**: Rate films on Cinematography, Direction, Acting, Screenplay/Story, Music/Score, and Overall Quality.
- **Following/Follower**: User can follow other user to see new review on feed.
- **Periodic update film**: New films are updated automatically.

## Project Apps

- `config`: Project settings and configurations.
- `films`: App for managing films.
- `profiles`: App for managing user profiles.
- `reviews`: App for managing film reviews.

## Django functionalities

### Models

- **OneToOneField**: Extend `AUTH_USER_MODEL` and use signals to create profiles.
- **SlugField**: Identify instances instead of primary keys.
- **ManyToManyField**: Use a custom intermediate table.
- **Custom Managers**: Optimize SQL queries.

### Views
- **Class-based generic Views**: `DeleteView`, `ListView`, `DetailView`, `UpdateView`, `View`.
- **Mixins**: `LoginRequiredMixin`, `SuccessMessageMixin`, `UserPassesTestMixin`.

### Forms
- **Custom Widgets**: Custom `ChoiceWidget`.
- **crispy_forms**: Integrate with `crispy_forms` helper.
- **django_filters**: Easily filter and sort in `ListView`.

### Templates
- **Inheritance**: Template inheritance.
- **Custom Filters and Tags**: Custom filters and tags.
- **Partials**: Partial templates with `include` tag.
- **Custom Error Pages**: Custom 404.html, 500.html, etc.

### Permission
- **Moderator Group**: Add moderator permissions, e.g., for marking spoilers.

### Custom `django-admin` Command
- Add *create_moderator_group* command for adding *moderator* group.

### Admin
- **Customization**: Customize admin fieldsets and inlines.

### Websocket
- **Real-time Notifications**: Notify users when their reviews are liked or commented on.

### Internationalization and Localization
- **Multi-language Support**: English and Thai.

## Deployment
- **Heroku**: Deploy with Heroku using a `Procfile` and `heroku-postgresql` addons.
- **Cloudflare R2**: Store uploaded media files.

## Tools and Extensions
- **htmx** and **django-htmx** for dynamic website without using javascript.
- **Tailwindcss** and **Daisyui** for styling and components.
- **whitenoise** for serving static files.
- **pytest** and **pytest-django** for testing.
- **django-allauth** for authentication, registration, account management.
- **django-restframework** for serving APIs.
- **django-crispy-forms** for helping with forms.
- **django-filter** for easily filtering feature.
- **django-debug-toolbar** for monitor debugging and optimizing performance.
- **celery** for running periodic and background asynchronouse task by using `Redis` as broker and backend.
- **django-celery-beat** store the periodic task schedule in the database.
- **django-storages** for managing uploaded file on cloud storage.

## Other Features

- **Initial Data Load**: Use `python manage.py loaddata initial` to load initial fixture data.

## Demo

Check out the [live demo](https://thaifilmreview-89c6f8cce2d8.herokuapp.com).
