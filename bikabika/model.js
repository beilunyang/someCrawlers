const mongoose = require('mongoose');

const ComicSchema = mongoose.Schema({
	"updated_at": String,
	"id": Number,
	"name": String,
	"author": String,
	"finished": Number,
	"total_page": Number,
	"description": String,
	"display_name": String,
	"cover_image": String,
	"rank": Number,
	"user_id": Number,
	"eps": {},
});

ComicSchema.index({ id: 1}, { unique: true });

const Comic = mongoose.model('Comic', ComicSchema);

exports.saveComic = (comic) => {
	const c = new Comic(comic);
	c.save((err, c) => {
		if (err) {
			return console.log('save fail');
		}
		console.log('save success');
	});
};