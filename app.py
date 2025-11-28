from flask import Flask, render_template, request, redirect, url_for
import requests
app = Flask(__name__)

@app.route('/')
def home():
    # Fetch a few featured posts to show on the homepage
    try:
        posts_resp = requests.get('https://jsonplaceholder.typicode.com/posts')
        all_posts = posts_resp.json()
    except Exception:
        all_posts = []

    featured_posts = all_posts[:3] if all_posts else []
    return render_template("home.html", featured_posts=featured_posts)

@app.route('/blogs')
def blog():
    api_url="https://jsonplaceholder.typicode.com/posts"
    response = requests.get(api_url)
    posts=response.json()
    return render_template('blog.html',posts=posts)

@app.route('/blogs/<int:id>')
def blog_detail(id):
    api_url=f"https://jsonplaceholder.typicode.com/posts/{id}"
    comments=f"https://jsonplaceholder.typicode.com/posts/{id}/comments"
    response = requests.get(api_url)
    post=response.json()
    return render_template('blog_detail.html',post=post, comments=comments)

@app.route('/users')
def users():
    api_url="https://jsonplaceholder.typicode.com/users"
    response = requests.get(api_url)
    users=response.json()
    return render_template("user.html", users=users)

@app.route('/users/<int:id>')
def users_profile(id):
    # Fetch the user data
    user_url = f"https://jsonplaceholder.typicode.com/users/{id}"
    user_resp = requests.get(user_url)
    user = user_resp.json()

    # Fetch posts for this user
    posts_url = f"https://jsonplaceholder.typicode.com/posts?userId={id}"
    posts_resp = requests.get(posts_url)
    posts = posts_resp.json()

    return render_template("user_profile.html", user=user, posts=posts)


@app.route('/search')
def search():
    q = request.args.get('q', '').strip()
    scope = request.args.get('scope', 'all')

    if not q:
        # No query provided — redirect back to home
        return redirect(url_for('home'))

    q_lower = q.lower()
    results = {
        'posts': [],
        'users': []
    }

    # Search posts
    if scope in ('all', 'posts'):
        posts_url = 'https://jsonplaceholder.typicode.com/posts'
        posts_resp = requests.get(posts_url)
        try:
            all_posts = posts_resp.json()
        except ValueError:
            all_posts = []

        for p in all_posts:
            if q_lower in (p.get('title','') or '').lower() or q_lower in (p.get('body','') or '').lower():
                results['posts'].append(p)

    # Search users
    if scope in ('all', 'users'):
        users_url = 'https://jsonplaceholder.typicode.com/users'
        users_resp = requests.get(users_url)
        try:
            all_users = users_resp.json()
        except ValueError:
            all_users = []

        for u in all_users:
            if (q_lower in (u.get('name','') or '').lower() or
                q_lower in (u.get('username','') or '').lower() or
                q_lower in (u.get('email','') or '').lower()):
                results['users'].append(u)

    return render_template('search_results.html', query=q, scope=scope, results=results)

@app.route('/users/<int:id>/blogs')
def user_blogs(id):
    api_url=f"https://jsonplaceholder.typicode.com/users/{id}/posts"
    response = requests.get(api_url)
    users=response.json()
    return render_template("user_blogs.html", user_id=id)

@app.route('/users/<int:id>/comments')
def user_comments(id):
    api_url=f"https://jsonplaceholder.typicode.com/users/{id}/comments"
    response = requests.get(api_url)
    comments=response.json()
    return render_template("user_comments.html", comments=comments, user_id=id)

if __name__ == '__main__':
    app.run(debug=True)