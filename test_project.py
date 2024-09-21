import pytest
from project import search, details, fetch

def test_search():
    assert search("avengers")["status"]
    assert search("wgcyegc")["status"] == False

def test_details():
    assert details("tt0848228")["status"]
    assert details("2iuegd2yugd")["status"] == False

def test_fetch():
    assert fetch("http://www.omdbapi.com/?s=avengers&page=1")["status"]
    assert fetch("http://www.omdbapi.com/?s=fhgfhbbch&page=1")["status"] == False
    assert fetch("http://www.omdbapi.com/?i=tt0848228&plot=full")["status"]
    assert fetch("http://www.omdbapi.com/?i=wcjbjqwecb&plot=full")["status"] == False
