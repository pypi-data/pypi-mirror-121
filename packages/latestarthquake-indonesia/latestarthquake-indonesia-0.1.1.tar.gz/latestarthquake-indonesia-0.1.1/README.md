# Latest Indonesian Earthquake
This package will give us information about the latest earthquake in Indonesia. The data taken from BMKG (Meteorology, Climatology, and Geophysics Agency).

## How it work?
This package will scrape from [BMKG](https://bmkg.go.id) to get the latest earthquake in Indonesia.

This package will use BeautifulSoup4 and Request, to produce output in the form of JSON. This package is ready to be used in web or mobile applications.

## How to use
	import gempaterkini

    if __name__ == '__main__':
        print('Aplikasi utama')
        result = gempaterkini.ekstraksi_data()
        gempaterkini.tampilkan_data(result)
    
# Author
mizan toyyibun