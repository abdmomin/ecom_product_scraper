from requests_html import HTMLSession
import csv


headers = {
    'authority': 'themes.woocommerce.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}


s = HTMLSession()


def get_links():
    url = 'https://themes.woocommerce.com/storefront/product-category/clothing'
    links = []
    while True:
        r = s.get(url, headers=headers)
       
        products = r.html.find('ul.products.columns-4 li')
        for product in products:
            link = product.find('a', first=True).attrs['href']
            links.append(link)

        if r.html.find('a.next.page-numbers', first=True) is None:
            break
        else:
            url = r.html.find('a.next.page-numbers', first=True).attrs['href']
    return links



def get_product_data(link):
    r = s.get(link, headers=headers)

    title = r.html.find('h1.product_title.entry-title', first=True).text.strip()
    price = float(r.html.find('p.price', first=True).text.strip().replace('£','').split('\n')[-1])
    try:
        sku = r.html.find('span.sku', first=True).text.strip()
    except AttributeError:
        sku = 'N/A'
    try:
        tag = r.html.find('span.tagged_as a', first=True).text.strip()
    except AttributeError:
        tag = 'N/A'
    category = r.html.find('span.posted_in a', first=True).text.strip()

    return dict(
        title=title,
        price=price,
        sku=sku,
        tag=tag,
        category=category
    )


def save_to_csv(results):
    keys = results[0].keys()
    with open('product_data.csv', 'w') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)
    print('Saved to CSV')




if __name__ == "__main__":
    results = []
    for link in get_links():
        print('Getting data from:', link)
        results.append(get_product_data(link))
    save_to_csv(results)

