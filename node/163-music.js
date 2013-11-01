var http = require('http'),
	qs = require('querystring'),
	conf = require('./conf.json');

var HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
	'Referer': 'http://music.163.com/'
}

function downloadSongs() {

}

function getAlbum() {

}

var commandOption, fileName;

fileName = process.argv[2];

if(fileName && fileName.indexOf('-') === 0) {
	commandOption = fileName.substring(1);
}

if(commandOption === 's') {
	var params, options;

	params = {
		'csrf_token': '',
		'id': '386835',
		'ids': '[386835]'
	}

	options = {
		hostname: 'music.163.com',
		port: 80,
		path: '/api/song/detail/?' + qs.stringify(params),
		method: 'get',
		headers: HEADERS
	};

	var req = http.request(options, function(res) {
		res.setEncoding('utf8');
		var data = '';	
		res.on('data', function(chunk) {
			data += chunk;
		});
		res.on('end', function() {
			console.log(JSON.parse(data))
		});
	});

	req.on('error', function(e) {
		console.log('problem with request: ' + e.message);
	});

	req.end();
}

if(commandOption === 'a') {

}

if(commandOption === 'se') {

}