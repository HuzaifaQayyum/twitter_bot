class TwitterUrls:
    twitter_loginurl = "https://twitter.com/login"
    twitter_url = "https://twitter.com"
    twitter_home_url = 'https://twitter.com/home'

    @staticmethod
    def get_link_of_user_followers(username):
        return f'https://twitter.com/{username}/followers'

    @staticmethod
    def get_twitter_users_link(query):
        return f'https://twitter.com/search?q={query}&src=typed_query&f=user'