var http = require('http'),
	fs = require('fs'),
	qs = require('querystring'),
	url = require('url'),
	conf = require('./conf.json');

var HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
	'Referer': 'http://music.163.com/'
}

// https://gist.github.com/wilsonpage/1393666
function urlReq(req_url, options, cb) {
	if(typeof options === "function"){ cb = options; options = {}; }

	req_url = url.parse(req_url);

	var settings = {
		host: req_url.hostname,
		port: req_url.port || 80,
		path: req_url.path,
		headers: options.headers || {},
		method: options.method || 'get'
	}

	if(options.params) {
		options.params = qs.stringify(options.params);
		settings.headers['Content-Type'] = 'application/x-www-form-urlencoded';
		settings.headers['Content-Length'] = options.params.length;
	}

	var req = http.request(settings);

	if(options.params){ req.write(options.params) };

	req.on('response', function(res) {
		res.body = '';
		res.setEncoding('utf-8');

		res.on('data', function(chunk) {
			res.body += chunk;
		});

		res.on('end', function() {
			cb(res.body, res);
		});
	});

	req.end();
}

function downloadSongs(songs, folder) {
	songs.forEach(function(obj, index, list) {
		var link = obj.mp3Url;
		var info = {
			name: obj.name,
			artist: obj.artists[0].name,
			album: obj.album.name,
			track_num: index
		}

		if(folder) {
			fs.mkdir(folder);
		} else {
			folder = conf.dest;
		}

		var file = fs.createWriteStream(folder + '/' + info.name+'.mp3');	

		urlReq(link, {
			method: 'GET',
			headers: HEADERS
		}, function(body, res) {
			res.pipe(file);
		});
	});
}

var commandOption, fileName, args

fileName = process.argv[2];

if(fileName && fileName.indexOf('-') === 0) {
	commandOption = fileName.substring(1);
}

if(commandOption === 's') {
	var params;

	args = process.argv[3];

	params = {
		csrf_token: '',
		id: args,
		ids: '['+args+']'
	}

	urlReq('http://music.163.com/api/song/detail/?'+qs.stringify(params), {
		headers: HEADERS,
		method: 'GET'
	}, function(body, res) {
		console.log(body)
		downloadSongs(JSON.parse(body).songs);
	});
}

if(commandOption === 'a') {
	args = process.argv[3];

	urlReq('http://music.163.com/api/album/'+args, {
		headers: HEADERS,
		method: 'GET',
		params: {
			id: args,
			csrf_token: ''
		}
	}, function(body, res) {
		var data = JSON.parse(body);
		if(data['album']) {
			var album = data['album'];
			var folder = conf.dest + '/' + album.name;
			downloadSongs(album.songs, folder);
		} else {
			console.log(data);
		}
	});
}

if(commandOption === 'se') {
	args = process.argv.slice(3).toString().replace(',', ' ');

	urlReq('http://music.163.com/api/search/suggest/web?csrf_token=',{
		method: 'POST',
		headers: HEADERS,
		params: {
			limit: 20,
			s: args
		}
	}, function(body, res) {
		var data = JSON.parse(body).result;
		if(data.albums) {
			console.log('-------------------------Album----------------------------\n');
			var albums = data.albums;
			albums.forEach(function(obj, index) {
				console.log(obj.name + '-' + obj.artist.name +'\n');
				console.log(obj.id + '\n');
			});
		}
		if(data.songs) {
			console.log('-------------------------Song----------------------------\n');
			var songs = data.songs;
			songs.forEach(function(obj, index) {
				console.log(obj.name + '-' + obj.artists[0].name + '\n');
				console.log(obj.id + '\n')
			});
		} else {
			console.log(data);
		}
	});
}