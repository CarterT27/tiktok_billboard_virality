import datetime
import pandas as pd
import requests
from selectolax.parser import HTMLParser
from tqdm import tqdm


def get_monthly_urls() -> list[str]:
    """
    Get list of monthly urls.

    >>> res = get_monthly_urls()
    >>> isinstance(res, list)
    True
    >>> all(isinstance(v, str) for v in res)
    True
    >>> res[0] == 'https://tokchart.com/monthly/february-2022'
    True
    >>> len(res) > 24 # At least two years of data
    True
    """
    months = ["january",
              "february",
              "march",
              "april",
              "may",
              "june",
              "july",
              "august",
              "september",
              "october",
              "november",
              "december"]
    current_date = datetime.date.today()
    start_year = 2022
    end_year = current_date.year + 1
    years = range(start_year, end_year)
    base_url = "https://tokchart.com/monthly/"
    start_month = "february"
    urls = []
    for year in years:
        for month in months:
            if year == start_year and months.index(month) <\
            months.index(start_month): # Ignore months before start month
                continue
            urls.append(base_url + f"{month}-{year}")
    return urls


def parse_monthly_html(html: str) -> list[str]:
    """
    Get list of weekly urls from monthly html.

    >>> html = requests.get('https://tokchart.com/monthly/february-2022').text
    >>> res = parse_monthly_html(html)
    >>> len(res) == 4
    True
    >>> res[0] == 'https://tokchart.com/weekly/6-february-2022'
    True
    >>> all('weekly' in x for x in res)
    True
    """
    parser = HTMLParser(html)
    a_nodes = parser.css('a')
    return [node.attrs.get('href') for node in a_nodes if 'weekly' in
            node.attrs.get('href', '')]


def parse_weekly_html(html: str):
    """
    Convert weekly html to dataframe.
    
    >>> html = requests.get('https://tokchart.com/weekly/25-february-2024').text
    >>> res = parse_weekly_html(html)
    >>> res.iloc[0].get('rank') == 1
    True
    >>> res.iloc[-1].get('rank') == 10
    True
    >>> res.iloc[0].get('artist') == 'hulio'
    True
    >>> res.iloc[0].get('song') == 'original sound - username.hulio'
    True
    >>> res.iloc[0].get('weekly_videos') == '710K'
    True
    >>> res.iloc[0].get('image_url') ==\
'https://tokchart.com/img/7332316910419577606/600'
    True
    """
    parser = HTMLParser(html)
    container = parser.css_first('.flow-root > div:nth-child(1)')
    ranking_nodes = container.css('div.col-span-full')
    rows_list = []
    date = parser.css_first('.mt-3').text(strip=True)
    date = " ".join(date.split()[-3:])
    dt = datetime.datetime.strptime(date, '%B %d, %Y')
    for node in ranking_nodes:
        rows_list.append({
            'date': dt.strftime('%Y-%m-%d'),
            'song': node.css_first('a.text-2xl').text(strip=True),
            'artist': node.css_first('span.text-slate-800').text(strip=True),
            'rank': int(node.css_first('span.text-3xl').text(strip=True)),
            'weekly_videos':
            node.css_first('a.text-cadet').text(strip=True).replace(' videos',
                                                                    ''),
            'image_url': node.css_first('img').attrs.get('src')
            })

    return pd.DataFrame(rows_list)


def scrape_month(url: str) -> pd.DataFrame:
    """
    Get all weekly dataframes for a month given url.
    
    >>> res = scrape_month('https://tokchart.com/monthly/january-2024')
    >>> res.shape[0] == 4 * 10
    True
    """
    monthly_html = requests.get(url).text
    weekly_urls = parse_monthly_html(monthly_html)
    dfs = []
    for weekly_url in tqdm(weekly_urls,
        desc = f"Scraping weekly data for {url.split('/')[-1]}"):
        weekly_html = requests.get(weekly_url).text
        dfs.append(parse_weekly_html(weekly_html))
    return pd.concat(dfs)


def scrape_all() -> None:
    """
    Scrape all months to present.
    """
    monthly_urls = get_monthly_urls()
    dfs = [scrape_month(url) for url in monthly_urls]
    df = pd.concat(dfs)
    df.to_csv('data/tokchart.csv', index=False)

def main() -> None:
    scrape_all()

if __name__ == "__main__":
    main()
