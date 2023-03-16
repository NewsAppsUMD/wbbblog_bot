# wbbblog_bot

This Python bot checks the [WBBBlog site](https://wbbblog.com/) for changes to specific pages and pushes a Slack message with the url of the page that has changed. Currently it only checks the [2023 Coaching Changes Tracker](https://wbbblog.com/womens-basketball-coaching-changes-tracker-2023/) but could be extended to other pages. To do so, it leverages the WordPress JSON API that the site has rather than scraping, because the site routinely serves 429 responses (Too Many Requests) to scrapers.