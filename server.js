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
    fileSize: 5 * 1024 * 1024 // no larger than 5mb
  }
});
// export GOOGLE_APPLICATION_CREDENTIALS="/Users/julienboyer/Desktop/tensor/console.json"

// Your Google Cloud Platform project ID
const projectId = "console-28d14";
// https://console.cloud.google.com/storage/browser/symfomany
// Creates a client
const storage = new Storage({
  projectId: projectId
});

let bucket = storage.bucket("symfomany");

const app = express();

// app.use(
//   fileUpload({
//     limits: { fileSize: 50 * 1024 * 1024 }
//   })
// );
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
  console.log("one");
  const firstname = req.body.firstname;
  if (!req.file) {
    return next();
  }

  const gcsname = Date.now() + req.file.originalname;
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
    req.file.cloudStoragePublicUrl;
    console.log(req.file.cloudStoragePublicUrl);
  }
});

app.listen(3000, () => {
  console.log("Example app listening on port 3000!");
});

setTimeout(() => {
  //opn("http://localhost:3000");
}, 1000);
