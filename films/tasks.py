import io
import requests
from bs4 import BeautifulSoup
from datetime import datetime

from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from celery import shared_task

from .models import Film, Genre, Person, Link, Role
from .utils import summarize_review_map_reduce

_FULL_MONTHS = [
    "มกราคม",
    "กุมภาพันธ์",
    "มีนาคม",
    "เมษายน",
    "พฤษภาคม",
    "มิถุนายน",
    "กรกฎาคม",
    "สิงหาคม",
    "กันยายน",
    "ตุลาคม",
    "พฤศจิกายน",
    "ธันวาคม",
]


@shared_task
def scrape_film_nangdee():
    """
    for periodic task (crontab 0 0 * * *)
    """
    URL = "https://www.nangdee.com/movies/?t=1&mt=1"
    CLASS_NAME = "col-xs-6 col-sm-3"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    links = list(
        map(lambda x: x.find("a").get("href"), soup.find_all(class_=CLASS_NAME))
    )

    for link in links:
        data = get_film_data(link)
        img_data = requests.get(data["image_url"]).content
        buffer = io.BytesIO(img_data)
        image = SimpleUploadedFile(
            name=f"{data['title']}.jpg", content=img_data, content_type="image/jpeg"
        )
        image.file = buffer
        film = Film.objects.filter(
            name=data["title"], release_date=data["release_date"]
        ).first()
        if not film:
            film = Film.objects.create(
                name=data["title"], release_date=data["release_date"], poster=image
            )
            film.save()

        # genres
        for genre in data["genres"]:
            genre_obj, created = Genre.objects.get_or_create(name=genre)
            film.genres.add(genre_obj)

        # directors
        for director in data["directors"]:
            person_obj, created = Person.objects.get_or_create(name=director)
            film.directors.add(person_obj)

        # roles
        for actor in data["actors"]:
            if len(actor) == 2:
                actor_name, role_name = actor
            else:
                actor_name = actor[0]
                role_name = None
            person_obj, created = Person.objects.get_or_create(name=actor_name)
            role, created = Role.objects.get_or_create(
                name=role_name, film=film, person=person_obj
            )

        # links
        link = Link.objects.get_or_create(name="nangdee", link=data["link"], film=film)


def add_poster():
    links = Link.objects.filter(name="nangdee", film__poster="")
    print(len(links))
    for i, link in enumerate(links):
        print(i, link)
        data = get_film_data(link.link)
        img_data = requests.get(data["image_url"]).content
        buffer = io.BytesIO(img_data)
        image = SimpleUploadedFile(
            name=f"{data['title']}.jpg", content=img_data, content_type="image/jpeg"
        )
        image.file = buffer

        film = link.film
        film.poster = image
        film.save()


def get_film_data(link):
    data = {}
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    title = soup.find("h1").find("a", {"title": True}).text
    en_title = soup.find("h4").find("span")
    en_title = en_title.text if en_title else None
    temp_lis = soup.find("nav", class_="mv-panel-nav").find_all("li")
    if "เข้าฉาย" not in temp_lis[1].text:
        return {}

    release_date = temp_lis[1].text.strip().splitlines()[1].strip("()")
    release_date = release_date.split(" ")
    release_date[1] = _FULL_MONTHS.index(release_date[1]) + 1
    release_date[2] = int(release_date[2]) - 543
    release_date = f"{release_date[2]}-{release_date[1]}-{release_date[0]}"
    release_date = datetime.strptime(release_date, "%Y-%m-%d")

    genres = [x.text.lower() for x in temp_lis[0].find_all("a")]
    temp = soup.find("h4", text="ผู้กำกับ")
    directors = [x.text for x in temp.parent.parent.find_all("b")] if temp else []
    temp = soup.find("h4", text="นักแสดง")
    actors = (
        [x.parent.parent.text.splitlines() for x in temp.parent.parent.find_all("b")]
        if temp
        else []
    )

    data.update(
        title=title,
        en_title=en_title,
        release_date=release_date,
        genres=genres,
        directors=directors,
        actors=actors,
        link=link,
        image_url=soup.find("div", class_="featured-art").find("img")["src"],
    )
    return data


@shared_task
def summarize_review():
    films = (
        Film.objects.prefetch_related("reviews")
        .with_reviews_data()
        .filter(reviews_count__gte=settings.NUM_REVIEWS_SUMMARY)
    )
    for film in films:
        reviews = [review.full_review for review in film.reviews.all()]
        film.review_summary = summarize_review_map_reduce(reviews)
        film.save()
