

### 

# 신박한 팀 - Project 10

팀명 : 신박한

팀원 : 신승호, 박홍은 (팀장)

## 1. 목표

- 협업을 통한 데이터베이스 모델링 및 기능 구현

## 2. `movies`

### 1) `models.py`

- `genres` : Genre 와 Movie 는 M:N 관계이므로 ManyToManyField를 사용
- `like_users` : User 와 Movie 는 M:N 관계이므로 ManyToManyField를 사용
- `movie` : Movie 와 Review는 1:N 관계
- `user` : User와 Review는 1:N 관계

```python
class Genre(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=30)
    audience = models.IntegerField()
    poster_url = models.CharField(max_length=140)
    description = models.TextField()
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like_movies', blank=True)
    genres = models.ManyToManyField(Genre, related_name='movies')
    def __str__(self):
        return self.title

class Review(models.Model):
    content = models.CharField(max_length=140)
    score = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    def __str__(self):
        return self.content
```

### 2) `index.html`

- 영화 이미지를 누르면 상세페이지로 넘어가도록 구현
- 각 영화별  좋아요 기능 구현 ( 처음 한 번 누르면 빨간색, 동일 유저가 한 번더 누르면 검은색 )

```html
{% extends 'movies/base.html' %}
{% block content %}
<h1 class="text-center">Movies List</h1>
<hr>
<div class="row justify-content-between">
  {% for movie in movies %}
  <div class="card mb-3" style="width: 18rem;">
    <a href="{% url 'movies:detail' movie.pk %}"><img src="{{ movie.poster_url }}" class="card-img-top" alt="img"></a>
    <div class="card-body">
      <h5 class="card-title">{{ movie.title }}</h5>
      <a href="{% url 'movies:like' movie.pk %}">
        {% if user in movie.like_users.all %}
        <i class="fab fa-gratipay" style="font-size: 20px; color: crimson;"></i>
        {% else %}
        <i class="fab fa-gratipay" style="font-size: 20px; color: black;"></i>
        {% endif %}
      </a>
    </div>
  </div>
  {% endfor %}
</div>
{% endblock content %}
```

### 3) `detail.html`

- 댓글을 작성한 유저와 평점을 출력하고 유저 이름을 클릭하면 해당 유저의 상세페이지로 넘어간다.

```html
{% for review in reviews %}
<div>
  <h4>댓글
  </h4>
  <a href="{% url 'accounts:userdetail' review.user.pk %}">{{ review.user }}</a> 댓글 {{ forloop.revcounter }} :
  {{ review.content }} / 평점 : {{ review.score }}
  {% if request.user == comment.user %}
  <form action="{% url 'movies:reviews_delete' movie.pk review.pk %}" method='POST'>
    {% csrf_token %}
    <input type="submit" value="DELETE">
  </form>
  {% endif %}
</div>
{% empty %}
<p><b>댓글이 없습니다.</b></p>
{% endfor %}
```



## 3. `accounts`

#### 3. 1. 목표

- 유저 회원가입과 로그인, 로그아웃 기능을 구현

- 유저 목록 구현 (사용자의 `username` 을 클릭하면 유저 상세보기 페이지로 이동)
- 유저 상세보기 ( /accounts/{user_pk}/ )
  - 해당 유저가 작성한 평점 정보
  - 해당 유저가 좋아하는 영화 정보
  - 해당 유저를 팔로우 한 사람의 수, 팔로잉 한 사람의 수
  - * 팔로우 하기 기능을 상세보기 페이지에 추가했습니다.

---

#### 3. 2.  기능 구현

admin 페이지를 이용해 임의의 유저들을 생성 후 가장 간단한 유저 목록과 상세보기 기능을 만들었습니다.

```django
from django.shortcuts import render, redirect, get_object_or_404

def userlist(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'accounts/userlist.html', context)


def userdetail(request, user_pk):
    user1 = get_object_or_404(User, pk=user_pk)
    context = {'user1': user1}
    return render(request, 'accounts/userdetail.html', context)
```

- ##### 유저 목록.html

  ```django
    <ul>
      {% for user in users  %}
      <li><a href="{% url 'accounts:userdetail' user.pk %}">{{ user.username }}</a></li>
      <br>
      {% endfor %}
    </ul>
  ```

  ​	for문으로 유저들 출력 후 a태그로 해당 유저 상세보기 페이지 연결

- ##### 유저 상세 보기.html

  ```django
  h4>{{ user1.username }} 님이 리뷰한 영화들</h4>
  {% for review in user1.review_set.all %}
  <p>영화 : {{ review.movie }}</p>
  <p>한 줄 평 :{{ review.content }}</p>
  <p>평점 : {{ review.score }}</p>
  {% endfor %}
  <hr>
  <h4>{{ user1.username }} 님이 좋아요한 영화</h4>
  {% for movie in user1.like_movies.all  %}
  <ul>
    <li>{{ movie }}</li>
  </ul>
  {% endfor %}
  <hr>
  ```

  ​	해당 유저가 작성한 리뷰들과 좋아요를 누른 영화들 출력
  - ##### 팔로우

    ```django
    {% if user.is_authenticated %}
    {% if user in user1.followers.all %}
    <a class="btn btn-primary btn-sm" href="{% url 'movies:follow' user1.pk %}" role="button">Unfollow</a>
    {% else %}
    <a class="btn btn-primary btn-sm" href="{% url 'movies:follow' user1.pk %}" role="button">follow</a>
    {% endif %}
    {% endif %}
    ```

    ​	로그인이 된 상태에서 팔로우 버튼이 출력되게 `is_authenticated`로 감싸고 if in 문으로 로그인 된 유저가 user1 (상세보기 유저)의 followers 테이블에 있을 경우 == 이미 팔로우한 경우이니 Unfollow 버튼을 출력

  - ##### Followers & Followings

    ```html
    <h4>Followers : {{ user1.followers.all|length }}</h4>
    {% for user in user1.followers.all %}
    <ul>
      <li>{{ user }}</li>
    </ul>
    {% endfor %}
    <hr>
    <h4>Followings: {{ user1.followings.all|length }}</h4>
    {% for user in user1.followings.all %}
    <ul>
      <li>{{ user }}</li>
    </ul>
    {% endfor %}
    ```

    ​	Followers 숫자와 Followings 숫자들 과 해당 유저들을 for 문 + ul 태그로 출력 

  - ##### 회원가입 & 로그인

  ```html
  {% if request.resolver_match.url_name == 'signup' %}
  <h1>회원가입</h1>
  {% elif request.resolver_match.url_name == 'login' %}
  <h1>로그인</h1>
  {% endif %}
  <form method="POST">
    {% csrf_token %}
    <p>{{ form }}</p>
  
    {% if request.resolver_match.url_name == 'signup' %}
    <input type="submit" value="회원가입">
    {% elif request.resolver_match.url_name == 'login' %}
    <input type="submit" value="로그인">
    {% endif %}
  </form>
  ```

  1. `resolver_match.url_name`으로 url을 분기하여 해당 페이지 상단에 `회원가입` or `로그인` 출력
  2. form 태그에 forms.py에 작성한 UserCreationForm을 `{{ form }}` 으로 받아 출력 

  3. 1번과 같은 방법으로 인풋 버튼 value 분기

     - ##### view

       ```django
       def signup(request):
           if request.user.is_authenticated:
               return redirect('movies:index')
           if request.method == "POST":
               form = CustomUserCreationForm(request.POST)
               if form.is_valid():
                   user = form.save()
                   auth_login(request, user)
                   return redirect('movies:index')
           else:
               form = CustomUserCreationForm()
           context = {'form': form}
           return render(request, 'accounts/auth_form.html', context)
       
       
       def login(request):
           if request.user.is_authenticated:
               return redirect('movies:index')
           if request.method == "POST":
               form = AuthenticationForm(request, request.POST)
               if form.is_valid():
                   auth_login(request, form.get_user())
                   return redirect(request.GET.get('next') or 'movies:index')
           else:
               form = AuthenticationForm()
           context = {'form': form}
           return render(request, 'accounts/auth_form.html', context)
       
       
       def logout(request):
           auth_logout(request)
           return redirect('movies:index')
       ```

       - 회원 가입
         - 로그인 되있을경우 redirect
         - POST로 들어올 경우 유효성 검증 후 로그인해서 redirect
         - else: 빈 form  전달후 auth_form.html 로 이동

       - 로그인
         - 로그인 되있을경우 redirect

## 4. 결과


https://user-images.githubusercontent.com/52685256/69300650-2cb57900-0c57-11ea-8c84-d2e4e61ef22e.png

https://user-images.githubusercontent.com/52685256/69300652-2cb57900-0c57-11ea-80d4-f70896188b86.png

https://user-images.githubusercontent.com/52685256/69300654-2d4e0f80-0c57-11ea-848b-ec7e0456bfe4.png

https://user-images.githubusercontent.com/52685256/69300656-2d4e0f80-0c57-11ea-853f-a3ea1a88ca58.png

## 5. 느낀점

- 익숙하지 않았던 Git을 통한 협업

  가상환경을 포함한 commit을  pull request 보내니 충돌이 자꾸 일어나서 어려움이 있었다.

- git 을 사용한 협업은 이번이 처음이었는데 생각보다 헷갈리는 부분이 많아서 주의가 필요해보였다. 

- 각자 파트를 나눠 작업을 하니 시간적으로 빨리 완성할 수 있었지만 변수명 충돌 등을 주의해야했다. 

- 팔로우 기능을 구현하는 데에서 시간을 많이 할애 했는데 혼자서 작업했다면 많은 어려움을 겪었을텐데 페어로 작업해 서로 부족한 점을 채워주어 더 빨리 끝낼 수 있었다.
