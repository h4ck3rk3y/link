# Link ReWrite

1. ~I want Link to be fast and it should run all requests asynchronously using grequests~
2. ~DESCOPED Maybe I want link to return the first 15 responses as soon as it gets them~
3. NEEDS VERIFICATION: I don't want link to run crawls if it has data worth next few pages
4. ~I want writing a new integration to be as easy as just writing searchers/new_integration.py and nothing more~
5. ~The new integration should expect some consts and define differently only things that are different like response parsing & rate limit~
6. ~I don't want link to make requests if a source has run out of data ( the last request didn't return data == per_page )~
7. I wan't link to handle user only searches
8. NEEDS VERIFICATION: I want link to support source filtering
9. ~Handle non valid and non rate limit exceeded states~
10. Switch stackoverflow API
11. Port trello
12. Port slack
