## Afiliepy

Replace other users affiliate link to own one.  

## Instration  

```
pip install affilipy
```

## Usage  

```
from affilipy.amazon import amazon as amz

amz.replace('https://amzn.to/...', your_key)
#=> https://www.amazon.co.jp/gp/product/...?tag={your_key}
amz.get_asin_from_url('https://www.amazon.co.jp/gp/product/...')
#=> B123456789
```
