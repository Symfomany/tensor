
// export GOOGLE_APPLICATION_CREDENTIALS="/Users/julienboyer/Desktop/tensor/console.json"
// https://console.cloud.google.com/apis/credentials/serviceaccountkey?hl=fr&_ga=2.175432614.-542718344.1549350786
// Upload file object: https://cloud.google.com/storage/docs/uploading-objects


const express = require("express");
const bodyParser = require("body-parser");
const path = require("path");
const { Storage } = require("@google-cloud/storage");
// const fileUpload = require("express-fileupload");
const opn = require("opn");
const Multer = require("multer");
const multer = Multer({
  storage: Multer.MemoryStorage,
  limits: {
    fileSize: 5 * 1024 * 1024 // no larger than 5MB
  }
});

// Your Google Cloud Platform project ID
const projectId = "console-28d14";
// https://console.cloud.google.com/storage/browser/symfomany
// Creates a client
const storage = new Storage({
  projectId: projectId
});

let bucket = storage.bucket(`taiwa_julien`);

const app = express();

app.use(bodyParser.json()); // to support JSON-encoded bodies
app.use(
  bodyParser.urlencoded({
    // to support URL-encoded bodies
    extended: true
  })
);
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname + "/index.html"));
});

/**
 * Middleware
 * @param {*} req
 * @param {*} res
 * @param {*} next
 */
function sendUploadToGCS(req, res, next) {
  const firstname = req.body.firstname;
  if (!req.file) {
    return next();
  }

  const gcsname = Date.now() + req.file.originalname;
  // https://cloud.google.com/nodejs/docs/reference/storage/1.3.x/File

  const file = bucket.file(gcsname);

  const stream = file.createWriteStream({
    metadata: {
      contentType: req.file.mimetype
    },
    resumable: false
  });

  stream.on("error", err => {
    req.file.cloudStorageError = err;
    next(err);
  });

  stream.on("finish", () => {
    req.file.cloudStorageObject = gcsname;
    file.makePublic().then(() => {
      req.file.cloudStoragePublicUrl = getPublicUrl(gcsname, firstname);
      next();
    });
  });

  stream.end(req.file.buffer);
}

function getPublicUrl(filename, firstname = "default") {
  return `https://storage.googleapis.com/symfomany/${firstname}/${filename}`;
}

app.post("/send", multer.single("image"), sendUploadToGCS, async (req, res) => {
  if (Object.keys(req.file).length == 0) {
    return res.status(400).send("No files were uploaded.");
  }

  if (req.file && req.file.cloudStoragePublicUrl) {
    res.send(req.file.cloudStoragePublicUrl);
  }

  res.send(false);
});

app.listen(3000, () => {
  console.log("Example app listening on port 3000!");
});

setTimeout(() => {
  // opn("http://localhost:3000");
}, 1000);
