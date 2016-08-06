const http = require('http');
const mongoose = require('mongoose');
const model = require('./model');

mongoose.connect('mongodb://localhost/doujin');
const db = mongoose.connection;
db.on('error', () => console.log('mongodb connect fail'));
db.on('open', () => console.log('mongodb connect success'));

const reTimes = 3;

function getCats(times=0) {
	http.get('http://picaman.picacomic.com/api/categories', (res) => {
		if (res.statusCode === 200 || res.statusCode === 304) {
			console.log(`res receive-->statusCode:${res.statusCode}`);
			let data = new Buffer([]);
			res.on('data', (buffer) => {
				data += buffer;
			});
			res.on('end', () => {
				const j = JSON.parse(data.toString());
				const arr = [];
				for (let v of j) {
					if (v.id === 31) {
						continue;
					}
					arr.push({
						id: v.id,
						pages: Math.ceil(v['all_comics'] / 20)
					});
				}
				arr.map(parseCat);

			});
		} else {
			console.log(`res statusCode:${res.statusCode}`);
		}
	}).on('error', e => {
		console.error('get categories error');
		if (times < reTimes) {
			times++;
			console.log(`restart get cats-->restart:the ${times} times`);
			getCats(times);
		} else {
			process.exit(1);
		}
	});
}


function requestCat(url, times=0) {
	http.get(url, (res) => {
		if (res.statusCode === 200 || res.statusCode === 304) {
			let data = new Buffer([]);
			res.on('data', (buffer) => {
				data += buffer;
			}).on('end', () => {
				const j = JSON.parse(data.toString());
				const arr = [];
				for (let v of j) {
					arr.push({
						id: v.id,
						cats: v.cats,
					});
				}
				arr.map(parseComic);
			});
		}
	}).on('error', (e) => {
		console.log('parse cat error');
		if (times < reTimes) {
			times++;
			console.log(`restart parse cat-->restart:the ${times} times`);
			requestCat(url, times);
		}
	});
};

function parseCat(obj) {
	for (let i=1, pages=obj.pages+1; i<pages; i++) {
		const url = `http://picaman.picacomic.com/api/categories/${obj.id}/page/${i}/comics`;
		requestCat(url);
	}
}

function parseComic(obj, times=0) {
	http.get(`http://picaman.picacomic.com/api/comics/${obj.id}`, (res) => {
		if (res.statusCode === 200 || res.statusCode === 304) {
			let data = new Buffer([]);
			res.on('data', (buffer) => {
				data+=buffer;
			}).on('end', () => {
				const j = JSON.parse(data.toString());
				const c = j.comic;
				const epNum = j.ep_count;
				delete c.comment_count;
				delete c.img_directory;
				delete c.views_count;
				c.user_id = 0;
				c.display_name = '天道';
				c.updated_at = Date.now();
				parseEps(epNum, c);
			});
		}
	}).on('error', (e) => {
		console.log('parse comic error');
		if (times < reTimes) {
			times++;
			console.log(`restart parse comic-->restart:the ${times} times`);
			parseComic(obj, times);
		}
	});
}


function parseEp(url, times=0, i, resolve, reject) {
	http.get(url, (res) => {
		if (res.statusCode === 200 || res.statusCode === 304) {
			let data = new Buffer([]);
			res.on('data', (buffer) => {
				data += buffer;
			}).on('end', () => {
				const j = JSON.parse(data.toString());
				resolve({ ['ep'+i]: j });
			});
		}
	}).on('error',() => {
		console.log('parse ep error');
		if (times < reTimes) {
			times++;
			console.log(`restart parse ep-->restart:the ${times} times`);
			parseEp(url, times, resolve, reject);
		} else {
			reject();
		}
	});	
}

function parseEps(epNum, c, times=0) {
	const promises = [];
	for (let i=1; i<epNum+1; i++) {
		const p = new Promise((resolve, reject) => {
			const url = `http://picaman.picacomic.com/api/comics/${c.id}/ep/${i}`;
			parseEp(url, 0, i, resolve, reject);
		});
		promises.push(p);
	};
	Promise.all(promises).then((result) => {
		// 将数组内的元素合并为一个对象
		c.eps = result.reduce((a, b) => Object.assign(a, b));
		model.saveComic(c);
	}).catch((e) => {
		console.log('parse eps error');
	});
}

// main

process.on('uncaughtException', function (e) { 
  console.log(`Caught exception: ${e}`); 
}); 

getCats();



