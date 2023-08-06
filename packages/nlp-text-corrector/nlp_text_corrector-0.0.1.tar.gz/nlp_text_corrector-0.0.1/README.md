# How to run : 

## Install :
```
pip install nlp-text-corrector
```

## Code :
```
from nlp_text_corrector import asr_post_process

asr_post_process.convert("Book twenty first century marvel movie for my two kids of age nine and thirteen at eight twenty two pm tonight"))
```

## Examples : 
```
asr_post_process.convert("Book a first class flight ticket for my two childs of age twenty one and sixteen on thirty first march twenty twenty one which leaves after seven forty five pm") 

Output : "Book a first class flight ticket for my 2 childs of age 21 and 16 on 31st march 2021 which leaves after 7:45 pm
```

```
asr_post_process.convert("send an email to chandra at iamplus dot com")

Output : send an email to chandra@iamplus.com
```
