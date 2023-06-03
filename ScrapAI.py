import streamlit as st
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from reportlab.pdfgen import canvas

# Define a function to extract all hyperlinks from a webpage
def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('http'):
            links.append(href)
    return links

# Define a function to extract sitemaps from a webpage
def get_sitemaps(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    sitemaps = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and 'sitemap' in href.lower():
            sitemaps.append(href)
    return sitemaps

# Define a function to filter content and convert to PDF
def filter_content(links):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    for link in links:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        for p in soup.find_all('p'):
            text = p.get_text()
            if 'technology' in text.lower():
                pdf.drawString(100, 750, text)
                pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer

# Define the Streamlit app
def app():
    st.set_page_config(page_title='Website Scraper', page_icon=':computer:', layout='wide')
    st.title('Website Scraper')
    st.markdown('Enter a URL to scrape the website for hyperlinks, extract sitemaps, and filter content into a PDF file.')
    url = st.text_input('Enter a URL:')
    if url:
        st.write('Scraping website...')
        links = get_links(url)
        sitemaps = get_sitemaps(url)
        st.write(f'Found {len(links)} hyperlinks and {len(sitemaps)} sitemaps.')
        st.write('Filtering content...')
        buffer = filter_content(links)
        st.write('Converting to PDF...')
        st.download_button('Download PDF', data=buffer, file_name='filtered_content.pdf', mime='application/pdf')

