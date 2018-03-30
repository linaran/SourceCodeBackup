response=$(curl -u root:2244112233RaCu http://localhost:8000/faketweeter/api/users/);
if [ "$response" == '[{"id":1,"username":"root","tweets":[27,28,34,35]},{"id":2,"username":"linaran","tweets":[29,30,32,33]}]' ]
	then echo "pass"
	else echo "fail"
fi

response=$(curl -u root:2244112233RaCu http://localhost:8000/faketweeter/api/users/1);
if [ "$response" == '{"id":1,"username":"root","tweets":[27,28,34,35]}' ]
  then echo "pass"
  else echo "fail"
fi

response=$(curl -u root:2244112233RaCu -H "Content-Type: application/json" http://localhost:8000/faketweeter/api/tweets/);
if [ "$response" == '[{"id":27,"user":"root","tweet":"Admin100","date_published":"2016-12-06T06:10:15.887391Z"},{"id":28,"user":"root","tweet":"Admin3","date_published":"2016-12-06T05:58:08.428462Z"},{"id":29,"user":"linaran","tweet":"Linaran1","date_published":"2016-12-06T06:01:57.749017Z"},{"id":30,"user":"linaran","tweet":"Linaran2","date_published":"2016-12-06T06:02:00.858100Z"},{"id":32,"user":"linaran","tweet":"Linaran3","date_published":"2016-12-06T06:08:12.590335Z"},{"id":33,"user":"linaran","tweet":"Joooooj","date_published":"2016-12-06T06:09:48.031593Z"},{"id":34,"user":"root","tweet":"Pokušaj broj 2","date_published":"2016-12-05T11:11:00Z"},{"id":35,"user":"root","tweet":"hahaha","date_published":"2016-12-04T11:11:00Z"}]' ] 
  then echo "pass"
  else echo "fail"
fi

response=$(curl -u root:2244112233RaCu -H "Content-Type: application/json" http://localhost:8000/faketweeter/api/users/1/tweets);
if [ "$response" == '[{"id":27,"user":"root","tweet":"Admin100","date_published":"2016-12-06T06:10:15.887391Z"},{"id":28,"user":"root","tweet":"Admin3","date_published":"2016-12-06T05:58:08.428462Z"},{"id":34,"user":"root","tweet":"Pokušaj broj 2","date_published":"2016-12-05T11:11:00Z"},{"id":35,"user":"root","tweet":"hahaha","date_published":"2016-12-04T11:11:00Z"}]' ] 
  then echo "pass"
  else echo "fail"
fi

response=$(curl -u root:2244112233RaCu -H "Content-Type: application/json" http://localhost:8000/faketweeter/api/tweets/27);
if [ "$response" == '{"id":27,"user":"root","tweet":"Admin100","date_published":"2016-12-06T06:10:15.887391Z"}' ] 
  then echo "pass"
  else echo "fail"
fi

response=$(curl -u root:2244112233RaCu -H "Content-Type: application/json" -X POST -d '{"tweet": "BRIŠI", "date_published": "2016-12-04T11:11:00Z"}' http://localhost:8000/faketweeter/api/tweets/);
if [ "$response" == '{"id":50,"user":"root","tweet":"BRIŠI","date_published":"2016-12-04T11:11:00Z"}' ]
  then echo "pass"
  else echo "fail"
fi

response=$(curl -u root:2244112233RaCu -H "Content-Type: application/json" -X DELETE http://localhost:8000/faketweeter/api/tweets/50);
if [ "$response" == '' ]
  then echo "pass"
  else echo "fail"
fi
