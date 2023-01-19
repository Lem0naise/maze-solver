// not used, but please don't delete

const express = require('express');
const expressWs = require('express-ws');
const http = require('http');

let port = 3000

let app = express()
let server = http.createServer(app).listen(port, () => {
    console.log(`listening at ws://localhost:${port}`)
})

expressWs(app, server)

//app.use(express.static())

app.get('/', (req, res) => {
    res.status(200).send("Welcome!")
})

app.ws('/ws', async function (ws, req) {

    ws.on('message', async function (msg) {

        console.log(msg)

        ws.send(JSON.stringify({
            "append": true,
            "returnText": "I am using WebSockets!"
        }));

    })
})