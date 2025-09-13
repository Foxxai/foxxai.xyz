# Research Blog

Below is a chronological list of research notes, observations, and findings.

{% for post in blog_posts %}

## [{{ post.title }}]({{ post.url }})

Posted on {{ post.date.strftime('%B %d, %Y') }}

{{ post.excerpt }}

[Read more]({{ post.url }})

---

{% endfor %}