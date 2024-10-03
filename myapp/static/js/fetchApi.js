// Fetch navbar links from the Django API
fetch('/api/navbar/')
    .then(response => response.json())
    .then(data => {
        const menu = document.getElementById('main-menu');
        const maxItems = 6; // Maximum number of visible items
        let dropdownCreated = false;

        // Clear existing static links if any
        menu.innerHTML = '';

        // Create the "More" dropdown
        const moreDropdown = document.createElement('li');
        moreDropdown.classList.add('has-dropdown');
        moreDropdown.innerHTML = `
<a href="#">More</a>
<ul class="submenu"></ul>
`;

        // Loop through the data and create list items for each navbar link
        data.forEach((link, index) => {
            const listItem = document.createElement('li');
            const anchor = document.createElement('a');
            anchor.href =  link.url.startsWith('/') ? link.url : `/${link.url}`;
            anchor.textContent = link.name;

            if (index < maxItems) {
                // Append first 5 items directly to the menu
                listItem.appendChild(anchor);
                menu.appendChild(listItem);
            } else {
                // Append the 6th item and beyond to the "More" dropdown submenu
                const submenu = moreDropdown.querySelector('.submenu');
                listItem.appendChild(anchor);
                submenu.appendChild(listItem);

                // Add the dropdown to the main menu (only once)
                if (!dropdownCreated) {
                    menu.appendChild(moreDropdown);
                    dropdownCreated = true;
                }
            }
        });

        // Hide the "More" dropdown if there are fewer than 6 items
        if (data.length <= maxItems) {
            moreDropdown.style.display = 'none';
        }
    })
    .catch(error => console.error('Error fetching navbar links:', error));


// Top 10 News API
const maxCarouselItems = 4;  // Maximum items for the carousel
const maxNewsContainerItems = 6;  // Maximum items for the news container
const maxTotalNews = 10;  // Maximum total items

// Function to replace the first news item in the container
function replaceFirstNewsItem(newsContainer, newItemHTML) {
    // Remove the first item
    if (newsContainer.children.length > 0) {
        newsContainer.removeChild(newsContainer.firstChild);
    }
    // Add the new item at the end
    const newItem = document.createElement('div');
    newItem.classList.add('col-xl-4', 'col-sm-6');
    newItem.innerHTML = newItemHTML;
    newsContainer.appendChild(newItem);
}

// Fetch top news data from API
fetch('/api/topnews/')
    .then(response => response.json())
    .then(data => {
        const newsCarousel = document.getElementById('news-carousel');
        const newsContainer = document.getElementById('news-container');

        data.slice(0, maxTotalNews).forEach((newsItem, index) => {
            const newsHTML = `
                    <div class="axil-img-container m-b-xs-15 m-b-sm-30">
                        <a href="#" class="d-block">
                            <img src="${newsItem.image}" alt="${newsItem.title}">
                            <div class="grad-overlay grad-overlay__transparent"></div>
                        </a>
                        <div class="media post-block grad-overlay position-absolute">
                            <div class="media-body justify-content-end">
                                <div class="post-cat-group m-b-xs-10">
                                    <a href="#" class="post-cat cat-btn btn-mid bg-color-purple-one">${newsItem.category}</a>
                                </div>
                                <div class="axil-media-bottom">
                                    <h3 class="axil-post-title hover-line m-b-xs-0">
                                        <a href="/topnews/${newsItem.id}">${newsItem.title}</a>
                                    </h3>
                                </div>
                            </div>
                        </div>
                    </div>`;

            if (index < maxCarouselItems) {
                // Add first 4 items to the carousel
                newsCarousel.innerHTML += `
                        <div class="item">
                            <div class="axil-img-container video-container__type-2 m-b-xs-15 m-b-sm-30">
                                <a href="#" class="d-block">
                                    <img src="${newsItem.image}" alt="${newsItem.title}" class="img-fluid">
                                    <div class="grad-overlay grad-overlay__transparent"></div>
                                    <div class="post-format video-play-btn">
                                        <i class="fas fa-play"></i>
                                    </div>
                                </a>
                                <div class="media post-block position-absolute m-b-xs-30">
                                    <div class="media-body media-body__big">
                                        <div class="axil-media-bottom mt-auto">
                                            <div class="post-cat-group m-b-xs-10">
                                                <a href="#" class="post-cat cat-btn btn-big bg-color-red-two">
                                                    ${newsItem.category}
                                                </a>
                                            </div>
                                            <h3 class="axil-post-title hover-line">
                                                <a href="/topnews/${newsItem.id}">${newsItem.title}</a>
                                            </h3>
                                            <div class="post-metas">
                                                <ul class="list-inline">
                                                    <li>By <a href="#" class="post-author">${newsItem.author}</a></li>
                                                    <li><i class="dot">.</i>${newsItem.date}</li>
                                                    <li><a href="#"><i class="feather icon-activity"></i>5k Views</a></li>
                                                    <li><a href="#"><i class="feather icon-share-2"></i>230 Shares</a></li>
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>`;
            } else if (index < maxTotalNews) {
                // Add to news container until maxNewsContainerItems is reached
                if (newsContainer.children.length < maxNewsContainerItems) {
                    const itemDiv = document.createElement('div');
                    itemDiv.classList.add('col-xl-4', 'col-sm-6');
                    itemDiv.innerHTML = newsHTML;
                    newsContainer.appendChild(itemDiv);
                } else {
                    // Replace the first news item if we already have max items
                    replaceFirstNewsItem(newsContainer, newsHTML);
                }
            }
        });

        // Initialize the Owl Carousel after content is added
        $(document).ready(function () {
            $('#news-carousel').owlCarousel({
                items: 1,
                loop: true,
                autoplay: true,
                dots: false,
                nav: true,
                margin: 0,
                animateIn: 'fadeIn',
                animateOut: 'fadeOut',
                navText: ['<span class="owl-prev"><i class="feather icon-chevron-left"></i></span>', '<span class="owl-next"><i class="feather icon-chevron-right"></i></span>']
            });
        });
    })
    .catch(error => console.error('Error fetching news:', error));


// Top Stories API

fetch('/api/news/')
    .then(response => response.json())
    .then(data => {
        const sectionNewsContainer = document.querySelector('.section-gap #topWeekNewContainer');

        // Get current date and calculate the date 7 days ago
        const today = new Date();
        const last7DaysDate = new Date();
        last7DaysDate.setDate(today.getDate() - 7);

        // Filter news items to only include those from the last 7 days
        const recentNews = data.filter(newsItem => {
            const newsDate = new Date(newsItem.date); // Assuming newsItem.date is in YYYY-MM-DD format
            return newsDate >= last7DaysDate;
        });

        // Check if there is enough recent news
        if (recentNews.length === 0) {
            sectionNewsContainer.innerHTML = '<p>No recent news found.</p>';
            return;
        }

        // Handle the first news item
        const firstNews = recentNews[0];
        const secondAndThirdNews = recentNews.slice(1, 3);  // Get the second and third news items

        // HTML for the first large news item
        let firstNewsHTML = `
        <div class="col-lg-8">
            <div class="axil-img-container m-b-xs-30">
                <a href="/news/${firstNews.id}" class="d-block">
                    <img src="${firstNews.image}" alt="${firstNews.title}" class="w-100">
                    <div class="grad-overlay"></div>
                </a>
                <div class="media post-block position-absolute">
                    <div class="media-body media-body__big">
                        <div class="post-cat-group m-b-xs-10">
                            <a href="#" class="post-cat cat-btn bg-color-purple-one">
                                ${firstNews.category}
                            </a>
                        </div>
                        <div class="axil-media-bottom">
                            <h3 class="axil-post-title hover-line hover-line">
                                <a href="/news/${firstNews.id}">${firstNews.title}</a>
                            </h3>
                            <div class="post-metas">
                                <ul class="list-inline">
                                    <li>By <a href="#" class="post-author">${firstNews.author}</a></li>
                                    <li><i class="dot">.</i>${firstNews.date}</li>
                                    
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>`;

        sectionNewsContainer.innerHTML += firstNewsHTML;

        // HTML for the second and third news items, grouped in one col-lg-4
        let secondThirdNewsHTML = `
        <div class="col-lg-4">
            ${secondAndThirdNews.map(newsItem => `
                <div class="axil-img-container m-b-xs-30">
                    <a href="/news/${newsItem.id}" class="d-block">
                        <img src="${newsItem.image}" alt="${newsItem.title}" class="w-100">
                        <div class="grad-overlay"></div>
                    </a>
                    <div class="media post-block position-absolute">
                        <div class="media-body">
                            <div class="post-cat-group m-b-xs-10">
                                <a href="#" class="post-cat cat-btn bg-color-purple-two">
                                    ${newsItem.category}
                                </a>
                            </div>
                            <div class="axil-media-bottom">
                                <h3 class="axil-post-title hover-line hover-line">
                                    <a href="/news/${newsItem.id}">${newsItem.title}</a>
                                </h3>
                                <div class="post-metas">
                                    <ul class="list-inline">
                                        <li>By <a href="#" class="post-author">${newsItem.author}</a></li>
                                        <li><i class="dot">.</i>${newsItem.date}</li>
                                       
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `).join('')}
        </div>`;

        sectionNewsContainer.innerHTML += secondThirdNewsHTML;


        // Trending API

        const trendingNewsContainer = document.getElementById('trendingNewsContainer');
        trendingNewsContainer.innerHTML = ''; // Clear existing content

        // Keep track of the number of trending articles added
        let trendingCount = 0;

        // Loop through the fetched news articles
        data.forEach(article => {
            if (article.is_trending && trendingCount < 6) {
                // Create HTML structure for each article
                const articleHTML = `
                    <div class="col-lg-6">
                        <div class="media post-block m-b-xs-30">
                            <a href="${article.link}" class="align-self-center">
                                <img class="m-r-xs-30" src="${article.image}" alt="${article.title}">
                            </a>
                            <div class="media-body">
                                <div class="post-cat-group m-b-xs-10">
                                    <a href="${article.categoryLink}" class="post-cat cat-btn bg-color-blue-grey-one">
                                        ${article.category}
                                    </a>
                                </div>
                                <h3 class="axil-post-title hover-line hover-line">
                                    <a href="/news/${article.id}">${article.title}</a>
                                </h3>
                                <div class="post-metas">
                                    <ul class="list-inline">
                                        <li>By <a href="#">${article.author}</a></li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                `;

                // Append each trending article to the trendingNewsContainer
                trendingNewsContainer.innerHTML += articleHTML;

                // Increment the count of trending articles added
                trendingCount++;
            }
        })
    })
    .catch(error => console.error('Error fetching news:', error));


// Load More News Button 
document.getElementById('load-more-btn').addEventListener('click', function() {
    const nextPage = this.getAttribute('data-next-page');
    
    fetch(`?page=${nextPage}`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest' // Indicate that this is an AJAX request
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        const newsContainer = document.getElementById('popular-news-container');
        data.news.forEach(item => {
            console.log(data.news,"data.news");
            
            const newsItem = document.createElement('div');
            newsItem.className = 'col-lg-6 news-item';
            newsItem.innerHTML = `
                <div class="media post-block m-b-xs-30">
                    <a href="/news/${item.id}/" class="align-self-center">
                        <img class="m-r-xs-30" src="${item.image}" alt="${item.title}">
                    </a>
                    <div class="media-body">
                        <div class="post-cat-group m-b-xs-10">
                            <a href="" class="post-cat cat-btn bg-color-blue-grey-one">${item.category}</a>
                        </div>
                        <h3 class="axil-post-title hover-line hover-line">
                            <a href="/news/${item.id}/">${item.title}</a>
                        </h3>
                        <div class="post-metas">
                            <ul class="list-inline">
                                <li>By <a href="#">${item.author}</a></li>
                            </ul>
                        </div>
                    </div>
                </div>
            `;
            newsContainer.appendChild(newsItem);
        });

        // Update the Load More button
        if (data.has_next) {
            this.setAttribute('data-next-page', parseInt(nextPage) + 1);
        } else {
            this.remove(); // Remove button if there's no next page
        }
    })
    .catch(error => console.error('Error loading more news:', error));
});

// Top Stories All Page
